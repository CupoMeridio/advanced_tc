# AdvancedTC - Documentazione Tecnica

## 🏗️ Panoramica dell'Architettura

AdvancedTC è costruito come applicazione Frappe/ERPNext con architettura web moderna:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│                 │    │                 │    │                 │
│ FullCalendar.js │◄──►│ Python/Frappe   │◄──►│ MariaDB/MySQL   │
│ JavaScript      │    │ API Endpoints   │    │ Schema ERPNext  │
│ CSS/HTML        │    │ Logica Business │    │ Dati Timesheet  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Struttura File Dettagliata

### File Applicazione Principali

#### `advanced_tc/hooks.py`
File di configurazione principale che definisce:

```python
app_name = "advanced_tc"
app_title = "AdvancedTC"
app_publisher = "Prova"
app_description = "Calendar view per i timesheets details"
app_version = "0.0.1"

# Integrazione sezione Apps
add_to_apps_screen = [
    {
        "name": "advanced_tc",
        "logo": "/assets/advanced_tc/images/logo.svg",
        "title": _("Advanced Timesheet Calendar"),
        "route": "app/advanced_tc",
        "has_permission": "advanced_tc.api.timesheet_details.has_permission"
    }
]

# Inclusioni CSS e JS
app_include_css = "/assets/advanced_tc/css/timesheet_calendar.css"
page_js = {"advanced_tc" : "public/js/timesheet_calendar.js"}

# Hook di installazione
after_install = "advanced_tc.install.after_install"
before_uninstall = "advanced_tc.install.before_uninstall"
```

#### `advanced_tc/install.py`
Script di installazione con procedure di setup:

```python
import frappe
from frappe import _

def after_install():
    """Setup post-installazione"""
    try:
        print("🚀 Inizializzazione Advanced Timesheet Calendar...")
        
        # Crea workspace custom dedicata
        create_custom_workspace()
        
        frappe.db.commit()
        print("✅ Installazione completata con successo!")
        print("ℹ️ L'app è accessibile tramite:")
        print("   • Link diretto: /app/advanced_tc")
        print("   • Icona nella sezione Apps del desktop ERPNext")
        print("   • Workspace dedicata: Advanced Timesheet Calendar")
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Errore durante l'installazione: {str(e)}", "Timesheet Calendar Install")
        print(f"❌ Errore durante l'installazione: {str(e)}")

def create_custom_workspace():
    """Crea una workspace dedicata per Advanced Timesheet Calendar"""
    # Dettagli implementazione...

def before_uninstall():
    """Pulizia prima della disinstallazione"""
    # Rimuove workspace custom e esegue pulizia
```

### Architettura Frontend

#### `advanced_tc/advanced_tc/page/advanced_tc/advanced_tc.js`
Controller frontend principale:

```javascript
class AdvancedTimesheetCalendar {
    constructor(wrapper) {
        this.wrapper = wrapper;
        this.page = frappe.ui.make_app_page({
            parent: wrapper,
            title: 'Advanced Timesheet Calendar',
            single_column: true
        });
        
        this.init_calendar();
        this.setup_filters();
        this.setup_event_handlers();
    }
    
    init_calendar() {
        // Inizializzazione FullCalendar con localizzazione
        this.calendar = new FullCalendar.Calendar(this.calendar_container, {
            initialView: 'timeGridWeek',
            timeZone: 'local', // Usa timezone locale
            locale: 'it', // Localizzazione italiana
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            selectable: true,
            editable: true,
            events: this.fetch_events.bind(this),
            select: this.handle_time_selection.bind(this),
            eventDrop: this.handle_event_drop.bind(this),
            eventResize: this.handle_event_resize.bind(this),
            eventClick: this.handle_event_click.bind(this)
        });
        
        // Aggiunge classe CSS per styling specifico della pagina
        $(this.wrapper).addClass('page-advanced_tc');
    }
}
```

#### `advanced_tc/public/js/timesheet_calendar.js`
Funzioni utility e helper:

```javascript
// Utility per date
function formatDateForAPI(date) {
    return date.toISOString().split('T')[0];
}

function formatTimeForAPI(date) {
    return date.toISOString();
}

// Generazione colori per progetti
function generateProjectColor(projectName) {
    const colors = [
        '#3498db', '#e74c3c', '#f39c12', '#2ecc71',
        '#9b59b6', '#1abc9c', '#34495e', '#e67e22'
    ];
    
    let hash = 0;
    for (let i = 0; i < projectName.length; i++) {
        hash = projectName.charCodeAt(i) + ((hash << 5) - hash);
    }
    
    return colors[Math.abs(hash) % colors.length];
}

// Funzioni di validazione
function validateTimeRange(fromTime, toTime) {
    const from = new Date(fromTime);
    const to = new Date(toTime);
    
    if (from >= to) {
        return {
            valid: false,
            message: 'L\'orario di fine deve essere successivo a quello di inizio'
        };
    }
    
    const diffHours = (to - from) / (1000 * 60 * 60);
    if (diffHours > 24) {
        return {
            valid: false,
            message: 'L\'attività non può durare più di 24 ore'
        };
    }
    
    return { valid: true };
}
```

### Architettura Backend API

#### `advanced_tc/api/timesheet_details.py`
Endpoint API principali:

```python
import frappe
from frappe import _
from datetime import datetime, timedelta
import hashlib

@frappe.whitelist()
def get_timesheet_details(start_date=None, end_date=None, filters=None):
    """
    Recupera dettagli timesheet per visualizzazione calendario
    
    Args:
        start_date (str): Data inizio in formato YYYY-MM-DD
        end_date (str): Data fine in formato YYYY-MM-DD
        filters (dict): Filtri aggiuntivi (employee, project, etc.)
    
    Returns:
        list: Eventi formattati per FullCalendar
    """
    
    # Controllo permessi
    if not has_permission():
        frappe.throw(_("Permessi insufficienti"))
    
    # Costruzione condizioni query
    conditions = ["ts.docstatus = 1"]
    values = {}
    
    if start_date and end_date:
        conditions.append("tsd.date BETWEEN %(start_date)s AND %(end_date)s")
        values.update({
            "start_date": start_date,
            "end_date": end_date
        })
    
    # Applicazione filtri basati sui ruoli
    user_roles = frappe.get_roles()
    if not any(role in user_roles for role in ['System Manager', 'HR Manager', 'HR User']):
        # Employee può vedere solo i propri record
        conditions.append("ts.employee = %(employee)s")
        values["employee"] = frappe.session.user
    
    # Applicazione filtri aggiuntivi
    if filters:
        if filters.get("employee"):
            conditions.append("ts.employee = %(employee)s")
            values["employee"] = filters["employee"]
        
        if filters.get("project"):
            conditions.append("tsd.project = %(project)s")
            values["project"] = filters["project"]
        
        if filters.get("activity_type"):
            conditions.append("tsd.activity_type = %(activity_type)s")
            values["activity_type"] = filters["activity_type"]
        
        if filters.get("task"):
            conditions.append("tsd.task = %(task)s")
            values["task"] = filters["task"]
    
    # Esecuzione query
    query = f"""
        SELECT 
            tsd.name,
            tsd.date,
            tsd.from_time,
            tsd.to_time,
            tsd.hours,
            tsd.description,
            tsd.project,
            tsd.task,
            tsd.activity_type,
            ts.employee,
            emp.employee_name,
            proj.project_name,
            task.subject as task_subject
        FROM 
            `tabTimesheet Detail` tsd
        INNER JOIN 
            `tabTimesheet` ts ON tsd.parent = ts.name
        LEFT JOIN 
            `tabEmployee` emp ON ts.employee = emp.name
        LEFT JOIN 
            `tabProject` proj ON tsd.project = proj.name
        LEFT JOIN 
            `tabTask` task ON tsd.task = task.name
        WHERE 
            {' AND '.join(conditions)}
        ORDER BY 
            tsd.date, tsd.from_time
    """
    
    results = frappe.db.sql(query, values, as_dict=True)
    
    # Formattazione per FullCalendar
    events = []
    for row in results:
        event = {
            "id": row.name,
            "title": format_event_title(row),
            "start": combine_date_time(row.date, row.from_time),
            "end": combine_date_time(row.date, row.to_time),
            "backgroundColor": get_event_color(row.project),
            "borderColor": get_event_color(row.project),
            "extendedProps": {
                "employee": row.employee,
                "employee_name": row.employee_name,
                "project": row.project,
                "project_name": row.project_name,
                "task": row.task,
                "task_subject": row.task_subject,
                "activity_type": row.activity_type,
                "description": row.description,
                "hours": row.hours
            }
        }
        events.append(event)
    
    return events

@frappe.whitelist()
def create_timesheet_detail(data):
    """
    Crea una nuova voce timesheet detail
    
    Args:
        data (dict): Dati timesheet detail
    
    Returns:
        dict: Info timesheet detail creato
    """
    
    # Validazione dati input
    validate_timesheet_data(data)
    
    # Controllo sovrapposizioni
    check_time_overlaps(data)
    
    # Ottieni o crea timesheet settimanale
    timesheet = get_or_create_weekly_timesheet(
        data['employee'], 
        data['date']
    )
    
    # Crea timesheet detail
    timesheet_detail = frappe.get_doc({
        "doctype": "Timesheet Detail",
        "parent": timesheet.name,
        "parenttype": "Timesheet",
        "parentfield": "time_logs",
        "date": data['date'],
        "from_time": data['from_time'],
        "to_time": data['to_time'],
        "project": data.get('project'),
        "task": data.get('task'),
        "activity_type": data.get('activity_type'),
        "description": data.get('description', ''),
        "hours": calculate_hours(data['from_time'], data['to_time'])
    })
    
    timesheet_detail.insert()
    
    # Aggiorna timesheet padre
    timesheet.reload()
    timesheet.save()
    
    return {
        "name": timesheet_detail.name,
        "timesheet": timesheet.name
    }

def validate_timesheet_data(data):
    """
    Valida dati timesheet prima della creazione
    """
    required_fields = ['employee', 'date', 'from_time', 'to_time']
    
    for field in required_fields:
        if not data.get(field):
            frappe.throw(_(f"Il campo '{field}' è obbligatorio"))
    
    # Validazione intervallo temporale
    from_time = datetime.fromisoformat(data['from_time'].replace('Z', '+00:00'))
    to_time = datetime.fromisoformat(data['to_time'].replace('Z', '+00:00'))
    
    if from_time >= to_time:
        frappe.throw(_("L'orario di fine deve essere successivo a quello di inizio"))
    
    # Validazione durata (max 24 ore)
    duration = (to_time - from_time).total_seconds() / 3600
    if duration > 24:
        frappe.throw(_("La durata dell'attività non può superare le 24 ore"))

def check_time_overlaps(data):
    """
    Controlla sovrapposizioni temporali con voci esistenti
    """
    employee = data['employee']
    date = data['date']
    from_time = data['from_time']
    to_time = data['to_time']
    
    # Query log temporali esistenti per stesso employee e data
    existing_logs = frappe.db.sql("""
        SELECT 
            tsd.from_time, 
            tsd.to_time,
            tsd.name
        FROM 
            `tabTimesheet Detail` tsd
        INNER JOIN 
            `tabTimesheet` ts ON tsd.parent = ts.name
        WHERE 
            ts.employee = %(employee)s 
            AND tsd.date = %(date)s
            AND ts.docstatus = 1
    """, {
        "employee": employee,
        "date": date
    }, as_dict=True)
    
    new_from = datetime.fromisoformat(from_time.replace('Z', '+00:00'))
    new_to = datetime.fromisoformat(to_time.replace('Z', '+00:00'))
    
    for log in existing_logs:
        existing_from = log.from_time
        existing_to = log.to_time
        
        # Controllo sovrapposizione
        if (new_from < existing_to and new_to > existing_from):
            frappe.throw(_("Rilevata sovrapposizione temporale con voce esistente"))

def get_or_create_weekly_timesheet(employee, date):
    """
    Ottieni timesheet settimanale esistente o creane uno nuovo
    """
    week_start = get_week_start_date(date)
    week_end = week_start + timedelta(days=6)
    
    # Controlla timesheet esistente
    existing_timesheet = frappe.db.get_value(
        "Timesheet",
        {
            "employee": employee,
            "start_date": week_start,
            "end_date": week_end
        },
        "name"
    )
    
    if existing_timesheet:
        return frappe.get_doc("Timesheet", existing_timesheet)
    
    # Crea nuovo timesheet
    timesheet = frappe.get_doc({
        "doctype": "Timesheet",
        "employee": employee,
        "start_date": week_start,
        "end_date": week_end,
        "company": frappe.defaults.get_user_default("Company")
    })
    
    timesheet.insert()
    timesheet.submit()
    
    return timesheet

def get_week_start_date(date_str):
    """
    Ottieni data inizio settimana (lunedì) per una data specifica
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    days_since_monday = date_obj.weekday()
    week_start = date_obj - timedelta(days=days_since_monday)
    return week_start

def get_event_color(project_name):
    """
    Genera colore consistente per progetto usando hash
    """
    if not project_name:
        return "#95a5a6"  # Grigio predefinito
    
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
    
    # Genera hash e seleziona colore
    hash_object = hashlib.md5(project_name.encode())
    hash_int = int(hash_object.hexdigest(), 16)
    color_index = hash_int % len(colors)
    
    return colors[color_index]

def has_permission():
    """
    Controlla se l'utente ha permessi per accedere ai dati timesheet
    """
    user_roles = frappe.get_roles()
    allowed_roles = [
        'System Manager', 
        'HR Manager', 
        'HR User', 
        'Employee'
    ]
    
    return any(role in user_roles for role in allowed_roles)
```

## 🔒 Implementazione Sicurezza

### Controllo Accessi Basato sui Ruoli

```python
def get_employee_projects(employee=None):
    """
    Ottieni progetti accessibili a un employee basati sulle assegnazioni
    """
    user_roles = frappe.get_roles()
    
    # I manager vedono tutti i progetti
    if any(role in user_roles for role in ['System Manager', 'HR Manager', 'HR User']):
        return frappe.get_all(
            "Project",
            filters={"status": "Open"},
            fields=["name", "project_name"]
        )
    
    # Gli employee vedono solo progetti assegnati
    if not employee:
        employee = frappe.session.user
    
    # Ottieni progetti assegnati via "Assign To"
    assigned_projects = frappe.db.sql("""
        SELECT DISTINCT 
            p.name, 
            p.project_name
        FROM 
            `tabProject` p
        INNER JOIN 
            `tabToDo` t ON t.reference_name = p.name
        WHERE 
            t.reference_type = 'Project'
            AND t.allocated_to = %(employee)s
            AND p.status = 'Open'
    """, {"employee": employee}, as_dict=True)
    
    return assigned_projects
```

### Validazione Dati

```python
class TimesheetValidator:
    @staticmethod
    def validate_time_format(time_str):
        """Valida formato tempo ISO"""
        try:
            datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_date_range(start_date, end_date):
        """Valida che l'intervallo di date sia logico"""
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return start <= end
    
    @staticmethod
    def validate_employee_access(employee):
        """Valida che l'utente possa accedere ai dati employee"""
        user_roles = frappe.get_roles()
        
        # I manager possono accedere a qualsiasi employee
        if any(role in user_roles for role in ['System Manager', 'HR Manager', 'HR User']):
            return True
        
        # Gli employee possono accedere solo ai propri dati
        return employee == frappe.session.user
```

## 🎨 Styling Frontend

### Architettura CSS

```css
/* advanced_tc/public/css/timesheet_calendar.css */

/* Container principale */
.advanced-tc-container {
    padding: 20px;
    background: #f8f9fa;
    min-height: 100vh;
}

/* Styling calendario */
.fc-event {
    border-radius: 4px;
    border: none;
    padding: 2px 4px;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.fc-event:hover {
    opacity: 0.8;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Sidebar filtri */
.filter-sidebar {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.filter-section {
    margin-bottom: 15px;
}

.filter-section label {
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 5px;
    display: block;
}

/* Design responsive */
@media (max-width: 768px) {
    .advanced-tc-container {
        padding: 10px;
    }
    
    .fc-toolbar {
        flex-direction: column;
        gap: 10px;
    }
    
    .fc-toolbar-chunk {
        display: flex;
        justify-content: center;
    }
}

/* Stati di caricamento */
.loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Personalizzazioni dialog */
.modal-dialog.modal-lg {
    max-width: 800px;
}

.timesheet-form .form-group {
    margin-bottom: 15px;
}

.timesheet-form .control-label {
    font-weight: 600;
    color: #2c3e50;
}

/* Styling pulsanti */
.btn-primary {
    background-color: #3498db;
    border-color: #3498db;
}

.btn-primary:hover {
    background-color: #2980b9;
    border-color: #2980b9;
}

.btn-success {
    background-color: #2ecc71;
    border-color: #2ecc71;
}

.btn-success:hover {
    background-color: #27ae60;
    border-color: #27ae60;
}
```

## 🧪 Framework di Testing

### Test Backend

```python
# tests/test_timesheet_api.py
import unittest
import frappe
from advanced_tc.api.timesheet_details import (
    create_timesheet_detail,
    get_timesheet_details,
    check_time_overlaps
)

class TestTimesheetAPI(unittest.TestCase):
    def setUp(self):
        """Imposta dati di test"""
        self.test_employee = "test@example.com"
        self.test_date = "2024-01-15"
        
    def test_create_timesheet_detail(self):
        """Testa creazione timesheet detail"""
        data = {
            "employee": self.test_employee,
            "date": self.test_date,
            "from_time": "2024-01-15T09:00:00Z",
            "to_time": "2024-01-15T17:00:00Z",
            "description": "Attività di test"
        }
        
        result = create_timesheet_detail(data)
        self.assertIsNotNone(result.get("name"))
        
    def test_time_overlap_validation(self):
        """Testa rilevamento sovrapposizioni"""
        # Crea prima attività
        data1 = {
            "employee": self.test_employee,
            "date": self.test_date,
            "from_time": "2024-01-15T09:00:00Z",
            "to_time": "2024-01-15T12:00:00Z"
        }
        create_timesheet_detail(data1)
        
        # Prova a creare attività sovrapposta
        data2 = {
            "employee": self.test_employee,
            "date": self.test_date,
            "from_time": "2024-01-15T11:00:00Z",
            "to_time": "2024-01-15T15:00:00Z"
        }
        
        with self.assertRaises(frappe.ValidationError):
            create_timesheet_detail(data2)
    
    def tearDown(self):
        """Pulisci dati di test"""
        frappe.db.rollback()
```

### Test Frontend

```javascript
// tests/test_calendar.js
describe('AdvancedTimesheetCalendar', () => {
    let calendar;
    
    beforeEach(() => {
        // Setup DOM
        document.body.innerHTML = '<div id="calendar-container"></div>';
        calendar = new AdvancedTimesheetCalendar('#calendar-container');
    });
    
    test('dovrebbe inizializzare il calendario', () => {
        expect(calendar.calendar).toBeDefined();
        expect(calendar.calendar.view.type).toBe('dayGridMonth');
    });
    
    test('dovrebbe validare intervallo temporale', () => {
        const validRange = validateTimeRange(
            '2024-01-15T09:00:00Z',
            '2024-01-15T17:00:00Z'
        );
        expect(validRange.valid).toBe(true);
        
        const invalidRange = validateTimeRange(
            '2024-01-15T17:00:00Z',
            '2024-01-15T09:00:00Z'
        );
        expect(invalidRange.valid).toBe(false);
    });
    
    test('dovrebbe generare colori consistenti per progetti', () => {
        const color1 = generateProjectColor('Progetto A');
        const color2 = generateProjectColor('Progetto A');
        const color3 = generateProjectColor('Progetto B');
        
        expect(color1).toBe(color2);
        expect(color1).not.toBe(color3);
    });
});
```

## 🚀 Ottimizzazione Performance

### Indicizzazione Database

```sql
-- Indici database raccomandati per performance ottimali

-- Indice su data timesheet detail per query intervalli date
CREATE INDEX idx_timesheet_detail_date 
ON `tabTimesheet Detail` (date);

-- Indice su employee timesheet per filtri utente
CREATE INDEX idx_timesheet_employee 
ON `tabTimesheet` (employee);

-- Indice composito per combinazioni filtri comuni
CREATE INDEX idx_timesheet_detail_composite 
ON `tabTimesheet Detail` (date, project, activity_type);

-- Indice su ToDo per assegnazioni progetti
CREATE INDEX idx_todo_assignment 
ON `tabToDo` (reference_type, reference_name, allocated_to);
```

### Strategia Caching

```python
# Cache per dati acceduti frequentemente
@frappe.cache()
def get_employee_list():
    """Cache lista employee per opzioni filtri"""
    return frappe.get_all(
        "Employee",
        fields=["name", "employee_name"],
        filters={"status": "Active"}
    )

@frappe.cache(ttl=300)  # Cache 5 minuti
def get_project_assignments(employee):
    """Cache assegnazioni progetti per employee"""
    return get_employee_projects(employee)
```

### Ottimizzazione Frontend

```javascript
// Aggiornamenti filtri con debounce
const debouncedFilterUpdate = debounce((filters) => {
    calendar.refetchEvents();
}, 300);

// Caricamento lazy per dataset grandi
function fetchEvents(info, successCallback, failureCallback) {
    const pageSize = 100;
    const offset = this.currentOffset || 0;
    
    frappe.call({
        method: 'advanced_tc.api.timesheet_details.get_timesheet_details',
        args: {
            start_date: info.startStr,
            end_date: info.endStr,
            limit: pageSize,
            offset: offset
        },
        callback: (r) => {
            if (r.message) {
                successCallback(r.message);
            }
        }
    });
}

// Gestione memoria
function cleanup() {
    if (this.calendar) {
        this.calendar.destroy();
    }
    
    // Rimuovi event listener
    $(window).off('resize.advancedtc');
    $(document).off('click.advancedtc');
}
```

## 🔧 Opzioni di Configurazione

### Variabili Ambiente

```python
# Aggiunte site_config.json
{
    "advanced_tc": {
        "max_hours_per_day": 24,
        "default_activity_type": "Sviluppo",
        "auto_break_rules": {
            "enabled": true,
            "min_duration_hours": 6,
            "break_duration_minutes": 30
        },
        "color_scheme": "default",
        "cache_ttl": 300
    }
}
```

### Hook Personalizzazione

```python
# hooks.py - Handler eventi personalizzati
doc_events = {
    "Timesheet": {
        "before_save": "advanced_tc.utils.validate_timesheet",
        "after_insert": "advanced_tc.utils.notify_timesheet_creation"
    },
    "Project": {
        "after_insert": "advanced_tc.utils.setup_project_defaults"
    }
}

# Validazione personalizzata
def validate_timesheet(doc, method):
    """Validazione timesheet personalizzata"""
    total_hours = sum(log.hours for log in doc.time_logs)
    if total_hours > 24:
        frappe.throw("Le ore giornaliere non possono superare 24")
```

## 📊 Monitoraggio e Analytics

### Tracciamento Errori

```python
import logging

# Setup logging
logger = logging.getLogger('advanced_tc')
handler = logging.FileHandler('/path/to/advanced_tc.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_api_call(method_name, args, user):
    """Log chiamate API per monitoraggio"""
    logger.info(f"Chiamata API: {method_name} da {user} con args: {args}")

def log_error(error, context):
    """Log errori con contesto"""
    logger.error(f"Errore: {error} | Contesto: {context}")
```

### Metriche Performance

```python
import time
from functools import wraps

def measure_performance(func):
    """Decorator per misurare performance funzioni"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} eseguita in {execution_time:.2f} secondi")
        
        return result
    return wrapper

@measure_performance
def get_timesheet_details(start_date, end_date, filters):
    # Implementazione
    pass
```

---

## 📚 Risorse Aggiuntive

- [Documentazione Frappe Framework](https://frappeframework.com/docs)
- [Guida Sviluppatore ERPNext](https://docs.erpnext.com/docs/v13/user/manual/en/setting-up/articles/developer-guide)
- [Documentazione FullCalendar.js](https://fullcalendar.io/docs)
- [Ottimizzazione Performance MariaDB](https://mariadb.com/kb/en/optimization-and-tuning/)

---

*Questa documentazione tecnica è mantenuta insieme alla documentazione principale del progetto e dovrebbe essere aggiornata con qualsiasi cambiamento architetturale.*