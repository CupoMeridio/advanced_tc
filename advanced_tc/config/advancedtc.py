from frappe import _

def get_data():
	return [
		{
			"label": _("Advanced Timesheet Calendar"),
			"icon": "fa fa-calendar",
			"items": [
				{
					"type": "page",
					"name": "advanced_tc",
					"label": _("Timesheet Calendar"),
					"description": _("Visualizzazione calendario per timesheet")
				}
			]
		}
	]