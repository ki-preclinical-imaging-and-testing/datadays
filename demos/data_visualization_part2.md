# Data Visualization with Science Data Kit (Continued)

This document is a continuation of the [Data Visualization](data_visualization.md) tutorial. We'll complete the sections on customizing visualizations for different audiences and cover exporting and sharing visualizations.

## 5. Customizing Visualizations for Different Audiences (Continued)

### For PIs and Administrators (Continued)

```python
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
    meta_df = pd.DataFrame([dict(record) for record in result])

    if not meta_df.empty:
        axs[0, 1].bar(meta_df['file_type'], meta_df['completeness_percentage'])
        axs[0, 1].set_title('Metadata Completeness')
        axs[0, 1].set_ylabel('Completeness (%)')
        axs[0, 1].set_xticklabels(meta_df['file_type'], rotation=45)
    else:
        axs[0, 1].text(0.5, 0.5, 'No metadata completeness data available', ha='center', va='center')

    # 3. Data growth over time (bottom left)
    if not df.empty:
        axs[1, 0].plot(df['date'], df['cumulative_size_mb'], marker='o', linestyle='-')
        axs[1, 0].set_title('Data Growth Over Time')
        axs[1, 0].set_ylabel('Cumulative Size (MB)')
        axs[1, 0].grid(True)
        axs[1, 0].tick_params(axis='x', rotation=45)
    else:
        axs[1, 0].text(0.5, 0.5, 'No data growth information available', ha='center', va='center')

    # 4. Experiment progress (bottom right)
    if not exp_df.empty and 'target' in exp_df.columns and exp_df['target'].sum() > 0:
        # Limit to top 5 experiments for clarity
        top_exp_df = exp_df.head(5)

        # Create progress bars
        y_pos = np.arange(len(top_exp_df))

        # Plot target bars (background)
        axs[1, 1].barh(y_pos, top_exp_df['target'], 0.4, color='lightgray', alpha=0.5, label='Target')

        # Plot current progress bars
        axs[1, 1].barh(y_pos, top_exp_df['current'], 0.4, color='steelblue', label='Current')

        # Add percentage labels
        for i, (_, row) in enumerate(top_exp_df.iterrows()):
            axs[1, 1].text(row['target'] + 1, i, f"{row['completion_percentage']:.1f}%", 
                    va='center', fontsize=8)

        axs[1, 1].set_yticks(y_pos)
        axs[1, 1].set_yticklabels(top_exp_df['experiment'])
        axs[1, 1].set_title('Experiment Progress')
        axs[1, 1].legend(loc='upper right')
    else:
        axs[1, 1].text(0.5, 0.5, 'No experiment progress data available', ha='center', va='center')

    plt.tight_layout()
    plt.show()

    return {
        'data_growth': df if not df.empty else None,
        'experiment_progress': exp_df if not exp_df.empty else None,
        'file_distribution': file_df if not file_df.empty else None,
        'metadata_completeness': meta_df if not meta_df.empty else None
    }

# Create admin-focused visualization
admin_viz = create_admin_visualization(graph)
```

### For Research Collaborators

```python
# Create a visualization focused on data sharing and collaboration
def create_collaboration_visualization(graph):
    # Query to get collaboration network
    query = """
    MATCH (r:Researcher)-[:CONTRIBUTED_TO]->(f:File)<-[:CONTRIBUTED_TO]-(r2:Researcher)
    WHERE r <> r2
    RETURN r.name as researcher1, r2.name as researcher2, count(f) as collaboration_count
    ORDER BY collaboration_count DESC
    """

    result = graph.run_query(query)

    # Convert to DataFrame
    df = pd.DataFrame([dict(record) for record in result])

    if df.empty:
        print("No collaboration data found. Please add researcher contributions to files.")

        # Create sample data for demonstration
        print("Creating sample visualization with mock data...")
        researchers = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank']
        mock_data = []

        for i, r1 in enumerate(researchers):
            for r2 in researchers[i+1:]:
                # Generate random collaboration count
                count = np.random.randint(1, 10)
                mock_data.append({'researcher1': r1, 'researcher2': r2, 'collaboration_count': count})

        df = pd.DataFrame(mock_data)

    # Create a collaboration network visualization
    G = nx.Graph()

    # Add edges with weights based on collaboration count
    for _, row in df.iterrows():
        r1 = row['researcher1']
        r2 = row['researcher2']
        count = row['collaboration_count']

        if not G.has_node(r1):
            G.add_node(r1)
        if not G.has_node(r2):
            G.add_node(r2)

        G.add_edge(r1, r2, weight=count)

    # Calculate node sizes based on number of collaborations
    node_size = {node: 300 + 100 * G.degree(node) for node in G.nodes()}

    # Calculate edge widths based on collaboration count
    edge_width = [0.5 + 0.5 * G[u][v]['weight'] for u, v in G.edges()]

    # Set up the plot
    plt.figure(figsize=(12, 10))

    # Create layout
    pos = nx.spring_layout(G, seed=42)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, 
                          node_size=[node_size[node] for node in G.nodes()],
                          node_color='lightblue',
                          alpha=0.8)

    # Draw edges with varying widths
    nx.draw_networkx_edges(G, pos, width=edge_width, alpha=0.5)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10)

    # Draw edge labels (collaboration counts)
    edge_labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title('Research Collaboration Network')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    # Create a heatmap of collaborations
    if len(G.nodes()) > 1:
        # Create a matrix of collaboration counts
        researchers = list(G.nodes())
        n = len(researchers)
        collaboration_matrix = np.zeros((n, n))

        for i, r1 in enumerate(researchers):
            for j, r2 in enumerate(researchers):
                if i != j and G.has_edge(r1, r2):
                    collaboration_matrix[i, j] = G[r1][r2]['weight']

        # Create heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(collaboration_matrix, annot=True, fmt=".0f", cmap="YlGnBu",
                   xticklabels=researchers, yticklabels=researchers)
        plt.title('Collaboration Intensity Heatmap')
        plt.tight_layout()
        plt.show()

    return G

# Create collaboration-focused visualization
collab_viz = create_collaboration_visualization(graph)
```

## 6. Exporting and Sharing Visualizations

### Exporting Static Visualizations

```python
# Function to export visualizations to various formats
def export_visualization(fig, filename, formats=['png', 'pdf', 'svg']):
    """
    Export a matplotlib figure to multiple formats

    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        The figure to export
    filename : str
        Base filename without extension
    formats : list
        List of formats to export to
    """
    for fmt in formats:
        output_file = f"{filename}.{fmt}"
        fig.savefig(output_file, format=fmt, dpi=300, bbox_inches='tight')
        print(f"Saved visualization to {output_file}")

# Example: Create and export a visualization
plt.figure(figsize=(10, 6))

# Create a sample visualization
query = """
MATCH (f:File)
RETURN f.file_type as file_type, count(*) as count
ORDER BY count DESC
"""
result = graph.run_query(query)
df = pd.DataFrame([dict(record) for record in result])

if not df.empty:
    plt.pie(df['count'], labels=df['file_type'], autopct='%1.1f%%', startangle=90, shadow=True)
    plt.axis('equal')
    plt.title('File Type Distribution')

    # Export the visualization
    export_visualization(plt.gcf(), "file_distribution", formats=['png', 'pdf'])
else:
    print("No data available for visualization")
```

### Creating Interactive HTML Visualizations

```python
# Function to create an interactive HTML visualization using Plotly
def create_interactive_visualization(graph):
    try:
        import plotly.graph_objects as go
        import plotly.express as px
        from plotly.subplots import make_subplots

        # Query to get file type distribution
        query = """
        MATCH (f:File)
        RETURN f.file_type as file_type, count(*) as count
        ORDER BY count DESC
        """
        result = graph.run_query(query)
        df = pd.DataFrame([dict(record) for record in result])

        if df.empty:
            print("No data available for visualization")
            return None

        # Create a subplot with 1 row and 2 columns
        fig = make_subplots(rows=1, cols=2, 
                           specs=[[{"type": "pie"}, {"type": "bar"}]],
                           subplot_titles=("File Type Distribution", "File Count by Type"))

        # Add pie chart
        fig.add_trace(
            go.Pie(labels=df['file_type'], values=df['count'], hole=.3),
            row=1, col=1
        )

        # Add bar chart
        fig.add_trace(
            go.Bar(x=df['file_type'], y=df['count']),
            row=1, col=2
        )

        # Update layout
        fig.update_layout(
            title_text="Interactive File Distribution Visualization",
            height=600,
            width=1000
        )

        # Save as HTML
        html_file = "interactive_visualization.html"
        fig.write_html(html_file)
        print(f"Interactive visualization saved to {html_file}")

        # Display in notebook if running in one
        return fig

    except ImportError:
        print("Plotly is required for interactive visualizations.")
        print("Install with: pip install plotly")
        return None

# Create an interactive visualization
interactive_viz = create_interactive_visualization(graph)
```

### Sharing Dashboards

```python
# Function to export a NeoDash dashboard for sharing
def export_dashboard(dashboard_path):
    """
    Export a NeoDash dashboard for sharing

    Parameters:
    -----------
    dashboard_path : str
        Path to the dashboard JSON file

    Returns:
    --------
    str
        Path to the exported dashboard
    """
    import json
    import shutil
    from datetime import datetime

    # Load the dashboard
    try:
        with open(dashboard_path, 'r') as f:
            dashboard = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading dashboard: {e}")
        return None

    # Create an export version with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_path = f"dashboard_export_{timestamp}.json"

    # Copy the dashboard file
    shutil.copy2(dashboard_path, export_path)

    print(f"Dashboard exported to {export_path}")
    print("To share this dashboard:")
    print("1. Send this JSON file to your collaborator")
    print("2. They should place it in their NeoDash dashboards directory")
    print("3. They can then load it from the NeoDash dashboard selector")

    return export_path

# Example: Export a dashboard
# export_dashboard("research_data_dashboard.json")
```

## Summary

In this tutorial, we've demonstrated how to:

1. Understand the different visualization options available in the Science Data Kit
2. Set up the visualization environment
3. Create basic graph visualizations to explore the structure of your knowledge graph
4. Build interactive dashboards with NeoDash
5. Customize visualizations for different audiences:
   - Trainees
   - PIs and administrators
   - Research collaborators
6. Export and share visualizations in various formats

Effective visualization is crucial for understanding complex research data and communicating insights to different audiences. The Science Data Kit provides a range of tools to create visualizations tailored to your specific needs.

## Next Steps

To continue exploring the Science Data Kit, check out these additional tutorials:

- [Natural Language Interaction](nlp_interaction.md): Learn how to use natural language to interact with your knowledge graph
- [Advanced Graph Queries](graph_queries.md): Write and execute advanced queries against the knowledge graph
- [Custom Visualization Development](custom_visualization.md): Develop custom visualizations for specific research domains

You can also refer to the [User Guide for PIs & Administrators](../docs/user_guide_admins.md) for more information on using visualizations for research management.
