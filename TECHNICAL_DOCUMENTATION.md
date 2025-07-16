# AdvancedTC - Technical Documentation

## 🏗️ Architecture Overview

AdvancedTC is built as a Frappe/ERPNext application with a modern web-based architecture:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│                 │    │                 │    │                 │
│ FullCalendar.js │◄──►│ Python/Frappe   │◄──►│ MariaDB/MySQL   │
│ JavaScript      │    │ API Endpoints   │    │ ERPNext Schema  │
│ CSS/HTML        │    │ Business Logic  │    │ Timesheet Data  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Detailed File Structure

### Core Application Files

#### `advanced_tc/hooks.py`
Main configuration file that defines:

```python
app_name = "advanced_tc"
app_title = "Advanced Timesheet Calendar"
app_publisher = "Youbiquo"
app_description = "Advanced calendar interface for ERPNext timesheets"
app_version = "0.1.1"

# CSS and JS includes
app_include_css = [
    "/assets/advanced_tc/css/timesheet_calendar.css"
]

app_include_js = [
    "/assets/advanced_tc/js/timesheet_calendar.js"
]

# Page definitions
website_route_rules = [
    {"from_route": "/advanced-tc", "to_route": "advanced_tc"}
]
```

#### `advanced_tc/install.py`
Installation script with setup procedures:

```python
import frappe

def after_install():
    """Post-installation setup"""
    print("\n" + "="*50)
    print("🎉 AdvancedTC Installation Complete!")
    print("="*50)
    print("📋 Next Steps:")
    print("1. Assign users appropriate ERPNext roles")
    print("2. Configure project assignments via 'Assign To'")
    print("3. Access via: Modules > AdvancedTC")
    print("="*50 + "\n")
```

### Frontend Architecture

#### `advanced_tc/advanced_tc/page/advanced_tc/advanced_tc.js`
Main frontend controller:

```javascript
class AdvancedTimesheetCalendar {
    constructor(wrapper) {
        this.wrapper = wrapper;
        this.page = frappe.ui.make_app_page({
            parent: wrapper,
            title: 'Advanced Timesheet Calendar',
            single_column: true
        });
        
        this.init_calendar();
        this.setup_filters();
        this.setup_event_handlers();
    }
    
    init_calendar() {
        // FullCalendar initialization
        this.calendar = new FullCalendar.Calendar(this.calendar_container, {
            initialView: 'dayGridMonth',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            selectable: true,
            editable: true,
            events: this.fetch_events.bind(this),
            select: this.handle_time_selection.bind(this),
            eventDrop: this.handle_event_drop.bind(this),
            eventResize: this.handle_event_resize.bind(this),
            eventClick: this.handle_event_click.bind(this)
        });
    }
}
```

#### `advanced_tc/public/js/timesheet_calendar.js`
Utility functions and helpers:

```javascript
// Date utilities
function formatDateForAPI(date) {
    return date.toISOString().split('T')[0];
}

function formatTimeForAPI(date) {
    return date.toISOString();
}

// Color generation for projects
function generateProjectColor(projectName) {
    const colors = [
        '#3498db', '#e74c3c', '#f39c12', '#2ecc71',
        '#9b59b6', '#1abc9c', '#34495e', '#e67e22'
    ];
    
    let hash = 0;
    for (let i = 0; i < projectName.length; i++) {
        hash = projectName.charCodeAt(i) + ((hash << 5) - hash);
    }
    
    return colors[Math.abs(hash) % colors.length];
}

// Validation functions
function validateTimeRange(fromTime, toTime) {
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

### Backend API Architecture

#### `advanced_tc/api/timesheet_details.py`
Main API endpoints:

```python
import frappe
from frappe import _
from datetime import datetime, timedelta
import hashlib

@frappe.whitelist()
def get_timesheet_details(start_date=None, end_date=None, filters=None):
    """
    Retrieve timesheet details for calendar display
    
    Args:
        start_date (str): Start date in YYYY-MM-DD format
        end_date (str): End date in YYYY-MM-DD format
        filters (dict): Additional filters (employee, project, etc.)
    
    Returns:
        list: Formatted events for FullCalendar
    """
    
    # Permission check
    if not has_permission():
        frappe.throw(_("Insufficient permissions"))
    
    # Build query conditions
    conditions = ["ts.docstatus = 1"]
    values = {}
    
    if start_date and end_date:
        conditions.append("tsd.date BETWEEN %(start_date)s AND %(end_date)s")
        values.update({
            "start_date": start_date,
            "end_date": end_date
        })
    
    # Apply role-based filtering
    user_roles = frappe.get_roles()
    if not any(role in user_roles for role in ['System Manager', 'HR Manager', 'HR User']):
        # Employee can only see their own records
        conditions.append("ts.employee = %(employee)s")
        values["employee"] = frappe.session.user
    
    # Apply additional filters
    if filters:
        if filters.get("employee"):
            conditions.append("ts.employee = %(employee)s")
            values["employee"] = filters["employee"]
        
        if filters.get("project"):
            conditions.append("tsd.project = %(project)s")
            values["project"] = filters["project"]
        
        if filters.get("activity_type"):
            conditions.append("tsd.activity_type = %(activity_type)s")
            values["activity_type"] = filters["activity_type"]
        
        if filters.get("task"):
            conditions.append("tsd.task = %(task)s")
            values["task"] = filters["task"]
    
    # Execute query
    query = f"""
        SELECT 
            tsd.name,
            tsd.date,
            tsd.from_time,
            tsd.to_time,
            tsd.hours,
            tsd.description,
            tsd.project,
            tsd.task,
            tsd.activity_type,
            ts.employee,
            emp.employee_name,
            proj.project_name,
            task.subject as task_subject
        FROM 
            `tabTimesheet Detail` tsd
        INNER JOIN 
            `tabTimesheet` ts ON tsd.parent = ts.name
        LEFT JOIN 
            `tabEmployee` emp ON ts.employee = emp.name
        LEFT JOIN 
            `tabProject` proj ON tsd.project = proj.name
        LEFT JOIN 
            `tabTask` task ON tsd.task = task.name
        WHERE 
            {' AND '.join(conditions)}
        ORDER BY 
            tsd.date, tsd.from_time
    """
    
    results = frappe.db.sql(query, values, as_dict=True)
    
    # Format for FullCalendar
    events = []
    for row in results:
        event = {
            "id": row.name,
            "title": format_event_title(row),
            "start": combine_date_time(row.date, row.from_time),
            "end": combine_date_time(row.date, row.to_time),
            "backgroundColor": get_event_color(row.project),
            "borderColor": get_event_color(row.project),
            "extendedProps": {
                "employee": row.employee,
                "employee_name": row.employee_name,
                "project": row.project,
                "project_name": row.project_name,
                "task": row.task,
                "task_subject": row.task_subject,
                "activity_type": row.activity_type,
                "description": row.description,
                "hours": row.hours
            }
        }
        events.append(event)
    
    return events

@frappe.whitelist()
def create_timesheet_detail(data):
    """
    Create a new timesheet detail entry
    
    Args:
        data (dict): Timesheet detail data
    
    Returns:
        dict: Created timesheet detail info
    """
    
    # Validate input data
    validate_timesheet_data(data)
    
    # Check for overlaps
    check_time_overlaps(data)
    
    # Get or create weekly timesheet
    timesheet = get_or_create_weekly_timesheet(
        data['employee'], 
        data['date']
    )
    
    # Create timesheet detail
    timesheet_detail = frappe.get_doc({
        "doctype": "Timesheet Detail",
        "parent": timesheet.name,
        "parenttype": "Timesheet",
        "parentfield": "time_logs",
        "date": data['date'],
        "from_time": data['from_time'],
        "to_time": data['to_time'],
        "project": data.get('project'),
        "task": data.get('task'),
        "activity_type": data.get('activity_type'),
        "description": data.get('description', ''),
        "hours": calculate_hours(data['from_time'], data['to_time'])
    })
    
    timesheet_detail.insert()
    
    # Update parent timesheet
    timesheet.reload()
    timesheet.save()
    
    return {
        "name": timesheet_detail.name,
        "timesheet": timesheet.name
    }

def validate_timesheet_data(data):
    """
    Validate timesheet data before creation
    """
    required_fields = ['employee', 'date', 'from_time', 'to_time']
    
    for field in required_fields:
        if not data.get(field):
            frappe.throw(_(f"Field '{field}' is required"))
    
    # Validate time range
    from_time = datetime.fromisoformat(data['from_time'].replace('Z', '+00:00'))
    to_time = datetime.fromisoformat(data['to_time'].replace('Z', '+00:00'))
    
    if from_time >= to_time:
        frappe.throw(_("End time must be after start time"))
    
    # Validate duration (max 24 hours)
    duration = (to_time - from_time).total_seconds() / 3600
    if duration > 24:
        frappe.throw(_("Activity duration cannot exceed 24 hours"))

def check_time_overlaps(data):
    """
    Check for time overlaps with existing entries
    """
    employee = data['employee']
    date = data['date']
    from_time = data['from_time']
    to_time = data['to_time']
    
    # Query existing time logs for the same employee and date
    existing_logs = frappe.db.sql("""
        SELECT 
            tsd.from_time, 
            tsd.to_time,
            tsd.name
        FROM 
            `tabTimesheet Detail` tsd
        INNER JOIN 
            `tabTimesheet` ts ON tsd.parent = ts.name
        WHERE 
            ts.employee = %(employee)s 
            AND tsd.date = %(date)s
            AND ts.docstatus = 1
    """, {
        "employee": employee,
        "date": date
    }, as_dict=True)
    
    new_from = datetime.fromisoformat(from_time.replace('Z', '+00:00'))
    new_to = datetime.fromisoformat(to_time.replace('Z', '+00:00'))
    
    for log in existing_logs:
        existing_from = log.from_time
        existing_to = log.to_time
        
        # Check for overlap
        if (new_from < existing_to and new_to > existing_from):
            frappe.throw(_("Time overlap detected with existing entry"))

def get_or_create_weekly_timesheet(employee, date):
    """
    Get existing weekly timesheet or create new one
    """
    week_start = get_week_start_date(date)
    week_end = week_start + timedelta(days=6)
    
    # Check for existing timesheet
    existing_timesheet = frappe.db.get_value(
        "Timesheet",
        {
            "employee": employee,
            "start_date": week_start,
            "end_date": week_end
        },
        "name"
    )
    
    if existing_timesheet:
        return frappe.get_doc("Timesheet", existing_timesheet)
    
    # Create new timesheet
    timesheet = frappe.get_doc({
        "doctype": "Timesheet",
        "employee": employee,
        "start_date": week_start,
        "end_date": week_end,
        "company": frappe.defaults.get_user_default("Company")
    })
    
    timesheet.insert()
    timesheet.submit()
    
    return timesheet

def get_week_start_date(date_str):
    """
    Get the start date of the week (Monday) for a given date
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    days_since_monday = date_obj.weekday()
    week_start = date_obj - timedelta(days=days_since_monday)
    return week_start

def get_event_color(project_name):
    """
    Generate consistent color for project using hash
    """
    if not project_name:
        return "#95a5a6"  # Default gray
    
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
    
    # Generate hash and select color
    hash_object = hashlib.md5(project_name.encode())
    hash_int = int(hash_object.hexdigest(), 16)
    color_index = hash_int % len(colors)
    
    return colors[color_index]

def has_permission():
    """
    Check if user has permission to access timesheet data
    """
    user_roles = frappe.get_roles()
    allowed_roles = [
        'System Manager', 
        'HR Manager', 
        'HR User', 
        'Employee'
    ]
    
    return any(role in user_roles for role in allowed_roles)
```

## 🔒 Security Implementation

### Role-Based Access Control

```python
def get_employee_projects(employee=None):
    """
    Get projects accessible to an employee based on assignments
    """
    user_roles = frappe.get_roles()
    
    # Managers see all projects
    if any(role in user_roles for role in ['System Manager', 'HR Manager', 'HR User']):
        return frappe.get_all(
            "Project",
            filters={"status": "Open"},
            fields=["name", "project_name"]
        )
    
    # Employees see only assigned projects
    if not employee:
        employee = frappe.session.user
    
    # Get projects assigned via "Assign To"
    assigned_projects = frappe.db.sql("""
        SELECT DISTINCT 
            p.name, 
            p.project_name
        FROM 
            `tabProject` p
        INNER JOIN 
            `tabToDo` t ON t.reference_name = p.name
        WHERE 
            t.reference_type = 'Project'
            AND t.allocated_to = %(employee)s
            AND p.status = 'Open'
    """, {"employee": employee}, as_dict=True)
    
    return assigned_projects
```

### Data Validation

```python
class TimesheetValidator:
    @staticmethod
    def validate_time_format(time_str):
        """Validate ISO time format"""
        try:
            datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_date_range(start_date, end_date):
        """Validate date range is logical"""
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        return start <= end
    
    @staticmethod
    def validate_employee_access(employee):
        """Validate user can access employee data"""
        user_roles = frappe.get_roles()
        
        # Managers can access any employee
        if any(role in user_roles for role in ['System Manager', 'HR Manager', 'HR User']):
            return True
        
        # Employees can only access their own data
        return employee == frappe.session.user
```

## 🎨 Frontend Styling

### CSS Architecture

```css
/* advanced_tc/public/css/timesheet_calendar.css */

/* Main container */
.advanced-tc-container {
    padding: 20px;
    background: #f8f9fa;
    min-height: 100vh;
}

/* Calendar styling */
.fc-event {
    border-radius: 4px;
    border: none;
    padding: 2px 4px;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.fc-event:hover {
    opacity: 0.8;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Filter sidebar */
.filter-sidebar {
    background: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.filter-section {
    margin-bottom: 15px;
}

.filter-section label {
    font-weight: 600;
    color: #2c3e50;
    margin-bottom: 5px;
    display: block;
}

/* Responsive design */
@media (max-width: 768px) {
    .advanced-tc-container {
        padding: 10px;
    }
    
    .fc-toolbar {
        flex-direction: column;
        gap: 10px;
    }
    
    .fc-toolbar-chunk {
        display: flex;
        justify-content: center;
    }
}

/* Loading states */
.loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Dialog customizations */
.modal-dialog.modal-lg {
    max-width: 800px;
}

.timesheet-form .form-group {
    margin-bottom: 15px;
}

.timesheet-form .control-label {
    font-weight: 600;
    color: #2c3e50;
}

/* Button styling */
.btn-primary {
    background-color: #3498db;
    border-color: #3498db;
}

.btn-primary:hover {
    background-color: #2980b9;
    border-color: #2980b9;
}

.btn-success {
    background-color: #2ecc71;
    border-color: #2ecc71;
}

.btn-success:hover {
    background-color: #27ae60;
    border-color: #27ae60;
}
```

## 🧪 Testing Framework

### Backend Tests

```python
# tests/test_timesheet_api.py
import unittest
import frappe
from advanced_tc.api.timesheet_details import (
    create_timesheet_detail,
    get_timesheet_details,
    check_time_overlaps
)

class TestTimesheetAPI(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.test_employee = "test@example.com"
        self.test_date = "2024-01-15"
        
    def test_create_timesheet_detail(self):
        """Test timesheet detail creation"""
        data = {
            "employee": self.test_employee,
            "date": self.test_date,
            "from_time": "2024-01-15T09:00:00Z",
            "to_time": "2024-01-15T17:00:00Z",
            "description": "Test activity"
        }
        
        result = create_timesheet_detail(data)
        self.assertIsNotNone(result.get("name"))
        
    def test_time_overlap_validation(self):
        """Test overlap detection"""
        # Create first activity
        data1 = {
            "employee": self.test_employee,
            "date": self.test_date,
            "from_time": "2024-01-15T09:00:00Z",
            "to_time": "2024-01-15T12:00:00Z"
        }
        create_timesheet_detail(data1)
        
        # Try to create overlapping activity
        data2 = {
            "employee": self.test_employee,
            "date": self.test_date,
            "from_time": "2024-01-15T11:00:00Z",
            "to_time": "2024-01-15T15:00:00Z"
        }
        
        with self.assertRaises(frappe.ValidationError):
            create_timesheet_detail(data2)
    
    def tearDown(self):
        """Clean up test data"""
        frappe.db.rollback()
```

### Frontend Tests

```javascript
// tests/test_calendar.js
describe('AdvancedTimesheetCalendar', () => {
    let calendar;
    
    beforeEach(() => {
        // Setup DOM
        document.body.innerHTML = '<div id="calendar-container"></div>';
        calendar = new AdvancedTimesheetCalendar('#calendar-container');
    });
    
    test('should initialize calendar', () => {
        expect(calendar.calendar).toBeDefined();
        expect(calendar.calendar.view.type).toBe('dayGridMonth');
    });
    
    test('should validate time range', () => {
        const validRange = validateTimeRange(
            '2024-01-15T09:00:00Z',
            '2024-01-15T17:00:00Z'
        );
        expect(validRange.valid).toBe(true);
        
        const invalidRange = validateTimeRange(
            '2024-01-15T17:00:00Z',
            '2024-01-15T09:00:00Z'
        );
        expect(invalidRange.valid).toBe(false);
    });
    
    test('should generate consistent project colors', () => {
        const color1 = generateProjectColor('Project A');
        const color2 = generateProjectColor('Project A');
        const color3 = generateProjectColor('Project B');
        
        expect(color1).toBe(color2);
        expect(color1).not.toBe(color3);
    });
});
```

## 🚀 Performance Optimization

### Database Indexing

```sql
-- Recommended database indexes for optimal performance

-- Index on timesheet detail date for date range queries
CREATE INDEX idx_timesheet_detail_date 
ON `tabTimesheet Detail` (date);

-- Index on timesheet employee for user filtering
CREATE INDEX idx_timesheet_employee 
ON `tabTimesheet` (employee);

-- Composite index for common filter combinations
CREATE INDEX idx_timesheet_detail_composite 
ON `tabTimesheet Detail` (date, project, activity_type);

-- Index on ToDo for project assignments
CREATE INDEX idx_todo_assignment 
ON `tabToDo` (reference_type, reference_name, allocated_to);
```

### Caching Strategy

```python
# Cache frequently accessed data
@frappe.cache()
def get_employee_list():
    """Cache employee list for filter options"""
    return frappe.get_all(
        "Employee",
        fields=["name", "employee_name"],
        filters={"status": "Active"}
    )

@frappe.cache(ttl=300)  # 5 minute cache
def get_project_assignments(employee):
    """Cache project assignments per employee"""
    return get_employee_projects(employee)
```

### Frontend Optimization

```javascript
// Debounced filter updates
const debouncedFilterUpdate = debounce((filters) => {
    calendar.refetchEvents();
}, 300);

// Lazy loading for large datasets
function fetchEvents(info, successCallback, failureCallback) {
    const pageSize = 100;
    const offset = this.currentOffset || 0;
    
    frappe.call({
        method: 'advanced_tc.api.timesheet_details.get_timesheet_details',
        args: {
            start_date: info.startStr,
            end_date: info.endStr,
            limit: pageSize,
            offset: offset
        },
        callback: (r) => {
            if (r.message) {
                successCallback(r.message);
            }
        }
    });
}

// Memory management
function cleanup() {
    if (this.calendar) {
        this.calendar.destroy();
    }
    
    // Remove event listeners
    $(window).off('resize.advancedtc');
    $(document).off('click.advancedtc');
}
```

## 🔧 Configuration Options

### Environment Variables

```python
# site_config.json additions
{
    "advanced_tc": {
        "max_hours_per_day": 24,
        "default_activity_type": "Development",
        "auto_break_rules": {
            "enabled": true,
            "min_duration_hours": 6,
            "break_duration_minutes": 30
        },
        "color_scheme": "default",
        "cache_ttl": 300
    }
}
```

### Customization Hooks

```python
# hooks.py - Custom event handlers
doc_events = {
    "Timesheet": {
        "before_save": "advanced_tc.utils.validate_timesheet",
        "after_insert": "advanced_tc.utils.notify_timesheet_creation"
    },
    "Project": {
        "after_insert": "advanced_tc.utils.setup_project_defaults"
    }
}

# Custom validation
def validate_timesheet(doc, method):
    """Custom timesheet validation"""
    total_hours = sum(log.hours for log in doc.time_logs)
    if total_hours > 24:
        frappe.throw("Daily hours cannot exceed 24")
```

## 📊 Monitoring and Analytics

### Error Tracking

```python
import logging

# Setup logging
logger = logging.getLogger('advanced_tc')
handler = logging.FileHandler('/path/to/advanced_tc.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_api_call(method_name, args, user):
    """Log API calls for monitoring"""
    logger.info(f"API Call: {method_name} by {user} with args: {args}")

def log_error(error, context):
    """Log errors with context"""
    logger.error(f"Error: {error} | Context: {context}")
```

### Performance Metrics

```python
import time
from functools import wraps

def measure_performance(func):
    """Decorator to measure function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
        
        return result
    return wrapper

@measure_performance
def get_timesheet_details(start_date, end_date, filters):
    # Implementation
    pass
```

---

## 📚 Additional Resources

- [Frappe Framework Documentation](https://frappeframework.com/docs)
- [ERPNext Developer Guide](https://docs.erpnext.com/docs/v13/user/manual/en/setting-up/articles/developer-guide)
- [FullCalendar.js Documentation](https://fullcalendar.io/docs)
- [MariaDB Performance Tuning](https://mariadb.com/kb/en/optimization-and-tuning/)

---

*This technical documentation is maintained alongside the main project documentation and should be updated with any architectural changes.*