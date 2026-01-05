# doctors.py - Modulo per la gestione dei medici
# Progetto Fantasy ER Operations - Classe 4ª Informatica TPSIT
# Sviluppato dal gruppo Lourdes Direction
# Team Leader: Caraviello Salvatore
# Componenti: Coppola Nicole, Palumbo Annarita, Sarcinelli Valentina

# Importazione dei moduli necessari per il funzionamento
import time  # Importa modulo per gestione temporale e pause
import threading  # Importa modulo per programmazione concorrente con thread

# Definizione della classe che rappresenta un singolo medico
class Doctor:  # Classe base per tutti i medici del gioco
    def __init__(self, doctor_id, name, specialty, image_url):  # Costruttore classe
        # Inizializzazione di tutti gli attributi del medico
        self.id = doctor_id  # Identificativo numerico unico del medico
        self.name = name  # Nome completo del medico
        self.specialty = specialty  # Specializzazione medica del medico
        self.image_url = image_url  # Path dell'immagine rappresentativa del medico
        self.available = True  # Flag booleano che indica se il medico è disponibile
        self.fatigue = 0  # Contatore livello di affaticamento del medico
        self.current_patient = None  # Riferimento al paziente attualmente in cura
        self.treatment_start_time = None  # Timestamp di inizio trattamento corrente
        self.recovery_thread = None  # Riferimento al thread di recupero

# Lista predefinita dei tipi di medici disponibili nel gioco
DOCTOR_TYPES = [  # Array contenente le configurazioni dei medici
    {
        "name": "Nicki",  # Nome del medico
        "specialty": "Rap Therapy",  # Specializzazione medica del medico
        "image_url": "/static/images/nicki.png"  # Path immagine locale
    },
    {
        "name": "Barbara",  # Nome del medico
        "specialty": "Cultural Recovery",  # Specializzazione medica del medico
        "image_url": "/static/images/barbara.png"  # Path immagine locale
    },
    {
        "name": "Fagnani",  # Nome del medico
        "specialty": "Social Media Rehab",  # Specializzazione medica del medico
        "image_url": "/static/images/fagnani.png"  # Path immagine locale
    },
    {
        "name": "Gemma",  # Nome del medico
        "specialty": "TV Detox",  # Specializzazione medica del medico
        "image_url": "/static/images/gemma.png"  # Path immagine locale
    },
    {
        "name": "Elenoire",  # Nome del medico
        "specialty": "Stress Management",  # Specializzazione medica del medico
        "image_url": "/static/images/Elenoire.png"  # Immagine locale 
    },
    {
        "name": "Khloe",  # Nome del medico
        "specialty": "Meme Recovery",  # Specializzazione medica del medico
        "image_url": "/static/images/Khloe.png"  # Immagine locale 
    },
    {
        "name": "Cipriani",  # Nome del medico
        "specialty": "Reality Rehab",  # Specializzazione medica del medico
        "image_url": "/static/images/Cipriani.png"  # Path immagine locale
    }
]

# Lista delle coppie paziente-medico che danno bonus punti
PERFECT_COUPLES = [  # Array contenente le coppie speciali del gioco
    {"patient": "Cardi", "doctor": "Nicki"},  # Coppia speciale Cardi-Nicki
    {"patient": "Sgarbi", "doctor": "Barbara"},  # Coppia speciale Sgarbi-Barbara
    {"patient": "Rita", "doctor": "Fagnani"},  # Coppia speciale Rita-Fagnani
    {"patient": "Tina", "doctor": "Gemma"},  # Coppia speciale Tina-Gemma
    {"patient": "Sara", "doctor": "Elenoire"},  # Coppia speciale Sara-Elenoire
    {"patient": "Kim", "doctor": "Khloe"},  # Coppia speciale Kim-Khloe
    {"patient": "Giucas", "doctor": "Cipriani"}  # Coppia speciale Giucas-Cipriani
]

# Classe principale per la gestione di tutti i medici del gioco
class DoctorManager:  # Gestore centralizzato per operazioni sui medici
    def __init__(self):  # Costruttore del gestore medici
        # Inizializzazione delle variabili di istanza
        self.current_doctors = []  # Lista che contiene i medici attualmente disponibili
        self.doctor_counter = 0  # Contatore progressivo per ID univoci dei medici
        self.initialize_doctors()  # Chiama metodo per inizializzare i medici

    def initialize_doctors(self):  # Metodo per creare i medici iniziali
        # Itera attraverso tutti i tipi di medici predefiniti
        for doctor_type in DOCTOR_TYPES:  # Ciclo su ogni tipo di medico
            # Incrementa il contatore per generare un ID univoco
            self.doctor_counter += 1  # Incrementa contatore globale
            
            # Crea una nuova istanza di Doctor con i dati predefiniti
            doctor = Doctor(  # Istanzia nuovo oggetto medico
                doctor_id=self.doctor_counter,  # ID univoco progressivo
                name=doctor_type["name"],  # Nome predefinito del medico
                specialty=doctor_type["specialty"],  # Specializzazione predefinita
                image_url=doctor_type["image_url"]  # Path immagine predefinito
            )
            
            # Aggiunge il nuovo medico alla lista dei medici attuali
            self.current_doctors.append(doctor)  # Inserisce in coda alla lista

    def get_doctor_by_id(self, doctor_id):  # Metodo per cercare medico per ID
        # Itera attraverso tutti i medici attualmente presenti
        for doctor in self.current_doctors:  # Ciclo su ogni medico nella lista
            if doctor.id == doctor_id:  # Se l'ID corrisponde a quello cercato
                return doctor  # Restituisce il riferimento al medico trovato
        return None  # Se non trovato, restituisce None

    def get_doctor_by_name(self, doctor_name):  # Metodo per cercare medico per nome
        # Itera attraverso tutti i medici attualmente presenti
        for doctor in self.current_doctors:  # Ciclo su ogni medico nella lista
            if doctor.name == doctor_name:  # Se il nome corrisponde a quello cercato
                return doctor  # Restituisce il riferimento al medico trovato
        return None  # Se non trovato, restituisce None

    def get_available_doctors(self):  # Metodo per ottenere medici disponibili
        available = []  # Lista vuota che conterrà i medici disponibili
        
        # Itera attraverso tutti i medici attuali
        for doctor in self.current_doctors:  # Ciclo su ogni medico
            if doctor.available:  # Se il medico è attualmente disponibile
                available.append(doctor)  # Aggiunge alla lista dei disponibili
        
        return available  # Restituisce la lista dei medici disponibili

    def get_busy_doctors(self):  # Metodo per ottenere medici occupati
        busy = []  # Lista vuota che conterrà i medici occupati
        
        # Itera attraverso tutti i medici attuali
        for doctor in self.current_doctors:  # Ciclo su ogni medico
            if not doctor.available:  # Se il medico non è disponibile
                busy.append(doctor)  # Aggiunge alla lista degli occupati
        
        return busy  # Restituisce la lista dei medici occupati

    def assign_patient(self, doctor_id, patient):  # Metodo per assegnare paziente a medico
        # Cerca il medico specificato tramite ID
        doctor = self.get_doctor_by_id(doctor_id)  # Ottiene riferimento al medico
        
        if not doctor:  # Se il medico non esiste nel sistema
            return False, "Medico non trovato"  # Restituisce errore medico non trovato
        
        if not doctor.available:  # Se il medico non è attualmente disponibile
            return False, "Medico non disponibile"  # Restituisce errore medico occupato
        
        # Assegna il paziente al medico aggiornando i relativi attributi
        doctor.current_patient = patient  # Imposta il paziente corrente del medico
        doctor.available = False  # Imposta il medico come non disponibile
        doctor.treatment_start_time = time.time()  # Registra timestamp inizio trattamento
        patient.being_treated = True  # Imposta il paziente come in trattamento
        
        # Avvia il processo di recupero automatico del medico
        self.start_recovery(doctor_id)  # Avvia thread per recupero medico
        
        return True, "Paziente assegnato con successo"  # Restituisce successo

    def start_recovery(self, doctor_id):  # Metodo per avviare recupero medico
        def recovery_process():  # Funzione interna che gestisce il recupero
            # Attende 5 secondi per simulare il tempo di trattamento
            time.sleep(5)  # Pausa di 5 secondi
            
            # Cerca il medico per ID dopo il trattamento
            doctor = self.get_doctor_by_id(doctor_id)  # Ottiene riferimento al medico
            if doctor:  # Se il medico esiste ancora nel sistema
                # Resetta lo stato del medico per renderlo nuovamente disponibile
                doctor.available = True  # Imposta medico come disponibile
                doctor.current_patient = None  # Rimuove riferimento al paziente trattato
                doctor.treatment_start_time = None  # Resetta timestamp inizio trattamento
                doctor.fatigue += 1  # Incrementa livello di affaticamento
        
        # Crea e avvia il thread per il processo di recupero
        recovery_thread = threading.Thread(target=recovery_process)  # Crea thread
        recovery_thread.daemon = True  # Imposta come thread daemon
        recovery_thread.start()  # Avvia l'esecuzione del thread

    def check_perfect_couple(self, patient_name, doctor_name):  # Metodo per coppie perfette
        # Estrae il nome base del paziente (prima parola del nome completo)
        patient_base_name = patient_name.split()[0]  # Divide nome e prende prima parte
        
        # Itera attraverso tutte le coppie perfette definite
        for couple in PERFECT_COUPLES:  # Ciclo su ogni coppia speciale
            # Verifica la corrispondenza tra paziente e medico
            if (couple["patient"] == patient_base_name and  # Se nome paziente corrisponde
                couple["doctor"] == doctor_name):  # E nome medico corrisponde
                return True  # Restituisce True se è una coppia perfetta
        
        return False  # Se non corrisponde a nessuna coppia, restituisce False

    def get_available_doctors_sorted(self):  # Metodo per ottenere medici ordinati
        available_doctors = self.get_available_doctors()  # Ottiene medici disponibili
        sorted_doctors = []  # Lista vuota per medici ordinati
        
        # Separa i medici in base al livello di affaticamento
        low_fatigue = []  # Lista per medici con basso affaticamento
        high_fatigue = []  # Lista per medici con alto affaticamento
        
        # Itera attraverso i medici disponibili per classificarli
        for doctor in available_doctors:  # Ciclo su ogni medico disponibile
            if doctor.fatigue < 3:  # Se il livello di affaticamento è basso
                low_fatigue.append(doctor)  # Aggiunge alla lista basso affaticamento
            else:  # Altrimenti il livello di affaticamento è alto
                high_fatigue.append(doctor)  # Aggiunge alla lista alto affaticamento
        
        # Combina le liste mettendo prima quelli con basso affaticamento
        sorted_doctors.extend(low_fatigue)  # Aggiunge prima i medici meno affaticati
        sorted_doctors.extend(high_fatigue)  # Poi aggiunge i medici più affaticati
        
        return sorted_doctors  # Restituisce la lista ordinata dei medici

    def get_doctor_count(self):  # Metodo per contare medici totali
        return len(self.current_doctors)  # Restituisce lunghezza lista medici

    def get_available_count(self):  # Metodo per contare medici disponibili
        count = 0  # Inizializza contatore a zero
        
        # Itera attraverso tutti i medici attuali
        for doctor in self.current_doctors:  # Ciclo su ogni medico
            if doctor.available:  # Se il medico è disponibile
                count += 1  # Incrementa il contatore
        
        return count  # Restituisce il conteggio finale

    def reset_all_doctors(self):  # Metodo per resettare tutti i medici
        # Itera attraverso tutti i medici attuali
        for doctor in self.current_doctors:  # Ciclo su ogni medico
            # Resetta tutti gli attributi dello stato del medico
            doctor.available = True  # Imposta medico come disponibile
            doctor.current_patient = None  # Rimuove paziente corrente
            doctor.fatigue = 0  # Resetta livello affaticamento
            doctor.treatment_start_time = None  # Resetta timestamp inizio

    def to_dict_list(self):  # Metodo per convertire medici in lista dizionari
        result = []  # Lista vuota che conterrà i dizionari
        
        # Itera attraverso tutti i medici attuali
        for doctor in self.current_doctors:  # Ciclo su ogni medico
            # Crea un dizionario con tutti i dati del medico
            doctor_dict = {  # Dizionario che rappresenta il medico
                "id": doctor.id,  # ID univoco del medico
                "name": doctor.name,  # Nome completo del medico
                "specialty": doctor.specialty,  # Specializzazione del medico
                "image_url": doctor.image_url,  # Path immagine del medico
                "available": doctor.available,  # Stato disponibilità del medico
                "fatigue": doctor.fatigue,  # Livello affaticamento del medico
                "current_patient_id": (doctor.current_patient.id  # ID paziente corrente
                                     if doctor.current_patient else None)  # O None se nessuno
            }
            result.append(doctor_dict)  # Aggiunge il dizionario alla lista risultati
        
        return result  # Restituisce la lista completa di dizionari