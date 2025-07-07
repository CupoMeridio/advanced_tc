from frappe import _

def get_data():
    return {
        "name": _("Advanced Timesheet Calendar"),
        "category": "Modules",
        "icon": "fa fa-calendar",
        "color": "#3498db",
        "is_standard": 0,
        "parent_page": "",
        "__onload": {
            "is_standard": 0
        },
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
    }