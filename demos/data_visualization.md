# Data Visualization with Science Data Kit

This document demonstrates how to use the Science Data Kit (SDK) to create interactive visualizations of research data and knowledge graphs. We'll cover:

1. Understanding visualization options in the SDK
2. Setting up the visualization environment
3. Creating basic graph visualizations
4. Building interactive dashboards with NeoDash
5. Customizing visualizations for different audiences
6. Exporting and sharing visualizations

## Prerequisites

Before following this tutorial, ensure you have:
- Installed the Science Data Kit following the [Installation Guide](../docs/installation.md)
- Completed the [Data Scanning](data_scanning.md) and [Metadata Extraction](metadata_extraction.md) tutorials
- A Neo4j database populated with research data and metadata

## 1. Understanding Visualization Options in the SDK

The Science Data Kit offers several visualization approaches:

- **Graph Visualizations**: Explore the structure of your knowledge graph
- **NeoDash Dashboards**: Create interactive dashboards with multiple visualization components
- **Matplotlib/Seaborn Charts**: Generate static visualizations of data distributions and relationships
- **Interactive Jupyter Notebooks**: Combine code, visualizations, and narrative in a single document

Each approach has its strengths:

| Visualization Type | Best For | Audience |
|-------------------|----------|----------|
| Graph Visualizations | Exploring relationships | Data analysts, researchers |
| NeoDash Dashboards | Summarizing insights, monitoring | PIs, administrators |
| Static Charts | Publication, documentation | All audiences |
| Jupyter Notebooks | Analysis, teaching | Trainees |

## 2. Setting Up the Visualization Environment

First, let's set up our environment for visualization:

```python
# Import required libraries
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from IPython.display import HTML, display

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
        from science_data_kit.graph import GraphConnector
        from science_data_kit.visualization import GraphVisualizer, DashboardGenerator
    else:
        # Fall back to internal src.sdk if external repository is not available
        from src.sdk.graph import GraphConnector
        from src.sdk.visualization import GraphVisualizer, DashboardGenerator
except ImportError:
    # If both imports fail, raise an error
    raise ImportError("Could not import SDK modules. Please ensure either the science_data_kit repository is cloned alongside this repo or the src.sdk modules are available.")

# Set up plotting
plt.style.use('ggplot')
sns.set(style="whitegrid")

# Connect to the Neo4j database
graph = GraphConnector(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="datadays"
)

# Initialize the visualizer
visualizer = GraphVisualizer(graph_connector=graph)
```

## 3. Creating Basic Graph Visualizations

### Visualizing the Overall Graph Structure

Let's start by visualizing the overall structure of our knowledge graph:

```python
# Get a summary of the graph structure
def get_graph_summary(graph):
    query = """
    MATCH (n)
    RETURN DISTINCT labels(n) as node_type, count(*) as count
    ORDER BY count DESC
    """
    node_types = graph.run_query(query)

    query = """
    MATCH ()-[r]->()
    RETURN DISTINCT type(r) as relationship_type, count(*) as count
    ORDER BY count DESC
    """
    relationship_types = graph.run_query(query)

    return {
        'node_types': node_types,
        'relationship_types': relationship_types
    }

# Display graph summary
summary = get_graph_summary(graph)

print("Node types in the graph:")
for record in summary['node_types']:
    node_type = record['node_type']
    count = record['count']
    print(f"  - {node_type}: {count}")

print("\nRelationship types in the graph:")
for record in summary['relationship_types']:
    rel_type = record['relationship_type']
    count = record['count']
    print(f"  - {rel_type}: {count}")
```

Now, let's create a visualization of the graph structure:

```python
# Visualize a subset of the graph
def visualize_graph_sample(graph, limit=50):
    # Query to get a sample of nodes and relationships
    query = f"""
    MATCH (n)-[r]->(m)
    RETURN n, r, m
    LIMIT {limit}
    """

    result = graph.run_query(query)

    # Create a NetworkX graph
    G = nx.DiGraph()

    # Track nodes and edges we've added
    nodes_added = set()
    edges_added = set()

    # Process query results
    for record in result:
        source_node = record['n']
        target_node = record['m']
        relationship = record['r']

        # Get node labels and properties
        source_labels = list(source_node.labels)[0] if hasattr(source_node, 'labels') else 'Node'
        target_labels = list(target_node.labels)[0] if hasattr(target_node, 'labels') else 'Node'

        # Create node IDs
        source_id = f"{source_labels}_{source_node.id}" if hasattr(source_node, 'id') else f"{source_labels}_{len(nodes_added)}"
        target_id = f"{target_labels}_{target_node.id}" if hasattr(target_node, 'id') else f"{target_labels}_{len(nodes_added)}"

        # Add nodes if not already added
        if source_id not in nodes_added:
            G.add_node(source_id, label=source_labels, **dict(source_node))
            nodes_added.add(source_id)

        if target_id not in nodes_added:
            G.add_node(target_id, label=target_labels, **dict(target_node))
            nodes_added.add(target_id)

        # Add edge if not already added
        edge_id = (source_id, target_id)
        if edge_id not in edges_added:
            G.add_edge(source_id, target_id, label=type(relationship), **dict(relationship))
            edges_added.add(edge_id)

    # Set up the plot
    plt.figure(figsize=(12, 10))

    # Create layout
    pos = nx.spring_layout(G, seed=42)

    # Get node types for coloring
    node_types = {n: G.nodes[n].get('label', 'Unknown') for n in G.nodes()}
    unique_types = list(set(node_types.values()))

    # Create a color map
    color_map = plt.cm.get_cmap('tab10', len(unique_types))

    # Draw nodes by type
    for i, node_type in enumerate(unique_types):
        node_list = [n for n, t in node_types.items() if t == node_type]
        nx.draw_networkx_nodes(G, pos, 
                              nodelist=node_list, 
                              node_color=[color_map(i)], 
                              node_size=500,
                              alpha=0.8,
                              label=node_type)

    # Draw edges
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, arrowsize=15)

    # Draw labels (limit to avoid clutter)
    if len(G.nodes()) <= 20:
        nx.draw_networkx_labels(G, pos, font_size=8)

    plt.title('Knowledge Graph Sample Visualization')
    plt.legend()
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    return G

# Visualize a sample of the graph
G = visualize_graph_sample(graph, limit=30)
```

### Visualizing Specific Subgraphs

Now let's focus on specific parts of the graph, such as a particular experiment or file type:

```python
# Visualize files and collections for a specific experiment
def visualize_experiment(graph, experiment_id):
    # Query to get files and collections for the experiment
    query = f"""
    MATCH (c:Collection)-[:CONTAINS]->(f:File)
    WHERE c.experiment_id = '{experiment_id}'
    OPTIONAL MATCH (f)-[:HAS_METADATA]->(m:Metadata)
    RETURN c, f, m
    """

    result = graph.run_query(query)

    # Create a NetworkX graph
    G = nx.DiGraph()

    # Track nodes and edges we've added
    nodes_added = set()
    edges_added = set()

    # Process query results
    for record in result:
        collection = record['c']
        file_node = record['f']
        metadata = record['m']

        # Add collection node
        collection_id = f"Collection_{collection.id}"
        if collection_id not in nodes_added:
            G.add_node(collection_id, 
                      label='Collection', 
                      name=collection.get('name', 'Unnamed Collection'),
                      node_type='collection')
            nodes_added.add(collection_id)

        # Add file node
        if file_node:
            file_id = f"File_{file_node.id}"
            if file_id not in nodes_added:
                G.add_node(file_id, 
                          label='File', 
                          name=os.path.basename(file_node.get('path', 'Unknown')),
                          file_type=file_node.get('file_type', 'Unknown'),
                          node_type='file')
                nodes_added.add(file_id)

            # Add edge from collection to file
            edge_id = (collection_id, file_id)
            if edge_id not in edges_added:
                G.add_edge(collection_id, file_id, label='CONTAINS')
                edges_added.add(edge_id)

            # Add metadata node if it exists
            if metadata:
                metadata_id = f"Metadata_{metadata.id}"
                if metadata_id not in nodes_added:
                    # Get a few key metadata properties to display
                    metadata_dict = dict(metadata)
                    display_props = {}
                    for key in list(metadata_dict.keys())[:3]:  # First 3 properties
                        display_props[key] = metadata_dict[key]

                    G.add_node(metadata_id, 
                              label='Metadata', 
                              **display_props,
                              node_type='metadata')
                    nodes_added.add(metadata_id)

                # Add edge from file to metadata
                edge_id = (file_id, metadata_id)
                if edge_id not in edges_added:
                    G.add_edge(file_id, metadata_id, label='HAS_METADATA')
                    edges_added.add(edge_id)

    # Set up the plot
    plt.figure(figsize=(14, 10))

    # Create layout - hierarchical layout works well for this type of graph
    pos = nx.spring_layout(G, seed=42)

    # Define node colors by type
    color_map = {
        'collection': 'lightblue',
        'file': 'lightgreen',
        'metadata': 'lightsalmon'
    }

    # Draw nodes by type
    for node_type, color in color_map.items():
        node_list = [n for n, attr in G.nodes(data=True) if attr.get('node_type') == node_type]
        nx.draw_networkx_nodes(G, pos, 
                              nodelist=node_list, 
                              node_color=color, 
                              node_size=500,
                              alpha=0.8,
                              label=node_type.capitalize())

    # Draw edges
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, arrowsize=15)

    # Draw labels with the name property where available
    labels = {}
    for node in G.nodes():
        if 'name' in G.nodes[node]:
            labels[node] = G.nodes[node]['name']
        else:
            # For metadata nodes, use the first property
            props = {k: v for k, v in G.nodes[node].items() 
                    if k not in ['label', 'node_type']}
            if props:
                first_key = list(props.keys())[0]
                labels[node] = f"{first_key}: {props[first_key]}"
            else:
                labels[node] = node

    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)

    plt.title(f'Experiment: {experiment_id}')
    plt.legend()
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    return G

# Example: Visualize a specific experiment
# Replace 'EXP-2023-001' with an actual experiment ID from your graph
experiment_id = 'EXP-2023-001'
experiment_graph = visualize_experiment(graph, experiment_id)
```

### Creating Statistical Visualizations

Beyond graph structure, we can create statistical visualizations of our data:

```python
# Create a visualization of file types distribution
def visualize_file_distribution(graph):
    # Query to get file type counts
    query = """
    MATCH (f:File)
    RETURN f.file_type as file_type, count(*) as count
    ORDER BY count DESC
    """

    result = graph.run_query(query)

    # Convert to DataFrame for easier plotting
    df = pd.DataFrame([dict(record) for record in result])

    # Create a pie chart
    plt.figure(figsize=(10, 6))
    plt.pie(df['count'], labels=df['file_type'], autopct='%1.1f%%', startangle=90, shadow=True)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title('File Type Distribution')
    plt.tight_layout()
    plt.show()

    # Create a bar chart
    plt.figure(figsize=(10, 6))
    sns.barplot(x='file_type', y='count', data=df)
    plt.title('File Type Distribution')
    plt.xlabel('File Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    return df

# Visualize file type distribution
file_distribution = visualize_file_distribution(graph)
```

```python
# Visualize metadata completeness
def visualize_metadata_completeness(graph):
    # Query to get metadata completeness by file type
    query = """
    MATCH (f:File)
    OPTIONAL MATCH (f)-[:HAS_METADATA]->(m:Metadata)
    WITH f.file_type as file_type, 
         CASE WHEN m IS NOT NULL THEN 1 ELSE 0 END as has_metadata
    RETURN file_type, 
           sum(has_metadata) as files_with_metadata,
           count(*) as total_files,
           sum(has_metadata) * 100.0 / count(*) as completeness_percentage
    ORDER BY completeness_percentage DESC
    """

    result = graph.run_query(query)

    # Convert to DataFrame for easier plotting
    df = pd.DataFrame([dict(record) for record in result])

    # Create a bar chart of completeness percentage
    plt.figure(figsize=(10, 6))
    sns.barplot(x='file_type', y='completeness_percentage', data=df)
    plt.title('Metadata Completeness by File Type')
    plt.xlabel('File Type')
    plt.ylabel('Completeness (%)')
    plt.axhline(y=50, color='r', linestyle='--', alpha=0.5)  # Add a reference line at 50%
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Create a stacked bar chart showing files with and without metadata
    plt.figure(figsize=(10, 6))

    # Calculate files without metadata
    df['files_without_metadata'] = df['total_files'] - df['files_with_metadata']

    # Create stacked bars
    bar_width = 0.5
    indices = np.arange(len(df))

    plt.bar(indices, df['files_with_metadata'], bar_width, label='With Metadata', color='lightgreen')
    plt.bar(indices, df['files_without_metadata'], bar_width, bottom=df['files_with_metadata'], 
            label='Without Metadata', color='lightcoral')

    plt.title('Files With and Without Metadata by Type')
    plt.xlabel('File Type')
    plt.ylabel('Number of Files')
    plt.xticks(indices, df['file_type'], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return df

# Visualize metadata completeness
metadata_completeness = visualize_metadata_completeness(graph)
```

## 4. Building Interactive Dashboards with NeoDash

NeoDash is a powerful tool for creating interactive dashboards based on Neo4j data. Here's how to create a dashboard:

```python
# Initialize the dashboard generator
dashboard_generator = DashboardGenerator(graph_connector=graph)

# Create a new dashboard
dashboard = dashboard_generator.create_dashboard(
    title="Research Data Dashboard",
    description="Overview of research data and metadata"
)

# Add a card showing file type distribution
dashboard.add_card(
    title="File Type Distribution",
    query="""
    MATCH (f:File)
    RETURN f.file_type as file_type, count(*) as count
    ORDER BY count DESC
    """,
    visualization_type="pie",
    width=6,
    height=2
)

# Add a card showing metadata completeness
dashboard.add_card(
    title="Metadata Completeness",
    query="""
    MATCH (f:File)
    OPTIONAL MATCH (f)-[:HAS_METADATA]->(m:Metadata)
    WITH f.file_type as file_type, 
         CASE WHEN m IS NOT NULL THEN 1 ELSE 0 END as has_metadata
    RETURN file_type, 
           sum(has_metadata) * 100.0 / count(*) as completeness_percentage
    ORDER BY completeness_percentage DESC
    """,
    visualization_type="bar",
    width=6,
    height=2
)

# Add a card showing recent files
dashboard.add_card(
    title="Recent Files",
    query="""
    MATCH (f:File)
    RETURN f.path as File, 
           f.file_type as Type, 
           f.size_bytes as Size,
           f.creation_date as Created
    ORDER BY f.creation_date DESC
    LIMIT 10
    """,
    visualization_type="table",
    width=12,
    height=2
)

# Add a graph visualization card
dashboard.add_card(
    title="File Relationships",
    query="""
    MATCH (c:Collection)-[:CONTAINS]->(f:File)
    OPTIONAL MATCH (f)-[:HAS_METADATA]->(m:Metadata)
    RETURN c, f, m
    LIMIT 50
    """,
    visualization_type="graph",
    width=12,
    height=3
)

# Save the dashboard
dashboard_path = dashboard.save("research_data_dashboard")
print(f"Dashboard saved to: {dashboard_path}")

# Launch the dashboard
dashboard.launch()
```

## 5. Customizing Visualizations for Different Audiences

Different audiences have different needs. Let's create visualizations tailored to specific audiences:

### For Trainees

```python
# Create a visualization focused on learning about file organization
def create_trainee_visualization(graph):
    # Query to get a simple file organization structure
    query = """
    MATCH (c:Collection)-[:CONTAINS]->(f:File)
    WHERE c.name CONTAINS 'Tutorial'
    RETURN c.name as collection, f.file_type as file_type, count(*) as file_count
    ORDER BY collection, file_type
    """

    result = graph.run_query(query)

    # Convert to DataFrame
    df = pd.DataFrame([dict(record) for record in result])

    if df.empty:
        print("No tutorial collections found. Please create some collections with 'Tutorial' in the name.")
        return None

    # Create a grouped bar chart
    plt.figure(figsize=(12, 6))

    # Pivot the data for easier plotting
    pivot_df = df.pivot(index='collection', columns='file_type', values='file_count')
    pivot_df.fillna(0, inplace=True)

    # Plot
    pivot_df.plot(kind='bar', stacked=True, ax=plt.gca())
    plt.title('File Organization in Tutorial Collections')
    plt.xlabel('Collection')
    plt.ylabel('Number of Files')
    plt.legend(title='File Type')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Create a simple graph visualization
    print("\nFile Organization Structure:")

    # Query for a simple graph structure
    query = """
    MATCH (c:Collection)-[:CONTAINS]->(f:File)
    WHERE c.name CONTAINS 'Tutorial'
    WITH c, f LIMIT 20
    OPTIONAL MATCH (f)-[:HAS_METADATA]->(m:Metadata)
    RETURN c, f, m
    """

    result = graph.run_query(query)

    # Create a NetworkX graph
    G = nx.DiGraph()

    # Track nodes and edges we've added
    nodes_added = set()
    edges_added = set()

    # Process query results
    for record in result:
        collection = record['c']
        file_node = record['f']
        metadata = record['m']

        # Add collection node
        collection_id = f"Collection_{collection.id}"
        if collection_id not in nodes_added:
            G.add_node(collection_id, 
                      label='Collection', 
                      name=collection.get('name', 'Unnamed Collection'),
                      node_type='collection')
            nodes_added.add(collection_id)

        # Add file node
        if file_node:
            file_id = f"File_{file_node.id}"
            if file_id not in nodes_added:
                G.add_node(file_id, 
                          label='File', 
                          name=os.path.basename(file_node.get('path', 'Unknown')),
                          file_type=file_node.get('file_type', 'Unknown'),
                          node_type='file')
                nodes_added.add(file_id)

            # Add edge from collection to file
            edge_id = (collection_id, file_id)
            if edge_id not in edges_added:
                G.add_edge(collection_id, file_id, label='CONTAINS')
                edges_added.add(edge_id)

            # Add metadata node if it exists
            if metadata:
                metadata_id = f"Metadata_{metadata.id}"
                if metadata_id not in nodes_added:
                    G.add_node(metadata_id, 
                              label='Metadata', 
                              node_type='metadata')
                    nodes_added.add(metadata_id)

                # Add edge from file to metadata
                edge_id = (file_id, metadata_id)
                if edge_id not in edges_added:
                    G.add_edge(file_id, metadata_id, label='HAS_METADATA')
                    edges_added.add(edge_id)

    # Set up the plot
    plt.figure(figsize=(12, 8))

    # Create layout
    pos = nx.spring_layout(G, seed=42)

    # Define node colors and sizes by type
    color_map = {
        'collection': 'skyblue',
        'file': 'lightgreen',
        'metadata': 'lightsalmon'
    }

    size_map = {
        'collection': 800,
        'file': 500,
        'metadata': 300
    }

    # Draw nodes by type
    for node_type in color_map:
        node_list = [n for n, attr in G.nodes(data=True) if attr.get('node_type') == node_type]
        nx.draw_networkx_nodes(G, pos, 
                              nodelist=node_list, 
                              node_color=color_map[node_type], 
                              node_size=size_map[node_type],
                              alpha=0.8,
                              label=node_type.capitalize())

    # Draw edges
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.6, arrowsize=20)

    # Draw labels
    labels = {}
    for node in G.nodes():
        if 'name' in G.nodes[node]:
            labels[node] = G.nodes[node]['name']
        else:
            labels[node] = G.nodes[node]['label']

    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10)

    plt.title('Knowledge Graph Structure for Tutorial Data')
    plt.legend()
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    return G

# Create trainee-focused visualization
trainee_viz = create_trainee_visualization(graph)
```

### For PIs and Administrators

```python
# Create a visualization focused on research progress and resource usage
def create_admin_visualization(graph):
    # Query to get data growth over time
    query = """
    MATCH (f:File)
    WHERE f.creation_date IS NOT NULL
    WITH date(f.creation_date) as date, sum(f.size_bytes) / 1024 / 1024 as size_mb
    RETURN date, size_mb
    ORDER BY date
    """

    result = graph.run_query(query)

    # Convert to DataFrame
    df = pd.DataFrame([dict(record) for record in result])

    if not df.empty:
        # Calculate cumulative sum
        df['cumulative_size_mb'] = df['size_mb'].cumsum()

        # Plot data growth
        plt.figure(figsize=(12, 6))
        plt.plot(df['date'], df['cumulative_size_mb'], marker='o', linestyle='-')
        plt.title('Cumulative Data Growth Over Time')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Size (MB)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        print("No file creation date data available.")

    # Query to get experiment progress
    query = """
    MATCH (c:Collection)
    WHERE c.experiment_id IS NOT NULL
    OPTIONAL MATCH (c)-[:CONTAINS]->(f:File)
    WITH c.experiment_id as experiment, 
         c.target_file_count as target,
         count(f) as current
    RETURN experiment, current, target,
           CASE WHEN target > 0 THEN current * 100.0 / target ELSE 0 END as completion_percentage
    ORDER BY completion_percentage DESC
    """

    result = graph.run_query(query)

    # Convert to DataFrame
    exp_df = pd.DataFrame([dict(record) for record in result])

    if not exp_df.empty and 'target' in exp_df.columns and exp_df['target'].sum() > 0:
        # Plot experiment progress
        plt.figure(figsize=(12, 6))

        # Create progress bars
        bar_height = 0.4
        y_pos = np.arange(len(exp_df))

        # Plot target bars (background)
        plt.barh(y_pos, exp_df['target'], bar_height, color='lightgray', alpha=0.5, label='Target')

        # Plot current progress bars
        plt.barh(y_pos, exp_df['current'], bar_height, color='steelblue', label='Current')

        # Add percentage labels
        for i, (_, row) in enumerate(exp_df.iterrows()):
            plt.text(row['target'] + 1, i, f"{row['completion_percentage']:.1f}%", 
                    va='center', fontsize=10)

        plt.yticks(y_pos, exp_df['experiment'])
        plt.xlabel('Number of Files')
        plt.title('Experiment Progress')
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        print("No experiment progress data available.")

    # Create a summary dashboard-like visualization
    fig, axs = plt.subplots(2, 2, figsize=(14, 10))

    # 1. File type distribution (top left)
    query = """
    MATCH (f:File)
    RETURN f.file_type as file_type, count(*) as count
    ORDER BY count DESC
    """
    result = graph.run_query(query)
    file_df = pd.DataFrame([dict(record) for record in result])

    if not file_df.empty:
        axs[0, 0].pie(file_df['count'], labels=file_df['file_type'], autopct='%1.1f%%', startangle=90)
        axs[0, 0].set_title('File Type Distribution')
    else:
        axs[0, 0].text(0.5, 0.5, 'No file type data available', ha='center', va='center')

    # 2. Metadata completeness (top right)
    query = """
    MATCH (f:File)
    OPTIONAL MATCH (f)-[:HAS_METADATA]->(m:Metadata)
    WITH f.file_type as file_type, 
         CASE WHEN m IS NOT NULL THEN 1 ELSE 0 END as has_metadata
    RETURN file_type, 
           sum(has_metadata) * 100.0 / count(*) as completeness_percentage
    ORDER BY completeness_percentage DESC
    """
    result = graph.run_query(query)
    meta_
