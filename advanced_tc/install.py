import frappe
from frappe import _

def after_install():
    """
    Configurazioni post-installazione per l'app Advanced Timesheet Calendar
    """
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
    """
    Crea una workspace custom dedicata per Advanced Timesheet Calendar
    """
    try:
        # Verifica se la workspace esiste già
        if frappe.db.exists("Workspace", "Advanced Timesheet Calendar"):
            print("ℹ️ Workspace 'Advanced Timesheet Calendar' già esistente, rimuovo i ruoli per renderlo pubblico...")
            # Rimuovi tutti i ruoli per renderlo visibile a tutti
            existing_workspace = frappe.get_doc("Workspace", "Advanced Timesheet Calendar")
            existing_workspace.roles = []
            existing_workspace.public = 1
            existing_workspace.is_hidden = 0
            existing_workspace.save(ignore_permissions=True)
            print("✅ Workspace reso pubblico per tutti gli utenti")
            return
        
        # Crea la nuova workspace
        workspace = frappe.get_doc({
            "doctype": "Workspace",
            "title": "Advanced Timesheet Calendar",
            "label": "Advanced Timesheet Calendar",
            "module": "advanced_tc",
            "icon": "calendar",
            "is_hidden": 0,
            "public": 1,
            "roles": [],
            "sequence_id": 99,
            "content": '[{"id":"header1","type":"header","data":{"text":"<span class=\\"h4\\"><b>Advanced Timesheet Calendar</b></span>","col":12}},{"id":"intro1","type":"paragraph","data":{"text":"<p class=\\"text-muted\\">Visualizza e gestisci i tuoi timesheet in un formato calendario intuitivo. Questa applicazione ti permette di:</p><ul class=\\"text-muted\\"><li>📅 Visualizzare i timesheet in formato calendario</li><li>⏱️ Aggiungere rapidamente nuove voci timesheet</li><li>📊 Monitorare le ore lavorate per progetto</li><li>🔍 Filtrare per dipendente, progetto e periodo</li></ul><p class=\\"text-muted mb-4\\">Usa il pulsante nella barra degli strumenti per accedere all\'applicazione.</p>","col":12}}]',
            "shortcuts": [
                {
                    "type": "URL",
                    "label": "Advanced Timesheet Calendar",
                    "url": "/app/advanced_tc",
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