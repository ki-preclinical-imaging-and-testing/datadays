# User Guide for Tutorial Users

This guide is designed for tutorial users who are looking to learn about knowledge graph approaches to research data management through structured examples and documentation.

## Getting Started

### Prerequisites

Before you begin, ensure you have:
- Installed the Science Data Kit (SDK) following the [Installation Guide](installation.md)
- Basic familiarity with Python (helpful but not required)
- Interest in knowledge graph concepts and data organization

### Learning Path Overview

This guide offers a structured learning path:

1. **Fundamentals**: Understanding the core concepts
2. **Hands-on Tutorials**: Step-by-step guided exercises
3. **Example Projects**: Complete example workflows
4. **Advanced Topics**: Specialized techniques and customization

## Fundamentals

### Knowledge Graph Concepts

Start by understanding the basic concepts:

1. Read the [Knowledge Graph Introduction](knowledge_graph_intro.md)
2. Review the [SDK Architecture](sdk_architecture.md) document
3. Explore the [Data Model Overview](data_model.md)

### Core Components

Familiarize yourself with the main components:

1. **Data Scanner**: How files are discovered and indexed
2. **Metadata Extraction**: How information is pulled from files
3. **Graph Database**: How Neo4j stores and queries data
4. **Visualization Tools**: How to explore and present data

## Hands-on Tutorials

### Tutorial 1: Your First Knowledge Graph

Follow this step-by-step tutorial to create your first knowledge graph:

1. Navigate to the "Tutorials" section in the sidebar
2. Select "Tutorial 1: First Knowledge Graph"
3. Follow the guided instructions to:
   - Scan a sample dataset
   - Extract basic metadata
   - Create a simple graph
   - Visualize the results

### Tutorial 2: Metadata and Relationships

Build on your knowledge with more advanced metadata handling:

1. Navigate to "Tutorial 2: Metadata and Relationships"
2. Follow the guided instructions to:
   - Extract detailed metadata from files
   - Create custom metadata fields
   - Define relationships between entities
   - Query related data

### Tutorial 3: Visualization and Dashboards

Learn to create effective visualizations:

1. Navigate to "Tutorial 3: Visualization and Dashboards"
2. Follow the guided instructions to:
   - Create a basic dashboard
   - Add different visualization components
   - Configure interactive filters
   - Share your dashboard

## Example Projects

### Example 1: Microscopy Data Organization

A complete workflow for organizing microscopy data:

1. Navigate to "Examples" in the sidebar
2. Select "Microscopy Data Organization"
3. The example demonstrates:
   - Scanning microscopy image files
   - Extracting instrument and acquisition metadata
   - Organizing by experiment and sample
   - Creating a microscopy-specific dashboard

### Example 2: Flow Cytometry Analysis

A workflow for managing flow cytometry data:

1. Select "Flow Cytometry Analysis" from the Examples
2. The example demonstrates:
   - Working with FCS files
   - Extracting channel and marker information
   - Organizing by panel and sample
   - Visualizing experiment structure

### Example 3: Multi-omics Integration

An advanced example showing integration of multiple data types:

1. Select "Multi-omics Integration" from the Examples
2. The example demonstrates:
   - Combining imaging, sequencing, and proteomics data
   - Creating relationships across data types
   - Building integrated visualizations
   - Querying across the integrated dataset

## Jupyter Notebook Tutorials

For a more interactive learning experience, explore our Jupyter notebooks:

1. Navigate to the [Jupyter Tutorials](../demos/README.md) section
2. Launch Jupyter Lab from the SDK:
   ```bash
   python -m src.integration.jupyter.launch
   ```
3. Open the introductory notebooks in order:
   - `01_introduction.ipynb`
   - `02_data_scanning.ipynb`
   - `03_metadata_extraction.ipynb`
   - `04_graph_creation.ipynb`
   - `05_visualization.ipynb`

## Advanced Topics

Once you're comfortable with the basics, explore these advanced topics:

### Custom Metadata Extractors

Learn to create custom extractors for specialized file formats:

1. Read the [Custom Extractors Guide](custom_extractors.md)
2. Follow the tutorial to create a simple extractor
3. Explore the example extractors in the codebase

### Advanced Graph Queries

Master the Cypher query language for powerful data exploration:

1. Read the [Cypher Query Guide](cypher_queries.md)
2. Practice with the interactive query builder
3. Try the example queries provided in the documentation

### Integration with External Tools

Learn to connect the SDK with other research tools:

1. Explore the [Integration Guide](integration_guide.md)
2. Follow tutorials for common integrations:
   - Electronic Lab Notebooks
   - Analysis Pipelines
   - Data Repositories

## Learning Resources

### Reference Materials

- [Neo4j Documentation](https://neo4j.com/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)

### Community Resources

- Join the [Data Days Community Forum](https://community.datadays.mit.edu)
- Attend virtual or in-person [Data Days events](../outreach/events.md)
- Contribute to the [SDK on GitHub](https://github.com/mit-koch/datadays)

## Creating Your Own Tutorials

Once you've mastered the SDK, you might want to create tutorials for your team:

1. Read the [Tutorial Creation Guide](tutorial_creation.md)
2. Use the tutorial template provided
3. Share your tutorials with the community

## Troubleshooting

If you encounter issues during the tutorials:

- Check the [Tutorial FAQ](tutorial_faq.md)
- Look for the "Help" button in each tutorial
- Reset the tutorial data with the "Reset" button
- Contact the Data Days team at datadays@mit.edu

---

[Back to Documentation Home](README.md) | [User Guide for Trainees](user_guide_trainees.md) | [User Guide for PIs & Administrators](user_guide_admins.md)
