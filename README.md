[![it](https://img.shields.io/badge/lang-it-blue.svg)](https://github.com/CupoMeridio/advanced_tc/blob/main/README.it.md)

# 📅 AdvancedTC - Advanced Timesheet Calendar

A custom app for ERPNext that provides an advanced calendar view for managing timesheet details (Time Sheet Detail) with complete CRUD functionality, export and reporting capabilities.

## 🎯 Why AdvancedTC?

### Limitations of the Base ERPNext System

ERPNext, while being an excellent open-source ERP system, has some significant limitations in timesheet management that motivated the development of this custom app:

#### 🚫 **Standard System Issues**

1. **Limited Calendar View**: ERPNext provides a calendar view only for main Timesheets, but not for Timesheet Details, which can only be managed through tabular interface, making it difficult to visualize and edit individual activities temporally

2. **Unintuitive Interface**: Timesheet Detail management occurs through traditional forms, without drag & drop or visual editing

3. **Limited Filters**: The base system doesn't offer advanced filters for Employee, Project, Activity Type and Task in a single view

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
5. [Accessing the Application](#-accessing-the-application)
6. [Configuration Verification](#-configuration-verification)
7. [Project Access Control](#-project-access-control)
8. [Troubleshooting](#-troubleshooting)
9. [Usage](#-usage)
10. [Technical Architecture](#-technical-architecture)
11. [Detailed Features](#-detailed-features)
12. [Customization](#-customization)
13. [Configuration](#-configuration)
14. [Troubleshooting](#-troubleshooting-1)
15. [Additional Features](#-additional-features)
16. [Additional Resources](#-additional-resources)
17. [Contributing](#-contributing)
18. [License](#-license)
19. [Support](#-support)
20. [Changelog](#-changelog)
21. [Project Information](#-project-information)

## 🎯 Key Features

- **Interactive Calendar View**: Modern visualization with FullCalendar.js
- **Advanced Filters**: Employee, Project, Activity Type and Task with role-based visibility
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
│   ├── patches.txt                    # Database patches
│   ├── install.py                     # Installation script
│   ├── pyproject.toml                 # Python project config
│   ├── api/
│   │   ├── __init__.py
│   │   └── timesheet_details.py       # Backend API
│   ├── public/
│   │   ├── .gitkeep
│   │   ├── css/
│   │   │   └── timesheet_calendar.css # CSS styles
│   │   ├── images/                    # Image assets
│   │   └── js/
│   │       └── timesheet_calendar.js  # JS utilities
│   ├── config/                        # Configuration files (empty)
│   ├── templates/
│   │   ├── __init__.py
│   │   └── pages/                     # Template pages
│   └── advanced_tc/
│       ├── .frappe                    # Frappe metadata
│       ├── __init__.py
│       └── page/
│           └── advanced_tc/
│               ├── __init__.py
│               ├── advanced_tc.json   # Page configuration
│               └── advanced_tc.js     # Frontend logic
├── .gitignore                         # Git ignore rules
├── .pre-commit-config.yaml            # Pre-commit hooks
├── setup.py                           # Python setup
├── pyproject.toml                     # Project configuration
├── README.md                          # Documentation (English)
├── README.it.md                       # Documentation (Italian)
├── license.txt                        # License

```

### Key Components

1. **hooks.py**: Configures app_name="advanced_tc", CSS, JS and workspace
2. **install.py**: Installation script with informative messages
3. **advanced_tc.json**: Defines the main page configuration
4. **advanced_tc.js**: Frontend logic for interactive calendar
5. **timesheet_details.py**: Backend API endpoints for timesheet management
6. **timesheet_calendar.css/js**: Styling and utility functions for the calendar

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
- **Employee**: Filter by specific employee (managers see all, employees see only themselves)
- **Project**: Filter by project (based on "Assign To" assignments)
- **Activity Type**: Filter by activity type
- **Task**: Filter by specific task

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

The app implements intelligent timesheet management:

- **Automatic Creation**: Creates weekly timesheets automatically when needed
- **Work Week Management**: Automatically calculates week start (Monday)
- **Smart Deletion**: Removes empty timesheets automatically

### 2. Dynamic Color System

Each project automatically receives a consistent color:

- **Consistent Colors**: Same project = same color always
- **Uniform Distribution**: Algorithm distributes colors evenly
- **No Configuration**: Works automatically without setup

### 3. Validation and Controls

The app includes automatic controls to ensure data quality:

- **Overlap Control**: Prevents time overlaps between activities
- **Time Validation**: Verifies that times are logical and valid
- **Permission Control**: Verifies user can modify the data
- **Duration Validation**: Checks that activities have reasonable duration

### 4. Advanced Drag & Drop

Intuitive drag functionality:

- **Move Activities**: Drag to change date and time
- **Resize**: Modify duration by dragging borders
- **Visual Feedback**: Notifications and loading states
- **Automatic Rollback**: Cancels changes on error

### 5. Filter System

Advanced filters for efficient navigation:

- **Employee**: Filter by employee (with permission control)
- **Project**: Filter by project (based on assignments)
- **Activity Type**: Filter by activity type
- **Task**: Filter by specific task
- **Combinations**: Use multiple filters simultaneously

### 6. Advanced Export and Reporting

Complete export and analysis functionality:

- **CSV Export**: Export data in CSV format with all details
- **Summary Dialog**: Display statistics for selected period
- **Detailed Breakdown**: Analysis by employee, project and activity type
- **Export Filters**: Export only filtered data

### 7. Break and Pause Management

Complete support for break management:

- **Break Start/End**: Define break times within activity
- **Automatic Calculation**: Break hours are subtracted from total
- **Validation**: Automatic checks for valid break times
- **Actual Hours**: Precise calculation of worked hours

## 🎨 Customization

The app offers various customization options:

### Visual Customization
- **Automatic Colors**: Dynamic color assignment for projects
- **Responsive Interface**: Adapts to different screen sizes
- **Theme Support**: Compatible with ERPNext themes
- **Custom Styling**: Modify CSS for personalized appearance

### Extensibility
- **Modular Architecture**: Easy to extend with new features
- **API Integration**: Add custom endpoints as needed
- **Event Hooks**: Integrate with ERPNext workflows
- **Custom Fields**: Support for additional data fields

## 🔧 Configuration

### Permissions

The app uses ERPNext standard roles and permissions:

**Required ERPNext Roles:**
- `Employee`: Basic timesheet access for own records
- `HR User`: Extended HR functionality
- `HR Manager`: Full HR management capabilities
- `System Manager`: Complete system access

**Required DocType Access:**
- Timesheet, Timesheet Detail, Employee, Project, Task, Activity Type

### Performance Optimization

For optimal performance with large datasets:

- **Period Filters**: Use date range filters to limit data
- **Database Optimization**: Automatic indexing for faster queries
- **Caching**: Intelligent caching of frequently accessed data
- **Pagination**: Efficient data loading for large result sets

### Default Configurations

The app includes sensible defaults:

- **CSS and JavaScript**: Automatically loaded assets
- **Activity Types**: Pre-configured common activity types
- **Calendar Settings**: Optimized for business use
- **Performance**: Efficient caching and indexing

## 🐛 Troubleshooting

### Common Issues

#### 1. Calendar doesn't load

**Solutions**:
- Rebuild and restart: `bench build && bench restart`
- Verify user has appropriate ERPNext roles
- Clear browser cache (Ctrl+Shift+R)
- Check browser console for JavaScript errors

#### 2. API Errors

**Solutions**:
- Check ERPNext error logs
- Verify user permissions for Timesheet DocType
- Ensure proper site configuration

#### 3. Styles not applied

**Solutions**:
- Recompile assets: `bench build --app advanced_tc`
- Hard refresh browser (Ctrl+F5)
- Check CSS file paths

#### 4. Drag & Drop Issues

**Common causes**:
- Insufficient permissions
- Time overlaps with existing activities
- Validation errors

**Solutions**:
- Check user permissions
- Verify no time conflicts
- Review activity validation rules

For advanced debugging and development, the app includes:

- **Backend Logging**: Detailed error tracking and debugging
- **Frontend Logging**: Browser console debugging tools
- **Testing Framework**: Unit and integration tests
- **Development Tools**: Code quality and testing utilities

## 🚀 Additional Features

### Advanced Break Management
- **Automatic Break Rules**: Configurable break policies
- **Net Hours Calculation**: Precise work time calculation
- **Break Validation**: Ensures breaks are within activity time

### Keyboard Shortcuts
- **Ctrl+N**: Create new activity
- **Ctrl+R**: Refresh calendar
- **Esc**: Close dialogs

## 📚 Additional Resources

- **[📖 Technical Documentation](TECHNICAL_DOCUMENTATION.md)** - Detailed technical architecture, API reference, and development guide
- [ERPNext Documentation](https://docs.erpnext.com/)
- [Frappe Framework Documentation](https://frappeframework.com/docs)
- [FullCalendar.js Documentation](https://fullcalendar.io/docs)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the project
2. **Create** a feature branch
3. **Commit** your changes with clear messages
4. **Test** your changes thoroughly
5. **Submit** a Pull Request

### Development Guidelines

- Follow ERPNext coding standards
- Include appropriate documentation
- Test all functionality before submitting
- Ensure compatibility with latest ERPNext version

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