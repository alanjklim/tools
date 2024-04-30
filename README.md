### Dashboard Layout Design

#### 1. Summary View
- **KPI Indicators**: Place Key Performance Indicators (KPIs) at the top of the dashboard for quick reference. These should include:
  - Total Jobs
  - Successful Runs
  - Failed Runs
  - Running Jobs
  - Skipped and Not Ready Jobs

#### 2. Job Status and Overview
- **Job Status Pie Chart**: Display a pie chart to show the distribution of job statuses (Running, Successful, Failed, Not Ready, Skipped).
- **Heat Map or Color-Coded Grid**: Use a grid or heat map to represent the status of each job, with colors indicating the job status (e.g., red for failed, green for success).

#### 3. Detailed Job Metrics and Execution Data
- **Detailed Table**: Use a detailed table to show job information such as ETL ID, Load Details, System, Job Status, Schedule, Load Type, Business Date, Last Success Date, Last Failed Date, Execution Time, SLA Breach Time.
  - Allow sorting and filtering by columns to drill down into specific data.
- **Gantt Chart for Execution Timeline**: Provide a Gantt chart to visualize the duration of each job relative to its scheduled time.

#### 4. Trends and Historical Data
- **Line or Bar Charts**: Implement line or bar charts to show trends over time, such as job duration and success/failure rates.
  - Filter options by date range to view historical performance.

#### 5. Resource Utilization and SLA Monitoring
- **Resource Utilization Graphs**: Graphs to show data volume, CPU, and memory usage if available.
- **SLA Compliance Chart**: A chart to show jobs meeting SLA deadlines versus those breaching them.

#### 6. Notifications and Alerts Panel
- **Alerts Section**: Include a section to display recent alerts or issues that need attention.
  - Implement clickable links or buttons to take users directly to detailed error logs or warning messages.

#### 7. Filters for Customized Viewing
- **Interactive Filters**: Allow users to filter the dashboard based on various criteria like system, schedule, load type, date range, etc. This will enable users to view specific segments of data that are most relevant to them.

#### 8. Drill-Down Capability
- **Drill-Down Features**: Implement drill-down features on charts and tables. Users can click on a particular job in the summary view to see detailed execution logs, attempt details, and error messages related to that job.

### Design Considerations
- **Responsiveness and Load Time**: Ensure the dashboard is optimized for performance, especially when dealing with large datasets.
- **User Experience**: Design the dashboard to be intuitive and easy to navigate, with clear labels, legends, and instructions.
- **Security and Access Controls**: Set up appropriate security measures to ensure that users can only access data they are authorized to view.

```
+-----------------------------------------------------------------------------+
|                            Database Load Dashboard                          |
+-----------------------------------------------------------------------------+
| +-----------+ +-----------+ +-----------+ +-----------+ +-----------+      |
| | Total Jobs| | Successful| |   Failed  | |  Running  | |   Skipped |      |
| |           | |   Runs    | |   Runs    | |   Jobs    | | and Not   |      |
| |   120     | |    95     | |    20     | |     5     | |   Ready   |      |
| +-----------+ +-----------+ +-----------+ +-----------+ +-----------+      |
+-----------------------------------------------------------------------------+
| +-----------------------+ +-----------------------+                         |
| | Job Status Pie Chart  | | SLA Compliance Chart  |                         |
| |                       | |                       |                         |
| |     (Pie Chart)       | |     (Bar Chart)       |                         |
| +-----------------------+ +-----------------------+                         |
+-----------------------------------------------------------------------------+
| +-------------------------------------------------------------------------+ |
| |                           Job Status Heat Map                           | |
| |                (Color-coded grid for quick status overview)             | |
| +-------------------------------------------------------------------------+ |
+-----------------------------------------------------------------------------+
| +-------------------------+ +---------------------------------------------+ |
| | Inactive Jobs Last 3    | |                  Detailed Table              | |
| | Days (List/Table)       | | ETL ID | Status | Execution Time | Last Run | |
| |                         | |                                             | |
| | (Marked as 'YES')       | +---------------------------------------------+ |
| +-------------------------+ | Filter: [System] [Job Status] [Date Range]   | |
+-----------------------------------------------------------------------------+
| +---------------------------------+ +-------------------------------------+ |
| |    Execution Timeline (Gantt)   | |   Historical Trends (Line Chart)   | |
| |                                 | |                                     | |
| +---------------------------------+ +-------------------------------------+ |
+-----------------------------------------------------------------------------+
| +-------------------+ +-------------------+ +-----------------------------+ |
| | Recent Alerts     | | Resource Utilization | | Detailed Error Logs         | |
| | (Notifications)  | | (Graphs)            | | (Clickable for more info)   | |
| +-------------------+ +-------------------+ +-----------------------------+ |
+-----------------------------------------------------------------------------+
```

### Key Additions:
- **Inactive Jobs Last 3 Days**:
  - This section will list all jobs marked as 'YES' under the `is_inactive_for_3_days` flag from your SQL query.
  - It could be presented as a simple list or a more detailed table depending on the amount of information you want to display (e.g., ETL ID, Last Run Date, System, Load Details).
  - This panel should ideally be interactive, allowing users to click on a job to see more detailed metrics or reasons for inactivity.

### Benefits of the Addition:
- **Proactive Monitoring**: Quickly identify jobs that have not been executed as planned, which can be critical for operations depending on timely data loads.
- **Troubleshooting and Maintenance**: Easier identification and access to jobs that may require reconfiguration, investigation, or rerunning.
- **Resource Optimization**: Helps in assessing if there are any resources being underutilized or if there are potential scheduling improvements.
