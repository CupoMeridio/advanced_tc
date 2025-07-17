[![it](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/CupoMeridio/advanced_tc/blob/main/README.md)

# 📅 AdvancedTC - Advanced Timesheet Calendar

Una app custom per ERPNext che fornisce una vista calendario avanzata per gestire i dettagli dei timesheet (Time Sheet Detail) con funzionalità complete di CRUD, export e reporting.

## 🎯 Perché AdvancedTC?

### Limitazioni del Sistema Base ERPNext

ERPNext, pur essendo un eccellente sistema ERP open-source, presenta alcune limitazioni significative nella gestione dei timesheet che hanno motivato lo sviluppo di questa custom app:

#### 🚫 **Problemi del Sistema Standard**

1. **Vista Calendario Limitata**: ERPNext fornisce una vista calendario solo per i Timesheet principali, ma non per i Timesheet Detail, che sono gestibili esclusivamente tramite interfaccia tabulare, rendendo difficile la visualizzazione e modifica temporale delle singole attività

2. **Interfaccia Poco Intuitiva**: La gestione dei Timesheet Detail avviene tramite form tradizionali, senza drag & drop o editing visuale

3. **Filtri Limitati**: Il sistema base non offre filtri avanzati per Employee, Project, Activity Type e Task in un'unica vista

4. **Export Limitato**: Mancanza di funzionalità di export CSV personalizzate con statistiche dettagliate

5. **Gestione Pause Complessa**: Difficoltà nella gestione di break e pause pranzo all'interno delle attività

6. **Validazione Task-Employee-Project Mancante**: ERPNext permette di creare task per un progetto e assegnarle a dipendenti che non sono associati a quel progetto, causando confusione nella gestione e problemi di controllo accessi

#### ✅ **Soluzioni Implementate in AdvancedTC**

- **Vista Calendario Moderna**: Interfaccia basata su FullCalendar.js con visualizzazione temporale intuitiva
- **Drag & Drop**: Modifica visuale delle attività con trascinamento e ridimensionamento
- **Filtri Avanzati**: Sistema di filtri integrato nella sidebar per una navigazione efficiente
- **Export Intelligente**: Funzionalità di export CSV
- **Gestione Pause Avanzata**: Supporto nativo per break con creazione automatica di attività separate
- **Validazione Task-Employee-Project**: Sistema di controllo che impedisce l'assegnazione di task a dipendenti non associati al progetto
- **Integrazione Completa**: Mantiene la compatibilità totale con il sistema ERPNext esistente

## 📑 Indice

1. [Perché AdvancedTC?](#-perché-advancedtc)
2. [Caratteristiche Principali](#-caratteristiche-principali)
3. [Prerequisiti](#-prerequisiti)
4. [Installazione](#-installazione)
5. [Accesso all'Applicazione](#-accesso-allapplicazione)
6. [Verifica Configurazione](#-verifica-configurazione)
7. [Controllo Accessi Progetti](#-controllo-accessi-progetti)
8. [Risoluzione Problemi](#-risoluzione-problemi)
9. [Utilizzo](#-utilizzo)
10. [Architettura Tecnica](#-architettura-tecnica)
11. [Funzionalità Dettagliate](#-funzionalità-dettagliate)
12. [Personalizzazione](#-personalizzazione)
13. [Configurazione](#-configurazione)
14. [Troubleshooting](#-troubleshooting)
15. [Testing](#-testing)
16. [Funzionalità Avanzate](#-funzionalità-avanzate)
17. [Contribuire](#-contribuire)
18. [Licenza](#-licenza)
19. [Supporto](#-supporto)
20. [Changelog](#-changelog)
21. [Informazioni sul Progetto](#-informazioni-sul-progetto)
22. [Risorse Aggiuntive](#-risorse-aggiuntive)

## 🎯 Caratteristiche Principali

- **Vista Calendario Interattiva**: Visualizzazione moderna con FullCalendar.js
- **Filtri Avanzati**: Employee, Project, Activity Type e Task con visibilità basata sui ruoli
- **Gestione Completa CRUD**: Crea, modifica, elimina attività
- **Drag & Drop**: Sposta e ridimensiona attività
- **Integrazione ERPNext**: Completa con Timesheet e Timesheet Detail
- **Sistema di Assegnazione Progetti**: Utilizza la funzionalità "Assign To" di ERPNext per il controllo accessi
- **Accesso Basato sui Ruoli**: I manager vedono tutti i progetti, gli employee solo quelli assegnati
- **Export e Reporting**: CSV export con statistiche dettagliate
- **Gestione Pause**: Supporto completo per break e pause pranzo
- **Personalizzazione**: Colori dinamici e configurazioni avanzate
- **Creazione Automatica Workspace**: Workspace dedicata creata durante l'installazione
- **Integrazione Sezione Apps**: Accesso diretto dalla sezione apps di ERPNext

## 📋 Prerequisiti

- **ERPNext**: v15+ o Frappe Framework v15+
- **Python**: 3.10+ (come specificato nel pyproject.toml)
- **Moduli**: Accesso ai moduli Timesheet di ERPNext
- **Permessi**: Gestione Timesheet e Timesheet Detail
- **Browser**: Moderno con supporto ES6+
- **Bench**: Configurato correttamente per il sito ERPNext

## 🚀 Installazione

### 1. Ottieni l'app

```bash
# Naviga nella directory principale del bench
cd /path/to/frappe-bench

# Scarica l'app dal repository
bench get-app https://github.com/CupoMeridio/advanced_tc.git
```

### 2. Verifica la struttura dell'app

```bash
# Verifica che la struttura sia corretta
ls /path/to/frappe-bench/apps/advanced_tc/
# Dovresti vedere: advanced_tc/, setup.py, pyproject.toml, README.md, license.txt

# Verifica i file essenziali
ls /path/to/frappe-bench/apps/advanced_tc/advanced_tc/
# Dovresti vedere: __init__.py, hooks.py, modules.txt, install.py, api/, public/, config/
```

### 3. Installa l'app
```bash
# Far partire il bench
bench start
```
Aprire un nuovo terminale, navigare fino alla cartella del bench ed eseguire:
```bash
# Installa l'app sul sito specifico
bench --site [nome-sito] install-app advanced_tc
```

### 4. Migra il database

```bash
# Esegui la migrazione per applicare le modifiche al database
bench --site [nome-sito] migrate
```

### 5. Riavvia il server

```bash
bench restart
```

## 🚀 Accesso all'Applicazione

Dopo l'installazione riuscita, puoi accedere ad Advanced Timesheet Calendar in tre modi:

### 1. Sezione Apps
- Naviga al desktop di ERPNext
- Clicca sulla sezione **"Apps"**
- Cerca l'icona **"Advanced Timesheet Calendar"** con il simbolo del calendario
- Clicca sull'icona per avviare l'applicazione

### 2. Workspace Dedicata
- Naviga alla workspace **"Advanced Timesheet Calendar"**
- Questa workspace viene creata automaticamente durante l'installazione
- Contiene scorciatoie e collegamenti all'applicazione

### 3. Link Diretto
- Naviga direttamente a: `https://tuo-sito.com/app/advanced_tc`
- Oppure usa il percorso relativo: `/app/advanced_tc`

### Configurazione Iniziale

**Per i Manager:**
- Vedrai immediatamente tutti i progetti aperti nel calendario
- Usa la funzione "Assign To" di ERPNext per assegnare progetti agli employee

**Per gli Employee:**
- Se non hai progetti assegnati, vedrai un messaggio per contattare HR
- Una volta assegnati i progetti, vedrai solo i tuoi progetti assegnati

## ✅ Verifica Configurazione

### Struttura File Richiesta

L'app deve avere questa struttura per funzionare correttamente:

```
advanced_tc/
├── advanced_tc/
│   ├── __init__.py                    # Versione app (0.0.1)
│   ├── hooks.py                       # Configurazione app
│   ├── modules.txt                    # Moduli (advanced_tc)
│   ├── patches.txt                    # Patch database
│   ├── install.py                     # Script installazione
│   ├── pyproject.toml                 # Configurazione progetto Python
│   ├── api/
│   │   ├── __init__.py
│   │   └── timesheet_details.py       # API backend
│   ├── public/
│   │   ├── .gitkeep
│   │   ├── css/
│   │   │   └── timesheet_calendar.css # Stili CSS
│   │   ├── images/                    # Risorse immagini
│   │   └── js/
│   │       └── timesheet_calendar.js  # Utilities JS
│   ├── config/                        # File configurazione (vuota)
│   ├── templates/
│   │   ├── __init__.py
│   │   └── pages/                     # Pagine template
│   └── advanced_tc/
│       ├── .frappe                    # Metadata Frappe
│       ├── __init__.py
│       └── page/
│           └── advanced_tc/
│               ├── __init__.py
│               ├── advanced_tc.json   # Configurazione pagina
│               └── advanced_tc.js     # Logica frontend
├── .gitignore                         # Regole Git ignore
├── .pre-commit-config.yaml            # Hook pre-commit
├── setup.py                           # Setup Python
├── pyproject.toml                     # Configurazione progetto
├── README.md                          # Documentazione (Inglese)
├── README.it.md                       # Documentazione (Italiano)
├── license.txt                        # Licenza

```

### Componenti Chiave

1. **hooks.py**: Configura app_name="advanced_tc", CSS, JS e workspace
2. **install.py**: Script di installazione con messaggi informativi
3. **advanced_tc.json**: Definisce la configurazione della pagina principale
4. **advanced_tc.js**: Logica frontend per calendario interattivo
5. **timesheet_details.py**: Endpoint API backend per gestione timesheet
6. **timesheet_calendar.css/js**: Stili e funzioni utility per il calendario

## 🔐 Controllo Accessi Progetti

### Visibilità Progetti Basata sui Ruoli

AdvancedTC implementa un sofisticato sistema di controllo accessi ai progetti utilizzando la funzionalità nativa "Assign To" di ERPNext:

#### **Per i Manager** (System Manager, HR Manager, HR User)
- **Accesso Completo**: Possono visualizzare e creare attività per tutti i progetti aperti
- **Nessuna Restrizione**: Visibilità completa dei progetti nei filtri e nei dialog
- **Controllo Assegnazioni**: Possono assegnare progetti agli employee utilizzando la funzione "Assign To" di ERPNext

#### **Per gli Employee**
- **Accesso Limitato**: Possono visualizzare solo i progetti assegnati tramite "Assign To"
- **Filtri Automatici**: I filtri progetti e i dialog di creazione attività mostrano solo i progetti assegnati
- **Nessun Accesso senza Assegnazione**: Se non hanno progetti assegnati, vedono una lista vuota con istruzioni per contattare HR

### Come Assegnare Progetti agli Employee

1. **Naviga al Progetto**: Vai a qualsiasi documento Progetto in ERPNext
2. **Usa Assign To**: Clicca il pulsante "Assign To" nella sidebar
3. **Seleziona Employee**: Scegli l'employee/gli employee da assegnare al progetto
4. **Accesso Automatico**: L'employee vedrà immediatamente il progetto in AdvancedTC

### Funzionalità di Sicurezza

- **Controllo Accessi Automatico**: Gli employee vedono solo i progetti assegnati tramite "Assign To"
- **Filtri Coerenti**: Le stesse regole di accesso si applicano a tutti i filtri e dialog
- **Integrazione ERPNext**: Utilizza il sistema nativo ToDo di ERPNext per le assegnazioni

## 🔧 Risoluzione Problemi

### Errore "No module named 'advanced_tc'"

**Causa**: L'app non è stata copiata correttamente nella directory `apps/`

**Soluzione**:
```bash
# Verifica che l'app sia nella directory corretta
ls /path/to/frappe-bench/apps/advanced_tc

# Se non c'è, copia l'app
cp -r /path/to/advanced_tc /path/to/frappe-bench/apps/

# Verifica che i file essenziali esistano
ls /path/to/frappe-bench/apps/advanced_tc/advanced_tc/hooks.py
ls /path/to/frappe-bench/apps/advanced_tc/advanced_tc/__init__.py

# Riavvia il bench
# Alcune volte riavviare il bench risolve il problema
bench restart
# oppure riavvia manualmente con Ctrl+c e
bench start
```

### Errore "InvalidGitRepositoryError"

**Causa**: La cartella non è un repository Git valido

**Soluzione**:
```bash
# Opzione 1: Inizializza come repository Git
cd /path/to/advanced_tc
git init
git add .
git commit -m "Initial commit"

# Opzione 2: Copia manuale (più semplice)
cp -r /path/to/advanced_tc /path/to/frappe-bench/apps/
cd /path/to/frappe-bench
bench --site [nome-sito] install-app advanced_tc
```

### Errore durante l'installazione

**Verifica**:
1. **Versione Python**: Assicurati di usare Python 3.10+
2. **Permessi**: Verifica i permessi di base di ERPNext sui doctype Timesheet
3. **Dipendenze**: Controlla che ERPNext v15+ sia installato
4. **Logs**: Controlla i log per errori specifici

```bash
# Controlla i log
tail -f /path/to/frappe-bench/logs/web.log
tail -f /path/to/frappe-bench/logs/worker.log
```

### L'app è installata ma non funziona

**Verifica**:
1. **Migrazione**: Assicurati che la migrazione sia completata
2. **Permessi utente**: Verifica che l'utente abbia i ruoli di base di ERPNext necessari
3. **Cache**: Pulisci la cache del browser
4. **Riavvio**: Riavvia completamente il bench

```bash
# Forza migrazione
bench --site [nome-sito] migrate

# Pulisci cache
bench --site [nome-sito] clear-cache

# Riavvia tutto
bench restart
```

## 📖 Utilizzo

### Accesso alla Calendar View

1. **Accedi** a ERPNext
2. **Vai** al modulo **AdvancedTC** o cerca "Advanced Timesheet Calendar"
3. **Visualizza** la vista calendario con tutte le attività

### Funzionalità Principali

#### 🔍 Filtri Avanzati
- **Employee**: Filtra per dipendente specifico (manager vedono tutti, employee solo se stessi)
- **Project**: Filtra per progetto (basato su assegnazioni "Assign To")
- **Activity Type**: Filtra per tipo di attività
- **Task**: Filtra per task specifico

#### ➕ Aggiungere Attività
1. **Clicca** "Add Activity" o seleziona un intervallo di tempo nel calendario
2. **Compila** il form con:
   - Employee (obbligatorio)
   - From Time / To Time (obbligatori)
   - Project (opzionale)
   - Task (opzionale)
   - Activity Type (opzionale)
   - Description (opzionale)
   - Break Start/End (opzionale)
3. **Clicca** "Create" per salvare

#### ✏️ Modificare Attività
- **Drag & Drop**: Trascina l'attività per cambiarle data/ora
- **Ridimensiona**: Trascina i bordi per modificare la durata
- **Edit Dialog**: Clicca sull'attività per aprire il dialog di modifica

#### 🗑️ Eliminare Attività
1. **Clicca** sull'attività per aprire il dialog
2. **Clicca** "Delete"
3. **Conferma** l'eliminazione

#### 📊 Export e Reporting

**Accesso alla Funzionalità:**
La funzionalità di export è accessibile tramite il pulsante **"Generate Report"** nella sidebar laterale.

**Come utilizzare:**
1. **Naviga** nel calendario per selezionare il periodo desiderato
2. **Applica** eventuali filtri (dipendente, progetto) se necessario
3. **Clicca** sul pulsante "Generate Report" nella sidebar
4. **Visualizza** il dialog di riepilogo con:
   - Totale ore del periodo visualizzato
   - Breakdown dettagliato per dipendente
   - Breakdown per progetto
   - Breakdown per tipo di attività
5. **Clicca** "Export CSV" per scaricare i dati in formato CSV



#### ⚙️ Impostazioni
1. **Clicca** "Settings" nella sidebar
2. **Configura** le preferenze:
   - Default work shift time
   - Default break time
3. **Salva** le impostazioni

#### 📅 Viste Calendario
- **Month**: Vista mensile completa
- **Week**: Vista settimanale (default)
- **Day**: Vista giornaliera dettagliata

## 🏗️ Architettura Tecnica

### Integrazione ERPNext

AdvancedTC si integra completamente con ERPNext utilizzando:

- **Timesheet**: Contenitore settimanale delle attività
- **Timesheet Detail**: Singola attività/voce timesheet
- **Employee**: Informazioni dipendente
- **Project**: Collegamento ai progetti con sistema "Assign To"
- **Task**: Collegamento alle attività
- **Activity Type**: Categorizzazione delle attività

### Tecnologie Utilizzate

- **Backend**: Python con Frappe Framework
- **Frontend**: JavaScript con FullCalendar.js
- **Database**: MariaDB/MySQL (ERPNext standard)
- **UI**: Frappe UI components

## 🚀 Funzionalità Dettagliate

### 1. Gestione Timesheet Settimanali

L'app implementa una gestione intelligente dei timesheet:

- **Creazione Automatica**: Crea automaticamente timesheet settimanali quando necessario
- **Settimana Lavorativa**: Calcola automaticamente l'inizio settimana (lunedì)
- **Eliminazione Intelligente**: Rimuove automaticamente timesheet vuoti

### 2. Sistema di Colori Dinamici

Ogni progetto riceve automaticamente un colore consistente:

- **Colori Consistenti**: Stesso progetto = stesso colore sempre
- **Distribuzione Uniforme**: Algoritmo che distribuisce i colori equamente
- **Nessuna Configurazione**: Funziona automaticamente senza setup

### 3. Validazione e Controlli

L'app include controlli automatici per garantire la qualità dei dati:

- **Controllo Sovrapposizioni**: Previene sovrapposizioni temporali tra attività
- **Validazione Orari**: Verifica che gli orari siano logici e validi
- **Controllo Permessi**: Verifica che l'utente possa modificare i dati
- **Validazione Durata**: Controlla che le attività abbiano durata ragionevole

### 4. Drag & Drop Avanzato

Funzionalità di trascinamento intuitiva:

- **Sposta Attività**: Trascina per cambiare data e ora
- **Ridimensiona**: Modifica la durata trascinando i bordi
- **Feedback Visivo**: Notifiche e stati di caricamento
- **Rollback Automatico**: Annulla modifiche in caso di errore

### 5. Sistema di Filtri

Filtri avanzati per una navigazione efficiente:

- **Employee**: Filtra per dipendente (con controllo permessi)
- **Project**: Filtra per progetto (basato su assegnazioni)
- **Activity Type**: Filtra per tipo di attività
- **Task**: Filtra per task specifico
- **Combinazioni**: Usa più filtri contemporaneamente

### 6. Export e Reporting Avanzato

Funzionalità complete di esportazione e analisi:

- **Export CSV**: Esporta dati in formato CSV con tutti i dettagli
- **Dialog Riepilogo**: Visualizza statistiche del periodo selezionato
- **Breakdown Dettagliato**: Analisi per dipendente, progetto e tipo attività
- **Filtri Export**: Esporta solo i dati filtrati

### 7. Gestione Pause e Break

Supporto completo per la gestione delle pause:

- **Break Start/End**: Definisci orari di pausa nell'attività
- **Calcolo Automatico**: Le ore di pausa vengono sottratte dal totale
- **Validazione**: Controlli automatici per orari di pausa validi
- **Ore Effettive**: Calcolo preciso delle ore lavorate

## 🎨 Personalizzazione

AdvancedTC offre diverse opzioni di personalizzazione:

- **Colori Automatici**: I progetti ricevono automaticamente colori consistenti
- **Interfaccia Responsive**: Si adatta a desktop, tablet e mobile
- **Temi**: Compatibile con i temi di ERPNext
- **Estensibilità**: Possibilità di aggiungere funzionalità personalizzate

## 🔧 Configurazione

### Permessi

L'app utilizza i ruoli e permessi standard di ERPNext:

- **Employee**: Accesso ai propri timesheet
- **HR User**: Funzionalità HR estese
- **HR Manager**: Gestione completa HR
- **System Manager**: Accesso completo

### Performance

Per ottimizzare le prestazioni:

- **Filtri Periodo**: Limita la visualizzazione a periodi ragionevoli
- **Cache**: Utilizza la cache di ERPNext per i dati frequenti
- **Indici**: Database ottimizzato per query timesheet

## 🐛 Troubleshooting

### Problemi Comuni

#### 1. Calendar non si carica

**Sintomi**: 
- Pagina bianca o vuota
- Errori JavaScript nella console del browser
- Calendario non viene renderizzato

**Soluzioni**:

1. **Ricostruisci e riavvia il sistema**:
   ```bash
   bench build
   bench restart
   ```

2. **Verifica i permessi utente**:
   ```bash
   bench --site [nome-sito] console
   >>> frappe.get_roles("[nome-utente]")
   ```
   L'utente deve avere almeno i ruoli: `Employee`, `HR User`, `HR Manager`, o `System Manager` con accesso ai Timesheet.

3. **Pulisci la cache del browser**:
   - Premi `Ctrl+Shift+R` (Windows/Linux) o `Cmd+Shift+R` (Mac)
   - Oppure apri gli strumenti sviluppatore (F12) e fai click destro sul pulsante di ricarica → "Svuota cache e ricarica"

4. **Controlla la console del browser**:
   - Apri gli strumenti sviluppatore (F12)
   - Vai alla scheda "Console"
   - Cerca errori relativi a FullCalendar o file JavaScript mancanti

#### 2. Errori API

**Sintomi**: Errori 500 o timeout

**Debug**:
```python
# Abilita logging dettagliato
import frappe
frappe.log_error("Debug info", "Timesheet Calendar")

# Controlla query SQL
frappe.db.sql("SELECT * FROM tabTimesheet LIMIT 1", debug=1)
```

#### 3. Stili non applicati

**Soluzioni**:
```bash
# Ricompila assets
bench build --app advanced_tc

# Verifica path CSS
ls -la sites/assets/advanced_tc/css/

# Hard refresh browser
Ctrl+F5 (Windows) / Cmd+Shift+R (Mac)
```

#### 4. Problemi Drag & Drop

**Cause comuni**:
- Permessi insufficienti
- Sovrapposizioni temporali
- Validazione fallita

**Debug**:
```javascript
// Console browser
console.log("Event drop:", info.event);
console.log("New time:", info.event.start, info.event.end);
```

### Debug Avanzato

#### Logging Backend

```python
# In api/timesheet_details.py
import frappe
import json

def debug_log(message, data=None):
    frappe.log_error(
        json.dumps({
            "message": message,
            "data": data,
            "user": frappe.session.user
        }), 
        "AdvancedTC Debug"
    )
```

#### Logging Frontend

```javascript
// In advanced_tc.js
class DebugLogger {
    static log(message, data) {
        if (window.location.hostname === 'localhost') {
            console.log(`[AdvancedTC] ${message}`, data);
        }
    }
}
```

## 🧪 Testing

### Test Unitari

**File**: `tests/test_timesheet_details.py`

```python
import unittest
import frappe
from advanced_tc.api.timesheet_details import create_timesheet_detail

class TestTimesheetDetails(unittest.TestCase):
    def setUp(self):
        # Setup test data
        pass
    
    def test_create_activity(self):
        # Test creazione attività
        pass
    
    def test_overlap_validation(self):
        # Test validazione sovrapposizioni
        pass
```

### Test Integrazione

```python
def test_weekly_timesheet_creation():
    """Test creazione automatica timesheet settimanale"""
    # Crea attività per nuova settimana
    # Verifica creazione timesheet
    # Verifica calcolo ore
```

### Test Frontend

```javascript
// Test con Jest o simili
describe('AdvancedTimesheetCalendar', () => {
    test('should initialize calendar', () => {
        // Test inizializzazione
    });
    
    test('should handle time selection', () => {
        // Test selezione tempo
    });
});
```

## 🚀 Funzionalità Avanzate

### 1. Gestione Break Avanzata

#### Configurazione Break Automatici

```python
# Configurazione break automatici
AUTO_BREAK_RULES = {
    "lunch_break": {
        "min_duration_hours": 6,
        "break_duration_minutes": 30,
        "break_start_time": "12:00"
    }
}
```

#### Calcolo Ore Nette

```javascript
calculateNetHours: function(startTime, endTime, breakStart, breakEnd) {
    const totalMs = endTime - startTime;
    const breakMs = breakEnd && breakStart ? breakEnd - breakStart : 0;
    return (totalMs - breakMs) / (1000 * 60 * 60); // Ore nette
}
```

### 2. Keyboard Shortcuts

Scorciatoie da tastiera disponibili:
- **Ctrl+N**: Crea nuova attività
- **Ctrl+R**: Aggiorna calendario

## 🤝 Contribuire

### Processo di Contribuzione

1. **Fork** del progetto
2. **Crea** un branch per la feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** delle modifiche (`git commit -m 'Add some AmazingFeature'`)
4. **Push** al branch (`git push origin feature/AmazingFeature`)
5. **Apri** una Pull Request

### Guidelines di Sviluppo

#### Codice Python

```python
# Segui PEP 8
# Usa docstrings
def create_timesheet_detail(data):
    """Crea una nuova attività timesheet.
    
    Args:
        data (dict): Dati dell'attività
        
    Returns:
        dict: Risultato operazione
        
    Raises:
        ValidationError: Se i dati non sono validi
    """
```

#### Codice JavaScript

```javascript
// Usa ES6+
// Commenta funzioni complesse
/**
 * Gestisce la selezione di un intervallo di tempo nel calendario
 * @param {Object} info - Informazioni selezione FullCalendar
 */
handle_time_selection(info) {
    // Implementazione
}
```

#### CSS

```css
/* Usa BEM methodology */
.calendar-container__sidebar {
    /* Stili sidebar */
}

.calendar-container__sidebar--collapsed {
    /* Stato collassato */
}
```

### Testing

Prima di inviare una PR:

```bash
# Test Python
python -m pytest tests/

# Lint JavaScript
npm run lint

# Test manuale
# - Crea/modifica/elimina attività
# - Test drag & drop
# - Test export

```

## 📝 Licenza

Questo progetto è rilasciato sotto licenza **GPL-3.0**. Vedi il file `license.txt` per i dettagli completi.

### Utilizzo Commerciale

- ✅ **Permesso**: Uso commerciale
- ✅ **Permesso**: Modifica e distribuzione
- ✅ **Permesso**: Uso privato
- ❗ **Requisito**: Mantenere licenza GPL-3.0
- ❗ **Requisito**: Rendere disponibile il codice sorgente

## 📞 Supporto

### Canali di Supporto

- **Issues GitHub**: Per bug e feature request
- **Discussions**: Per domande generali
- **Wiki**: Per documentazione aggiuntiva

### Informazioni Debug

Quando riporti un problema, includi:

```bash
# Versione ERPNext
bench version

# Log errori
bench logs

# Configurazione browser
# - Versione browser
# - Console errors (F12)
# - Network tab per errori API
```

### FAQ

**Q: Come aggiungere nuovi Activity Types?**
A: Vai in ERPNext > Setup > Activity Type e crea nuovi tipi.

**Q: Posso personalizzare i colori?**
A: Sì, modifica la funzione `get_event_color()` in `api/timesheet_details.py`.

**Q: Come esportare dati per periodi lunghi?**
A: Usa i filtri per limitare il dataset, poi esporta in CSV.

**Q: L'app funziona con ERPNext Cloud?**
A: Sì, ma richiede installazione custom app (contatta il supporto ERPNext).

## 📋 Changelog

### v0.1.1 (Corrente)
- ✅ **NUOVO**: Pulsante "Generate Report" nella sidebar per accesso diretto all'export
- ✅ **MIGLIORATO**: Funzionalità di export ora completamente accessibile dall'UI
- ✅ **AGGIORNATO**: Documentazione consolidata in un unico file README
- ✅ Calendario interattivo con FullCalendar.js
- ✅ Integrazione completa con ERPNext
- ✅ Sistema di filtri avanzati
- ✅ Drag & drop per modifica attività
- ✅ Export CSV e reporting
- ✅ Gestione pause e break

- ✅ Validazione dati completa

### v0.1.0
- ✅ Versione iniziale con tutte le funzionalità base
- ✅ Calendario interattivo con FullCalendar.js
- ✅ Integrazione completa con ERPNext
- ✅ Sistema di filtri avanzati
- ✅ Drag & drop per modifica attività
- ✅ Gestione pause e break

- ✅ Validazione dati completa

### v0.0.1 (Iniziale)
- ✅ Setup progetto base
- ✅ Struttura app ERPNext
- ✅ Configurazione hooks
- ✅ Prime API di base

---

## 🎓 Informazioni sul Progetto

Questo progetto è stato realizzato come attività di tirocinio presso l'azienda [**Youbiquo**](https://youbiquo.eu) da parte di due studenti dell'Università degli Studi di Salerno di Ingegneria Informatica:

- [**Fabrizio D'Errico**](https://github.com/fabriziodrr)
- [**Vittorio Postiglione**](https://github.com/CupoMeridio) 

---


## 📚 Risorse Aggiuntive

- **[📖 Documentazione Tecnica](DOCUMENTAZIONE_TECNICA.md)** - Architettura tecnica dettagliata, riferimenti API e guida allo sviluppo
- [Documentazione ERPNext](https://docs.erpnext.com/)
- [Documentazione Frappe Framework](https://frappeframework.com/docs)
- [Documentazione FullCalendar.js](https://fullcalendar.io/docs)

---

**Sviluppato con ❤️ per la comunità ERPNext**
