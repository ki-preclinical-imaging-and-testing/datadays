"""
Science Data Kit (SDK) - Streamlit Web Application

This is the main Streamlit application for the Science Data Kit, providing
a web interface for organizing research data using a knowledge graph approach.
"""

import os
import sys
import json
import streamlit as st
import pandas as pd
import ast
from datetime import datetime

# Add the project root to the path so we can import the SDK modules
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

# Add the science_data_kit repository (assumed to be cloned alongside this repo)
science_data_kit_path = os.path.join(os.path.dirname(project_root), 'science_data_kit')
if os.path.exists(science_data_kit_path):
    sys.path.append(science_data_kit_path)

# Import SDK modules (these would be implemented in the actual SDK)
# For now, we'll create placeholder imports and functions
try:
    # Try importing from external science_data_kit repository first
    if os.path.exists(science_data_kit_path):
        from science_data_kit.scanner import FileScanner
        from science_data_kit.graph import GraphConnector
        from science_data_kit.metadata import MetadataExtractor
        from science_data_kit.nlp import NLPProcessor
        from science_data_kit.visualization import GraphVisualizer
    else:
        # Fall back to internal src.sdk if external repository is not available
        from src.sdk.scanner import FileScanner
        from src.sdk.graph import GraphConnector
        from src.sdk.metadata import MetadataExtractor
        from src.sdk.nlp import NLPProcessor
        from src.sdk.visualization import GraphVisualizer
except ImportError:
    # Create placeholder classes for demonstration
    class GraphConnector:
        def __init__(self, uri=None, username=None, password=None):
            self.uri = uri
            self.username = username
            self.password = password
            self.connected = False

        def connect(self):
            # In a real implementation, this would connect to Neo4j
            self.connected = True
            return self.connected

        def test_connection(self):
            return self.connected

        def run_query(self, query, parameters=None):
            # Placeholder for query execution
            return []

    class FileScanner:
        def __init__(self, graph_connector=None):
            self.graph_connector = graph_connector

        def scan_directory(self, directory, **kwargs):
            # Placeholder for directory scanning
            return {
                "files": [],
                "file_type_counts": {"image": 0, "table": 0, "document": 0}
            }

    class MetadataExtractor:
        def __init__(self, graph_connector=None):
            self.graph_connector = graph_connector

        def extract_from_file(self, file_path):
            # Placeholder for metadata extraction
            return {}

    class NLPProcessor:
        def process_text(self, text):
            # Placeholder for NLP processing
            return {"entities": [], "intents": []}

    class GraphVisualizer:
        def __init__(self, graph_connector=None):
            self.graph_connector = graph_connector

        def create_visualization(self, query_result):
            # Placeholder for visualization
            return None

# Get configuration from environment variable
def get_config():
    config_str = os.environ.get('SDK_CONFIG', '{}')
    try:
        # Convert string representation of dict to actual dict
        if isinstance(config_str, str):
            return ast.literal_eval(config_str)
        return config_str
    except:
        return {}

# Initialize session state
def init_session_state():
    if 'graph_connector' not in st.session_state:
        config = get_config()
        neo4j_config = config.get('neo4j', {
            'uri': 'bolt://localhost:7687',
            'username': 'neo4j',
            'password': 'datadays'
        })

        st.session_state.graph_connector = GraphConnector(
            uri=neo4j_config.get('uri'),
            username=neo4j_config.get('username'),
            password=neo4j_config.get('password')
        )

    if 'file_scanner' not in st.session_state:
        st.session_state.file_scanner = FileScanner(
            graph_connector=st.session_state.graph_connector
        )

    if 'metadata_extractor' not in st.session_state:
        st.session_state.metadata_extractor = MetadataExtractor(
            graph_connector=st.session_state.graph_connector
        )

    if 'nlp_processor' not in st.session_state:
        st.session_state.nlp_processor = NLPProcessor()

    if 'graph_visualizer' not in st.session_state:
        st.session_state.graph_visualizer = GraphVisualizer(
            graph_connector=st.session_state.graph_connector
        )

    if 'scan_results' not in st.session_state:
        st.session_state.scan_results = None

    if 'current_directory' not in st.session_state:
        st.session_state.current_directory = None

# Set page configuration
st.set_page_config(
    page_title="Science Data Kit",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
init_session_state()

# Sidebar navigation
st.sidebar.title("Science Data Kit")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/1200px-MIT_logo.svg.png", width=100)

# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Data Scanner", "Metadata Editor", "Graph Explorer", "Query Builder", "Visualizations", "Settings"]
)

# Database connection status
connection_status = st.session_state.graph_connector.test_connection()
if connection_status:
    st.sidebar.success("Connected to Neo4j")
else:
    st.sidebar.error("Not connected to Neo4j")
    if st.sidebar.button("Connect"):
        if st.session_state.graph_connector.connect():
            st.sidebar.success("Connected successfully!")
            st.experimental_rerun()
        else:
            st.sidebar.error("Connection failed")

# Display the selected page
if page == "Home":
    st.title("Welcome to the Science Data Kit")

    st.markdown("""
    The **Science Data Kit (SDK)** is a toolkit for organizing research data using a knowledge graph approach.

    ## Features

    - **Data Scanning**: Automatically scan and organize research files
    - **Metadata Extraction**: Extract metadata from various file formats
    - **Knowledge Graph**: Create a graph of your research data
    - **Visualization**: Explore your data through interactive visualizations
    - **Natural Language**: Query your data using natural language

    ## Getting Started

    Use the navigation menu on the left to explore the different features of the SDK.

    1. Start with the **Data Scanner** to scan your research files
    2. Use the **Metadata Editor** to view and edit metadata
    3. Explore your data in the **Graph Explorer**
    4. Build queries in the **Query Builder**
    5. Create visualizations in the **Visualizations** page

    ## Documentation

    For more information, check out the [documentation](https://github.com/mit-koch/datadays/docs).
    """)

    # Display some stats if connected to the database
    if connection_status:
        st.subheader("Database Statistics")

        # In a real implementation, these would be actual queries
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Files", "0")

        with col2:
            st.metric("Collections", "0")

        with col3:
            st.metric("Relationships", "0")

elif page == "Data Scanner":
    st.title("Data Scanner")

    st.markdown("""
    Use the Data Scanner to scan directories for research data files.
    The scanner will identify file types and extract basic metadata.
    """)

    # Directory selection
    st.subheader("Select Directory")
    directory = st.text_input("Directory Path", value=st.session_state.current_directory or "")

    # Scan options
    st.subheader("Scan Options")

    col1, col2 = st.columns(2)

    with col1:
        recursive = st.checkbox("Scan Subdirectories", value=True)
        extract_metadata = st.checkbox("Extract Basic Metadata", value=True)

    with col2:
        file_types = st.multiselect(
            "File Types to Include",
            ["image", "table", "document", "sequence", "other"],
            default=["image", "table", "document"]
        )

    # Scan button
    if st.button("Start Scan"):
        if not directory:
            st.error("Please enter a directory path")
        elif not os.path.isdir(directory):
            st.error("Directory does not exist")
        else:
            st.session_state.current_directory = directory

            # Show a spinner while scanning
            with st.spinner(f"Scanning {directory}..."):
                # In a real implementation, this would actually scan the directory
                # For now, we'll just simulate a scan
                st.session_state.scan_results = {
                    "files": [
                        {
                            "file_id": "file1",
                            "path": os.path.join(directory, "example1.tif"),
                            "file_type": "image",
                            "size_bytes": 1024000,
                            "creation_date": datetime.now().strftime("%Y-%m-%d")
                        },
                        {
                            "file_id": "file2",
                            "path": os.path.join(directory, "example2.csv"),
                            "file_type": "table",
                            "size_bytes": 5120,
                            "creation_date": datetime.now().strftime("%Y-%m-%d")
                        },
                        {
                            "file_id": "file3",
                            "path": os.path.join(directory, "example3.docx"),
                            "file_type": "document",
                            "size_bytes": 15360,
                            "creation_date": datetime.now().strftime("%Y-%m-%d")
                        }
                    ],
                    "file_type_counts": {
                        "image": 1,
                        "table": 1,
                        "document": 1
                    }
                }

            st.success(f"Scan completed! Found {len(st.session_state.scan_results['files'])} files.")

    # Display scan results
    if st.session_state.scan_results:
        st.subheader("Scan Results")

        # File type distribution
        st.write("File Type Distribution")
        file_types_df = pd.DataFrame({
            'File Type': st.session_state.scan_results['file_type_counts'].keys(),
            'Count': st.session_state.scan_results['file_type_counts'].values()
        })
        st.bar_chart(file_types_df.set_index('File Type'))

        # File list
        st.write("Files Found")
        files_df = pd.DataFrame(st.session_state.scan_results['files'])
        st.dataframe(files_df)

        # Save to database button
        if st.button("Save to Database"):
            # In a real implementation, this would save the files to the database
            st.success("Files saved to database!")

elif page == "Metadata Editor":
    st.title("Metadata Editor")

    st.markdown("""
    Use the Metadata Editor to view and edit metadata for your research files.
    """)

    # Placeholder for metadata editor
    st.info("This feature is under development. Check back soon!")

elif page == "Graph Explorer":
    st.title("Graph Explorer")

    st.markdown("""
    Use the Graph Explorer to explore the knowledge graph of your research data.
    """)

    # Placeholder for graph explorer
    st.info("This feature is under development. Check back soon!")

elif page == "Query Builder":
    st.title("Query Builder")

    st.markdown("""
    Use the Query Builder to create and execute queries against your knowledge graph.
    """)

    # Placeholder for query builder
    st.info("This feature is under development. Check back soon!")

elif page == "Visualizations":
    st.title("Visualizations")

    st.markdown("""
    Create interactive visualizations of your research data.
    """)

    # Placeholder for visualizations
    st.info("This feature is under development. Check back soon!")

elif page == "Settings":
    st.title("Settings")

    st.markdown("""
    Configure the Science Data Kit.
    """)

    # Database settings
    st.subheader("Database Settings")

    neo4j_uri = st.text_input("Neo4j URI", value=st.session_state.graph_connector.uri)
    neo4j_username = st.text_input("Neo4j Username", value=st.session_state.graph_connector.username)
    neo4j_password = st.text_input("Neo4j Password", value=st.session_state.graph_connector.password, type="password")

    if st.button("Save Database Settings"):
        # In a real implementation, this would update the configuration
        st.session_state.graph_connector = GraphConnector(
            uri=neo4j_uri,
            username=neo4j_username,
            password=neo4j_password
        )
        st.success("Database settings saved!")

    # Application settings
    st.subheader("Application Settings")

    # Placeholder for application settings
    st.info("Additional settings coming soon!")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("© 2023 MIT Koch Institute")
st.sidebar.markdown("Data Days Initiative")
