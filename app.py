# app.py - Applicazione principale Fantasy ER Operations
# Progetto Fantasy ER Operations - Classe 4ª Informatica TPSIT
# Sviluppato dal gruppo Lourdes Direction
# Team Leader: Caraviello Salvatore
# Componenti: Coppola Nicole, Palumbo Annarita, Sarcinelli Valentina

# Importazione librerie necessarie per il funzionamento dell'applicazione
from flask import Flask  # Importa la classe principale Flask per creare l'applicazione web
from flask import render_template  # Importa funzione per renderizzare template HTML
from flask import request  # Importa funzione per gestire richieste HTTP
from flask import jsonify  # Importa funzione per convertire dati in JSON
from flask import session  # Importa funzione per gestire sessioni utente
import json  # Importa modulo JSON per gestione file e serializzazione
import time  # Importa modulo time per gestione temporale e timestamp
import threading  # Importa modulo threading per programmazione concorrente
import random  # Importa modulo random per generazione numeri casuali
import os  # Importa modulo os per interazione con sistema operativo
from patients import PatientManager  # Importa classe PatientManager dal modulo patients
from doctors import DoctorManager  # Importa classe DoctorManager dal modulo doctors

# Creazione istanza dell'applicazione Flask
app = Flask(__name__)  # Inizializza l'applicazione Flask con il nome del modulo corrente

# Impostazione chiave segreta per sessioni sicure
app.secret_key = "fantasy_er_operations_2025"  # Chiave usata per firmare i cookie di sessione

# Dizionario globale per memorizzare lo stato corrente del gioco
game_state = {  # Dizionario che contiene tutte le variabili di stato del gioco
    "score": 0,  # Punteggio totale accumulato dal giocatore
    "cured_patients": 0,  # Numero totale di pazienti curati con successo
    "game_time": 0,  # Tempo di trascorso in secondi dall'inizio della partita
    "is_running": False,  # Flag booleano che indica se il gioco è in esecuzione
    "notifications": [],  # Lista che contiene tutte le notifiche generate durante il gioco
    "events": [],  # Lista che contiene gli eventi speciali generati casualmente
    "game_over": False,  # Flag che indica se il gioco è terminato e deve mostrare game over
    "hospital_pressure": 0  # Pressione del pronto soccorso (0-100), game over se raggiunge 100
}

# Inizializzazione dei gestori per pazienti e medici
patient_manager = PatientManager()  # Crea istanza del gestore pazienti per la loro gestione
doctor_manager = DoctorManager()  # Crea istanza del gestore medici per la loro gestione

# Variabili globali per il controllo dello stato del gioco
game_timer_thread = None  # Variabile che conterrà il thread del timer di gioco
selected_patient_id = None  # Variabile che memorizza l'ID del paziente selezionato
selected_doctor_id = None  # Variabile che memorizza l'ID del medico selezionato
lock = threading.Lock()  # Oggetto lock per garantire thread safety nelle operazioni critiche
SAVE_DIRECTORY = "saves"  # Directory dove salvare le partite

# Funzione per salvare lo stato corrente del gioco su file JSON
def save_game_to_file():  # Salva la partita corrente in un file
    global game_state  # Dichiara uso variabile globale
    global selected_patient_id  # Dichiara uso variabile globale
    global selected_doctor_id  # Dichiara uso variabile globale
    
    # Verifica che la directory di salvataggio esista, altrimenti la crea
    if not os.path.exists(SAVE_DIRECTORY):  # Se la directory non esiste
        os.makedirs(SAVE_DIRECTORY)  # Crea la directory per i salvataggi
    
    # Genera il nome del file con timestamp per identificare univocamente la partita
    timestamp = time.strftime("%Y%m%d_%H%M%S")  # Formatta data e ora come AAAAMMGG_HHMMSS
    filename = f"{SAVE_DIRECTORY}/game_{timestamp}.json"  # Nome file con percorso completo
    
    # Prepara il dizionario completo con tutti i dati da salvare
    save_data = {  # Dizionario contenente tutti i dati della partita
        "game_state": game_state.copy(),  # Stato completo del gioco
        "selected_patient_id": selected_patient_id,  # Paziente correntemente selezionato
        "selected_doctor_id": selected_doctor_id,  # Medico correntemente selezionato
        "patients": patient_manager.to_dict_list(),  # Lista completa dei pazienti
        "doctors": doctor_manager.to_dict_list(),  # Lista completa dei medici
        "save_timestamp": timestamp,  # Timestamp del salvataggio
        "save_date": time.strftime("%Y-%m-%d %H:%M:%S")  # Data leggibile del salvataggio
    }
    
    # Salva i dati su file JSON in modo sicuro con gestione errori
    try:  # Blocco try per gestire eventuali errori di I/O
        with open(filename, 'w', encoding='utf-8') as f:  # Apre file in scrittura con encoding UTF-8
            json.dump(save_data, f, indent=4, ensure_ascii=False)  # Scrive JSON formattato
        print(f"Partita salvata con successo: {filename}")  # Messaggio di conferma su console
        return True, filename  # Restituisce successo e nome del file
    except Exception as e:  # Se si verifica un errore durante il salvataggio
        print(f"Errore durante il salvataggio della partita: {e}")  # Stampa errore su console
        return False, str(e)  # Restituisce fallimento e messaggio di errore

# Definizione della route principale per la pagina iniziale
@app.route('/')  # Decoratore che registra la funzione per la route radice
def index():  # Funzione che gestisce le richieste alla pagina principale
    session.clear()  # Pulisce tutti i dati della sessione utente corrente
    return render_template('index.html')  # Renderizza e restituisce il template HTML della pagina iniziale

# Definizione della route per avviare una nuova partita
@app.route('/start_game')  # Decoratore che registra la funzione per la route di avvio gioco
def start_game():  # Funzione che gestisce l'avvio di una nuova partita
    global game_state  # Dichiara che userà la variabile globale game_state
    global patient_manager  # Dichiara che userà la variabile globale patient_manager
    global doctor_manager  # Dichiara che userà la variabile globale doctor_manager
    
    # Resetta lo stato del gioco a valori iniziali
    game_state = {  # Reinizializza completamente il dizionario di stato
        "score": 0,  # Azera il punteggio
        "cured_patients": 0,  # Azera il conteggio pazienti curati
        "game_time": 0,  # Azera il timer di gioco
        "is_running": True,  # Imposta il gioco come attivo
        "game_over": False,  # Resetta il flag di game over
        "notifications": [],  # Svuota la lista delle notifiche
        "events": [],  # Svuota la lista degli eventi speciali
        "hospital_pressure": 0  # Resetta la pressione del pronto soccorso
    }
    
    # Resetta i gestori per la nuova partita
    patient_manager = PatientManager()  # Crea nuova istanza del gestore pazienti
    doctor_manager.reset_all_doctors()  # Resetta tutti i medici allo stato iniziale
    
    # Avvia i sistemi concorrenti del gioco
    start_game_timer()  # Avvia il thread per il timer di gioco
    patient_manager.start_automatic_arrivals(handle_patient_arrival)  # Avvia arrivo automatico pazienti
    patient_manager.start_random_events(handle_random_event)  # Avvia eventi casuali
    
    # Aggiunge notifica di inizio gioco
    add_notification("🏥 Gioco Iniziato!", "I pazienti stanno arrivando...", "success")  # Notifica inizio partita
    
    # Restituisce risposta JSON di conferma
    return jsonify({"status": "success", "message": "Gioco avviato"})  # Risposta positiva all'avvio

# Definizione della route per ottenere lo stato corrente del gioco
@app.route('/game_state')  # Decoratore che registra la funzione per ottenere lo stato
def get_game_state():  # Funzione che fornisce lo stato completo del gioco
    # Controllo forzato della pressione per attivare game over immediato
    with lock:
        if game_state["is_running"] and game_state.get("hospital_pressure", 0) >= 100:
            print(f"🚨 Game Over attivato in /game_state: pressione = {game_state['hospital_pressure']}")
            trigger_game_over()
    
    # Prepara il dizionario con tutti i dati di stato correnti
    state_data = {  # Dizionario che conterrà lo stato completo da inviare al frontend
        "score": game_state["score"],  # Punteggio attuale
        "cured_patients": game_state["cured_patients"],  # Numero pazienti curati
        "game_time": game_state["game_time"],  # Tempo di gioco trascorso
        "is_running": game_state["is_running"],  # Stato di esecuzione del gioco
        "game_over": game_state.get("game_over", False),  # Flag di game over
        "hospital_pressure": game_state.get("hospital_pressure", 0),  # Pressione pronto soccorso
        "patients": patient_manager.to_dict_list(),  # Lista pazienti convertita in dizionario
        "doctors": doctor_manager.to_dict_list(),  # Lista medici convertita in dizionario
        "selected_patient_id": selected_patient_id,  # ID paziente correntemente selezionato
        "selected_doctor_id": selected_doctor_id,  # ID medico correntemente selezionato
        "notifications": game_state["notifications"][-5:]  # Ultime 5 notifiche mostrate
    }
    
    return jsonify(state_data)  # Converte in JSON e restituisce lo stato

# Definizione della route per selezionare un paziente
@app.route('/select_patient/<int:patient_id>')  # Route con parametro ID paziente
def select_patient(patient_id):  # Funzione per gestire la selezione del paziente
    global selected_patient_id  # Dichiara l'uso della variabile globale per il paziente selezionato
    
    # Verifica l'esistenza del paziente richiesto
    patient = patient_manager.get_patient_by_id(patient_id)  # Cerca paziente per ID
    if not patient:  # Se il paziente non esiste nel sistema
        return jsonify({"status": "error", "message": "Paziente non trovato"})  # Errore paziente non trovato
    
    # Imposta il paziente come selezionato
    selected_patient_id = patient_id  # Memorizza l'ID del paziente selezionato
    
    # Controlla se è già stato selezionato un medico per assegnazione automatica
    if selected_doctor_id:  # Se esiste già un medico selezionato
        assign_doctor_to_patient()  # Esegue l'assegnazione automatica
    
    return jsonify({"status": "success", "message": "Paziente selezionato"})  # Conferma selezione

# Definizione della route per selezionare un medico
@app.route('/select_doctor/<int:doctor_id>')  # Route con parametro ID medico
def select_doctor(doctor_id):  # Funzione per gestire la selezione del medico
    global selected_doctor_id  # Dichiara l'uso della variabile globale per il medico selezionato
    
    # Verifica l'esistenza del medico richiesto
    doctor = doctor_manager.get_doctor_by_id(doctor_id)  # Cerca medico per ID
    if not doctor:  # Se il medico non esiste nel sistema
        return jsonify({"status": "error", "message": "Medico non trovato"})  # Errore medico non trovato
    
    # Verifica la disponibilità del medico
    if not doctor.available:  # Se il medico non è disponibile
        return jsonify({"status": "error", "message": "Medico non disponibile"})  # Errore medico occupato
    
    # Imposta il medico come selezionato
    selected_doctor_id = doctor_id  # Memorizza l'ID del medico selezionato
    
    # Controlla se è già stato selezionato un paziente per assegnazione automatica
    if selected_patient_id:  # Se esiste già un paziente selezionato
        assign_doctor_to_patient()  # Esegue l'assegnazione automatica
    
    return jsonify({"status": "success", "message": "Medico selezionato"})  # Conferma selezione

# Definizione della route per assegnazione manuale medico-paziente
@app.route('/assign_doctor/<int:doctor_id>/<int:patient_id>')  # Route per assegnazione diretta con entrambi gli ID
def assign_doctor(doctor_id, patient_id):  # Funzione per assegnare manualmente un medico specifico a un paziente specifico
    global selected_patient_id  # Dichiara l'uso della variabile globale per il paziente
    global selected_doctor_id  # Dichiara l'uso della variabile globale per il medico
    
    # Imposta direttamente entrambe le selezioni
    selected_patient_id = patient_id
    selected_doctor_id = doctor_id
    
    # Verifica che il paziente selezionato esista ancora
    patient = patient_manager.get_patient_by_id(selected_patient_id)
    if not patient:
        return jsonify({"status": "error", "message": "Il paziente selezionato non è più disponibile"})
    
    # Esegue l'assegnazione del medico al paziente
    result = assign_doctor_to_patient()
    
    return jsonify(result)  # Restituisce il risultato dell'assegnazione

# Definizione della route per terminare il gioco
@app.route('/end_game')  # Route per terminazione partita
def end_game():  # Funzione che gestisce la fine del gioco
    global game_state  # Dichiara l'uso della variabile globale di stato
    
    # Ferma il gioco impostando il flag appropriato
    game_state["is_running"] = False  # Imposta il gioco come non in esecuzione
    patient_manager.stop_threads()  # Ferma tutti i thread del gestore pazienti
    
    # Attende la terminazione del thread timer se esiste
    if game_timer_thread:  # Se il thread timer è attivo
        game_timer_thread.join(timeout=1)  # Attende la terminazione con timeout di 1 secondo
    
    # Salva la partita su file JSON prima di terminare
    save_success, save_result = save_game_to_file()  # Salva lo stato della partita
    if save_success:  # Se il salvataggio è riuscito
        print(f"✅ Partita salvata con successo: {save_result}")  # Messaggio di conferma
        add_notification("💾 Salvataggio Completato", f"Partita salvata: {save_result}", "success")  # Notifica utente
    else:  # Se il salvataggio è fallito
        print(f"❌ Errore salvataggio: {save_result}")  # Messaggio di errore
        add_notification("❌ Errore Salvataggio", f"Impossibile salvare la partita: {save_result}", "error")  # Notifica errore
    
    # Prepara e restituisce le statistiche finali
    return jsonify({  # Restituisce dizionario JSON con risultati finali
        "status": "success",  # Stato di successo
        "final_score": game_state["score"],  # Punteggio finale raggiunto
        "cured_patients": game_state["cured_patients"],  # Numero pazienti curati
        "game_time": game_state["game_time"],  # Tempo totale di gioco
        "saved_file": save_result if save_success else None  # Nome del file salvato
    })

# Definizione della route per abbandonare il gioco manualmente
@app.route('/abandon_game')  # Route per abbandono partita
def abandon_game():  # Funzione che gestisce l'abbandono del gioco
    global game_state  # Dichiara l'uso della variabile globale di stato
    
    # Ferma il gioco e aggiunge notifica di abbandono
    game_state["is_running"] = False  # Imposta il gioco come non in esecuzione
    patient_manager.stop_threads()  # Ferma tutti i thread del gestore pazienti
    
    # Aggiunge notifica di abbandono
    add_notification("🏳️ Gioco Abbandonato", "Hai deciso di abbandonare la partita", "warning")
    
    # Attende la terminazione del thread timer se esiste
    if game_timer_thread:  # Se il thread timer è attivo
        game_timer_thread.join(timeout=1)  # Attende la terminazione con timeout di 1 secondo
    
    # Salva la partita su file JSON prima di terminare
    save_success, save_result = save_game_to_file()  # Salva lo stato della partita
    if save_success:  # Se il salvataggio è riuscito
        print(f"✅ Partita salvata con successo: {save_result}")  # Messaggio di conferma
        add_notification("💾 Salvataggio Completato", f"Partita salvata: {save_result}", "success")  # Notifica utente
    else:  # Se il salvataggio è fallito
        print(f"❌ Errore salvataggio: {save_result}")  # Messaggio di errore
        add_notification("❌ Errore Salvataggio", f"Impossibile salvare la partita: {save_result}", "error")  # Notifica errore
    
    # Prepara e restituisce le statistiche finali
    return jsonify({  # Restituisce dizionario JSON con risultati finali
        "status": "success",  # Stato di successo
        "final_score": game_state["score"],  # Punteggio finale raggiunto
        "cured_patients": game_state["cured_patients"],  # Numero pazienti curati
        "game_time": game_state["game_time"],  # Tempo totale di gioco
        "saved_file": save_result if save_success else None  # Nome del file salvato
    })

# Funzione per avviare il timer di gioco
def start_game_timer():  # Funzione che gestisce il conteggio del tempo
    def timer_loop():  # Funzione interna che esegue il ciclo di timer
        while game_state["is_running"]:  # Continua finché il gioco è attivo
            time.sleep(1)  # Attende esattamente 1 secondo
            if game_state["is_running"]:  # Controlla nuovamente che il gioco sia attivo
                game_state["game_time"] += 1  # Incrementa il contatore del tempo di 1 secondo
    
    global game_timer_thread  # Dichiara l'uso della variabile globale per il thread
    game_timer_thread = threading.Thread(target=timer_loop)  # Crea nuovo thread per il timer
    game_timer_thread.daemon = True  # Imposta il thread come daemon (si chiude con il main)
    game_timer_thread.start()  # Avvia l'esecuzione del thread timer

# Funzione di callback per gestire arrivo nuovi pazienti
def handle_patient_arrival(event_type, patient):  # Gestisce eventi di arrivo pazienti
    if event_type == "patient_arrival":  # Se l'evento è di tipo arrivo paziente
        with lock:  # Acquisisce il lock per garantire thread safety
            # Verifica se il gioco è ancora in esecuzione prima di incrementare la pressione
            if not game_state["is_running"]:  # Se il gioco è terminato
                return  # Non fare nulla
            
            # Incrementa la pressione del pronto soccorso (più alta se urgenza alta)
            pressure_increase = 15 if patient.urgency == "high" else 10  # 15 se alta, 10 altrimenti
            game_state["hospital_pressure"] += pressure_increase  # Aggiunge incremento
            
            # Crea e aggiunge notifica per nuovo paziente arrivato
            add_notification(  # Chiama funzione per aggiungere notifica
                "🚑 Nuovo Paziente Arrivato",  # Titolo della notifica
                f"{patient.name} - {patient.condition}",  # Messaggio con nome e condizione
                "info"  # Tipo di notifica informativa
            )
            
            # Verifica se la pressione ha raggiunto la soglia critica
            if game_state["hospital_pressure"] >= 100:  # Se pressione >= 100
                print(f"🚨 Pressione critica raggiunta: {game_state['hospital_pressure']}")  # Log per debug
                trigger_game_over()  # Attiva procedura game over

# Funzione di callback per gestire eventi casuali speciali
def handle_random_event(event_type, event_text):  # Gestisce eventi random del gioco
    if event_type == "random_event":  # Se l'evento è di tipo casuale
        with lock:  # Acquisisce il lock per garantire thread safety
            # Aggiunge notifica per evento speciale
            add_notification("⚡ Evento Speciale", event_text, "warning")  # Notifica evento
            
            # Aggiunge l'evento alla lista degli eventi speciali
            game_state["events"].append({  # Aggiunge dizionario evento alla lista
                "event": event_text,  # Testo descrittivo dell'evento
                "time": time.strftime("%H:%M")  # Ora corrente formattata
            })
            
            # Mantiene solo gli ultimi 5 eventi per non sovraccaricare l'interfaccia
            if len(game_state["events"]) > 5:  # Se ci sono più di 5 eventi
                game_state["events"] = game_state["events"][-5:]  # Mantiene solo gli ultimi 5

# Funzione principale per assegnare un medico a un paziente
def assign_doctor_to_patient():  # Esegue la logica di assegnazione trattamento
    global selected_patient_id  # Dichiara uso variabile globale per paziente
    global selected_doctor_id  # Dichiara uso variabile globale per medico
    
    # Verifica che siano stati selezionati sia paziente che medico
    if not selected_patient_id or not selected_doctor_id:  # Se manca una delle selezioni
        return {"status": "error", "message": "Seleziona sia paziente che medico"}  # Errore selezioni incomplete
    
    # Recupera i riferimenti ai paziente e medico selezionati
    patient = patient_manager.get_patient_by_id(selected_patient_id)  # Ottiene oggetto paziente
    doctor = doctor_manager.get_doctor_by_id(selected_doctor_id)  # Ottiene oggetto medico
    

    # Verifica che il paziente esista ancora
    if not patient:  # Se il paziente non esiste più
        return {
            "status": "error", "message": "Il paziente selezionato non è più disponibile"}  # Errore paziente non trovato
    
    # Verifica che il paziente non sia già in trattamento
    if patient.being_treated:  # Se il paziente è già in trattamento
        return {
            "status": "error", "message": "Questo paziente è già in trattamento"}  # Errore paziente occupato
    
    # Verifica che il medico esista
    if not doctor:  # Se il medico non esiste
        return {
            "status": "error", "message": "Medico non trovato"}  # Errore medico non trovato
    
    # Verifica che il medico sia disponibile
    if not doctor.available:  # Se il medico è occupato
        return {"status": "error", "message": "Medico non disponibile"}  # Errore medico non disponibile
    
    # Esegue l'assegnazione del paziente al medico
    success, message = doctor_manager.assign_patient(selected_doctor_id, patient)  # Assegnazione
    
    if success:  # Se l'assegnazione è riuscita
        with lock:  # Acquisisce il lock per thread safety
            # Verifica che il gioco sia ancora in esecuzione
            if not game_state["is_running"]:
                return {"status": "error", "message": "Il gioco è terminato"}
            
            # Calcola i punti base per la cura
            points = 100  # Punti standard per una cura
            bonus_message = ""  # Messaggio di bonus inizialmente vuoto
            
            # Verifica se si tratta di una coppia perfetta per bonus punti
            is_perfect = doctor_manager.check_perfect_couple(patient.name, doctor.name)  # Controllo coppia
            if is_perfect:  # Se è una coppia perfetta
                points = 300  # Triplica i punti a 300
                bonus_message = " 💕 Coppia Perfetta!"  # Aggiunge messaggio bonus
            
            # Aggiunge punti bonus per urgenza alta
            if patient.urgency == "high":  # Se il paziente ha urgenza alta
                points += 50  # Aggiunge 50 punti bonus
            
            # Decrementa la pressione del pronto soccorso (più bassa se urgenza alta)
            pressure_decrease = 20 if patient.urgency == "high" else 15  # 20 se alta, 15 altrimenti
            game_state["hospital_pressure"] = max(0, game_state["hospital_pressure"] - pressure_decrease)  # Decrementa, minimo 0
            
            # Aggiorna le statistiche di gioco
            game_state["score"] += points  # Aggiunge i punti al totale
            game_state["cured_patients"] += 1  # Incrementa conteggio pazienti curati
        
        # Rimuove il paziente dalla lista dei pazienti in attesa (fuori dal lock)
        patient_manager.remove_patient(selected_patient_id)  # Rimuove paziente curato
        
        # Crea notifica di cura completata
        add_notification(  # Aggiunge notifica successo
            "✅ Paziente Curato!" + bonus_message,  # Titolo con eventuale bonus
            f"{patient.name} curato da {doctor.name}. +{points} punti. Pressione: -{pressure_decrease}",  # Dettagli cura
            "couple" if is_perfect else "success"  # Tipo notifica base o speciale
        )
        
        # Resetta le selezioni dopo la cura
        selected_patient_id = None  # Deseleziona paziente
        selected_doctor_id = None  # Deseleziona medico
        
        # Verifica le condizioni per la fine del gioco
        check_game_over_conditions()  # Controlla se il gioco deve terminare
        
        return {"status": "success", "message": "Paziente curato con successo"}  # Successo
    else:  # Se l'assegnazione è fallita
        return {"status": "error", "message": message}  # Restituisce errore

# Funzione per aggiungere notifiche al sistema
def add_notification(title, message, notification_type="info"):  # Aggiunge notifica alla lista
    # Crea il dizionario della notifica con tutti i campi necessari
    notification = {  # Dizionario che rappresenta una singola notifica
        "title": title,  # Titolo principale della notifica
        "message": message,  # Messaggio descrittivo della notifica
        "type": notification_type,  # Tipo di notifica per styling
        "timestamp": time.time(),  # Timestamp UNIX per ordinamento
        "id": len(game_state["notifications"])  # ID univoco progressivo
    }
    
    # Aggiunge la notifica alla lista globale delle notifiche
    game_state["notifications"].append(notification)  # Aggiunge in coda alla lista
    
    # Limita il numero di notifiche mantenute in memoria
    if len(game_state["notifications"]) > 20:  # Se ci sono più di 20 notifiche
        game_state["notifications"] = game_state["notifications"][-20:]  # Mantiene solo le ultime 20

# Funzione per verificare le condizioni di fine gioco
def check_game_over_conditions():  # Controlla se il gioco deve terminare
    with lock:  # Acquisisce il lock per sicurezza
        # Verifica che il gioco sia ancora in esecuzione
        if not game_state["is_running"]:
            return  # Non fare nulla se il gioco è terminato
        
        # Ottiene la lista dei medici attualmente disponibili
        available_doctors = doctor_manager.get_available_doctors()  # Lista medici disponibili
        all_busy = len(available_doctors) == 0  # Flag True se tutti i medici sono occupati
        
        # Conta il numero di pazienti con urgenza alta
        high_urgency_count = patient_manager.get_high_urgency_count()  #conteggio urgenze alte
        
        # Condizione 1: pressione raggiunge o supera 100
        if game_state["hospital_pressure"] >= 100:  # Se pressione >= 100
            print(f"🚨 Game Over per pressione: {game_state['hospital_pressure']}")  # Log
            trigger_game_over()  # Attiva la procedura di fine gioco
            return  # Esci immediatamente
        
        # Condizione 2: tutti medici occupati con troppi pazienti in attesa
        if all_busy and patient_manager.get_patient_count() > 3:  # Se tutti occupati e più di 3 pazienti
            print(f"🚨 Game Over per collasso: medici occupati, {patient_manager.get_patient_count()} pazienti")  # Log
            trigger_game_over()  # Attiva la procedura di fine gioco
        
        # Condizione 3: troppe emergenze in attesa
        if high_urgency_count >= 5:  # Se 5 o più pazienti con urgenza alta
            print(f"🚨 Game Over per emergenze: {high_urgency_count} pazienti urgenza alta")  # Log
            trigger_game_over()  # Attiva la procedura di fine gioco

# Funzione per attivare la procedura di fine gioco
def trigger_game_over():  # Esegue la terminazione del gioco
    # NOTA: Questa funzione DEVE essere chiamata solo all'interno di un blocco "with lock"
    # Non usa lock interno per evitare deadlock annidati
    
    # Determina il motivo del game over
    if game_state.get("hospital_pressure", 0) >= 100:  # Se pressione >= 100
        game_over_reason = "La pressione del pronto soccorso ha raggiunto il livello critico!"
    else:  # Altrimenti è collasso normale
        game_over_reason = "Il pronto soccorso è collassato!"
    
    game_state["is_running"] = False  # Imposta il flag di gioco inattivo
    game_state["game_over"] = True  # Imposta il flag di game over per mostrare schermata finale
    
    patient_manager.stop_threads()  # Ferma tutti i thread del gestore pazienti
    
    # Aggiunge notifica di game over
    add_notification("💀 Game Over!", game_over_reason, "error")

# Punto di ingresso principale del programma
if __name__ == '__main__':  # Eseguito solo quando il file è run direttamente
    # Verifica e crea la cartella templates se non esiste
    if not os.path.exists('templates'):  # Se la cartella non esiste
        os.makedirs('templates')  # Crea la cartella per i template HTML
    
    # Verifica e crea la cartella static se non esiste
    if not os.path.exists('static'):  # Se la cartella non esiste
        os.makedirs('static')  # Crea la cartella per file statici
    
    # Stampa messaggi di avvio per l'utente
    print("Avvio Fantasy ER Operations...")  # Messaggio inizio avvio
    print("Server disponibile su: http://localhost:8082")  # Indirizzo server
    
    # Avvia l'applicazione Flask con le configurazioni specificate
    app.run(  # Avvia il server di sviluppo Flask
        host='0.0.0.0',  # Host che accetta connessioni da qualsiasi indirizzo
        port=8085,  # Porta su cui il server è in ascolto (cambiata da 8084)
        debug=True,  # Abilita modalità debug per sviluppo
        threaded=True  # Abilita supporto multithreading per richieste concorrenti
    )