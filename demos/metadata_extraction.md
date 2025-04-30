# Metadata Extraction with Science Data Kit

This document demonstrates how to use the Science Data Kit (SDK) to extract metadata from various research file formats. We'll cover:

1. Understanding metadata in research data
2. Setting up the metadata extraction environment
3. Extracting metadata from different file types
4. Normalizing and standardizing metadata
5. Storing metadata in the knowledge graph
6. Querying and using metadata

## Prerequisites

Before following this tutorial, ensure you have:
- Installed the Science Data Kit following the [Installation Guide](../docs/installation.md)
- Completed the [Data Scanning](data_scanning.md) tutorial or have scanned files in your graph
- Access to research files with metadata (or use our provided sample data)

## 1. Understanding Metadata in Research Data

Metadata is "data about data" - information that describes your research files. Different file types contain different kinds of metadata:

- **Images**: Resolution, dimensions, color depth, acquisition parameters, microscope settings
- **Tables**: Column headers, data types, units, experimental conditions
- **Documents**: Author, creation date, keywords, sections
- **Sequence Files**: Sequencing platform, read length, quality scores, sample information

Extracting this metadata allows you to:
- Search and filter files based on their properties
- Compare experimental conditions across datasets
- Ensure data quality and consistency
- Create relationships between related files

## 2. Setting Up the Metadata Extraction Environment

First, let's set up our environment for metadata extraction:

```python
# Import required libraries
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pprint import pprint

# Add the project root to the path so we can import the SDK modules
sys.path.append('..')

# Add the science_data_kit repository (assumed to be cloned alongside this repo)
import os
science_data_kit_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath('.'))), 'science_data_kit')
if os.path.exists(science_data_kit_path):
    sys.path.append(science_data_kit_path)

# Import SDK modules
try:
    # Try importing from external science_data_kit repository first
    if os.path.exists(science_data_kit_path):
        from science_data_kit.metadata import MetadataExtractor
        from science_data_kit.graph import GraphConnector
        from science_data_kit.scanner import FileScanner
    else:
        # Fall back to internal src.sdk if external repository is not available
        from src.sdk.metadata import MetadataExtractor
        from src.sdk.graph import GraphConnector
        from src.sdk.scanner import FileScanner
except ImportError:
    # If both imports fail, raise an error
    raise ImportError("Could not import SDK modules. Please ensure either the science_data_kit repository is cloned alongside this repo or the src.sdk modules are available.")

# Connect to the Neo4j database
graph = GraphConnector(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="datadays"
)

# Initialize the metadata extractor
metadata_extractor = MetadataExtractor(graph_connector=graph)
```

## 3. Extracting Metadata from Different File Types

### Image Files (TIFF, JPEG, PNG)

Let's extract metadata from image files:

```python
# Get a list of image files from the graph
query = """
MATCH (f:File) 
WHERE f.file_type = 'image' 
RETURN f.file_id as file_id, f.path as path 
LIMIT 5
"""
image_files = graph.run_query(query)

# Extract metadata from each image file
for image in image_files:
    file_id = image.get('file_id')
    file_path = image.get('path')

    print(f"\nExtracting metadata from: {os.path.basename(file_path)}")

    # Extract metadata
    metadata = metadata_extractor.extract_from_file(file_path)

    # Display some key metadata fields
    print("Key metadata fields:")
    if metadata:
        for key in ['ImageWidth', 'ImageHeight', 'BitsPerSample', 'Make', 'Model', 'DateTime']:
            if key in metadata:
                print(f"  - {key}: {metadata[key]}")

    # Store metadata in the graph
    metadata_extractor.store_metadata(file_id, metadata)
```

### Microscopy Images (OME-TIFF)

For microscopy images, we can extract more specialized metadata:

```python
# Extract metadata from OME-TIFF files
query = """
MATCH (f:File) 
WHERE f.path ENDS WITH '.ome.tiff' OR f.path ENDS WITH '.ome.tif' 
RETURN f.file_id as file_id, f.path as path 
LIMIT 3
"""
ome_files = graph.run_query(query)

for ome_file in ome_files:
    file_id = ome_file.get('file_id')
    file_path = ome_file.get('path')

    print(f"\nExtracting OME metadata from: {os.path.basename(file_path)}")

    # Extract OME metadata (uses specialized extractor)
    metadata = metadata_extractor.extract_from_ome_tiff(file_path)

    # Display microscopy-specific metadata
    print("Microscopy metadata:")
    if metadata:
        for key in ['Microscope', 'Objective', 'PhysicalSizeX', 'PhysicalSizeY', 'Channel', 'AcquisitionDate']:
            if key in metadata:
                print(f"  - {key}: {metadata[key]}")

    # Store metadata in the graph
    metadata_extractor.store_metadata(file_id, metadata)
```

### Tabular Data (CSV, Excel)

For tabular data, we can extract column information and summary statistics:

```python
# Extract metadata from tabular files
query = """
MATCH (f:File) 
WHERE f.file_type = 'table' 
RETURN f.file_id as file_id, f.path as path 
LIMIT 3
"""
table_files = graph.run_query(query)

for table_file in table_files:
    file_id = table_file.get('file_id')
    file_path = table_file.get('path')

    print(f"\nExtracting table metadata from: {os.path.basename(file_path)}")

    # Extract table metadata
    metadata = metadata_extractor.extract_from_table(file_path)

    # Display table metadata
    print("Table metadata:")
    if metadata:
        print(f"  - Columns: {metadata.get('columns', [])}")
        print(f"  - Rows: {metadata.get('row_count', 0)}")
        print(f"  - Data types: {metadata.get('column_types', {})}")

        # Show summary statistics for numeric columns
        if 'summary_stats' in metadata:
            print("  - Summary statistics:")
            for col, stats in metadata['summary_stats'].items():
                print(f"    - {col}: min={stats['min']}, max={stats['max']}, mean={stats['mean']}")

    # Store metadata in the graph
    metadata_extractor.store_metadata(file_id, metadata)
```

### Flow Cytometry Data (FCS)

For flow cytometry data, we can extract channel and marker information:

```python
# Extract metadata from FCS files
query = """
MATCH (f:File) 
WHERE f.path ENDS WITH '.fcs' 
RETURN f.file_id as file_id, f.path as path 
LIMIT 3
"""
fcs_files = graph.run_query(query)

for fcs_file in fcs_files:
    file_id = fcs_file.get('file_id')
    file_path = fcs_file.get('path')

    print(f"\nExtracting FCS metadata from: {os.path.basename(file_path)}")

    # Extract FCS metadata
    metadata = metadata_extractor.extract_from_fcs(file_path)

    # Display FCS metadata
    print("FCS metadata:")
    if metadata:
        print(f"  - Channels: {len(metadata.get('channels', []))}")
        print(f"  - Events: {metadata.get('event_count', 0)}")
        print(f"  - Cytometer: {metadata.get('cytometer', 'Unknown')}")

        # Show channel information
        if 'channels' in metadata and len(metadata['channels']) > 0:
            print("  - Channel details:")
            for i, channel in enumerate(metadata['channels'][:3]):  # Show first 3 channels
                print(f"    - Channel {i+1}: {channel.get('name')} - {channel.get('marker', 'Unknown')}")

    # Store metadata in the graph
    metadata_extractor.store_metadata(file_id, metadata)
```

## 4. Normalizing and Standardizing Metadata

Metadata from different sources often needs to be normalized for consistency:

```python
# Function to normalize metadata across different file types
def normalize_metadata(metadata, file_type):
    normalized = {}

    # Common fields for all file types
    if 'creation_date' in metadata:
        normalized['creation_date'] = metadata['creation_date']
    if 'modified_date' in metadata:
        normalized['modified_date'] = metadata['modified_date']

    # File type specific normalization
    if file_type == 'image':
        # Normalize image dimensions
        if 'ImageWidth' in metadata and 'ImageHeight' in metadata:
            normalized['dimensions'] = f"{metadata['ImageWidth']}x{metadata['ImageHeight']}"
        elif 'width' in metadata and 'height' in metadata:
            normalized['dimensions'] = f"{metadata['width']}x{metadata['height']}"

        # Normalize bit depth
        if 'BitsPerSample' in metadata:
            normalized['bit_depth'] = metadata['BitsPerSample']
        elif 'bit_depth' in metadata:
            normalized['bit_depth'] = metadata['bit_depth']

    elif file_type == 'table':
        # Normalize row and column counts
        if 'row_count' in metadata:
            normalized['row_count'] = metadata['row_count']
        if 'columns' in metadata:
            normalized['column_count'] = len(metadata['columns'])

    return normalized

# Example of normalizing metadata for different file types
file_types = ['image', 'table', 'document']
for file_type in file_types:
    query = f"""
    MATCH (f:File)-[:HAS_METADATA]->(m:Metadata)
    WHERE f.file_type = '{file_type}'
    RETURN f.file_id as file_id, f.path as path, m as metadata
    LIMIT 2
    """

    results = graph.run_query(query)

    for result in results:
        file_id = result.get('file_id')
        file_path = result.get('path')
        metadata = result.get('metadata')

        if metadata:
            print(f"\nNormalizing metadata for: {os.path.basename(file_path)}")

            # Convert Neo4j node to dictionary
            metadata_dict = dict(metadata)

            # Normalize the metadata
            normalized = normalize_metadata(metadata_dict, file_type)

            print("Original metadata keys:", list(metadata_dict.keys())[:5], "...")
            print("Normalized metadata:", normalized)

            # Store normalized metadata
            metadata_extractor.store_normalized_metadata(file_id, normalized)
```

## 5. Storing Metadata in the Knowledge Graph

Let's look at how metadata is stored in the knowledge graph and how to add custom metadata:

```python
# Add custom metadata to a file
def add_custom_metadata(graph, file_id, custom_metadata):
    # Create a transaction
    with graph.driver.session() as session:
        result = session.run("""
        MATCH (f:File {file_id: $file_id})
        MERGE (f)-[:HAS_CUSTOM_METADATA]->(c:CustomMetadata)
        SET c += $metadata
        RETURN f.path as path, c as custom_metadata
        """, file_id=file_id, metadata=custom_metadata)

        record = result.single()
        if record:
            return {
                'path': record['path'],
                'custom_metadata': dict(record['custom_metadata'])
            }
        return None

# Example: Add experimental metadata to a file
file_query = """
MATCH (f:File) 
WHERE f.file_type = 'image' 
RETURN f.file_id as file_id, f.path as path 
LIMIT 1
"""
file = graph.run_query(file_query).single()

if file:
    file_id = file.get('file_id')
    file_path = file.get('path')

    # Custom experimental metadata
    experimental_metadata = {
        'experiment_id': 'EXP-2023-001',
        'sample_id': 'SAMPLE-A1',
        'treatment': 'Control',
        'concentration': '0 µM',
        'incubation_time': '24h',
        'researcher': 'Jane Doe',
        'notes': 'Baseline measurement for experiment series'
    }

    print(f"\nAdding custom metadata to: {os.path.basename(file_path)}")
    result = add_custom_metadata(graph, file_id, experimental_metadata)

    if result:
        print("Custom metadata added successfully:")
        pprint(result['custom_metadata'])
```

## 6. Querying and Using Metadata

Now let's see how to query and use the metadata we've extracted:

```python
# Find all files with specific metadata properties
def find_files_by_metadata(graph, metadata_criteria):
    query_parts = []
    for key, value in metadata_criteria.items():
        query_parts.append(f"m.{key} = '{value}'")

    metadata_conditions = " AND ".join(query_parts)

    query = f"""
    MATCH (f:File)-[:HAS_METADATA]->(m:Metadata)
    WHERE {metadata_conditions}
    RETURN f.file_id as file_id, f.path as path, f.file_type as file_type
    """

    return graph.run_query(query)

# Example: Find all images with specific dimensions
image_criteria = {
    'dimensions': '1024x768'
}

print("\nFinding images with specific dimensions:")
matching_images = find_files_by_metadata(graph, image_criteria)
for image in matching_images:
    print(f"  - {os.path.basename(image.get('path'))}")

# Find files by custom metadata
def find_files_by_custom_metadata(graph, metadata_criteria):
    query_parts = []
    for key, value in metadata_criteria.items():
        query_parts.append(f"c.{key} = '{value}'")

    metadata_conditions = " AND ".join(query_parts)

    query = f"""
    MATCH (f:File)-[:HAS_CUSTOM_METADATA]->(c:CustomMetadata)
    WHERE {metadata_conditions}
    RETURN f.file_id as file_id, f.path as path, f.file_type as file_type
    """

    return graph.run_query(query)

# Example: Find all files from a specific experiment
experiment_criteria = {
    'experiment_id': 'EXP-2023-001',
    'treatment': 'Control'
}

print("\nFinding files from a specific experiment:")
experiment_files = find_files_by_custom_metadata(graph, experiment_criteria)
for file in experiment_files:
    print(f"  - {os.path.basename(file.get('path'))}")
```

### Visualizing Metadata Relationships

We can visualize how files are connected through their metadata:

```python
# Visualize metadata relationships
def visualize_metadata_relationships(graph, central_file_id):
    try:
        import networkx as nx
        import matplotlib.pyplot as plt

        # Query to get the file and its metadata relationships
        query = """
        MATCH (f:File {file_id: $file_id})-[r1]->(m)
        OPTIONAL MATCH (f2:File)-[r2]->(m)
        WHERE f2 <> f
        RETURN f.path as source_path, type(r1) as relationship, 
               m as metadata_node, f2.path as related_path
        """

        result = graph.run_query(query, file_id=central_file_id)

        # Create a directed graph
        G = nx.DiGraph()

        # Add central file node
        central_file = None

        # Process query results
        for record in result:
            source_path = os.path.basename(record.get('source_path', ''))
            relationship = record.get('relationship', '')
            metadata_node = record.get('metadata_node', {})
            related_path = record.get('related_path')

            if not central_file:
                central_file = source_path

            # Add nodes and edges
            if source_path and not G.has_node(source_path):
                G.add_node(source_path, node_type='file')

            # Create a label for the metadata node
            if metadata_node:
                metadata_type = list(metadata_node.labels)[0] if hasattr(metadata_node, 'labels') else 'Metadata'
                metadata_id = f"{metadata_type}_{len(G.nodes)}"

                # Add metadata node with some key properties as label
                metadata_props = dict(metadata_node)
                metadata_label = metadata_type
                if len(metadata_props) > 0:
                    # Get first property as part of the label
                    first_key = list(metadata_props.keys())[0]
                    metadata_label += f": {first_key}={metadata_props[first_key]}"

                G.add_node(metadata_id, node_type='metadata', label=metadata_label)
                G.add_edge(source_path, metadata_id, label=relationship)

            # Add related file if it exists
            if related_path:
                related_name = os.path.basename(related_path)
                if not G.has_node(related_name):
                    G.add_node(related_name, node_type='related_file')

                if metadata_node:
                    G.add_edge(metadata_id, related_name, label='shared_with')

        # Set up the plot
        plt.figure(figsize=(12, 8))

        # Create layout
        pos = nx.spring_layout(G, seed=42)

        # Draw nodes with different colors based on type
        file_nodes = [n for n, attr in G.nodes(data=True) if attr.get('node_type') == 'file']
        metadata_nodes = [n for n, attr in G.nodes(data=True) if attr.get('node_type') == 'metadata']
        related_nodes = [n for n, attr in G.nodes(data=True) if attr.get('node_type') == 'related_file']

        nx.draw_networkx_nodes(G, pos, nodelist=file_nodes, node_color='lightblue', node_size=2000)
        nx.draw_networkx_nodes(G, pos, nodelist=metadata_nodes, node_color='lightgreen', node_size=1500)
        nx.draw_networkx_nodes(G, pos, nodelist=related_nodes, node_color='lightcoral', node_size=1500)

        # Draw edges
        nx.draw_networkx_edges(G, pos, width=1.5, arrowsize=15)

        # Draw labels
        file_labels = {n: n for n in file_nodes}
        related_labels = {n: n for n in related_nodes}
        metadata_labels = {n: G.nodes[n].get('label', n) for n in metadata_nodes}

        nx.draw_networkx_labels(G, pos, labels=file_labels, font_size=10)
        nx.draw_networkx_labels(G, pos, labels=related_labels, font_size=8)
        nx.draw_networkx_labels(G, pos, labels=metadata_labels, font_size=8)

        # Draw edge labels
        edge_labels = {(u, v): G.edges[u, v].get('label', '') for u, v in G.edges()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

        plt.title(f'Metadata Relationships for {central_file}')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    except ImportError as e:
        print(f"Could not visualize graph: {e}")
        print("Please install networkx: pip install networkx")

# Example: Visualize metadata relationships for a file
if file:
    print("\nVisualizing metadata relationships:")
    visualize_metadata_relationships(graph, file_id)
```

## Summary

In this tutorial, we've demonstrated how to:

1. Extract metadata from various file types (images, tables, microscopy data, flow cytometry data)
2. Normalize and standardize metadata across different sources
3. Store metadata in the knowledge graph
4. Add custom experimental metadata
5. Query files based on their metadata properties
6. Visualize metadata relationships between files

Metadata extraction is a crucial step in organizing research data, as it provides the foundation for creating meaningful connections between files and enables powerful search and analysis capabilities.

## Next Steps

To continue exploring the Science Data Kit, check out these additional tutorials:

- [Entity Mapping](entity_mapping.md): Map files and metadata to entities in the knowledge graph
- [Graph Queries](graph_queries.md): Write and execute queries against the knowledge graph
- [Visualization](data_visualization.md): Create interactive visualizations of your research data
