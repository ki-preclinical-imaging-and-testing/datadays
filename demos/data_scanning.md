# Data Scanning and Organization with Science Data Kit

This document demonstrates how to use the Science Data Kit (SDK) to scan and organize research data files. We'll cover:

1. Setting up the SDK environment
2. Scanning directories for research data
3. Organizing files by type and metadata
4. Creating collections and relationships
5. Visualizing the file organization

## Prerequisites

Before following this tutorial, ensure you have:
- Installed the Science Data Kit following the [Installation Guide](../docs/installation.md)
- Started the Neo4j database
- Access to some sample research data files (or use our provided sample data)

## 1. Setting Up the Environment

First, we need to import the required libraries and set up our environment:

```python
# Import required libraries
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
        from science_data_kit.scanner import FileScanner
        from science_data_kit.graph import GraphConnector
        from science_data_kit.metadata import MetadataExtractor
    else:
        # Fall back to internal src.sdk if external repository is not available
        from src.sdk.scanner import FileScanner
        from src.sdk.graph import GraphConnector
        from src.sdk.metadata import MetadataExtractor
except ImportError:
    # If both imports fail, raise an error
    raise ImportError("Could not import SDK modules. Please ensure either the science_data_kit repository is cloned alongside this repo or the src.sdk modules are available.")

# Set up plotting
%matplotlib inline
plt.style.use('ggplot')
sns.set(style="whitegrid")
```

### Connect to the Neo4j Database

Next, we'll connect to the Neo4j database:

```python
# Initialize the graph connector
graph = GraphConnector(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="datadays"
)

# Test the connection
if graph.test_connection():
    print("✅ Successfully connected to Neo4j database")
else:
    print("❌ Failed to connect to Neo4j database")
    print("Please ensure Neo4j is running and check your credentials")
```

### Download Sample Data (Optional)

If you don't have your own research data to work with, you can use our sample dataset:

```python
# Function to download and extract sample data
def get_sample_data(force_download=False):
    import requests
    import zipfile
    from pathlib import Path

    sample_dir = Path("./sample_data")

    # Check if sample data already exists
    if sample_dir.exists() and not force_download:
        print(f"Sample data already exists at {sample_dir}")
        return sample_dir

    # Create directory if it doesn't exist
    sample_dir.mkdir(exist_ok=True)

    # URL for sample data
    url = "https://github.com/mit-koch/datadays-samples/raw/main/research_data_sample.zip"

    print(f"Downloading sample data from {url}...")
    response = requests.get(url)

    if response.status_code == 200:
        zip_path = sample_dir / "sample_data.zip"
        with open(zip_path, 'wb') as f:
            f.write(response.content)

        print(f"Extracting sample data to {sample_dir}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(sample_dir)

        # Remove the zip file
        zip_path.unlink()

        print("✅ Sample data downloaded and extracted successfully")
    else:
        print(f"❌ Failed to download sample data: {response.status_code}")

    return sample_dir

# Download sample data
sample_data_dir = get_sample_data()
```

## 2. Scanning Directories for Research Data

Now we'll use the FileScanner to scan a directory for research data files:

```python
# Initialize the file scanner
scanner = FileScanner(graph_connector=graph)

# Set the directory to scan
# You can replace this with your own data directory
scan_dir = sample_data_dir

# Configure scanning options
scan_options = {
    "recursive": True,  # Scan subdirectories
    "file_types": ["image", "table", "document", "sequence"],  # Types of files to scan for
    "exclude_patterns": [".git", "__pycache__", ".ipynb_checkpoints"],  # Patterns to exclude
    "extract_basic_metadata": True  # Extract basic metadata during scan
}

# Perform the scan
print(f"Scanning directory: {scan_dir}")
scan_results = scanner.scan_directory(scan_dir, **scan_options)

# Display scan summary
print("\nScan Summary:")
print(f"Total files found: {len(scan_results['files'])}")
print("Files by type:")
for file_type, count in scan_results['file_type_counts'].items():
    print(f"  - {file_type}: {count}")
```

### Visualize File Type Distribution

We can visualize the distribution of file types:

```python
# Create a pie chart of file types
file_types = scan_results['file_type_counts']

plt.figure(figsize=(10, 6))
plt.pie(
    file_types.values(), 
    labels=file_types.keys(),
    autopct='%1.1f%%',
    startangle=90,
    shadow=True
)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
plt.title('File Type Distribution')
plt.show()
```

## 3. Organizing Files by Type and Metadata

Now that we've scanned the files, let's organize them based on their types and metadata:

```python
# Convert scan results to a DataFrame for easier manipulation
files_df = pd.DataFrame(scan_results['files'])

# Display the first few rows
files_df.head()
```

We can analyze the directory structure:

```python
# Group files by directory
directory_counts = files_df['directory'].value_counts()

# Plot the top 10 directories by file count
plt.figure(figsize=(12, 6))
directory_counts.head(10).plot(kind='barh')
plt.title('Top 10 Directories by File Count')
plt.xlabel('Number of Files')
plt.ylabel('Directory')
plt.tight_layout()
plt.show()
```

### Analyze File Metadata

Let's look at some basic metadata that was extracted during the scan:

```python
# Extract file sizes and convert to MB for better visualization
files_df['size_mb'] = files_df['size_bytes'] / (1024 * 1024)

# Group by file type and calculate statistics
size_stats = files_df.groupby('file_type')['size_mb'].agg(['count', 'min', 'max', 'mean', 'sum'])
size_stats = size_stats.sort_values('sum', ascending=False)

# Display the statistics
print("File Size Statistics by Type (in MB):")
size_stats
```

We can visualize the file size distribution:

```python
# Visualize file size distribution by type
plt.figure(figsize=(12, 6))
sns.boxplot(x='file_type', y='size_mb', data=files_df)
plt.title('File Size Distribution by Type')
plt.xlabel('File Type')
plt.ylabel('Size (MB)')
plt.yscale('log')  # Log scale for better visualization of wide ranges
plt.tight_layout()
plt.show()
```

## 4. Creating Collections and Relationships

Now let's organize our files into collections and establish relationships between them:

```python
# Create a collection for each experiment in our sample data
def create_collections_from_directories(scanner, files_df):
    # Group files by their parent directory (assuming each directory is an experiment)
    experiments = files_df['directory'].unique()

    collections = []
    for exp_dir in experiments:
        # Get the experiment name from the directory path
        exp_name = os.path.basename(exp_dir)

        # Skip if the directory name is not meaningful
        if exp_name in ['', '.', '..']:
            continue

        # Get files in this directory
        dir_files = files_df[files_df['directory'] == exp_dir]

        # Create a collection for this experiment
        collection = scanner.create_collection(
            name=f"Experiment: {exp_name}",
            description=f"Files from the {exp_name} experiment",
            file_ids=dir_files['file_id'].tolist()
        )

        collections.append(collection)
        print(f"Created collection '{collection['name']}' with {len(dir_files)} files")

    return collections

# Create collections
collections = create_collections_from_directories(scanner, files_df)
```

### Create Relationships Between Collections

Now let's establish relationships between collections based on common metadata or file types:

```python
# Function to create relationships between collections
def create_collection_relationships(graph, collections):
    # For this example, we'll create simple relationships based on collection names
    # In a real scenario, you might use more sophisticated criteria

    relationships = []

    # Create a simple sequence relationship between collections
    for i in range(len(collections) - 1):
        source = collections[i]
        target = collections[i + 1]

        # Create a relationship
        rel = graph.create_relationship(
            source_id=source['collection_id'],
            target_id=target['collection_id'],
            relationship_type="FOLLOWED_BY",
            properties={
                "description": f"Sequence relationship from {source['name']} to {target['name']}"
            }
        )

        relationships.append(rel)
        print(f"Created relationship: {source['name']} FOLLOWED_BY {target['name']}")

    return relationships

# Create relationships between collections
if len(collections) > 1:
    relationships = create_collection_relationships(graph, collections)
else:
    print("Not enough collections to create relationships")
```

## 5. Visualizing the File Organization

Finally, let's visualize our file organization structure using a graph visualization:

```python
# Function to visualize the graph structure
def visualize_graph(graph):
    try:
        import networkx as nx
        from networkx.drawing.nx_agraph import graphviz_layout

        # Query the graph to get collections and their relationships
        query = """
        MATCH (c:Collection)
        OPTIONAL MATCH (c)-[r]->(c2:Collection)
        RETURN c.name as source, c2.name as target, type(r) as relationship
        """

        result = graph.run_query(query)

        # Create a directed graph
        G = nx.DiGraph()

        # Add nodes and edges
        for record in result:
            source = record.get('source')
            target = record.get('target')
            relationship = record.get('relationship')

            if source and not G.has_node(source):
                G.add_node(source)

            if source and target and relationship:
                G.add_edge(source, target, label=relationship)

        # Set up the plot
        plt.figure(figsize=(12, 8))

        # Use graphviz for layout if available, otherwise use spring layout
        try:
            pos = graphviz_layout(G, prog='dot')
        except:
            pos = nx.spring_layout(G, seed=42)

        # Draw the graph
        nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='lightblue')
        nx.draw_networkx_edges(G, pos, width=2, arrowsize=20)
        nx.draw_networkx_labels(G, pos, font_size=10)

        # Draw edge labels
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.title('Collection Relationships')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    except ImportError as e:
        print(f"Could not visualize graph: {e}")
        print("Please install networkx and graphviz: pip install networkx graphviz pygraphviz")

# Visualize the graph
visualize_graph(graph)
```

## Summary

In this tutorial, we've demonstrated how to:

1. Set up the SDK environment and connect to Neo4j
2. Scan directories for research data files
3. Analyze and visualize file distributions and metadata
4. Create collections to organize files
5. Establish relationships between collections
6. Visualize the resulting organization structure

This workflow provides a foundation for organizing research data in a structured, graph-based format that can be easily queried, visualized, and shared.

## Next Steps

To continue exploring the Science Data Kit, check out these additional tutorials:

- [Metadata Extraction](metadata_extraction.md): Learn how to extract detailed metadata from various file formats
- [Entity Mapping](entity_mapping.md): Map files and metadata to entities in the knowledge graph
- [Graph Queries](graph_queries.md): Write and execute queries against the knowledge graph
- [Visualization](data_visualization.md): Create interactive visualizations of your research data
