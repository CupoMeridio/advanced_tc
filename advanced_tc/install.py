import frappe
from frappe import _

def after_install():
    """
    Configurazioni post-installazione per l'app Advanced Timesheet Calendar
    """
    try:
        print("🚀 Inizializzazione Advanced Timesheet Calendar...")
        
        # Aggiungi link alla workspace Projects
        add_link_to_projects_workspace()
        
        frappe.db.commit()
        print("✅ Installazione completata con successo!")
        print("ℹ️ L'app è accessibile tramite:")
        print("   • Link diretto: /app/advanced_tc")
        print("   • Icona nella sezione Apps del desktop ERPNext")
        print("   • Link 'Advanced Timesheet Calendar' nella sezione Time Tracking della workspace Projects")
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Errore durante l'installazione: {str(e)}", "Timesheet Calendar Install")
        print(f"❌ Errore durante l'installazione: {str(e)}")

# Funzioni rimosse: create_custom_roles() e setup_permissions()
# L'app ora utilizza i ruoli di base di ERPNext

def add_link_to_projects_workspace():
    """
    Aggiunge il link all'Advanced Timesheet Calendar nella sezione Time Tracking della workspace Projects
    """
    try:
        # Verifica se la workspace Projects esiste
        if not frappe.db.exists("Workspace", "Projects"):
            print("⚠️ Workspace Projects non trovata, salto l'aggiunta del link")
            return
        
        # Carica la workspace Projects
        workspace = frappe.get_doc("Workspace", "Projects")
        
        # Verifica se il link esiste già nella sezione Time Tracking
        for link in workspace.links:
            if link.get("label") == "Advanced Timesheet Calendar" and link.get("link_to") == "advanced_tc" and link.get("link_type") == "Page" and link.get("type") == "Link":
                print("ℹ️ Link 'Advanced Timesheet Calendar' già presente nella sezione Time Tracking della workspace Projects")
                return
        
        # Trova l'indice del Card Break "Time Tracking"
        time_tracking_index = None
        for i, link in enumerate(workspace.links):
            if link.get("type") == "Card Break" and link.get("label") == "Time Tracking":
                time_tracking_index = i
                break
        
        if time_tracking_index is None:
            print("⚠️ Sezione 'Time Tracking' non trovata nella workspace Projects")
            return
        
        # Trova l'indice dove inserire il nuovo link (dopo l'ultimo link della sezione Time Tracking)
        insert_index = time_tracking_index + 1
        for i in range(time_tracking_index + 1, len(workspace.links)):
            if workspace.links[i].get("type") == "Card Break":
                insert_index = i
                break
            else:
                insert_index = i + 1
        
        # Aggiungi il nuovo link nella sezione Time Tracking
        new_link = {
            "dependencies": "",
            "hidden": 0,
            "is_query_report": 0,
            "label": "Advanced Timesheet Calendar",
            "link_count": 0,
            "link_to": "advanced_tc",
            "link_type": "Page",
            "onboard": 0,
            "type": "Link"
        }
        
        workspace.links.insert(insert_index, new_link)
        workspace.save(ignore_permissions=True)
        print("✅ Link 'Advanced Timesheet Calendar' aggiunto nella sezione Time Tracking della workspace Projects")
            
    except Exception as e:
        frappe.log_error(f"Errore nell'aggiunta del link alla workspace Projects: {str(e)}", "Advanced TC Install")
        print(f"⚠️ Errore nell'aggiunta del link alla workspace Projects: {str(e)}")

def remove_link_from_projects_workspace():
    """
    Rimuove il link all'Advanced Timesheet Calendar dalla sezione Time Tracking della workspace Projects
    """
    try:
        # Verifica se la workspace Projects esiste
        if not frappe.db.exists("Workspace", "Projects"):
            return
        
        # Carica la workspace Projects
        workspace = frappe.get_doc("Workspace", "Projects")
        
        # Trova e rimuovi il link
        links_to_remove = []
        for i, link in enumerate(workspace.links):
            if link.get("label") == "Advanced Timesheet Calendar" and link.get("link_to") == "advanced_tc" and link.get("link_type") == "Page" and link.get("type") == "Link":
                links_to_remove.append(i)
        
        # Rimuovi i links in ordine inverso per mantenere gli indici corretti
        for i in reversed(links_to_remove):
            workspace.links.pop(i)
        
        if links_to_remove:
            workspace.save(ignore_permissions=True)
            print("🗑️ Link rimosso dalla sezione Time Tracking della workspace Projects")
            
    except Exception as e:
        frappe.log_error(f"Errore nella rimozione del link dalla workspace Projects: {str(e)}", "Advanced TC Uninstall")
        print(f"⚠️ Errore nella rimozione del link dalla workspace Projects: {str(e)}")

def before_uninstall():
    """
    Pulizia prima della disinstallazione
    """
    try:
        print("🧹 Avvio pulizia Advanced Timesheet Calendar...")
        
        # Rimuovi link dalla workspace Projects
        remove_link_from_projects_workspace()
        
        # Rimuovi workspace (se esistente da installazioni precedenti)
        workspace_name = "timesheet_calendar"
        if frappe.db.exists("Workspace", workspace_name):
            frappe.delete_doc("Workspace", workspace_name, ignore_permissions=True)
            print(f"🗑️ Rimosso workspace: {workspace_name}")
        
        frappe.db.commit()
        print("✅ Pulizia completata")
        print("ℹ️ Disinstallazione Advanced Timesheet Calendar completata")
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Errore durante la disinstallazione: {str(e)}", "Timesheet Calendar Uninstall")
        print(f"❌ Errore durante la pulizia: {str(e)}")