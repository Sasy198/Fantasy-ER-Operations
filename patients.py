# patients.py - Modulo per la gestione dei pazienti
# Progetto Fantasy ER Operations - Classe 4ª Informatica TPSIT
# Sviluppato dal gruppo Lourdes Direction
# Team Leader: Caraviello Salvatore
# Componenti: Coppola Nicole, Palumbo Annarita, Sarcinelli Valentina

# Importazione dei moduli necessari per il funzionamento
import random  # Importa modulo per generazione di numeri e scelte casuali
import time    # Importa modulo per gestione temporale e timestamp
import threading  # Importa modulo per programmazione concorrente con thread

# Definizione della classe che rappresenta un singolo paziente
class Patient:  # Classe base per tutti i pazienti del gioco
    def __init__(self, patient_id, name, condition, urgency, image_url):  # Costruttore classe
        # Inizializzazione di tutti gli attributi del paziente
        self.id = patient_id  # Identificativo numerico unico del paziente
        self.name = name      # Nome completo e descrittivo del paziente
        self.condition = condition  # Condizione medica o problema del paziente
        self.urgency = urgency      # Livello di urgenza: high, medium, low
        self.image_url = image_url  # Path dell'immagine rappresentativa del paziente
        self.arrival_time = time.time()  # Timestamp UNIX del momento di arrivo
        self.being_treated = False  # Flag booleano che indica se è in trattamento

# Lista predefinita dei tipi di pazienti possibili nel gioco
PATIENT_TYPES = [  # Array contenente le configurazioni dei pazienti
    {
        "name": "Cardi la Beef Dragon",  # Nome completo del paziente
        "condition": "Avvelenamento da Diss Track",  # Descrizione condizione medica
        "urgency": "high",  # Livello di urgenza alto per priorità immediata
        "image_url": "/static/images/cardi.png"  # Path immagine locale
    },
    {
        "name": "Vittorio il Critico Infuriato",  # Nome completo del paziente
        "condition": "Maledizione da Cafone",  # Descrizione condizione medica
        "urgency": "medium",  # Livello di urgenza medio per trattamento normale
        "image_url": "/static/images/sgarbi.png"  # Path immagine locale (usa Sgarbi)
    },
    {
        "name": "Rita la TikToker Esplosiva",  # Nome completo del paziente
        "condition": "Avvelenamento da Belve",  # Descrizione condizione medica
        "urgency": "high",  # Livello di urgenza alto per priorità immediata
        "image_url": "/static/images/rita.png"  # Path immagine locale
    },
    {
        "name": "Tina la Vamp Opinionista",  # Nome completo del paziente
        "condition": "Ferita da Trash TV",  # Descrizione condizione medica
        "urgency": "medium",  # Livello di urgenza medio per trattamento normale
        "image_url": "/static/images/tina.png"  # Path immagine locale
    },
    {
        "name": "Sara la Torreste Esaurita",  # Nome completo del paziente
        "condition": "Esaurimento da Torre Annunziata",  # Descrizione condizione medica
        "urgency": "low",  # Livello di urgenza basso per trattamento differibile
        "image_url": "/static/images/sara.png"  # Path immagine locale 
    },
    {
        "name": "Kim la Cry Queen",  # Nome completo del paziente
        "condition": "Crisi da Meme Face",  # Descrizione condizione medica
        "urgency": "medium",  # Livello di urgenza medio per trattamento normale
        "image_url": "/static/images/kim.png"  # Path immagine locale
    },
    {
        "name": "Giucas l'Hypno Esaurito",  # Nome completo del paziente
        "condition": "Ipnosi Fallita da Reality",  # Descrizione condizione medica
        "urgency": "high",  # Livello di urgenza alto per priorità immediata
        "image_url": "/static/images/Giucas.png"  # Path immagine locale
    }
]

# Lista degli eventi casuali speciali che possono verificarsi durante il gioco
RANDOM_EVENTS = [  # Array contenente i possibili eventi casuali
    "🔴 Codice Rosso: Arrivo massiccio di pazienti!",  # Evento emergenza con molti pazienti
    "⚡ Blackout ospedaliero: Medici rallentati!",  # Evento che riduce efficienza medici
    "💊 Scorte mediche esaurite: Cure meno efficaci!",  # Evento che riduce efficacia cure
    "⭐ VIP in arrivo: Bonus punti speciali!",  # Evento positivo con bonus punti
    "🦠 Epidemia controllata: Tutti i medici disponibili!",  # Evento positivo che libera medici
    "🎉 Giornata fortunata: Punteggio raddoppiato!",  # Evento molto positivo con punteggio doppio
    "😷 Protocollo sicurezza: Medici protetti!",  # Evento che protegge i medici
    "📰 Giornalisti all'ingresso: Pressione aumentata!"  # Evento che aumenta difficoltà
]

# Classe principale per la gestione di tutti i pazienti del gioco
class PatientManager:  # Gestore centralizzato per operazioni sui pazienti
    def __init__(self):  # Costruttore del gestore pazienti
        # Inizializzazione delle variabili di istanza
        self.current_patients = []  # Lista che contiene i pazienti attualmente in ospedale
        self.patient_counter = 0    # Contatore progressivo per ID univoci dei pazienti
        self.arrival_thread = None  # Riferimento al thread per arrivo automatico pazienti
        self.event_thread = None    # Riferimento al thread per eventi casuali
        self.running = False        # Flag booleano per controllare esecuzione thread

    def generate_patient(self):  # Metodo per generare un nuovo paziente
        # Rimuovo il limite di 5 pazienti per permettere pressione > 100
        # I pazienti possono arrivare senza limite, permettendo game over per pressione eccessiva
        
        # Seleziona casualmente un tipo di paziente dalla lista predefinita
        patient_type = random.choice(PATIENT_TYPES)  # Scelta casuale tra i tipi disponibili
        
        # Incrementa il contatore per generare un ID univoco
        self.patient_counter += 1  # Incrementa contatore globale
        
        # Crea una nuova istanza di Patient con i dati scelti
        patient = Patient(  # Istanzia nuovo oggetto paziente
            patient_id=self.patient_counter,  # ID univoco progressivo
            name=patient_type["name"],        # Nome predefinito del paziente
            condition=patient_type["condition"],  # Condizione medica predefinita
            urgency=patient_type["urgency"],  # Livello urgenza predefinito
            image_url=patient_type["image_url"]  # Path immagine predefinita
        )
        
        # Aggiunge il nuovo paziente alla lista dei pazienti attuali
        self.current_patients.append(patient)  # Inserisce in coda alla lista
        
        # Restituisce il paziente appena creato
        return patient  # Ritorna riferimento al nuovo paziente

    def get_patient_by_id(self, patient_id):  # Metodo per cercare paziente per ID
        # Itera attraverso tutti i pazienti attualmente presenti
        for patient in self.current_patients:  # Ciclo su ogni paziente nella lista
            if patient.id == patient_id:  # Se l'ID corrisponde a quello cercato
                return patient  # Restituisce il riferimento al paziente trovato
        return None  # Se non trovato, restituisce None

    def remove_patient(self, patient_id):  # Metodo per rimuovere paziente dalla lista
        # Itera con indice per poter rimuovere elementi durante il ciclo
        for i, patient in enumerate(self.current_patients):  # Ciclo con indice e valore
            if patient.id == patient_id:  # Se l'ID corrisponde a quello da rimuovere
                # Rimuove il paziente dalla lista usando l'indice
                removed_patient = self.current_patients.pop(i)  # Rimuove e recupera oggetto
                return removed_patient  # Restituisce il paziente rimosso
        return None  # Se non trovato, restituisce None

    def get_available_patients(self):  # Metodo per ottenere pazienti disponibili
        available = []  # Lista vuota che conterrà i pazienti disponibili
        
        # Itera attraverso tutti i pazienti attuali
        for patient in self.current_patients:  # Ciclo su ogni paziente
            if not patient.being_treated:  # Se il paziente non è in trattamento
                available.append(patient)  # Aggiunge alla lista dei disponibili
        
        return available  # Restituisce la lista dei pazienti disponibili

    def start_automatic_arrivals(self, callback):  # Metodo per avviare arrivo automatico
        self.running = True  # Imposta il flag che indica che i thread devono girare
        
        def arrival_loop():  # Funzione interna che esegue il ciclo di arrivo
            # Ciclo infinito che continua finché il flag running è True
            while self.running:  # Continua l'esecuzione se non fermato
                # Genera un tempo di attesa casuale tra 2 e 5 secondi (più veloce)
                delay = random.randint(2, 5)  # Numero casuale tra 2 e 5
                time.sleep(delay)  # Attende il tempo generato in secondi
                
                # Verifica che il sistema sia ancora in esecuzione
                if self.running:  # Controlla nuovamente il flag di esecuzione
                    # Genera un nuovo paziente casualmente
                    patient = self.generate_patient()  # Chiama metodo di generazione
                    if patient:  # Se il paziente è stato generato con successo
                        # Esegue il callback per notificare l'arrivo
                        callback("patient_arrival", patient)  # Notifica nuovo arrivo
        
        # Crea e avvia il thread per l'arrivo automatico dei pazienti
        self.arrival_thread = threading.Thread(target=arrival_loop)  # Crea thread
        self.arrival_thread.daemon = True  # Imposta come thread daemon
        self.arrival_thread.start()  # Avvia l'esecuzione del thread

    def start_random_events(self, callback):  # Metodo per avviare eventi casuali
        def event_loop():  # Funzione interna che esegue il ciclo eventi
            # Ciclo infinito che continua finché il flag running è True
            while self.running:  # Continua l'esecuzione se non fermato
                # Genera un tempo di attesa casuale tra 5 e 10 secondi (più frequenti)
                delay = random.randint(5, 10)  # Numero casuale tra 5 e 10
                time.sleep(delay)  # Attende il tempo generato in secondi
                
                # Verifica che il sistema sia ancora in esecuzione
                if self.running:  # Controlla nuovamente il flag di esecuzione
                    # Seleziona casualmente un evento dalla lista degli eventi
                    event = random.choice(RANDOM_EVENTS)  # Scelta casuale evento
                    # Esegue il callback per notificare l'evento
                    callback("random_event", event)  # Notifica evento casuale
        
        # Crea e avvia il thread per gli eventi casuali
        self.event_thread = threading.Thread(target=event_loop)  # Crea thread
        self.event_thread.daemon = True  # Imposta come thread daemon
        self.event_thread.start()  # Avvia l'esecuzione del thread

    def stop_threads(self):  # Metodo per fermare tutti i thread attivi
        self.running = False  # Imposta il flag a False per fermare i cicli

    def get_patient_count(self):  # Metodo per contare pazienti totali
        return len(self.current_patients)  # Restituisce lunghezza lista pazienti

    def get_high_urgency_count(self):  # Metodo per contare pazienti urgenza alta
        count = 0  # Inizializza contatore a zero
        
        # Itera attraverso tutti i pazienti attuali
        for patient in self.current_patients:  # Ciclo su ogni paziente
            if patient.urgency == "high":  # Se il paziente ha urgenza alta
                count += 1  # Incrementa il contatore
        
        return count  # Restituisce il conteggio finale

    def to_dict_list(self):  # Metodo per convertire pazienti in lista dizionari
        result = []  # Lista vuota che conterrà i dizionari
        
        # Itera attraverso tutti i pazienti attuali
        for patient in self.current_patients:  # Ciclo su ogni paziente
            # Crea un dizionario con tutti i dati del paziente
            patient_dict = {  # Dizionario che rappresenta il paziente
                "id": patient.id,  # ID univoco del paziente
                "name": patient.name,  # Nome completo del paziente
                "condition": patient.condition,  # Condizione medica del paziente
                "urgency": patient.urgency,  # Livello di urgenza del paziente
                "image_url": patient.image_url,  # Path immagine del paziente
                "arrival_time": patient.arrival_time,  # Timestamp di arrivo
                "being_treated": patient.being_treated  # Flag stato trattamento
            }
            result.append(patient_dict)  # Aggiunge il dizionario alla lista risultati
        
        return result  # Restituisce la lista completa di dizionari