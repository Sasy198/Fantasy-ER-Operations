# Fantasy ER Operations - Meme Edition (ENG)  
## Project Description

Fantasy ER Operations is a thematic emergency room simulation game featuring Italian and international meme characters. Manage a fantasy hospital where you must assign the right doctors to patients to treat them and create perfect pairs to earn special bonuses.

## Educational Requirements Met

### ✅ Mandatory
- **Python 3**: Primary development language
- **JSON files for saving**: Game state, scores, and configurations
- **Concurrent programming**: Threads for simultaneous events
- **Save and restore**: State preserved between sessions
- **Resource management**: Doctors, budget, pressure, and time
- **Modular structure**: Separate files for specific functionalities

### 🎨 Web Graphical Interface
- HTML5 + CSS3 + Bootstrap 5
- Responsive and modern design
- Smooth animations and transitions
- Popups for important events

## Game Features

### 🎮 Simplified Gameplay
- **No up-and-down mechanics**: Direct and immediate gameplay
- **Direct assignment**: Click on a patient and a doctor to treat
- **Doctor rest**: Dedicated function to recover energy

### 💕 Perfect Pair System
Seven special pairings that grant extra bonuses:
- Cardi ↔ Nicki (Dr. Nicki Fierce)
- Sgarbi ↔ Barbara (Dr. Barbara Gossip Queen)
- Rita ↔ Fagnani (Dr. Francesca Interview Beast)
- Tina ↔ Gemma (Dr. Gemma Love Seeker)
- Sara ↔ Elenoire (Dr. Elenoire VIP Drama)
- Kim ↔ Khloe (Dr. Khloe Cry Healer)
- Giucas ↔ Cipriani (Dr. Cipriani Opinionista)

### 🎯 Events and Popups
- **New patient**: Animated popup when a patient arrives
- **Patient treated**: Notification when a doctor completes treatment
- **Perfect pair**: Special celebration for correct pairings
- **Game Over**: Final screen with score

### 📊 Resource System
- **Score**: Increases with each treatment and special bonuses
- **Pressure**: Manage hospital stress (increases with arrivals, decreases with treatments)
- **Budget**: Limited financial resources for treatments
- **Doctor fatigue**: Energy system requiring rest

## Project Structure

```
├── app.py              # Flask server and main game logic
├── doctors.py          # Doctor class and management
├── patients.py         # Patient class and generation
├── utils.py            # Utility functions and save management
├── templates/
│   └── index.html      # Complete web graphical interface
├── images/             # Character images
├── data/               # JSON save files (created automatically)
└── README.md           # Project documentation
```

## Startup Instructions

### Prerequisites
- Python 3.8 or higher
- Pip (Python package manager)

### Installation
```bash
# Install required dependencies
pip install flask

# Start the game server
python app.py
```

### Access the Game
Open your browser and visit:
- **Local**: http://localhost:8085

## How to Play

1. **Wait for patients**: Patients arrive automatically every 5-10 seconds
2. **Selection**: Click on a patient and then on an available doctor
3. **Treatment**: Press "Assign Doctor" to start treatment
4. **Rest**: Use "Rest Doctor" to recover energy
5. **Pairs**: Try to create perfect pairs for extra bonuses
6. **Victory**: Survive as long as possible with limited resources

## Team Components

This project was developed as an example for computer science students, demonstrating the practical application of:
- Concurrent programming (threading)
- Persistent state management (JSON)
- Web development (Flask + HTML/CSS/JS)
- Modular code structure
- Game design and UX

## Technical Features

### 🔄 Concurrent Management
- Threads for patient arrivals (background)
- Threads for random events (emergencies)
- Locks for safe access to shared resources
- Real-time updates without refresh

### 💾 Data Persistence
- Automatic game state saving
- Restore previous sessions
- Standard and readable JSON format
- Error handling for loading

### 🎨 Responsive Design
- Bootstrap 5 for mobile-friendly layout
- CSS3 for smooth animations
- JavaScript for interactivity
- Modern and professional graphics

## Future Extensions

### Possible Improvements
- Level system and increasing difficulty
- New characters and medical specializations
- Online leaderboard for top scores
- Competitive multiplayer mode
- Achievement system and rewards

### Thematic Expansions
- Special seasons with limited characters
- Temporary events with unique bonuses
- Collaborations with other meme franchises
- Customizable avatars and hospital

## License

Educational project developed for learning purposes. Code freely usable for learning and inspiration.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Fantasy ER Operations - Meme Edition (IT)

## Descrizione del Progetto

Fantasy ER Operations è un gioco di simulazione di pronto soccorso tematico con personaggi meme italiani e internazionali. Gestisci un ospedale fantasy dove devi assegnare i medici giusti ai pazienti per curarli e creare coppie perfette per ottenere bonus speciali.

## Requisiti Didattici Soddisfatti

### ✅ Obbligatori
- **Python 3**: Linguaggio principale dello sviluppo
- **File JSON per salvataggio**: Stato del gioco, punteggi e configurazioni
- **Programmazione concorrente**: Thread per eventi simultanei
- **Salvataggio e ripristino**: Stato preservato tra sessioni
- **Gestione risorse**: Medici, budget, pressione e tempo
- **Struttura modulare**: File separati per funzionalità specifiche

### 🎨 Interfaccia Grafica Web
- HTML5 + CSS3 + Bootstrap 5
- Design responsive e moderno
- Animazioni e transizioni fluide
- Popup per eventi importanti

## Caratteristiche del Gioco

### 🎮 Gameplay Semplificato
- **Niente meccaniche di sali e scendi**: Gameplay diretto e immediato
- **Assegnazione diretta**: Click su paziente e medico per curare
- **Riposo medici**: Funzione dedicata per recuperare energia

### 💕 Sistema di Coppie Perfette
Sette abbinamenti speciali che garantiscono bonus extra:
- Cardi ↔ Nicki (Dr. Nicki Fierce)
- Sgarbi ↔ Barbara (Dr. Barbara Gossip Queen) 
- Rita ↔ Fagnani (Dr. Francesca Interview Beast)
- Tina ↔ Gemma (Dr. Gemma Love Seeker)
- Sara ↔ Elenoire (Dr. Elenoire VIP Drama)
- Kim ↔ Khloe (Dr. Khloe Cry Healer)
- Giucas ↔ Cipriani (Dr. Cipriani Opinionista)

### 🎯 Eventi e Popup
- **Nuovo paziente**: Popup animato quando arriva un paziente
- **Paziente curato**: Notifica quando un medico completa una cura
- **Coppia perfetta**: Celebrazione speciale per abbinamenti corretti
- **Game Over**: Schermata finale con punteggio

### 📊 Sistema di Risorse
- **Punteggio**: Aumenta con ogni cura e bonus speciali
- **Pressione**: Gestione stress ospedale (aumenta con arrivi, diminuisce con cure)
- **Budget**: Risorse finanziarie limitate per le cure
- **Fatica medici**: Sistema energia che richiede riposo

## Struttura del Progetto

```
├── app.py              # Server Flask e logica di gioco principale
├── doctors.py          # Classe Doctor e gestione medici
├── patients.py         # Classe Patient e generazione pazienti
├── utils.py            # Funzioni utili e gestione salvataggi
├── templates/
│   └── index.html      # Interfaccia grafica web completa
├── images/             # Immagini dei personaggi
├── data/               # File JSON di salvataggio (creato automaticamente)
└── README.md           # Documentazione del progetto
```

## Istruzioni di Avvio

### Prerequisiti
- Python 3.8 o superiore
- Pip (gestore pacchetti Python)

### Installazione
```bash
# Installa le dipendenze richieste
pip install flask

# Avvia il server di gioco
python app.py
```

### Accesso al Gioco
Apri il browser e visita:
- **Locale**: http://localhost:8085

## Come Giocare

1. **Attesa pazienti**: I pazienti arrivano automaticamente ogni 5-10 secondi
2. **Selezione**: Clicca su un paziente e poi su un medico disponibile
3. **Cura**: Premi "Assegna Medico" per iniziare il trattamento
4. **Riposo**: Usa "Fai Riposare Medico" per recuperare energia
5. **Coppie**: Cerca di creare le coppie perfette per bonus extra
6. **Vittoria**: Sopravvivi il più possibile con risorse limitate

## Componenti del Team

Questo progetto è stato sviluppato come esempio per studenti di informatica, dimostrando l'applicazione pratica dei concetti di:
- Programmazione concorrente (threading)
- Gestione stato persistente (JSON)
- Sviluppo web (Flask + HTML/CSS/JS)
- Struttura modulare del codice
- Game design e UX

## Funzionalità Tecniche

### 🔄 Gestione Concostante
- Thread per arrivi pazienti (background)
- Thread per eventi casuali (emergenze)
- Lock per accesso sicuro alle risorse condivise
- Aggiornamento real-time senza refresh

### 💾 Persistenza Dati
- Salvataggio automatico stato gioco
- Ripristino sessioni precedenti
- Formato JSON standard e leggibile
- Gestione errori di caricamento

### 🎨 Design Responsive
- Bootstrap 5 per layout mobile-friendly
- CSS3 per animazioni fluide
- JavaScript per interattività
- Grafica moderna e professionale

## Estensioni Future

### Possibili Miglioramenti
- Sistema di livelli e difficoltà crescente
- Nuovi personaggi e specializzazioni mediche
- Classifica online dei migliori punteggi
- Modalità multiplayer competitiva
- Sistema achievement e premi

### Espansioni Tematiche
- Stagioni speciali con personaggi limitati
- Eventi temporanei con bonus unici
- Collaborazioni con altri franchise meme
- Personalizzazione avatar e ospedale

## Licenza

Progetto educativo sviluppato per scopi didattici. Codice liberamente utilizzabile per apprendimento e ispirazione.
