import frappe
from frappe import _

def after_install():
    """
    Configurazioni post-installazione per l'app Advanced Timesheet Calendar
    """
    try:
        print("🚀 Inizializzazione Advanced Timesheet Calendar...")
        
        frappe.db.commit()
        print("✅ Installazione completata con successo!")
        print("ℹ️ L'app è accessibile tramite:")
        print("   • Link diretto: /app/advanced_tc")
        print("   • Icona nella sezione Apps del desktop ERPNext")
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Errore durante l'installazione: {str(e)}", "Timesheet Calendar Install")
        print(f"❌ Errore durante l'installazione: {str(e)}")

# Funzioni rimosse: create_custom_roles() e setup_permissions()
# L'app ora utilizza i ruoli di base di ERPNext





def before_uninstall():
    """
    Pulizia prima della disinstallazione
    """
    try:
        print("🧹 Avvio pulizia Advanced Timesheet Calendar...")
        
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