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
        
        # Crea workspace custom dedicata
        create_custom_workspace()
        
        frappe.db.commit()
        print("✅ Installazione completata con successo!")
        print("ℹ️ L'app è accessibile tramite:")
        print("   • Link diretto: /app/advanced_tc")
        print("   • Icona nella sezione Apps del desktop ERPNext")
        print("   • Shortcut 'Advanced Timesheet Calendar' nella sezione Your Shortcuts della workspace Projects")
        print("   • Workspace dedicata: Advanced Timesheet Calendar")
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Errore durante l'installazione: {str(e)}", "Timesheet Calendar Install")
        print(f"❌ Errore durante l'installazione: {str(e)}")

# Funzioni rimosse: create_custom_roles() e setup_permissions()
# L'app ora utilizza i ruoli di base di ERPNext

def add_link_to_projects_workspace():
    """
    Aggiunge il link all'Advanced Timesheet Calendar nella sezione Your Shortcuts della workspace Projects
    """
    try:
        # Verifica se la workspace Projects esiste
        if not frappe.db.exists("Workspace", "Projects"):
            print("⚠️ Workspace Projects non trovata, salto l'aggiunta del link")
            return
        
        # Carica la workspace Projects
        workspace = frappe.get_doc("Workspace", "Projects")
        
        # Verifica se il shortcut esiste già
        shortcut_exists = False
        for shortcut in workspace.shortcuts:
            if shortcut.link_to == "advanced_tc" and shortcut.type == "Page":
                shortcut_exists = True
                break
        
        if not shortcut_exists:
            # Crea il nuovo shortcut
            new_shortcut = {
                "label": "Advanced Timesheet Calendar",
                "link_to": "advanced_tc",
                "type": "Page",
                "color": "Green"
            }
            
            workspace.append("shortcuts", new_shortcut)
            workspace.save(ignore_permissions=True)
            print("✅ Shortcut aggiunto alla sezione Your Shortcuts della workspace Projects")
        else:
            print("ℹ️ Shortcut già presente nella sezione Your Shortcuts")
            
    except Exception as e:
        frappe.log_error(f"Errore nell'aggiunta del shortcut alla workspace Projects: {str(e)}", "Advanced TC Install")
        print(f"⚠️ Errore nell'aggiunta del shortcut alla workspace Projects: {str(e)}")

def remove_link_from_projects_workspace():
    """
    Rimuove il shortcut all'Advanced Timesheet Calendar dalla sezione Your Shortcuts della workspace Projects
    """
    try:
        # Verifica se la workspace Projects esiste
        if not frappe.db.exists("Workspace", "Projects"):
            return
        
        # Carica la workspace Projects
        workspace = frappe.get_doc("Workspace", "Projects")
        
        # Trova e rimuovi il shortcut
        shortcuts_to_remove = []
        for i, shortcut in enumerate(workspace.shortcuts):
            if shortcut.link_to == "advanced_tc" and shortcut.type == "Page":
                shortcuts_to_remove.append(i)
        
        # Rimuovi i shortcuts in ordine inverso per mantenere gli indici corretti
        for i in reversed(shortcuts_to_remove):
            workspace.shortcuts.pop(i)
        
        if shortcuts_to_remove:
            workspace.save(ignore_permissions=True)
            print("🗑️ Shortcut rimosso dalla sezione Your Shortcuts della workspace Projects")
            
    except Exception as e:
        frappe.log_error(f"Errore nella rimozione del shortcut dalla workspace Projects: {str(e)}", "Advanced TC Uninstall")
        print(f"⚠️ Errore nella rimozione del shortcut dalla workspace Projects: {str(e)}")

def create_custom_workspace():
    """
    Crea una workspace custom dedicata per Advanced Timesheet Calendar
    """
    try:
        # Verifica se la workspace esiste già
        if frappe.db.exists("Workspace", "Advanced Timesheet Calendar"):
            print("ℹ️ Workspace 'Advanced Timesheet Calendar' già esistente")
            return
        
        # Crea la nuova workspace
        workspace = frappe.get_doc({
            "doctype": "Workspace",
            "title": "Advanced Timesheet Calendar",
            "module": "Projects",
            "icon": "fa fa-calendar",
            "indicator_color": "blue",
            "is_standard": 0,
            "public": 1,
            "shortcuts": [
                {
                    "label": "Advanced Timesheet Calendar",
                    "link_to": "advanced_tc",
                    "type": "Page",
                    "color": "Blue"
                }
            ]
        })
        
        workspace.insert(ignore_permissions=True)
        print("✅ Workspace 'Advanced Timesheet Calendar' creata con successo")
        
    except Exception as e:
        frappe.log_error(f"Errore durante la creazione della workspace: {str(e)}", "Advanced TC Install")
        print(f"⚠️ Errore durante la creazione della workspace: {str(e)}")

def remove_custom_workspace():
    """
    Rimuove la workspace custom durante la disinstallazione
    """
    try:
        if frappe.db.exists("Workspace", "Advanced Timesheet Calendar"):
            frappe.delete_doc("Workspace", "Advanced Timesheet Calendar", ignore_permissions=True)
            print("🗑️ Workspace 'Advanced Timesheet Calendar' rimossa")
    except Exception as e:
        frappe.log_error(f"Errore durante la rimozione della workspace: {str(e)}", "Advanced TC Uninstall")
        print(f"⚠️ Errore durante la rimozione della workspace: {str(e)}")

def before_uninstall():
    """
    Pulizia prima della disinstallazione
    """
    try:
        print("🧹 Avvio pulizia Advanced Timesheet Calendar...")
        
        # Rimuovi link dalla workspace Projects
        remove_link_from_projects_workspace()
        
        # Rimuovi workspace custom dedicata
        remove_custom_workspace()
        
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