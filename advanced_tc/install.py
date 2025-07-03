import frappe
from frappe import _

def after_install():
    """
    Configurazioni post-installazione per l'app Advanced Timesheet Calendar
    """
    try:
        print("🚀 Inizializzazione Advanced Timesheet Calendar...")
        
        # Crea ruoli personalizzati
        create_custom_roles()
        
        # Configura permessi
        setup_permissions()
        

        
        frappe.db.commit()
        print("✅ Installazione completata con successo!")
        print("ℹ️ L'app è accessibile tramite link diretto: /app/advanced_tc")
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Errore durante l'installazione: {str(e)}", "Timesheet Calendar Install")
        print(f"❌ Errore durante l'installazione: {str(e)}")

def create_custom_roles():
    """
    Crea ruoli personalizzati per l'app
    """
    roles = [
        {
            "role_name": "Timesheet Calendar User",
            "description": "Can view and manage timesheet details in calendar view with Advanced Timesheet Calendar"
        },
        {
            "role_name": "Timesheet Calendar Manager",
            "description": "Can manage all timesheet details and view reports"
        }
    ]
    
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.get_doc({
                "doctype": "Role",
                "role_name": role_data["role_name"],
                "description": role_data["description"]
            })
            role.insert(ignore_permissions=True)
            print(f"✅ Creato ruolo: {role_data['role_name']}")

def setup_permissions():
    """
    Configura permessi di base per i ruoli personalizzati
    """
    # Permessi per Timesheet Calendar User
    user_permissions = [
        {
            "role": "Timesheet Calendar User",
            "doctype": "Timesheet",
            "permlevel": 0,
            "read": 1,
            "write": 1,
            "create": 1
        },
        {
            "role": "Timesheet Calendar User",
            "doctype": "Timesheet Detail",
            "permlevel": 0,
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1
        }
    ]
    
    # Permessi per Timesheet Calendar Manager
    manager_permissions = [
        {
            "role": "Timesheet Calendar Manager",
            "doctype": "Timesheet",
            "permlevel": 0,
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1,
            "submit": 1,
            "cancel": 1
        },
        {
            "role": "Timesheet Calendar Manager",
            "doctype": "Timesheet Detail",
            "permlevel": 0,
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 1
        }
    ]
    
    all_permissions = user_permissions + manager_permissions
    
    for perm in all_permissions:
        # Controlla se il permesso esiste già
        existing = frappe.db.get_value("Custom DocPerm", {
            "role": perm["role"],
            "parent": perm["doctype"],
            "permlevel": perm["permlevel"]
        })
        
        if not existing:
            try:
                doc_perm = frappe.get_doc({
                    "doctype": "Custom DocPerm",
                    "role": perm["role"],
                    "parent": perm["doctype"],
                    "parenttype": "DocType",
                    "parentfield": "permissions",
                    "permlevel": perm["permlevel"],
                    "read": perm.get("read", 0),
                    "write": perm.get("write", 0),
                    "create": perm.get("create", 0),
                    "delete": perm.get("delete", 0),
                    "submit": perm.get("submit", 0),
                    "cancel": perm.get("cancel", 0)
                })
                doc_perm.insert(ignore_permissions=True)
                print(f"✅ Creato permesso per {perm['role']} su {perm['doctype']}")
            except Exception as e:
                print(f"⚠️ Errore creando permesso per {perm['role']}: {str(e)}")



def before_uninstall():
    """
    Pulizia prima della disinstallazione
    """
    try:
        print("🧹 Avvio pulizia Advanced Timesheet Calendar...")
        
        # Rimuovi ruoli personalizzati
        custom_roles = ["Timesheet Calendar User", "Timesheet Calendar Manager"]
        
        for role in custom_roles:
            if frappe.db.exists("Role", role):
                # Rimuovi prima i permessi
                frappe.db.delete("Custom DocPerm", {"role": role})
                # Poi rimuovi il ruolo
                frappe.delete_doc("Role", role, ignore_permissions=True)
                print(f"🗑️ Rimosso ruolo: {role}")
        
        # Rimuovi workspace (se esistente da installazioni precedenti)
        workspace_name = "timesheet_calendar"
        if frappe.db.exists("Workspace", workspace_name):
            frappe.delete_doc("Workspace", workspace_name, ignore_permissions=True)
            print(f"🗑️ Rimosso workspace: {workspace_name}")
        
        frappe.db.commit()
        print("✅ Pulizia completata")
        
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(f"Errore durante la disinstallazione: {str(e)}", "Timesheet Calendar Uninstall")
        print(f"❌ Errore durante la pulizia: {str(e)}")