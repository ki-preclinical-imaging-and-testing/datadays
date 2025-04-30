# User Guide for Trainees

This guide is designed for trainees who are working in the thick of data and may want to simplify ease of use in aggregating information and recalculating analyses. We offer office hour workshopping of your datasets to develop protocols for handling different types of data and help curate datasets for specific uses like telling a story or updating dashboards with recalculated values.

## Getting Started

### Prerequisites

Before you begin, ensure you have:
- Installed the Science Data Kit (SDK) following the [Installation Guide](installation.md)
- Access to your research data files
- Basic understanding of your data types (images, tables, etc.)

### First Steps

1. **Launch the Application**:
   ```bash
   python main.py
   ```
   This will start the Streamlit web application, accessible at http://localhost:8501

2. **Navigate the Interface**:
   - The left sidebar contains the main navigation menu
   - The main panel displays the active tool or dashboard
   - The top bar provides access to settings and help

## Data Scanning and Organization

### Scanning Your Data

1. Navigate to the "Data Scanner" page from the sidebar
2. Click "Select Directory" and choose the folder containing your research data
3. Configure scanning options:
   - **Recursive Scan**: Enable to scan subdirectories
   - **File Types**: Select which file types to include
   - **Metadata Extraction**: Choose which metadata to extract automatically

4. Click "Start Scan" to begin the scanning process
5. Review the scan results, which will show:
   - Number of files found by type
   - Directory structure
   - Basic file metadata

### Organizing Your Data

After scanning, you can organize your data:

1. Navigate to the "Data Organization" page
2. Use the file browser to explore your scanned files
3. Create collections by:
   - Selecting files and clicking "Create Collection"
   - Naming your collection and adding a description
   - Assigning tags for easier searching

4. Organize files by:
   - Dragging and dropping into collections
   - Using filters to find specific files
   - Creating hierarchical structures

## Metadata Management

### Viewing and Editing Metadata

1. Select a file in the file browser
2. The metadata panel will display all extracted metadata
3. Edit metadata by:
   - Clicking on a field to modify its value
   - Adding new fields with the "Add Field" button
   - Removing fields with the "Remove" button next to each field

4. Save changes by clicking "Save Metadata"

### Batch Editing

For editing metadata across multiple files:

1. Select multiple files using checkboxes
2. Click "Batch Edit" to open the batch editor
3. Choose which fields to edit across all selected files
4. Apply changes and review the results

### Metadata Templates

Create templates for consistent metadata:

1. Navigate to "Metadata Templates" in the sidebar
2. Click "Create Template"
3. Define fields and default values
4. Save the template
5. Apply templates to files or collections as needed

## Knowledge Graph Interaction

### Viewing the Graph

1. Navigate to "Graph Explorer" in the sidebar
2. The graph visualization will show:
   - Files as nodes
   - Metadata as properties
   - Relationships between files and collections

3. Interact with the graph by:
   - Zooming in/out
   - Clicking nodes to see details
   - Dragging nodes to rearrange the view

### Creating Relationships

Connect related files in the graph:

1. Select a file in the graph view
2. Click "Add Relationship"
3. Select the target file and relationship type
4. Add properties to the relationship if needed
5. Click "Create" to establish the connection

## Practical Workflows

### Example: Organizing Microscopy Data

1. Scan your microscopy data directory
2. Create collections for each experiment
3. Edit metadata to add experiment details
4. Create relationships between related images
5. Generate a visualization of your experiment structure

### Example: Managing Flow Cytometry Data

1. Scan your FCS files
2. Use the metadata extractor to pull channel information
3. Create templates for consistent annotation
4. Organize files by experiment and condition
5. Visualize relationships between samples

## Exporting and Sharing

### Exporting Data

1. Navigate to "Export" in the sidebar
2. Choose what to export:
   - File listings
   - Metadata in CSV/JSON format
   - Graph data for external analysis
   - Visualizations as images

3. Configure export options and download the files

### Sharing with Collaborators

1. Export your organized data structure
2. Share the export file with collaborators
3. They can import it into their SDK installation
4. Alternatively, set up a shared Neo4j instance for real-time collaboration

## Troubleshooting

### Common Issues

- **Scan is taking too long**: Try scanning smaller directories or disabling recursive scanning
- **Metadata extraction fails**: Check if the file format is supported or try manual metadata entry
- **Graph visualization is cluttered**: Use filters to show only relevant nodes and relationships

### Getting Help

- Check the [FAQ](faq.md) for common questions
- Refer to the [Technical Documentation](sdk_architecture.md) for advanced topics
- Contact the Data Days team at datadays@mit.edu for assistance

## Next Steps

After mastering the basics:
- Explore [advanced graph queries](graph_queries.md)
- Learn about [custom metadata extractors](custom_extractors.md)
- Try the [natural language interface](nlp_interface.md)
- Attend a Data Days event to learn from experts

---

[Back to Documentation Home](README.md) | [User Guide for PIs & Administrators](user_guide_admins.md) | [User Guide for Tutorial Users](user_guide_tutorial.md)
