# Data Days Overview

## What is Data Days?

Data Days is a recurring open house initiative at the MIT Koch Institute where researchers can bring their experimental datasets (imaging, flow cytometry, histology, etc.) and learn to organize and structure them using the Science Data Kit (SDK). The program aims to help researchers manage their data more effectively, enabling better collaboration, reproducibility, and insights.

## Mission and Goals

The primary mission of Data Days is to empower researchers with tools and knowledge to transform their messy, unstructured data into organized, interconnected knowledge graphs. Our goals include:

1. **Improving Data Organization**: Help researchers organize their experimental data in a structured, searchable format
2. **Enhancing Metadata Management**: Extract and standardize metadata from various file formats
3. **Enabling Knowledge Discovery**: Create connections between datasets to reveal new insights
4. **Promoting Reproducibility**: Make research workflows more transparent and reproducible
5. **Facilitating Collaboration**: Enable easier sharing and collaboration around research data

## The Science Data Kit (SDK)

The Science Data Kit (SDK) is the core technology behind Data Days. It is a comprehensive toolkit that uses a knowledge graph model backed by Neo4j to provide:

### Key Features

- **Data Scanning and Organization**: Automatically scan and organize research files
- **Metadata Extraction**: Extract metadata from various file formats (images, spreadsheets, etc.)
- **Entity Mapping**: Map files and metadata to entities in a knowledge graph
- **Relationship Modeling**: Define and visualize relationships between research entities
- **Interactive Visualization**: Explore data through interactive dashboards
- **Natural Language Interaction**: Query and explore data using natural language

### Technical Architecture

The SDK is built on a modern technology stack:

- **Backend**: Python-based core with Neo4j graph database
- **Frontend**: Streamlit web application for intuitive user interaction
- **Visualization**: NeoDash for creating interactive dashboards
- **Integration**: Docker for containerization, Jupyter Lab for interactive analysis

## Target Audiences

Data Days and the SDK are designed to serve three primary audiences:

1. **Trainees**
   - Working in the thick of data
   - May want to simplify ease of use in aggregating information and recalculating analyses
   - Benefit from office hour workshopping of datasets to develop protocols for handling different types of data
   - Need help curating datasets for specific uses (telling a story, updating dashboards with recalculated values, etc.)

2. **Principal Investigators and Administrators**
   - Want to see the big picture of research data
   - Need clean dashboards and intuitive visualization
   - Focus on insights and downstream usability

3. **Tutorial Users**
   - Looking to learn about knowledge graph approaches to data
   - Need structured examples and documentation
   - Focus on educational aspects and best practices

## Getting Involved

There are several ways to get involved with Data Days:

- **Attend an Open House**: Bring your data to a Data Days event at MIT Koch Institute
- **Try the SDK**: Follow our [Installation Guide](installation.md) to set up the SDK
- **Contribute**: Help improve the SDK by contributing to our GitHub repository
- **Spread the Word**: Share information about Data Days with colleagues who might benefit

## Next Steps

- Learn how to [install the SDK](installation.md)
- Explore [demo workflows](../demos/README.md) to see the SDK in action
- Check out the [user guides](user_guide_trainees.md) tailored to your role
- Review the [technical documentation](sdk_architecture.md) for more details

---

[Back to Documentation Home](README.md)
