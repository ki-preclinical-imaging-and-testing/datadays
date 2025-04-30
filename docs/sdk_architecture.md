# SDK Architecture

This document provides a technical overview of the Science Data Kit (SDK) architecture, explaining how the different components work together to provide a comprehensive solution for research data management.

## System Overview

The Science Data Kit is built on a modular architecture with several key components:

```
+---------------------+     +---------------------+     +---------------------+
|                     |     |                     |     |                     |
|  Streamlit Frontend |<--->|    Python Backend   |<--->|    Neo4j Database   |
|                     |     |                     |     |                     |
+---------------------+     +---------------------+     +---------------------+
         ^                           ^                           ^
         |                           |                           |
         v                           v                           v
+---------------------+     +---------------------+     +---------------------+
|                     |     |                     |     |                     |
|  NeoDash Dashboards |     |     Jupyter Lab     |     |   Docker Containers |
|                     |     |                     |     |                     |
+---------------------+     +---------------------+     +---------------------+
```

## Core Components

### 1. Data Scanning and Organization (`scanner.py`)

The scanner module is responsible for:
- Recursively scanning directories for research data files
- Identifying file types and organizing them into categories
- Extracting basic file metadata (size, creation date, etc.)
- Creating file entities in the knowledge graph

Key classes:
- `FileScanner`: Main scanning engine
- `FileTypeDetector`: Identifies file types based on extensions and content
- `DirectoryIndexer`: Creates directory structure representations

### 2. Metadata Extraction (`metadata.py`)

The metadata module handles:
- Extracting metadata from various file formats
- Normalizing metadata across different sources
- Validating metadata against schemas
- Storing metadata in the knowledge graph

Supported file types:
- Images (TIFF, JPEG, PNG) with EXIF data
- Tabular data (CSV, Excel)
- Microscopy files (OME-TIFF)
- Flow cytometry data (FCS)
- Sequencing data (FASTQ, BAM)

### 3. Graph Database Interface (`graph.py`)

The graph module provides:
- Connection management to Neo4j
- Query building and execution
- Transaction management
- Schema definition and enforcement

Key components:
- `GraphConnector`: Manages database connections
- `QueryBuilder`: Constructs Cypher queries
- `SchemaManager`: Defines and enforces graph schema
- `EntityMapper`: Maps Python objects to graph entities

### 4. Natural Language Processing (`nlp.py`)

The NLP module enables:
- Natural language queries against the graph
- Query translation to Cypher
- Text extraction from documents
- Entity recognition in text

Technologies used:
- spaCy for NLP processing
- Transformers for advanced language understanding
- Custom query parsers for domain-specific language

## Web Application

The Streamlit-based web application provides:
- User authentication and session management
- Interactive data scanning and visualization
- Metadata editing and validation
- Graph exploration and querying
- Dashboard configuration

Key pages:
- Home dashboard
- Data scanner
- Metadata editor
- Graph explorer
- Query builder
- Settings and configuration

## Visualization

The visualization components include:
- NeoDash dashboards for interactive graph visualization
- Custom chart components for data visualization
- Export utilities for sharing visualizations

## Integration

Integration components enable the SDK to work with:
- Jupyter notebooks for interactive analysis
- Docker containers for deployment
- External APIs for data exchange

## Data Flow

1. **Data Ingestion**:
   - Files are scanned using the scanner module
   - Basic metadata is extracted
   - File entities are created in the graph

2. **Metadata Processing**:
   - Detailed metadata is extracted from files
   - Metadata is normalized and validated
   - Metadata entities are created and linked to files

3. **Knowledge Graph Construction**:
   - Relationships are established between entities
   - Additional context is added through user input
   - Graph schema is enforced

4. **Visualization and Analysis**:
   - Graph data is queried and visualized
   - Dashboards present insights
   - Natural language queries enable exploration

## Configuration

The SDK is configured through:
- YAML configuration files
- Environment variables
- Web-based configuration interface

## Security

Security features include:
- Authentication for web and database access
- Authorization for different user roles
- Encryption for sensitive data
- Audit logging for system activities

## Extensibility

The SDK can be extended through:
- Custom metadata extractors
- Plugin architecture for new file types
- Custom visualization components
- API integrations

## Next Steps

- Review the [Installation Guide](installation.md) for setup instructions
- Explore the [API Reference](api_reference.md) for detailed API documentation
- Check out the [Demo Workflows](../demos/README.md) to see the SDK in action

---

[Back to Documentation Home](README.md)