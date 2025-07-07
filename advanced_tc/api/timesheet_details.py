import frappe
from frappe import _
from frappe.utils import getdate, get_datetime, nowdate, add_days
import json
import re
from datetime import datetime, timedelta

def get_week_start_date(date):
    """
    Calcola l'inizio della settimana (lunedì) per una data specifica
    """
    if isinstance(date, str):
        date = getdate(date)
    
    # Calcola quanti giorni sottrarre per arrivare al lunedì (0=lunedì, 6=domenica)
    days_since_monday = date.weekday()
    week_start = date - timedelta(days=days_since_monday)
    
    return week_start

@frappe.whitelist()
def get_timesheet_details(start_date=None, end_date=None, filters=None):
    """
    Recupera i Time Sheet Detail per la calendar view con controllo permessi basato sui ruoli
    """
    try:
        # Parse dei filtri se forniti come stringa JSON
        if filters and isinstance(filters, str):
            filters = json.loads(filters)
        
        # Controllo permessi basato sui ruoli
        user_roles = frappe.get_roles(frappe.session.user)
        is_manager = any(role in user_roles for role in ["System Manager", "HR Manager", "HR User"])
        
        # Costruzione della query base
        conditions = []
        values = {}
        
        # Se l'utente è solo Employee, limita ai propri timesheet
        if not is_manager and "Employee" in user_roles:
            # Ottieni l'employee associato all'utente corrente
            current_employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
            if current_employee:
                conditions.append("ts.employee = %(current_employee)s")
                values["current_employee"] = current_employee
            else:
                # Se non è associato a nessun employee, non mostrare nulla
                return []
        
        # Filtri per date
        if start_date:
            conditions.append("tsd.from_time >= %(start_date)s")
            values["start_date"] = get_datetime(start_date)
        
        if end_date:
            conditions.append("tsd.to_time <= %(end_date)s")
            values["end_date"] = get_datetime(end_date)
        
        # Filtri aggiuntivi (solo per manager o se il filtro employee corrisponde all'utente corrente)
        if filters:
            if filters.get("employee"):
                # Se non è manager, verifica che stia filtrando solo per se stesso
                if not is_manager:
                    current_employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
                    if filters["employee"] != current_employee:
                        return []  # Non autorizzato a vedere altri employee
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
        
        # Query SQL
        where_clause = " AND " + " AND ".join(conditions) if conditions else ""
        
        query = f"""
            SELECT 
                tsd.name,
                tsd.parent as timesheet,
                tsd.from_time,
                tsd.to_time,
                tsd.hours,
                tsd.project,
                tsd.task,
                tsd.activity_type,
                tsd.description,
                ts.employee,
                ts.employee_name,
                ts.company,
                ts.docstatus,
                p.project_name,
                t.subject as task_subject
            FROM 
                `tabTimesheet Detail` tsd
            INNER JOIN 
                `tabTimesheet` ts ON tsd.parent = ts.name
            LEFT JOIN 
                `tabProject` p ON tsd.project = p.name
            LEFT JOIN 
                `tabTask` t ON tsd.task = t.name
            WHERE 
                ts.docstatus < 2 {where_clause}
            ORDER BY 
                tsd.from_time ASC
        """
        
        results = frappe.db.sql(query, values, as_dict=True)
        
        # Formattazione per FullCalendar
        events = []
        for row in results:
            event = {
                "id": row.name,
                "title": f"{row.project or ''} - {row.activity_type or ''}",
                "start": row.from_time.isoformat() if row.from_time else None,
                "end": row.to_time.isoformat() if row.to_time else None,
                "extendedProps": {
                    "timesheet": row.timesheet,
                    "employee": row.employee,
                    "employee_name": row.employee_name,
                    "project": row.project,
                    "project_name": row.project_name,
                    "task": row.task,
                    "task_subject": row.task_subject,
                    "activity_type": row.activity_type,
                    "description": row.description,
                    "hours": row.hours,
                    "company": row.company,
                    "docstatus": row.docstatus
                },
                "backgroundColor": get_event_color(row.project),
                "borderColor": get_event_color(row.project)
            }
            events.append(event)
        
        return events
    
    except Exception as e:
        frappe.log_error(f"Errore in get_timesheet_details: {str(e)}")
        frappe.throw(_("Errore nel recupero dei dati: {0}").format(str(e)))

@frappe.whitelist()
def create_timesheet_detail(data):
    """
    Crea un nuovo Timesheet Detail con controllo permessi
    """
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        # Controllo permessi: gli Employee possono creare solo per se stessi
        user_roles = frappe.get_roles(frappe.session.user)
        is_manager = any(role in user_roles for role in ["System Manager", "HR Manager", "HR User"])
        
        if not is_manager and "Employee" in user_roles:
            current_employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
            if not current_employee:
                frappe.throw(_("Utente non associato a nessun dipendente"))
            
            # Verifica che stia creando per se stesso
            if data.get("employee") != current_employee:
                frappe.throw(_("Non autorizzato a creare attività per altri dipendenti"))
        
        timesheet_name = data.get("timesheet")
        if timesheet_name:
            timesheet = frappe.get_doc("Timesheet", timesheet_name)
            # Verifica permessi sul timesheet esistente
            if not is_manager and "Employee" in user_roles:
                current_employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
                if timesheet.employee != current_employee:
                    frappe.throw(_("Non autorizzato a modificare questo timesheet"))
        else:
            # Calcola l'inizio della settimana per la data dell'attività
            activity_date = getdate(data.get("from_time"))
            week_start = get_week_start_date(activity_date)
            
            timesheet = get_or_create_timesheet(
                employee=data.get("employee"),
                start_date=week_start,
                company=data.get("company")
            )
        
        # Verifica sovrapposizioni con time_logs esistenti
        new_from_time = get_datetime(data.get("from_time"))
        new_to_time = get_datetime(data.get("to_time"))
        
        for existing_log in timesheet.time_logs:
            existing_from = existing_log.from_time
            existing_to = existing_log.to_time
            
            # Controlla che i valori non siano None prima del confronto
            if not existing_from or not existing_to:
                continue  # Salta questo log se ha valori mancanti
            
            # Controlla sovrapposizioni
            if (new_from_time < existing_to and new_to_time > existing_from):
                frappe.throw(_("Time overlap detected with existing entry from {0} to {1}").format(
                    existing_from.strftime("%H:%M"),
                    existing_to.strftime("%H:%M")
                ))
        
        # Aggiungere alla child table del timesheet
        timesheet_detail = timesheet.append("time_logs", {
            "from_time": new_from_time,
            "to_time": new_to_time,
            "project": data.get("project"),
            "task": data.get("task"),
            "activity_type": data.get("activity_type"),
            "description": data.get("description", "")
        })
        
        # Calcola le ore automaticamente
        if timesheet_detail.from_time and timesheet_detail.to_time:
            time_diff = timesheet_detail.to_time - timesheet_detail.from_time
            timesheet_detail.hours = time_diff.total_seconds() / 3600
        
        # Inserisci il timesheet solo se è nuovo
        if not timesheet.name:
            timesheet.insert()
        
        # Salva il timesheet con il nuovo detail
        timesheet.calculate_hours()
        timesheet.save()
        
        return {
            "success": True,
            "timesheet_detail": timesheet_detail.name,
            "timesheet": timesheet.name
        }
    
    except Exception as e:
        frappe.log_error(f"Errore in create_timesheet_detail: {str(e)}")
        frappe.throw(_("Errore nella creazione: {0}").format(str(e)))

@frappe.whitelist()
def update_timesheet_detail(name, data):
    """
    Aggiorna un Time Sheet Detail esistente con controllo permessi
    """
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        doc = frappe.get_doc("Timesheet Detail", name)
        
        # Controllo permessi: gli Employee possono modificare solo i propri timesheet
        user_roles = frappe.get_roles(frappe.session.user)
        is_manager = any(role in user_roles for role in ["System Manager", "HR Manager", "HR User"])
        
        if not is_manager and "Employee" in user_roles:
            current_employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
            if not current_employee:
                frappe.throw(_("Utente non associato a nessun dipendente"))
            
            # Verifica che il timesheet appartenga all'utente corrente
            timesheet = frappe.get_doc("Timesheet", doc.parent)
            if timesheet.employee != current_employee:
                frappe.throw(_("Non autorizzato a modificare questo timesheet"))
        
        # Funzione helper per pulire le date
        def clean_datetime(dt_str):
            if not dt_str:
                return None
            # Rimuovi timezone info
            dt_str = re.sub(r'[+-]\d{2}:\d{2}$', '', dt_str)
            dt_str = dt_str.replace('Z', '')
            return get_datetime(dt_str)
        
        # Aggiorna i campi
        if "from_time" in data:
            doc.from_time = clean_datetime(data["from_time"])
            
        if "to_time" in data:
            doc.to_time = clean_datetime(data["to_time"])
            
        if "project" in data:
            doc.project = data["project"]
        if "task" in data:
            doc.task = data["task"]
        if "activity_type" in data:
            doc.activity_type = data["activity_type"]
        if "description" in data:
            doc.description = data["description"]
        
        # Calcola automaticamente le ore
        if doc.from_time and doc.to_time:
            time_diff = doc.to_time - doc.from_time
            doc.hours = time_diff.total_seconds() / 3600
        
        doc.save()
        
        # Aggiorna il timesheet parent
        timesheet = frappe.get_doc("Timesheet", doc.parent)
        timesheet.calculate_hours()
        timesheet.save()
        
        return {"success": True}
    
    except Exception as e:
        frappe.log_error(f"Errore in update_timesheet_detail: {str(e)}")
        frappe.throw(_("Errore nell'aggiornamento: {0}").format(str(e)))

@frappe.whitelist()
def delete_timesheet_detail(name):
    """
    Elimina un Time Sheet Detail con controllo permessi
    """
    try:
        doc = frappe.get_doc("Timesheet Detail", name)
        timesheet_name = doc.parent
        
        # Controllo permessi: gli Employee possono eliminare solo dai propri timesheet
        user_roles = frappe.get_roles(frappe.session.user)
        is_manager = any(role in user_roles for role in ["System Manager", "HR Manager", "HR User"])
        
        if not is_manager and "Employee" in user_roles:
            current_employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name")
            if not current_employee:
                frappe.throw(_("Utente non associato a nessun dipendente"))
            
            # Verifica che il timesheet appartenga all'utente corrente
            timesheet = frappe.get_doc("Timesheet", timesheet_name)
            if timesheet.employee != current_employee:
                frappe.throw(_("Non autorizzato a eliminare da questo timesheet"))
        
        doc.delete()
        
        # Aggiorna il timesheet parent
        timesheet = frappe.get_doc("Timesheet", timesheet_name)
        
        # ✅ AGGIUNTO: Controlla se il timesheet è rimasto vuoto
        if not timesheet.time_logs or len(timesheet.time_logs) == 0:
            # Se non ci sono più time_logs, elimina anche il timesheet
            timesheet.delete()
            frappe.db.commit()
            return {
                "success": True,
                "timesheet_deleted": True,
                "message": "Activity and empty timesheet deleted successfully"
            }
        else:
            # Se ci sono ancora time_logs, aggiorna il timesheet
            timesheet.calculate_hours()
            timesheet.save()
            return {
                "success": True,
                "timesheet_deleted": False,
                "message": "Activity deleted successfully"
            }
    
    except Exception as e:
        frappe.log_error(f"Errore in delete_timesheet_detail: {str(e)}")
        frappe.throw(_("Errore nell'eliminazione: {0}").format(str(e)))

@frappe.whitelist()
def get_filter_options():
    """
    Recupera le opzioni per i filtri con controllo permessi
    """
    try:
        # Controllo permessi basato sui ruoli
        user_roles = frappe.get_roles(frappe.session.user)
        is_manager = any(role in user_roles for role in ["System Manager", "HR Manager", "HR User"])
        
        # Progetti: per Employee solo quelli assegnati tramite "Assign To", per Manager tutti aperti
        if is_manager:
            projects = frappe.get_all("Project", 
                filters={"status": "Open"}, 
                fields=["name", "project_name"],
                order_by="project_name")
        else:
            # Per Employee: progetti assegnati tramite sistema "Assign To" di ERPNext
            current_user = frappe.session.user
            assigned_projects = frappe.db.sql("""
                SELECT DISTINCT p.name, p.project_name
                FROM `tabProject` p
                INNER JOIN `tabToDo` t ON t.reference_type = 'Project' AND t.reference_name = p.name
                WHERE t.allocated_to = %s AND t.status = 'Open' AND p.status = 'Open'
                ORDER BY p.project_name
            """, (current_user,), as_dict=True)
            
            if assigned_projects:
                projects = [{"name": p.name, "project_name": p.project_name} for p in assigned_projects]
            else:
                # Se non ha progetti assegnati, lista vuota - l'utente deve contattare HR
                projects = []
        
        # Lista employees: manager vedono tutti, employee solo se stesso
        if is_manager:
            employees = frappe.get_all("Employee", 
                fields=["name", "employee_name"], 
                filters={"status": "Active"},
                order_by="employee_name"
            )
        else:
            # Employee vede solo se stesso
            current_employee = frappe.db.get_value("Employee", {"user_id": frappe.session.user}, ["name", "employee_name"])
            if current_employee:
                employees = [{
                    "name": current_employee[0],
                    "employee_name": current_employee[1] or current_employee[0]  # Fallback se employee_name è None
                }]
            else:
                # Se l'utente non ha un Employee associato, restituisci lista vuota
                frappe.log_error(f"Utente {frappe.session.user} non ha un Employee associato")
                employees = []
        
        return {
            "employees": employees,
            "projects": projects,
            "activity_types": frappe.get_all("Activity Type", 
                fields=["name", "activity_type"], 
                order_by="activity_type"
            ),
            "user_permissions": {
                "is_manager": is_manager,
                "is_employee_only": not is_manager,
                "current_employee": frappe.db.get_value("Employee", {"user_id": frappe.session.user}, "name") or None
            }
        }
    except Exception as e:
        frappe.log_error(f"Errore in get_filter_options: {str(e)}")
        return {"employees": [], "projects": [], "activity_types": [], "user_permissions": {"is_manager": False}}

def get_or_create_timesheet(employee, start_date, company):
    """
    Recupera o crea un timesheet settimanale per l'employee e la data specificata
    """
    # Assicurati che start_date sia l'inizio della settimana
    week_start = get_week_start_date(start_date)
    week_end = add_days(week_start, 6)
    
    # Cerca un timesheet esistente che inizi esattamente in questa settimana
    existing = frappe.get_all("Timesheet", 
        filters={
            "employee": employee,
            "start_date": week_start,
            "docstatus": ["<", 2]
        },
        fields=["name", "start_date", "end_date"],
        limit=1
    )
    
    if existing:
        return frappe.get_doc("Timesheet", existing[0].name)
    
    # Crea un nuovo timesheet settimanale SENZA salvarlo
    timesheet = frappe.get_doc({
        "doctype": "Timesheet",
        "employee": employee,
        "start_date": week_start,
        "end_date": week_end,
        "company": company or frappe.defaults.get_user_default("Company")
    })
    
    return timesheet

# ✅ Prima funzione (linea 339) - per progetti
def get_event_color(project):
    """Restituisce un colore per il progetto"""
    # ✅ MODIFICATO: Genera colori dinamici basati sul nome del progetto
    if not project:
        return "#95a5a6"  # Colore grigio di default
    
    # Lista di colori predefiniti
    colors = [
        "#3498db",  # Blu
        "#e74c3c",  # Rosso
        "#f39c12",  # Arancione
        "#2ecc71",  # Verde
        "#9b59b6",  # Viola
        "#1abc9c",  # Turchese
        "#e67e22",  # Arancione scuro
        "#34495e",  # Blu scuro
        "#f1c40f",  # Giallo
        "#e91e63",  # Rosa
        "#00bcd4",  # Ciano
        "#ff9800"   # Ambra
    ]
    
    # Genera un hash del nome del progetto per assegnare sempre lo stesso colore
    import hashlib
    hash_object = hashlib.md5(project.encode())
    hash_hex = hash_object.hexdigest()
    color_index = int(hash_hex, 16) % len(colors)
    
    return colors[color_index]


@frappe.whitelist()
def get_timesheet_projects(doctype, txt, searchfield, start, page_len, filters):
    """
    Restituisce i progetti associati a un timesheet specifico
    basandosi sui progetti già presenti nel timesheet
    """
    try:
        timesheet = filters.get('timesheet')
        if not timesheet:
            return []
        
        # Query per ottenere solo i progetti già presenti nel timesheet
        # più tutti i progetti aperti se il timesheet non ha ancora dettagli
        query = """
            SELECT DISTINCT p.name, p.project_name
            FROM `tabProject` p
            WHERE p.status = 'Open'
            AND (
                p.name IN (
                    SELECT DISTINCT tsd.project
                    FROM `tabTimesheet Detail` tsd
                    WHERE tsd.parent = %(timesheet)s
                    AND tsd.project IS NOT NULL
                    AND tsd.project != ''
                )
                OR NOT EXISTS (
                    SELECT 1 FROM `tabTimesheet Detail` tsd2
                    WHERE tsd2.parent = %(timesheet)s
                    AND tsd2.project IS NOT NULL
                    AND tsd2.project != ''
                )
            )
            AND (p.name LIKE %(txt)s OR p.project_name LIKE %(txt)s)
            ORDER BY p.project_name
            LIMIT %(start)s, %(page_len)s
        """
        
        return frappe.db.sql(query, {
            'timesheet': timesheet,
            'txt': f'%{txt}%',
            'start': start,
            'page_len': page_len
        })
        
    except Exception as e:
        frappe.log_error(f"Errore in get_timesheet_projects: {str(e)}")
        return []


@frappe.whitelist()
def get_employee_projects(doctype, txt, searchfield, start, page_len, filters):
    """
    Restituisce i progetti per i dialog di creazione attività
    Utilizza il sistema di assegnazione ToDo di ERPNext
    """
    try:
        # Controllo permessi basato sui ruoli
        user_roles = frappe.get_roles(frappe.session.user)
        is_manager = any(role in user_roles for role in ["System Manager", "HR Manager", "HR User"])
        
        if is_manager:
            # Manager vedono tutti i progetti aperti
            query = """
                SELECT p.name, p.project_name
                FROM `tabProject` p
                WHERE p.status = 'Open'
                AND (p.name LIKE %(txt)s OR p.project_name LIKE %(txt)s)
                ORDER BY p.project_name
                LIMIT %(start)s, %(page_len)s
            """
            
            return frappe.db.sql(query, {
                'txt': f'%{txt}%',
                'start': start,
                'page_len': page_len
            })
        else:
            # Employee vedono solo progetti assegnati tramite "Assign To"
            current_user = frappe.session.user
            query = """
                SELECT DISTINCT p.name, p.project_name
                FROM `tabProject` p
                INNER JOIN `tabToDo` t ON t.reference_type = 'Project' AND t.reference_name = p.name
                WHERE t.allocated_to = %(user)s AND t.status = 'Open' AND p.status = 'Open'
                AND (p.name LIKE %(txt)s OR p.project_name LIKE %(txt)s)
                ORDER BY p.project_name
                LIMIT %(start)s, %(page_len)s
            """
            
            assigned_projects = frappe.db.sql(query, {
                'user': current_user,
                'txt': f'%{txt}%',
                'start': start,
                'page_len': page_len
            })
            
            if assigned_projects:
                 return assigned_projects
             else:
                 # Se non ha progetti assegnati, lista vuota - l'utente deve contattare HR
                 return []
        
    except Exception as e:
        frappe.log_error(f"Errore in get_employee_projects: {str(e)}")
        return []


@frappe.whitelist()
def get_project_timesheets(doctype, txt, searchfield, start, page_len, filters):
    """
    Restituisce i timesheet associati a un progetto specifico
    """
    try:
        project = filters.get('project')
        if not project:
            return frappe.db.sql("""
                SELECT name, employee
                FROM `tabTimesheet`
                WHERE docstatus = 0
                AND employee IS NOT NULL
                AND (name LIKE %(txt)s OR employee LIKE %(txt)s)
                ORDER BY creation DESC
                LIMIT %(start)s, %(page_len)s
            """, {
                'txt': f'%{txt}%',
                'start': start,
                'page_len': page_len
            })
        
        # Trova gli employee che hanno lavorato su questo progetto
        query = """
            SELECT DISTINCT ts.name, ts.employee
            FROM `tabTimesheet` ts
            INNER JOIN `tabTimesheet Detail` tsd ON tsd.parent = ts.name
            WHERE ts.docstatus = 0
            AND tsd.project = %(project)s
            AND (ts.name LIKE %(txt)s OR ts.employee LIKE %(txt)s)
            ORDER BY ts.creation DESC
            LIMIT %(start)s, %(page_len)s
        """
        
        return frappe.db.sql(query, {
            'project': project,
            'txt': f'%{txt}%',
            'start': start,
            'page_len': page_len
        })
        
    except Exception as e:
        frappe.log_error(f"Errore in get_project_timesheets: {str(e)}")
        return []


def has_permission():
    """
    Verifica se l'utente corrente ha i permessi per accedere all'app Advanced Timesheet Calendar
    Utilizza solo i ruoli di base di ERPNext
    """
    try:
        # Verifica se l'utente ha uno dei ruoli di base di ERPNext
        user_roles = frappe.get_roles(frappe.session.user)
        required_roles = ["System Manager", "HR Manager", "HR User", "Employee"]
        
        # Se l'utente ha almeno uno dei ruoli richiesti, può accedere
        if any(role in user_roles for role in required_roles):
            return True
        
        # Verifica se l'utente ha permessi sui doctype Timesheet o Timesheet Detail
        if frappe.has_permission("Timesheet", "read") or frappe.has_permission("Timesheet Detail", "read"):
            return True
        
        return False
        
    except Exception as e:
        frappe.log_error(f"Errore in has_permission: {str(e)}")
        return False
