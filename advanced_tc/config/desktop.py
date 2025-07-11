from frappe import _

def get_data():
	return [
		{
			"module_name": "advancedtc",
			"label": _("Advanced Timesheet Calendar"),
			"color": "#3498db",
			"icon": "/assets/advanced_tc/images/logo.svg",
			"type": "link",
			"link": "#advanced_tc",
			"description": _("Visualizzazione calendario avanzata per la gestione dei timesheet con funzionalità di drag & drop, filtri intelligenti e controlli di accesso basati sui ruoli.")
		}
	]