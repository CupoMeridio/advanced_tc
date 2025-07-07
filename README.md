# 📅 AdvancedTC - Advanced Timesheet Calendar

Una app custom per ERPNext che fornisce una vista calendario avanzata per gestire i dettagli dei timesheet (Time Sheet Detail) con funzionalità complete di CRUD, export e reporting.

## 🎯 Perché AdvancedTC?

### Limitazioni del Sistema Base ERPNext

ERPNext, pur essendo un eccellente sistema ERP open-source, presenta alcune limitazioni significative nella gestione dei timesheet che hanno motivato lo sviluppo di questa custom app:

#### 🚫 **Problemi del Sistema Standard**

1. **Vista Calendario Limitata**: ERPNext fornisce una vista calendario solo per i Timesheet principali, ma non per i Timesheet Detail, che sono gestibili esclusivamente tramite interfaccia tabulare, rendendo difficile la visualizzazione e modifica temporale delle singole attività

2. **Interfaccia Poco Intuitiva**: La gestione dei Timesheet Detail avviene tramite form tradizionali, senza drag & drop o editing visuale

3. **Filtri Limitati**: Il sistema base non offre filtri avanzati per Employee, Project e Activity Type in un'unica vista

4. **Export Limitato**: Mancanza di funzionalità di export CSV personalizzate con statistiche dettagliate

5. **Gestione Pause Complessa**: Difficoltà nella gestione di break e pause pranzo all'interno delle attività

#### ✅ **Soluzioni Implementate in AdvancedTC**

- **Vista Calendario Moderna**: Interfaccia basata su FullCalendar.js con visualizzazione temporale intuitiva
- **Drag & Drop**: Modifica visuale delle attività con trascinamento e ridimensionamento
- **Filtri Avanzati**: Sistema di filtri integrato nella sidebar per una navigazione efficiente
- **Export Intelligente**: Funzionalità di export CSV
- **Gestione Pause Avanzata**: Supporto nativo per break con creazione automatica di attività separate
- **Integrazione Completa**: Mantiene la compatibilità totale con il sistema ERPNext esistente

## 📑 Indice

1. [Perché AdvancedTC?](#-perché-advancedtc)
2. [Caratteristiche Principali](#-caratteristiche-principali)
3. [Prerequisiti](#-prerequisiti)
4. [Installazione](#-installazione)
5. [Utilizzo](#-utilizzo)
6. [Architettura Tecnica](#-architettura-tecnica)
7. [Funzionalità Dettagliate](#-funzionalità-dettagliate)
8. [Personalizzazione](#-personalizzazione)
9. [Configurazione Avanzata](#-configurazione-avanzata)
10. [Troubleshooting](#-troubleshooting)
11. [Testing](#-testing)
12. [Funzionalità Avanzate](#-funzionalità-avanzate)
13. [Contribuire](#-contribuire)
14. [Licenza](#-licenza)
15. [Supporto](#-supporto)
16. [Changelog](#-changelog)

## 🎯 Caratteristiche Principali

- **Vista Calendario Interattiva**: Visualizzazione moderna con FullCalendar.js
- **Filtri Avanzati**: Employee, Project
- **Gestione Completa CRUD**: Crea, modifica, elimina attività
- **Drag & Drop**: Sposta e ridimensiona attività
- **Integrazione ERPNext**: Completa con Timesheet e Timesheet Detail
- **Export e Reporting**: CSV export
- **Gestione Pause**: Supporto completo per break e pause pranzo
- **Personalizzazione**: Colori dinamici e configurazioni avanzate

## 📋 Prerequisiti

- **ERPNext**: v15+ o Frappe Framework v15+
- **Moduli**: Accesso ai moduli Timesheet di ERPNext
- **Permessi**: Gestione Timesheet e Timesheet Detail
- **Browser**: Moderno con supporto ES6+

## 🚀 Installazione

### 1. Clona o scarica l'app

```bash
# Naviga nella directory delle app di Frappe
cd /path/to/frappe-bench/apps

# Clona il repository
git clone <repository-url> advanced_tc
# oppure copia la cartella
cp -r /path/to/advanced_tc .
```

### 2. Installa l'app

```bash
# Torna alla directory principale del bench
cd /path/to/frappe-bench

# Installa l'app
bench install-app advanced_tc

# Installa l'app sul sito specifico
bench --site [nome-sito] install-app advanced_tc
```

### 3. Migra il database

```bash
bench --site [nome-sito] migrate
```

### 4. Riavvia il server

```bash
bench restart
```

## 📖 Utilizzo

### Accesso alla Calendar View

1. **Accedi** a ERPNext
2. **Vai** al modulo **AdvancedTC** o cerca "Advanced Timesheet Calendar"
3. **Visualizza** la vista calendario con tutte le attività

### Funzionalità Principali

#### 🔍 Filtri Avanzati
- **Employee**: Filtra per dipendente specifico
- **Project**: Filtra per progetto

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

**Implementazione Tecnica:**
```javascript
// Funzione nel file advanced_tc.js
show_report_dialog() {
    const events = this.calendar.getEvents();
    const view = this.calendar.view;
    const startDate = view.activeStart;
    const endDate = view.activeEnd;
    
    if (window.TimesheetCalendarUtils && window.TimesheetCalendarUtils.showSummaryDialog) {
        window.TimesheetCalendarUtils.showSummaryDialog(events, startDate, endDate);
    }
}
```

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

### Backend (Python)

#### API Endpoints

**File**: `api/timesheet_details.py`

```python
@frappe.whitelist()
def get_timesheet_details(start_date=None, end_date=None, filters=None):
    """Recupera le attività timesheet per il calendario"""
    
@frappe.whitelist()
def create_timesheet_detail(data):
    """Crea una nuova attività timesheet"""
    
@frappe.whitelist()
def update_timesheet_detail(name, data):
    """Aggiorna attività esistente"""
    
@frappe.whitelist()
def delete_timesheet_detail(name):
    """Elimina attività timesheet"""
```

#### Logica di Business

1. **Gestione Timesheet Settimanali**:
   - Creazione automatica se non esistente
   - Calcolo automatico dell'inizio settimana (lunedì)
   - Eliminazione automatica timesheet vuoti

2. **Validazione Dati**:
   - Controllo sovrapposizioni temporali
   - Validazione range orari
   - Verifica permessi utente

3. **Calcolo Ore**:
   - Calcolo automatico durata
   - Gestione pause e break
   - Arrotondamenti configurabili

### Frontend (JavaScript)

#### Componenti Principali

**File**: `public/js/advanced_tc.js`

```javascript
class AdvancedTimesheetCalendar {
    constructor() {
        this.init_calendar();
        this.setup_filters();
        this.setup_event_handlers();
    }
    
    init_calendar() {
        // Inizializzazione FullCalendar
    }
    
    setup_filters() {
        // Configurazione filtri
    }
    
    handle_time_selection(info) {
        // Gestione selezione tempo
    }
}
```

**File**: `public/js/timesheet_calendar.js`

```javascript
window.TimesheetCalendarUtils = {
    showSummaryDialog: function(events, startDate, endDate) {
        // Dialog di riepilogo e export
    },
    
    exportToCSV: function(activities, filename) {
        // Funzionalità export CSV
    }
};
```

#### Librerie Utilizzate
- **FullCalendar.js**: Componente calendario principale
- **Frappe Framework**: Integrazione con ERPNext
- **jQuery**: Manipolazione DOM e AJAX

### Integrazione ERPNext

#### DocTypes Coinvolti
- **Timesheet**: Contenitore settimanale delle attività
- **Timesheet Detail**: Singola attività/voce timesheet
- **Employee**: Informazioni dipendente
- **Project**: Collegamento ai progetti
- **Task**: Collegamento alle attività
- **Activity Type**: Categorizzazione delle attività

## 🚀 Funzionalità Dettagliate

### 1. Gestione Timesheet Settimanali

#### Logica Automatica

L'app implementa una gestione intelligente dei timesheet:

1. **Creazione Automatica**: Quando si crea una nuova attività, l'app:
   - Calcola l'inizio della settimana (lunedì)
   - Cerca un timesheet esistente per quella settimana
   - Se non esiste, crea automaticamente un nuovo timesheet settimanale

2. **Gestione Settimana Lavorativa**:
   ```python
   def get_week_start_date(date):
       """Calcola l'inizio della settimana (lunedì)"""
       if isinstance(date, str):
           date = getdate(date)
       days_since_monday = date.weekday()
       week_start = date - timedelta(days=days_since_monday)
       return week_start
   ```

3. **Eliminazione Intelligente**: Quando si elimina l'ultima attività di un timesheet, l'app elimina automaticamente anche il timesheet vuoto.

### 2. Sistema di Colori Dinamici

#### Algoritmo di Assegnazione

Ogni progetto riceve automaticamente un colore basato su:

```python
def get_event_color(project):
    if not project:
        return "#95a5a6"  # Grigio default
    
    # Genera hash MD5 del nome progetto
    import hashlib
    hash_object = hashlib.md5(project.encode())
    hash_hex = hash_object.hexdigest()
    
    # Seleziona colore dalla palette
    color_index = int(hash_hex, 16) % len(colors)
    return colors[color_index]
```

**Vantaggi**:
- Stesso progetto = stesso colore sempre
- Distribuzione uniforme dei colori
- Nessuna configurazione manuale richiesta

### 3. Validazione e Controlli

#### Controllo Sovrapposizioni

L'app previene sovrapposizioni temporali:

```python
# Controlla sovrapposizioni con time_logs esistenti
for existing_log in timesheet.time_logs:
    existing_from = existing_log.from_time
    existing_to = existing_log.to_time
    
    # Controlla sovrapposizioni
    if (new_from_time < existing_to and new_to_time > existing_from):
        frappe.throw(_("Time overlap detected with existing entry"))
```

#### Validazione Frontend

```javascript
validateTimeRange: function(fromTime, toTime) {
    const from = new Date(fromTime);
    const to = new Date(toTime);
    
    if (from >= to) {
        return {
            valid: false,
            message: 'End time must be after start time'
        };
    }
    
    const diffHours = (to - from) / (1000 * 60 * 60);
    if (diffHours > 24) {
        return {
            valid: false,
            message: 'Activity cannot be longer than 24 hours'
        };
    }
    
    return { valid: true };
}
```

### 4. Drag & Drop Avanzato

#### Event Handlers FullCalendar

```javascript
eventDrop: (info) => {
    this.update_activity(info.event);
},

eventResize: (info) => {
    this.update_activity(info.event);
},

update_activity(event) {
    const data = {
        from_time: event.start.toISOString(),
        to_time: event.end.toISOString()
    };
    
    this.update_activity_data(event.id, data);
}
```

#### Feedback Visivo

- **Toast Notifications**: Conferma operazioni
- **Loading States**: Durante aggiornamenti
- **Error Handling**: Rollback automatico in caso di errore

### 5. Sistema di Filtri

#### Filtri Disponibili

1. **Employee**: Filtra per dipendente specifico
2. **Project**: Filtra per progetto
3. **Activity Type**: Filtra per tipo di attività
4. **Task**: Filtra per task specifico

#### Implementazione Backend

```python
# Filtri aggiuntivi
if filters:
    if filters.get("employee"):
        conditions.append("ts.employee = %(employee)s")
        values["employee"] = filters["employee"]
    
    if filters.get("project"):
        conditions.append("tsd.project = %(project)s")
        values["project"] = filters["project"]
    
    # ... altri filtri
```

### 6. Export e Reporting Avanzato

#### Funzionalità Export CSV

```javascript
exportToCSV: function(activities, filename = 'timesheet_details.csv') {
    const headers = [
        'Date', 'Employee', 'Project', 'Task', 
        'Activity Type', 'From Time', 'To Time', 
        'Hours', 'Description'
    ];
    
    const rows = activities.map(activity => {
        const props = activity.extendedProps;
        return [
            new Date(activity.start).toLocaleDateString(),
            props.employee_name || props.employee,
            props.project_name || props.project || '',
            props.task_subject || props.task || '',
            props.activity_type || '',
            new Date(activity.start).toLocaleTimeString(),
            new Date(activity.end).toLocaleTimeString(),
            props.hours || 0,
            props.description || ''
        ];
    });
    
    // Genera e scarica CSV
    const csvContent = [headers, ...rows]
        .map(row => row.map(field => `"${field}"`).join(','))
        .join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}
```

#### Dialog di Riepilogo

```javascript
showSummaryDialog: function(events, startDate, endDate) {
    // Calcola statistiche
    const stats = this.calculateStatistics(events);
    
    // Crea dialog con:
    // - Totale ore periodo
    // - Breakdown per dipendente
    // - Breakdown per progetto
    // - Breakdown per activity type
    // - Pulsante Export CSV
}
```

### 7. Gestione Pause e Break

#### Campi Break nel Dialog

- **Break Start**: Ora inizio pausa
- **Break End**: Ora fine pausa
- **Calcolo Automatico**: Le ore di pausa vengono sottratte dal totale

#### Validazione Break

```javascript
validateBreakTimes: function(activityStart, activityEnd, breakStart, breakEnd) {
    // Verifica che break sia dentro l'attività
    // Verifica che break start < break end
    // Calcola ore effettive lavorate
}
```

## 🎨 Personalizzazione

### Colori Attività

I colori delle attività sono definiti dinamicamente:

```python
# Palette colori predefinita
colors = [
    "#3498db",  # Blu
    "#e74c3c",  # Rosso
    "#f39c12",  # Arancione
    "#2ecc71",  # Verde
    "#9b59b6",  # Viola
    "#1abc9c",  # Turchese
    "#34495e",  # Grigio scuro
    "#e67e22"   # Arancione scuro
]
```

### CSS Personalizzato

**File**: `public/css/timesheet_calendar.css`

```css
/* Personalizzazione calendario */
.fc-event {
    border-radius: 4px;
    border: none;
    padding: 2px 4px;
}

/* Stili filtri */
.filter-section {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
}

/* Responsive design */
@media (max-width: 768px) {
    .calendar-container {
        padding: 10px;
    }
}
```

### Funzionalità Aggiuntive

Per aggiungere nuove funzionalità:

1. **Estendi la classe principale**:
   ```javascript
   class CustomTimesheetCalendar extends AdvancedTimesheetCalendar {
       // Nuove funzionalità
   }
   ```

2. **Aggiungi nuovi endpoint API**:
   ```python
   @frappe.whitelist()
   def custom_function():
       # Logica personalizzata
   ```

3. **Modifica il CSS** per nuovi stili

## 🔧 Configurazione Avanzata

### Permessi

Assicurati che gli utenti abbiano i permessi appropriati:

```json
{
    "Timesheet": ["read", "write", "create"],
    "Timesheet Detail": ["read", "write", "create", "delete"],
    "Employee": ["read"],
    "Project": ["read"],
    "Task": ["read"],
    "Activity Type": ["read"]
}
```

### Performance

Per siti con molti dati:

1. **Indici Database**:
   ```sql
   CREATE INDEX idx_timesheet_detail_date ON `tabTimesheet Detail` (date);
   CREATE INDEX idx_timesheet_employee ON `tabTimesheet` (employee);
   ```

2. **Paginazione**:
   ```python
   # Limita risultati per periodo
   limit_days = 90  # Massimo 3 mesi
   ```

3. **Cache**:
   ```python
   # Cache per filtri frequenti
   @frappe.cache()
   def get_employees():
       return frappe.get_all("Employee", fields=["name", "employee_name"])
   ```

### Configurazioni Default

**File**: `hooks.py`

```python
# Configurazioni app
app_include_css = [
    "/assets/advanced_tc/css/timesheet_calendar.css"
]

app_include_js = [
    "/assets/advanced_tc/js/advanced_tc.js",
    "/assets/advanced_tc/js/timesheet_calendar.js"
]

# Activity types default
default_activity_types = [
    "Development",
    "Testing", 
    "Meeting",
    "Documentation",
    "Support",
    "Training"
]
```

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
   L'utente deve avere almeno i ruoli: `Employee`, `System Manager` o ruoli personalizzati con accesso ai Timesheet.

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

Questo progetto è stato realizzato come attività di tirocinio presso l'azienda **Youbiquo** da parte di due studenti dell'Università degli Studi di Salerno di Ingegneria Informatica:

- **Fabrizio D'Errico**
- **Vittorio Postiglione**

---

**Sviluppato con ❤️ per la comunità ERPNext**