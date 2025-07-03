# Test Implementation Guide

Questa guida ti aiuterà a testare l'implementazione di AdvancedTC.

## 🧪 Test di Base

### 1. Verifica Installazione

```bash
# Controlla che l'app sia installata
bench --site [nome-sito] list-apps

# Dovrebbe mostrare 'AdvancedTC' nella lista
```

### 2. Accesso alla Pagina

1. Accedi a ERPNext
2. Vai a: `http://[tuo-sito]/app/advanced_tc`
3. Dovresti vedere la pagina "Advanced Timesheet Calendar"

### 3. Test API Backend

Apri la console del browser (F12) e testa le API:

```javascript
// Test get_filter_options
frappe.call({
    method: 'advanced_tc.api.timesheet_details.get_filter_options',
    callback: (r) => {
        console.log('Filter Options:', r.message);
    }
});

// Test get_timesheet_details
frappe.call({
    method: 'advanced_tc.api.timesheet_details.get_timesheet_details',
    args: {
        start_date: '2024-01-01T00:00:00',
        end_date: '2024-12-31T23:59:59',
        filters: '{}'
    },
    callback: (r) => {
        console.log('Timesheet Details:', r.message);
    }
});
```

## 🔧 Test Funzionalità

### Test 1: Creazione Attività

1. Clicca "Add Activity"
2. Compila il form:
   - Employee: Seleziona un dipendente
   - From Time: Oggi alle 09:00
   - To Time: Oggi alle 10:00
   - Activity Type: Development
   - Description: "Test activity"
3. Clicca "Create"
4. Verifica che l'attività appaia nel calendario

### Test 2: Modifica Attività (Drag & Drop)

1. Trascina l'attività creata in un altro slot temporale
2. Verifica che l'orario si aggiorni automaticamente
3. Ridimensiona l'attività trascinando i bordi
4. Verifica che la durata si aggiorni

### Test 3: Modifica Attività (Dialog)

1. Clicca sull'attività
2. Modifica la descrizione
3. Clicca "Update"
4. Verifica che le modifiche siano salvate

### Test 4: Filtri

1. Seleziona un dipendente specifico nel filtro
2. Clicca "Apply Filters"
3. Verifica che vengano mostrate solo le attività di quel dipendente
4. Ripeti per Project e Activity Type

### Test 5: Eliminazione

1. Clicca su un'attività
2. Clicca "Delete"
3. Conferma l'eliminazione
4. Verifica che l'attività sia rimossa dal calendario

## 🐛 Troubleshooting Test

### Problema: Calendar non si carica

**Possibili cause:**
- FullCalendar non disponibile
- Errori JavaScript
- Permessi insufficienti

**Debug:**
```javascript
// Controlla se FullCalendar è disponibile
console.log('FullCalendar available:', typeof FullCalendar !== 'undefined');

// Controlla errori nella console
// Apri Developer Tools (F12) e guarda la tab Console
```

### Problema: API Errors

**Debug:**
```bash
# Controlla i log di Frappe
bench logs

# Controlla i log specifici dell'app
tail -f sites/[nome-sito]/logs/web.log
```

### Problema: Permessi

**Verifica permessi:**
1. Vai a: Setup > Permissions > Role Permissions Manager
2. Controlla i permessi per:
   - Timesheet
   - Timesheet Detail
   - Employee
   - Project
   - Activity Type

## 📊 Test Performance

### Test con Dati di Esempio

```python
# Script per creare dati di test
# Esegui in bench console: bench --site [nome-sito] console

import frappe
from datetime import datetime, timedelta
import random

def create_test_data():
    # Ottieni dipendenti esistenti
    employees = frappe.get_all("Employee", fields=["name"], limit=5)
    if not employees:
        print("Nessun dipendente trovato. Crea prima alcuni dipendenti.")
        return
    
    # Ottieni progetti esistenti
    projects = frappe.get_all("Project", fields=["name"], limit=3)
    
    # Activity types
    activity_types = ["Development", "Testing", "Meeting", "Documentation"]
    
    # Crea timesheet details per gli ultimi 7 giorni
    for i in range(7):
        date = datetime.now() - timedelta(days=i)
        
        for emp in employees[:3]:  # Solo primi 3 dipendenti
            # Crea 2-4 attività per dipendente per giorno
            num_activities = random.randint(2, 4)
            
            for j in range(num_activities):
                start_hour = 9 + j * 2
                end_hour = start_hour + random.randint(1, 2)
                
                from_time = date.replace(hour=start_hour, minute=0, second=0)
                to_time = date.replace(hour=end_hour, minute=0, second=0)
                
                # Crea o ottieni timesheet
                timesheet_name = f"TS-{emp['name']}-{date.strftime('%Y-%m-%d')}"
                
                if not frappe.db.exists("Timesheet", timesheet_name):
                    timesheet = frappe.get_doc({
                        "doctype": "Timesheet",
                        "name": timesheet_name,
                        "employee": emp["name"],
                        "start_date": date.date(),
                        "end_date": date.date()
                    })
                    timesheet.insert()
                else:
                    timesheet = frappe.get_doc("Timesheet", timesheet_name)
                
                # Aggiungi timesheet detail
                timesheet.append("time_logs", {
                    "from_time": from_time,
                    "to_time": to_time,
                    "activity_type": random.choice(activity_types),
                    "project": projects[0]["name"] if projects else None,
                    "description": f"Test activity {j+1} for {date.strftime('%Y-%m-%d')}"
                })
                
                timesheet.save()
    
    frappe.db.commit()
    print(f"Creati dati di test per {len(employees)} dipendenti negli ultimi 7 giorni")

# Esegui la funzione
create_test_data()
```

### Test Load Performance

1. Crea almeno 100+ timesheet details
2. Apri la calendar view
3. Misura il tempo di caricamento
4. Testa il filtraggio con grandi dataset

## ✅ Checklist Test Completo

- [ ] App installata correttamente
- [ ] Pagina calendar accessibile
- [ ] API backend funzionanti
- [ ] Creazione attività funziona
- [ ] Modifica drag & drop funziona
- [ ] Modifica tramite dialog funziona
- [ ] Eliminazione funziona
- [ ] Filtri funzionano correttamente
- [ ] CSS applicato correttamente

- [ ] Nessun errore JavaScript
- [ ] Performance accettabile
- [ ] Permessi configurati
- [ ] Integrazione ERPNext completa

## 📝 Report Bug

Se trovi problemi, raccogli queste informazioni:

1. **Versione ERPNext/Frappe**
2. **Browser e versione**
3. **Passi per riprodurre il problema**
4. **Errori nella console JavaScript**
5. **Log di Frappe**
6. **Screenshot se applicabile**

## 🚀 Test Avanzati

### Test Sicurezza

1. Testa con utenti con permessi limitati
2. Verifica che non si possano modificare timesheet di altri utenti
3. Testa la validazione dei dati in input

### Test Integrazione

1. Verifica che i timesheet creati siano visibili nella vista standard ERPNext
2. Testa l'integrazione con il workflow di approvazione timesheet
3. Verifica il calcolo corretto delle ore totali



---

**Buon testing! 🎯**