import frappe
from frappe import _

def after_install():
    """
    Configurazioni post-installazione per l'app AdvancedTC
    """
    try:
        # Crea ruoli personalizzati se non esistono
        create_custom_roles()
        
        # Configura permessi di base
        setup_permissions()
        
        # Crea Activity Types di default se non esistono
        create_default_activity_types()
        
        # Crea workspace per l'app
        create_workspace()
        
        frappe.db.commit()
        
        print("✅ AdvancedTC installata con successo!")
        print("📅 Vai alla pagina 'advanced_tc' per iniziare a usare la calendar view.")
        
    except Exception as e:
        frappe.log_error(f"Errore durante l'installazione: {str(e)}", "Timesheet Calendar Install")
        print(f"❌ Errore durante l'installazione: {str(e)}")

def create_custom_roles():
    """
    Crea ruoli personalizzati per l'app
    """
    roles = [
        {
            "role_name": "Timesheet Calendar User",
            "description": "Can view and edit own timesheet details"
        },
        {
            "role_name": "Timesheet Calendar Manager",
            "description": "Can manage all timesheet details and view reports"
        }
    ]
    
    for role_data in roles:
        role_name = role_data["role_name"]
        
        if frappe.db.exists("Role", role_name):
            # Il ruolo esiste già, controlla se è disabilitato
            role_doc = frappe.get_doc("Role", role_name)
            if role_doc.disabled:
                # Riabilita il ruolo
                role_doc.disabled = 0
                role_doc.save(ignore_permissions=True)
                print(f"🔓 Riabilitato ruolo esistente: {role_name}")
            else:
                print(f"ℹ️ Ruolo già attivo: {role_name}")
        else:
            # Crea un nuovo ruolo
            role = frappe.get_doc({
                "doctype": "Role",
                "role_name": role_name,
                "description": role_data["description"]
            })
            role.insert(ignore_permissions=True)
            print(f"✅ Creato ruolo: {role_name}")

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
        
        if existing:
            # Il permesso esiste già, aggiornalo per assicurarsi che sia corretto
            try:
                doc_perm = frappe.get_doc("Custom DocPerm", existing)
                doc_perm.read = perm.get("read", 0)
                doc_perm.write = perm.get("write", 0)
                doc_perm.create = perm.get("create", 0)
                doc_perm.delete = perm.get("delete", 0)
                doc_perm.submit = perm.get("submit", 0)
                doc_perm.cancel = perm.get("cancel", 0)
                doc_perm.save(ignore_permissions=True)
                print(f"🔄 Aggiornato permesso per {perm['role']} su {perm['doctype']}")
            except Exception as e:
                print(f"⚠️ Errore aggiornando permesso per {perm['role']}: {str(e)}")
        else:
            # Crea un nuovo permesso
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

def create_default_activity_types():
    """
    Crea Activity Types di default se non esistono
    """
    default_activity_types = [
        "Development",
        "Testing",
        "Meeting",
        "Documentation",
        "Support",
        "Training",
        "Research",
        "Planning",
        "Review",
        "Deployment"
    ]
    
    for activity_type in default_activity_types:
        if not frappe.db.exists("Activity Type", activity_type):
            try:
                doc = frappe.get_doc({
                    "doctype": "Activity Type",
                    "activity_type": activity_type
                })
                doc.insert(ignore_permissions=True)
                print(f"✅ Creato Activity Type: {activity_type}")
            except Exception as e:
                print(f"⚠️ Errore creando Activity Type {activity_type}: {str(e)}")

def create_workspace():
    """
    Crea il workspace per l'app AdvancedTC
    """
    workspace_name = "Advanced Timesheet Calendar"
    
    # Controlla se il workspace esiste già
    if frappe.db.exists("Workspace", workspace_name):
        print(f"ℹ️ Workspace '{workspace_name}' già esistente")
        return
    
    try:
        # Crea il workspace
        workspace = frappe.get_doc({
            "doctype": "Workspace",
            "name": workspace_name,
            "title": workspace_name,
            "category": "Modules",
            "icon": "fa fa-calendar",
            "color": "#3498db",
            "is_standard": 0,
            "parent_page": "",
            "public": 1,
            "charts": [],
            "shortcuts": [
                {
                    "label": _("Advanced Timesheet Calendar"),
                    "name": "advanced_tc",
                    "type": "Page",
                    "icon": "fa fa-calendar",
                    "color": "#3498db",
                    "description": _("Calendar view for timesheet details management")
                }
            ],
            "cards": [
                {
                    "label": _("Timesheet Management"),
                    "items": [
                        {
                            "type": "Page",
                            "name": "advanced_tc",
                            "label": _("Advanced Timesheet Calendar"),
                            "description": _("Interactive calendar view for managing timesheet details")
                        }
                    ]
                }
            ]
        })
        workspace.insert(ignore_permissions=True)
        print(f"✅ Creato workspace: {workspace_name}")
        
    except Exception as e:
        print(f"⚠️ Errore creando workspace: {str(e)}")
        frappe.log_error(f"Errore creando workspace: {str(e)}", "Workspace Creation Error")

def before_uninstall():
    """
    Pulizia prima della disinstallazione
    """
    try:
        # Rimuovi workspace
        workspace_name = "Advanced Timesheet Calendar"
        if frappe.db.exists("Workspace", workspace_name):
            frappe.delete_doc("Workspace", workspace_name, ignore_permissions=True)
            print(f"🗑️ Rimosso workspace: {workspace_name}")
        
        # Disabilita ruoli personalizzati invece di eliminarli
        custom_roles = ["Timesheet Calendar User", "Timesheet Calendar Manager"]
        
        for role_name in custom_roles:
            if frappe.db.exists("Role", role_name):
                try:
                    # Rimuovi prima i permessi personalizzati
                    frappe.db.delete("Custom DocPerm", {"role": role_name})
                    print(f"🗑️ Rimossi permessi per ruolo: {role_name}")
                    
                    # Disabilita il ruolo invece di eliminarlo
                    role_doc = frappe.get_doc("Role", role_name)
                    role_doc.disabled = 1
                    role_doc.save(ignore_permissions=True)
                    print(f"🔒 Disabilitato ruolo: {role_name}")
                    
                except Exception as role_error:
                    print(f"⚠️ Errore gestendo ruolo {role_name}: {str(role_error)}")
                    # Continua con gli altri ruoli anche se uno fallisce
                    continue
        
        frappe.db.commit()
        print("✅ Pulizia completata")
        
    except Exception as e:
        frappe.log_error(f"Errore durante la disinstallazione: {str(e)}", "Timesheet Calendar Uninstall")
        print(f"❌ Errore durante la pulizia: {str(e)}")