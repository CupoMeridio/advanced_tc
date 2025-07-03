app_name = "advanced_tc"
app_title = "AdvancedTC"
app_publisher = "Prova"
app_description = "Calendar view per i timesheets details"
app_email = "prova@prova.it"
app_license = "gpl-3.0"



# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/advanced_tc/css/timesheet_calendar.css"


# include js in page
page_js = {"advanced_tc" : "public/js/timesheet_calendar.js"}





# Installation
# ------------


after_install = "advanced_tc.install.after_install"

# Uninstallation
# ------------

before_uninstall = "advanced_tc.install.before_uninstall"

