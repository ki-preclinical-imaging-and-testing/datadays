# User Guide for PIs and Administrators

This guide is designed for Principal Investigators and Administrators who want to see clean dashboards, intuitive visualizations, and understand the downstream usability of research data organized with the Science Data Kit (SDK).

## Getting Started

### Prerequisites

Before you begin, ensure you have:
- Access to an installed instance of the Science Data Kit (SDK)
- Appropriate access permissions (admin or viewer role)
- Basic understanding of your research data structure

### First Steps

1. **Access the Dashboard**:
   ```bash
   python main.py
   ```
   This will start the Streamlit web application, accessible at http://localhost:8501

2. **Navigate to the Admin Dashboard**:
   - Click on "Admin Dashboard" in the sidebar
   - Log in with your administrator credentials if prompted

## Overview Dashboard

The Overview Dashboard provides a high-level summary of your research data ecosystem:

### Key Metrics Panel

This panel displays:
- Total number of files in the system
- Number of collections and projects
- Storage usage statistics
- Recent activity metrics
- Data completeness score

### Data Distribution Charts

Visualizations showing:
- File types distribution (pie chart)
- Data volume by project (bar chart)
- Activity timeline (line chart)
- Metadata completeness by collection (heat map)

### Quick Actions

Buttons for common administrative tasks:
- Generate reports
- Manage users
- System settings
- Backup and restore

## Project Management

### Viewing Projects

1. Navigate to "Projects" in the sidebar
2. View a list of all research projects with summary statistics
3. Click on a project to see detailed information:
   - Team members
   - Collections within the project
   - Timeline and milestones
   - Data statistics

### Managing Projects

As an administrator, you can:
1. Create new projects with the "New Project" button
2. Edit project details with the "Edit" button
3. Archive completed projects
4. Set access permissions for team members

## Data Visualization

### Interactive Dashboards

1. Navigate to "Visualizations" in the sidebar
2. Select from available dashboard templates:
   - Research Progress Dashboard
   - Data Quality Dashboard
   - Collaboration Network
   - Custom Dashboards

3. Interact with dashboards by:
   - Filtering data using dropdown menus
   - Adjusting date ranges
   - Drilling down into specific metrics
   - Exporting visualizations

### Creating Custom Dashboards

1. Click "Create Dashboard" in the Visualizations page
2. Select a layout template
3. Add visualization components:
   - Drag and drop charts, graphs, and tables
   - Configure data sources for each component
   - Set refresh intervals and filters

4. Save and share your dashboard with team members

## Knowledge Graph Exploration

### Exploring the Research Graph

1. Navigate to "Graph Explorer" in the sidebar
2. View the knowledge graph of your research data:
   - Projects as parent nodes
   - Collections as intermediate nodes
   - Files as leaf nodes
   - Relationships showing data connections

3. Use the exploration tools:
   - Zoom and pan controls
   - Search for specific entities
   - Filter by node type or property
   - Highlight paths between entities

### Insights and Patterns

1. Navigate to "Insights" in the sidebar
2. View automatically generated insights:
   - Collaboration patterns
   - Data reuse metrics
   - Methodology similarities
   - Research trends

## Reporting and Compliance

### Generating Reports

1. Navigate to "Reports" in the sidebar
2. Select from available report templates:
   - Project Progress Report
   - Data Management Compliance
   - Storage Utilization
   - User Activity

3. Configure report parameters:
   - Date range
   - Projects to include
   - Output format (PDF, Excel, etc.)

4. Generate and download the report

### Compliance Monitoring

The Compliance Dashboard shows:
- Data management policy adherence
- Metadata completeness metrics
- Backup status
- Access control audit information

## User and Access Management

### Managing Users

1. Navigate to "User Management" in the sidebar
2. View all users with their roles and permissions
3. Add new users with the "Add User" button
4. Edit user permissions with the "Edit" button
5. Deactivate users when needed

### Setting Access Policies

1. Navigate to "Access Policies" in the sidebar
2. Create and manage access rules:
   - Project-level access
   - Collection-level permissions
   - File-type restrictions
   - Role-based access controls

## System Configuration

### General Settings

1. Navigate to "Settings" in the sidebar
2. Configure system-wide settings:
   - Storage locations
   - Backup schedules
   - Email notifications
   - Integration settings

### Integration Configuration

Configure integrations with:
- Institutional repositories
- Electronic lab notebooks
- Data archives
- Authentication systems

## Best Practices for Administrators

### Data Governance

- Establish clear data management policies
- Define metadata requirements for different data types
- Create templates for common research workflows
- Regularly review data quality metrics

### Team Training

- Organize training sessions for new users
- Create custom documentation for your institution
- Highlight successful use cases
- Provide regular updates on new features

## Troubleshooting

### Common Issues

- **Dashboard loading slowly**: Check server resources and optimize queries
- **Missing data in reports**: Verify data access permissions
- **Visualization errors**: Check for incomplete metadata or schema issues

### Getting Support

- Check the [Administrator FAQ](admin_faq.md) for common questions
- Refer to the [Technical Documentation](sdk_architecture.md) for advanced topics
- Contact the Data Days team at datadays@mit.edu for assistance

---

[Back to Documentation Home](README.md) | [User Guide for Trainees](user_guide_trainees.md) | [User Guide for Tutorial Users](user_guide_tutorial.md)
