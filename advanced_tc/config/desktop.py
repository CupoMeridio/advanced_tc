from frappe import _

def get_data():
    return [
        {
            "module_name": "advanced_tc",
            "color": "#3498db",
            "icon": "fa fa-calendar",
            "type": "page",
            "link": "advanced_tc",
            "label": _("Advanced Timesheet Calendar"),
            "description": _("Calendar view for timesheet details management")
        }
    ]