// Timesheet Calendar Helper Functions and Utilities

// Utility functions for timesheet calendar
window.TimesheetCalendarUtils = {
    
    // Format duration in hours and minutes
    formatDuration: function(hours) {
        if (!hours) return '0h';
        
        const h = Math.floor(hours);
        const m = Math.round((hours - h) * 60);
        
        if (h === 0) {
            return `${m}m`;
        } else if (m === 0) {
            return `${h}h`;
        } else {
            return `${h}h ${m}m`;
        }
    },
    
    // Get activity type color
    getActivityColor: function(activityType) {
        const colors = {
            'Development': '#3498db',
            'Testing': '#e74c3c',
            'Meeting': '#f39c12',
            'Documentation': '#2ecc71',
            'Support': '#9b59b6',
            'Training': '#1abc9c',
            'Research': '#34495e',
            'Planning': '#e67e22',
            'Review': '#8e44ad',
            'Deployment': '#16a085'
        };
        return colors[activityType] || '#95a5a6';
    },
    
    // Validate time range
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
    },
    
    // Check for overlapping activities
    checkOverlap: function(newActivity, existingActivities, excludeId = null) {
        const newStart = new Date(newActivity.from_time);
        const newEnd = new Date(newActivity.to_time);
        
        for (let activity of existingActivities) {
            if (excludeId && activity.id === excludeId) continue;
            if (activity.extendedProps.employee !== newActivity.employee) continue;
            
            const existingStart = new Date(activity.start);
            const existingEnd = new Date(activity.end);
            
            // Check for overlap
            if (newStart < existingEnd && newEnd > existingStart) {
                return {
                    hasOverlap: true,
                    conflictingActivity: activity
                };
            }
        }
        
        return { hasOverlap: false };
    },
    
    // Calculate total hours for a day
    calculateDayTotal: function(activities, date, employee = null) {
        const targetDate = new Date(date).toDateString();
        let total = 0;
        
        activities.forEach(activity => {
            const activityDate = new Date(activity.start).toDateString();
            if (activityDate === targetDate) {
                if (!employee || activity.extendedProps.employee === employee) {
                    total += activity.extendedProps.hours || 0;
                }
            }
        });
        
        return total;
    },
    
    // Generate activity summary
    generateSummary: function(activities, startDate, endDate) {
        const summary = {
            totalHours: 0,
            byEmployee: {},
            byProject: {},
            byActivityType: {},
            dailyTotals: {}
        };
        
        activities.forEach(activity => {
            const hours = activity.extendedProps.hours || 0;
            const employee = activity.extendedProps.employee;
            const project = activity.extendedProps.project;
            const activityType = activity.extendedProps.activity_type;
            const date = new Date(activity.start).toDateString();
            
            // Total hours
            summary.totalHours += hours;
            
            // By employee
            if (!summary.byEmployee[employee]) {
                summary.byEmployee[employee] = {
                    name: activity.extendedProps.employee_name,
                    hours: 0
                };
            }
            summary.byEmployee[employee].hours += hours;
            
            // By project
            if (project) {
                if (!summary.byProject[project]) {
                    summary.byProject[project] = {
                        name: activity.extendedProps.project_name || project,
                        hours: 0
                    };
                }
                summary.byProject[project].hours += hours;
            }
            
            // By activity type
            if (activityType) {
                if (!summary.byActivityType[activityType]) {
                    summary.byActivityType[activityType] = 0;
                }
                summary.byActivityType[activityType] += hours;
            }
            
            // Daily totals
            if (!summary.dailyTotals[date]) {
                summary.dailyTotals[date] = 0;
            }
            summary.dailyTotals[date] += hours;
        });
        
        return summary;
    },
    
    // Export to CSV
    exportToCSV: function(activities, filename = 'timesheet_details.csv') {
        const headers = [
            'Date',
            'Employee',
            'Project',
            'Task',
            'Activity Type',
            'From Time',
            'To Time',
            'Hours',
            'Description'
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
    },
    
    // Show summary dialog
    showSummaryDialog: function(activities, startDate, endDate) {
        const summary = this.generateSummary(activities, startDate, endDate);
        
        let content = `
            <div class="summary-content">
                <h5>Period Summary</h5>
                <p><strong>Total Hours:</strong> ${this.formatDuration(summary.totalHours)}</p>
                
                <h6>By Employee:</h6>
                <ul>
        `;
        
        Object.entries(summary.byEmployee).forEach(([emp, data]) => {
            content += `<li>${data.name}: ${this.formatDuration(data.hours)}</li>`;
        });
        
        content += `
                </ul>
                
                <h6>By Project:</h6>
                <ul>
        `;
        
        Object.entries(summary.byProject).forEach(([proj, data]) => {
            content += `<li>${data.name}: ${this.formatDuration(data.hours)}</li>`;
        });
        
        content += `
                </ul>
                
                <h6>By Activity Type:</h6>
                <ul>
        `;
        
        Object.entries(summary.byActivityType).forEach(([type, hours]) => {
            content += `<li>${type}: ${this.formatDuration(hours)}</li>`;
        });
        
        content += `
                </ul>
            </div>
        `;
        
        const dialog = new frappe.ui.Dialog({
            title: 'Timesheet Summary',
            fields: [
                {
                    fieldtype: 'HTML',
                    fieldname: 'summary_html',
                    options: content
                }
            ],
            primary_action_label: 'Export CSV',
            primary_action: () => {
                this.exportToCSV(activities);
                dialog.hide();
            }
        });
        
        dialog.show();
    },
    
    // Quick time presets
    getTimePresets: function() {
        const now = new Date();
        const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        
        return {
            'Morning (9-12)': {
                start: new Date(today.getTime() + 9 * 60 * 60 * 1000),
                end: new Date(today.getTime() + 12 * 60 * 60 * 1000)
            },
            'Afternoon (13-17)': {
                start: new Date(today.getTime() + 13 * 60 * 60 * 1000),
                end: new Date(today.getTime() + 17 * 60 * 60 * 1000)
            },
            'Evening (18-20)': {
                start: new Date(today.getTime() + 18 * 60 * 60 * 1000),
                end: new Date(today.getTime() + 20 * 60 * 60 * 1000)
            }
        };
    },
    
    // Local storage helpers
    saveUserPreferences: function(preferences) {
        localStorage.setItem('timesheet_calendar_prefs', JSON.stringify(preferences));
    },
    
    loadUserPreferences: function() {
        const prefs = localStorage.getItem('timesheet_calendar_prefs');
        return prefs ? JSON.parse(prefs) : {
            defaultView: 'timeGridWeek',
            defaultEmployee: frappe.session.user,
            showWeekends: true,
            slotDuration: '00:30:00'
        };
    },
    
    // Notification helpers
    showSuccess: function(message) {
        frappe.show_alert({
            message: message,
            indicator: 'green'
        }, 3);
    },
    
    showError: function(message) {
        frappe.show_alert({
            message: message,
            indicator: 'red'
        }, 5);
    },
    
    showWarning: function(message) {
        frappe.show_alert({
            message: message,
            indicator: 'orange'
        }, 4);
    }
};

// Global keyboard shortcuts
$(document).ready(function() {
    // Only apply shortcuts when on the timesheet calendar page
    if (window.location.pathname.includes('advanced_tc')) {
        $(document).keydown(function(e) {
            // Ctrl+N for new activity
            if (e.ctrlKey && e.keyCode === 78) {
                e.preventDefault();
                $('#add-activity').click();
            }
            
            // Ctrl+R for refresh
            if (e.ctrlKey && e.keyCode === 82) {
                e.preventDefault();
                if (window.currentCalendar) {
                    window.currentCalendar.refetchEvents();
                }
            }
        });
    }
});

// Extend frappe utils
if (typeof frappe !== 'undefined') {
    frappe.timesheet_calendar = window.TimesheetCalendarUtils;
}