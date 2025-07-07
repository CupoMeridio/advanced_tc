[![it](https://img.shields.io/badge/lang-it-blue.svg)](https://github.com/CupoMeridio/advanced_tc/blob/main/README.it.md)

# 📅 AdvancedTC - Advanced Timesheet Calendar

A custom app for ERPNext that provides an advanced calendar view for managing timesheet details (Time Sheet Detail) with complete CRUD functionality, export and reporting capabilities.

## 🎯 Why AdvancedTC?

### Limitations of the Base ERPNext System

ERPNext, while being an excellent open-source ERP system, has some significant limitations in timesheet management that motivated the development of this custom app:

#### 🚫 **Standard System Issues**

1. **Limited Calendar View**: ERPNext provides a calendar view only for main Timesheets, but not for Timesheet Details, which can only be managed through tabular interface, making it difficult to visualize and edit individual activities temporally

2. **Unintuitive Interface**: Timesheet Detail management occurs through traditional forms, without drag & drop or visual editing

3. **Limited Filters**: The base system doesn't offer advanced filters for Employee, Project and Activity Type in a single view

4. **Limited Export**: Lack of custom CSV export functionality with detailed statistics

5. **Complex Break Management**: Difficulty in managing breaks and lunch breaks within activities

#### ✅ **Solutions Implemented in AdvancedTC**

- **Modern Calendar View**: Interface based on FullCalendar.js with intuitive temporal visualization
- **Drag & Drop**: Visual activity modification with dragging and resizing
- **Advanced Filters**: Integrated filter system in the sidebar for efficient navigation
- **Smart Export**: CSV export functionality
- **Advanced Break Management**: Native support for breaks with automatic creation of separate activities
- **Complete Integration**: Maintains full compatibility with the existing ERPNext system

## 📑 Table of Contents

1. [Why AdvancedTC?](#-why-advancedtc)
2. [Key Features](#-key-features)
3. [Prerequisites](#-prerequisites)
4. [Installation](#-installation)
5. [Usage](#-usage)
6. [Technical Architecture](#-technical-architecture)
7. [Detailed Features](#-detailed-features)
8. [Customization](#-customization)
9. [Advanced Configuration](#-advanced-configuration)
10. [Troubleshooting](#-troubleshooting)
11. [Testing](#-testing)
12. [Advanced Features](#-advanced-features)
13. [Contributing](#-contributing)
14. [License](#-license)
15. [Support](#-support)
16. [Changelog](#-changelog)

## 🎯 Key Features

- **Interactive Calendar View**: Modern visualization with FullCalendar.js
- **Advanced Filters**: Employee, Project with role-based visibility
- **Complete CRUD Management**: Create, edit, delete activities
- **Drag & Drop**: Move and resize activities
- **ERPNext Integration**: Complete with Timesheet and Timesheet Detail
- **Project Assignment System**: Uses ERPNext's "Assign To" functionality for project access control
- **Role-Based Access**: Managers see all projects, employees only see assigned projects
- **Export and Reporting**: CSV export
- **Break Management**: Complete support for breaks and lunch breaks
- **Customization**: Dynamic colors and advanced configurations

## 📋 Prerequisites

- **ERPNext**: v15+ or Frappe Framework v15+
- **Python**: 3.10+ (as specified in pyproject.toml)
- **Modules**: Access to ERPNext Timesheet modules
- **Permissions**: Timesheet and Timesheet Detail management
- **Browser**: Modern with ES6+ support
- **Bench**: Properly configured for ERPNext site

## 🚀 Installation

### 1. Get the app

```bash
# Navigate to the main bench directory
cd /path/to/frappe-bench

# Download the app from repository
bench get-app https://github.com/CupoMeridio/advanced_tc.git
```

### 2. Verify app structure

```bash
# Verify the structure is correct
ls /path/to/frappe-bench/apps/advanced_tc/
# You should see: advanced_tc/, setup.py, pyproject.toml, README.md, license.txt

# Verify essential files
ls /path/to/frappe-bench/apps/advanced_tc/advanced_tc/
# You should see: __init__.py, hooks.py, modules.txt, install.py, api/, public/, config/
```

### 3. Install the app
```bash
# Start the bench
bench start
```
Open a new terminal, navigate to the bench folder and run:
```bash
# Install the app on specific site
bench --site [site-name] install-app advanced_tc
```

### 4. Migrate the database

```bash
# Run migration to apply database changes
bench --site [site-name] migrate
```

### 5. Restart the server

```bash
bench restart
```

## 🚀 Accessing the Application

After successful installation, you can access Advanced Timesheet Calendar in two ways:

### 1. Apps Section (Recommended)
- Navigate to your ERPNext desktop
- Click on the **"Apps"** section
- Look for the **"Advanced Timesheet Calendar"** icon with a calendar symbol
- Click the icon to launch the application

### 2. Direct Link
- Navigate directly to: `https://your-site.com/app/advanced_tc`
- Or use the relative path: `/app/advanced_tc`

### First Time Setup

**For Managers:**
- You will immediately see all open projects in the calendar
- Use ERPNext's "Assign To" feature to assign projects to employees

**For Employees:**
- If no projects are assigned, you'll see a message to contact HR
- Once projects are assigned, you'll see only your assigned projects

## ✅ Configuration Verification

### Required File Structure

The app must have this structure to work correctly:

```
advanced_tc/
├── advanced_tc/
│   ├── __init__.py                    # App version (0.0.1)
│   ├── hooks.py                       # App configuration
│   ├── modules.txt                    # Modules (advanced_tc)
│   ├── install.py                     # Installation script
│   ├── api/
│   │   └── timesheet_details.py       # Backend API
│   ├── public/
│   │   ├── css/
│   │   │   └── timesheet_calendar.css # CSS styles
│   │   └── js/
│   │       └── timesheet_calendar.js  # JS utilities
│   ├── config/
│   │   ├── desktop.py                 # Desktop configuration
│   │   └── workspace.py               # Workspace configuration
│   └── advanced_tc/
│       └── page/
│           └── advanced_tc/
│               ├── advanced_tc.json   # Page configuration
│               └── advanced_tc.js     # Frontend logic
├── setup.py                           # Python setup
├── pyproject.toml                     # Project configuration
├── README.md                          # Documentation
└── license.txt                        # License
```

### Key Components

1. **hooks.py**: Configures app_name="advanced_tc", CSS, JS and workspace
2. **install.py**: Configures the app to use ERPNext base permissions
3. **advanced_tc.json**: Defines the main page
4. **API**: Endpoints for timesheet details management
5. **Frontend**: JavaScript for interactive calendar

## 🔐 Project Access Control

### Role-Based Project Visibility

AdvancedTC implements a sophisticated project access control system using ERPNext's native "Assign To" functionality:

#### **For Managers** (System Manager, HR Manager, HR User)
- **Full Access**: Can view and create activities for all open projects
- **No Restrictions**: Complete project visibility in filters and dialogs
- **Assignment Control**: Can assign projects to employees using ERPNext's "Assign To" feature

#### **For Employees**
- **Restricted Access**: Can only view projects assigned to them via "Assign To"
- **Automatic Filtering**: Project filters and activity creation dialogs show only assigned projects
- **No Assignment Access**: If no projects are assigned, they see an empty list with instructions to contact HR

### How to Assign Projects to Employees

1. **Navigate to Project**: Go to any Project document in ERPNext
2. **Use Assign To**: Click the "Assign To" button in the sidebar
3. **Select Employee**: Choose the employee(s) to assign to the project
4. **Automatic Access**: The employee will immediately see the project in AdvancedTC

### Security Features

- **No Fallback Access**: Employees without assignments cannot see any projects
- **Clear Messaging**: Users are informed when they need HR assistance for project assignment
- **Consistent Filtering**: Same access rules apply to sidebar filters and activity creation dialogs
- **ERPNext Integration**: Uses native ERPNext ToDo system for assignments

## 🔧 Troubleshooting

### Error "No module named 'advanced_tc'"

**Cause**: The app was not copied correctly to the `apps/` directory

**Solution**:
```bash
# Verify the app is in the correct directory
ls /path/to/frappe-bench/apps/advanced_tc

# If not there, copy the app
cp -r /path/to/advanced_tc /path/to/frappe-bench/apps/

# Verify essential files exist
ls /path/to/frappe-bench/apps/advanced_tc/advanced_tc/hooks.py
ls /path/to/frappe-bench/apps/advanced_tc/advanced_tc/__init__.py
```

### Error "InvalidGitRepositoryError"

**Cause**: The folder is not a valid Git repository

**Solution**:
```bash
# Option 1: Initialize as Git repository
cd /path/to/advanced_tc
git init
git add .
git commit -m "Initial commit"

# Option 2: Manual copy (simpler)
cp -r /path/to/advanced_tc /path/to/frappe-bench/apps/
cd /path/to/frappe-bench
bench --site [site-name] install-app advanced_tc
```

### Installation error

**Verify**:
1. **Python Version**: Make sure to use Python 3.10+
2. **Permissions**: Verify ERPNext base permissions on Timesheet doctypes
3. **Dependencies**: Check that ERPNext v15+ is installed
4. **Logs**: Check logs for specific errors

```bash
# Check logs
tail -f /path/to/frappe-bench/logs/web.log
tail -f /path/to/frappe-bench/logs/worker.log
```

### App is installed but not working

**Verify**:
1. **Migration**: Make sure migration is completed
2. **User permissions**: Verify user has necessary ERPNext base roles
3. **Cache**: Clear browser cache
4. **Restart**: Completely restart the bench

```bash
# Force migration
bench --site [site-name] migrate

# Clear cache
bench --site [site-name] clear-cache

# Restart everything
bench restart
```

## 📖 Usage

### Accessing the Calendar View

1. **Login** to ERPNext
2. **Go** to **AdvancedTC** module or search "Advanced Timesheet Calendar"
3. **View** the calendar view with all activities

### Main Features

#### 🔍 Advanced Filters
- **Employee**: Filter by specific employee
- **Project**: Filter by project

#### ➕ Adding Activities
1. **Click** "Add Activity" or select a time range in the calendar
2. **Fill** the form with:
   - Employee (required)
   - From Time / To Time (required)
   - Project (optional)
   - Task (optional)
   - Activity Type (optional)
   - Description (optional)
   - Break Start/End (optional)
3. **Click** "Create" to save

#### ✏️ Editing Activities
- **Drag & Drop**: Drag the activity to change date/time
- **Resize**: Drag the borders to modify duration
- **Edit Dialog**: Click on the activity to open the edit dialog

#### 🗑️ Deleting Activities
1. **Click** on the activity to open the dialog
2. **Click** "Delete"
3. **Confirm** deletion

#### 📊 Export and Reporting

**Accessing the Feature:**
The export functionality is accessible through the **"Generate Report"** button in the sidebar.

**How to use:**
1. **Navigate** in the calendar to select the desired period
2. **Apply** any filters (employee, project) if needed
3. **Click** the "Generate Report" button in the sidebar
4. **View** the summary dialog with:
   - Total hours for the displayed period
   - Detailed breakdown by employee
   - Breakdown by project
   - Breakdown by activity type
5. **Click** "Export CSV" to download data in CSV format

**Technical Implementation:**
```javascript
// Function in advanced_tc.js file
show_report_dialog() {
    const events = this.calendar.getEvents();
    const view = this.calendar.view;
    const startDate = view.activeStart;
    const endDate = view.activeEnd;
    
    if (window.TimesheetCalendarUtils && window.TimesheetCalendarUtils.showSummaryDialog) {
        window.TimesheetCalendarUtils.showSummaryDialog(events, startDate, endDate);
    }
}
```

#### ⚙️ Settings
1. **Click** "Settings" in the sidebar
2. **Configure** preferences:
   - Default work shift time
   - Default break time
3. **Save** settings

#### 📅 Calendar Views
- **Month**: Complete monthly view
- **Week**: Weekly view (default)
- **Day**: Detailed daily view

## 🏗️ Technical Architecture

### Backend (Python)

#### API Endpoints

**File**: `api/timesheet_details.py`

```python
@frappe.whitelist()
def get_timesheet_details(start_date=None, end_date=None, filters=None):
    """Retrieve timesheet activities for the calendar"""
    
@frappe.whitelist()
def create_timesheet_detail(data):
    """Create a new timesheet activity"""
    
@frappe.whitelist()
def update_timesheet_detail(name, data):
    """Update existing activity"""
    
@frappe.whitelist()
def delete_timesheet_detail(name):
    """Delete timesheet activity"""
```

#### Business Logic

1. **Weekly Timesheet Management**:
   - Automatic creation if non-existent
   - Automatic calculation of week start (Monday)
   - Automatic deletion of empty timesheets

2. **Data Validation**:
   - Time overlap control
   - Time range validation
   - User permission verification

3. **Hours Calculation**:
   - Automatic duration calculation
   - Break and pause management
   - Configurable rounding

### Frontend (JavaScript)

#### Main Components

**File**: `public/js/advanced_tc.js`

```javascript
class AdvancedTimesheetCalendar {
    constructor() {
        this.init_calendar();
        this.setup_filters();
        this.setup_event_handlers();
    }
    
    init_calendar() {
        // FullCalendar initialization
    }
    
    setup_filters() {
        // Filter configuration
    }
    
    handle_time_selection(info) {
        // Time selection handling
    }
}
```

**File**: `public/js/timesheet_calendar.js`

```javascript
window.TimesheetCalendarUtils = {
    showSummaryDialog: function(events, startDate, endDate) {
        // Summary dialog and export
    },
    
    exportToCSV: function(activities, filename) {
        // CSV export functionality
    }
};
```

#### Used Libraries
- **FullCalendar.js**: Main calendar component
- **Frappe Framework**: ERPNext integration
- **jQuery**: DOM manipulation and AJAX

### ERPNext Integration

#### Involved DocTypes
- **Timesheet**: Weekly activity container
- **Timesheet Detail**: Single activity/timesheet entry
- **Employee**: Employee information
- **Project**: Project connection
- **Task**: Task connection
- **Activity Type**: Activity categorization

## 🚀 Detailed Features

### 1. Weekly Timesheet Management

#### Automatic Logic

The app implements intelligent timesheet management:

1. **Automatic Creation**: When creating a new activity, the app:
   - Calculates the week start (Monday)
   - Searches for an existing timesheet for that week
   - If it doesn't exist, automatically creates a new weekly timesheet

2. **Work Week Management**:
   ```python
   def get_week_start_date(date):
       """Calculate week start (Monday)"""
       if isinstance(date, str):
           date = getdate(date)
       days_since_monday = date.weekday()
       week_start = date - timedelta(days=days_since_monday)
       return week_start
   ```

3. **Smart Deletion**: When deleting the last activity of a timesheet, the app automatically deletes the empty timesheet as well.

### 2. Dynamic Color System

#### Assignment Algorithm

Each project automatically receives a color based on:

```python
def get_event_color(project):
    if not project:
        return "#95a5a6"  # Default gray
    
    # Generate MD5 hash of project name
    import hashlib
    hash_object = hashlib.md5(project.encode())
    hash_hex = hash_object.hexdigest()
    
    # Select color from palette
    color_index = int(hash_hex, 16) % len(colors)
    return colors[color_index]
```

**Advantages**:
- Same project = same color always
- Uniform color distribution
- No manual configuration required

### 3. Validation and Controls

#### Overlap Control

The app prevents time overlaps:

```python
# Check overlaps with existing time_logs
for existing_log in timesheet.time_logs:
    existing_from = existing_log.from_time
    existing_to = existing_log.to_time
    
    # Check overlaps
    if (new_from_time < existing_to and new_to_time > existing_from):
        frappe.throw(_("Time overlap detected with existing entry"))
```

#### Frontend Validation

```javascript
validateTimeRange: function(fromTime, toTime) {
    const from = new Date(fromTime);
    const to = new Date(toTime);
    
    if (from >= to) {
        return {
            valid: false,
            message: 'End time must be after start time'
        };
    }
    
    const diffHours = (to - from) / (1000 * 60 * 60);
    if (diffHours > 24) {
        return {
            valid: false,
            message: 'Activity cannot be longer than 24 hours'
        };
    }
    
    return { valid: true };
}
```

### 4. Advanced Drag & Drop

#### FullCalendar Event Handlers

```javascript
eventDrop: (info) => {
    this.update_activity(info.event);
},

eventResize: (info) => {
    this.update_activity(info.event);
},

update_activity(event) {
    const data = {
        from_time: event.start.toISOString(),
        to_time: event.end.toISOString()
    };
    
    this.update_activity_data(event.id, data);
}
```

#### Visual Feedback

- **Toast Notifications**: Operation confirmation
- **Loading States**: During updates
- **Error Handling**: Automatic rollback on error

### 5. Filter System

#### Available Filters

1. **Employee**: Filter by specific employee
2. **Project**: Filter by project
3. **Activity Type**: Filter by activity type
4. **Task**: Filter by specific task

#### Backend Implementation

```python
# Additional filters
if filters:
    if filters.get("employee"):
        conditions.append("ts.employee = %(employee)s")
        values["employee"] = filters["employee"]
    
    if filters.get("project"):
        conditions.append("tsd.project = %(project)s")
        values["project"] = filters["project"]
    
    # ... other filters
```

### 6. Advanced Export and Reporting

#### CSV Export Functionality

```javascript
exportToCSV: function(activities, filename = 'timesheet_details.csv') {
    const headers = [
        'Date', 'Employee', 'Project', 'Task', 
        'Activity Type', 'From Time', 'To Time', 
        'Hours', 'Description'
    ];
    
    const rows = activities.map(activity => {
        const props = activity.extendedProps;
        return [
            new Date(activity.start).toLocaleDateString(),
            props.employee_name || props.employee,
            props.project_name || props.project || '',
            props.task_subject || props.task || '',
            props.activity_type || '',
            new Date(activity.start).toLocaleTimeString(),
            new Date(activity.end).toLocaleTimeString(),
            props.hours || 0,
            props.description || ''
        ];
    });
    
    // Generate and download CSV
    const csvContent = [headers, ...rows]
        .map(row => row.map(field => `"${field}"`).join(','))
        .join('\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}
```

#### Summary Dialog

```javascript
showSummaryDialog: function(events, startDate, endDate) {
    // Calculate statistics
    const stats = this.calculateStatistics(events);
    
    // Create dialog with:
    // - Total period hours
    // - Breakdown by employee
    // - Breakdown by project
    // - Breakdown by activity type
    // - Export CSV button
}
```

### 7. Break and Pause Management

#### Break Fields in Dialog

- **Break Start**: Break start time
- **Break End**: Break end time
- **Automatic Calculation**: Break hours are subtracted from total

#### Break Validation

```javascript
validateBreakTimes: function(activityStart, activityEnd, breakStart, breakEnd) {
    // Verify break is within activity
    // Verify break start < break end
    // Calculate actual work hours
}
```

## 🎨 Customization

### Activity Colors

Activity colors are defined dynamically:

```python
# Default color palette
colors = [
    "#3498db",  # Blue
    "#e74c3c",  # Red
    "#f39c12",  # Orange
    "#2ecc71",  # Green
    "#9b59b6",  # Purple
    "#1abc9c",  # Turquoise
    "#34495e",  # Dark gray
    "#e67e22"   # Dark orange
]
```

### Custom CSS

**File**: `public/css/timesheet_calendar.css`

```css
/* Calendar customization */
.fc-event {
    border-radius: 4px;
    border: none;
    padding: 2px 4px;
}

/* Filter styles */
.filter-section {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
}

/* Responsive design */
@media (max-width: 768px) {
    .calendar-container {
        padding: 10px;
    }
}
```

### Additional Features

To add new features:

1. **Extend the main class**:
   ```javascript
   class CustomTimesheetCalendar extends AdvancedTimesheetCalendar {
       // New features
   }
   ```

2. **Add new API endpoints**:
   ```python
   @frappe.whitelist()
   def custom_function():
       # Custom logic
   ```

3. **Modify CSS** for new styles

## 🔧 Advanced Configuration

### Permissions

The app uses ERPNext base roles and permissions. Make sure users have appropriate permissions:

**Required ERPNext Roles:**
- `Employee`: Basic timesheet access for own records
- `HR User`: Extended HR functionality
- `HR Manager`: Full HR management capabilities
- `System Manager`: Complete system access

**Required DocType Permissions:**
```json
{
    "Timesheet": ["read", "write", "create"],
    "Timesheet Detail": ["read", "write", "create", "delete"],
    "Employee": ["read"],
    "Project": ["read"],
    "Task": ["read"],
    "Activity Type": ["read"]
}
```

**Note**: The app no longer creates custom roles. It relies entirely on ERPNext's built-in permission system.

### Performance

For sites with lots of data:

1. **Database Indexes**:
   ```sql
   CREATE INDEX idx_timesheet_detail_date ON `tabTimesheet Detail` (date);
   CREATE INDEX idx_timesheet_employee ON `tabTimesheet` (employee);
   ```

2. **Pagination**:
   ```python
   # Limit results by period
   limit_days = 90  # Maximum 3 months
   ```

3. **Cache**:
   ```python
   # Cache for frequent filters
   @frappe.cache()
   def get_employees():
       return frappe.get_all("Employee", fields=["name", "employee_name"])
   ```

### Default Configurations

**File**: `hooks.py`

```python
# App configurations
app_include_css = [
    "/assets/advanced_tc/css/timesheet_calendar.css"
]

app_include_js = [
    "/assets/advanced_tc/js/advanced_tc.js",
    "/assets/advanced_tc/js/timesheet_calendar.js"
]

# Default activity types
default_activity_types = [
    "Development",
    "Testing", 
    "Meeting",
    "Documentation",
    "Support",
    "Training"
]
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Calendar doesn't load

**Symptoms**: 
- White or empty page
- JavaScript errors in browser console
- Calendar not rendering

**Solutions**:

1. **Rebuild and restart the system**:
   ```bash
   bench build
   bench restart
   ```

2. **Verify user permissions**:
   ```bash
   bench --site [site-name] console
   >>> frappe.get_roles("[username]")
   ```
   User must have at least the roles: `Employee`, `HR User`, `HR Manager`, or `System Manager` with Timesheet access.

3. **Clear browser cache**:
   - Press `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
   - Or open developer tools (F12) and right-click refresh button → "Empty cache and reload"

4. **Check browser console**:
   - Open developer tools (F12)
   - Go to "Console" tab
   - Look for errors related to FullCalendar or missing JavaScript files

#### 2. API Errors

**Symptoms**: 500 errors or timeouts

**Debug**:
```python
# Enable detailed logging
import frappe
frappe.log_error("Debug info", "Timesheet Calendar")

# Check SQL queries
frappe.db.sql("SELECT * FROM tabTimesheet LIMIT 1", debug=1)
```

#### 3. Styles not applied

**Solutions**:
```bash
# Recompile assets
bench build --app advanced_tc

# Verify CSS path
ls -la sites/assets/advanced_tc/css/

# Hard refresh browser
Ctrl+F5 (Windows) / Cmd+Shift+R (Mac)
```

#### 4. Drag & Drop Issues

**Common causes**:
- Insufficient permissions
- Time overlaps
- Failed validation

**Debug**:
```javascript
// Browser console
console.log("Event drop:", info.event);
console.log("New time:", info.event.start, info.event.end);
```

### Advanced Debug

#### Backend Logging

```python
# In api/timesheet_details.py
import frappe
import json

def debug_log(message, data=None):
    frappe.log_error(
        json.dumps({
            "message": message,
            "data": data,
            "user": frappe.session.user
        }), 
        "AdvancedTC Debug"
    )
```

#### Frontend Logging

```javascript
// In advanced_tc.js
class DebugLogger {
    static log(message, data) {
        if (window.location.hostname === 'localhost') {
            console.log(`[AdvancedTC] ${message}`, data);
        }
    }
}
```

## 🧪 Testing

### Unit Tests

**File**: `tests/test_timesheet_details.py`

```python
import unittest
import frappe
from advanced_tc.api.timesheet_details import create_timesheet_detail

class TestTimesheetDetails(unittest.TestCase):
    def setUp(self):
        # Setup test data
        pass
    
    def test_create_activity(self):
        # Test activity creation
        pass
    
    def test_overlap_validation(self):
        # Test overlap validation
        pass
```

### Integration Tests

```python
def test_weekly_timesheet_creation():
    """Test automatic weekly timesheet creation"""
    # Create activity for new week
    # Verify timesheet creation
    # Verify hours calculation
```

### Frontend Tests

```javascript
// Test with Jest or similar
describe('AdvancedTimesheetCalendar', () => {
    test('should initialize calendar', () => {
        // Test initialization
    });
    
    test('should handle time selection', () => {
        // Test time selection
    });
});
```

## 🚀 Advanced Features

### 1. Advanced Break Management

#### Automatic Break Configuration

```python
# Automatic break configuration
AUTO_BREAK_RULES = {
    "lunch_break": {
        "min_duration_hours": 6,
        "break_duration_minutes": 30,
        "break_start_time": "12:00"
    }
}
```

#### Net Hours Calculation

```javascript
calculateNetHours: function(startTime, endTime, breakStart, breakEnd) {
    const totalMs = endTime - startTime;
    const breakMs = breakEnd && breakStart ? breakEnd - breakStart : 0;
    return (totalMs - breakMs) / (1000 * 60 * 60); // Net hours
}
```

### 2. Keyboard Shortcuts

Available keyboard shortcuts:
- **Ctrl+N**: Create new activity
- **Ctrl+R**: Refresh calendar

## 🤝 Contributing

### Contribution Process

1. **Fork** the project
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines

#### Python Code

```python
# Follow PEP 8
# Use docstrings
def create_timesheet_detail(data):
    """Create a new timesheet activity.
    
    Args:
        data (dict): Activity data
        
    Returns:
        dict: Operation result
        
    Raises:
        ValidationError: If data is not valid
    """
```

#### JavaScript Code

```javascript
// Use ES6+
// Comment complex functions
/**
 * Handles time range selection in the calendar
 * @param {Object} info - FullCalendar selection info
 */
handle_time_selection(info) {
    // Implementation
}
```

#### CSS

```css
/* Use BEM methodology */
.calendar-container__sidebar {
    /* Sidebar styles */
}

.calendar-container__sidebar--collapsed {
    /* Collapsed state */
}
```

### Testing

Before submitting a PR:

```bash
# Python tests
python -m pytest tests/

# JavaScript lint
npm run lint

# Manual testing
# - Create/edit/delete activities
# - Test drag & drop
# - Test export
```

## 📝 License

This project is released under **GPL-3.0** license. See the `license.txt` file for complete details.

### Commercial Use

- ✅ **Allowed**: Commercial use
- ✅ **Allowed**: Modification and distribution
- ✅ **Allowed**: Private use
- ❗ **Required**: Maintain GPL-3.0 license
- ❗ **Required**: Make source code available

## 📞 Support

### Support Channels

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For general questions
- **Wiki**: For additional documentation

### Debug Information

When reporting an issue, include:

```bash
# ERPNext version
bench version

# Error logs
bench logs

# Browser configuration
# - Browser version
# - Console errors (F12)
# - Network tab for API errors
```

### FAQ

**Q: How to add new Activity Types?**
A: Go to ERPNext > Setup > Activity Type and create new types.

**Q: Can I customize colors?**
A: Yes, modify the `get_event_color()` function in `api/timesheet_details.py`.

**Q: How to export data for long periods?**
A: Use filters to limit the dataset, then export to CSV.

**Q: Does the app work with ERPNext Cloud?**
A: Yes, but requires custom app installation (contact ERPNext support).

## 📋 Changelog

### v0.1.1 (Current)
- ✅ **NEW**: "Generate Report" button in sidebar for direct export access
- ✅ **IMPROVED**: Export functionality now fully accessible from UI
- ✅ **UPDATED**: Documentation consolidated in single README file
- ✅ Interactive calendar with FullCalendar.js
- ✅ Complete ERPNext integration
- ✅ Advanced filter system
- ✅ Drag & drop for activity editing
- ✅ CSV export and reporting
- ✅ Break and pause management
- ✅ Complete data validation

### v0.1.0
- ✅ Initial version with all base features
- ✅ Interactive calendar with FullCalendar.js
- ✅ Complete ERPNext integration
- ✅ Advanced filter system
- ✅ Drag & drop for activity editing
- ✅ Break and pause management
- ✅ Complete data validation

### v0.0.1 (Initial)
- ✅ Base project setup
- ✅ ERPNext app structure
- ✅ Hooks configuration
- ✅ First basic APIs

---

## 🎓 Project Information

This project was developed as an internship activity at [**Youbiquo**](https://youbiquo.eu) company by two Computer Engineering students from the University of Salerno:

- [**Fabrizio D'Errico**](https://github.com/fabriziodrr)
- [**Vittorio Postiglione**](https://github.com/CupoMeridio) 

---

**Developed with ❤️ for the ERPNext community**