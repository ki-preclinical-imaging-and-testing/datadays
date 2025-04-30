# Science Data Kit (SDK) Source Code

This directory contains the source code for the Science Data Kit (SDK), a toolkit for organizing research data using a knowledge graph approach.

## Directory Structure

- **[app/](app/)**: Streamlit web application
  - [app.py](app/app.py): Main Streamlit application entry point

- **sdk/**: Core SDK modules (to be implemented)
  - `scanner.py`: File scanning and organization
  - `metadata.py`: Metadata extraction and processing
  - `graph.py`: Neo4j graph database interaction
  - `nlp.py`: Natural language processing utilities
  - `visualization.py`: Data visualization tools

- **integration/**: Integration with external tools (to be implemented)
  - `jupyter/`: Jupyter notebook integration
  - `docker/`: Docker configuration files
  - `api/`: API endpoints for external access

## Implementation Status

The SDK is currently in development. The following components are available:

- ✅ Application structure and entry points
- ✅ Streamlit web interface
- ⏳ Core SDK modules (placeholder implementations)
- ⏳ Integration components

## Development

To contribute to the SDK development:

1. Create the necessary module files in the appropriate directories
2. Implement the required functionality following the architecture described in the [SDK Architecture](../docs/sdk_architecture.md) document
3. Add tests for your implementations
4. Update the documentation to reflect your changes

## Running the Application

The main entry point for the application is [main.py](../main.py) in the root directory. To run the application:

```bash
python main.py
```

This will start the Streamlit web application, which you can access at http://localhost:8501.

## Configuration

The application can be configured using a YAML configuration file. See the [Installation Guide](../docs/installation.md) for details on configuration options.

## Dependencies

The SDK depends on the following Python packages:

- streamlit: Web application framework
- neo4j: Neo4j database driver
- pandas: Data manipulation and analysis
- pyyaml: YAML parsing for configuration

Additional dependencies may be required for specific modules.

## Related Resources

- [Documentation](../docs/README.md): Comprehensive documentation
- [Demo Workflows](../demos/README.md): Example workflows and tutorials
- [Outreach Materials](../outreach/README.md): Templates for promotion and communication