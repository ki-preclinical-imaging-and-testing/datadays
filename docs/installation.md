# Installation Guide

This guide provides step-by-step instructions for setting up the Science Data Kit (SDK) for use in the Data Days initiative.

## Prerequisites

Before installing the SDK, ensure you have the following prerequisites:

- Python 3.8 or higher
- Docker and Docker Compose
- Git
- 8GB RAM minimum (16GB recommended)
- 20GB free disk space

## Installation Steps

### 1. Clone the Repositories

```bash
# Clone the main Data Days repository
git clone https://github.com/mit-koch/datadays.git

# Clone the Science Data Kit repository alongside it
git clone https://github.com/mit-koch/science_data_kit.git

# Navigate to the Data Days directory
cd datadays
```

The Science Data Kit repository should be cloned at the same level as the Data Days repository, not inside it. Your directory structure should look like:

```
parent_directory/
├── datadays/
└── science_data_kit/
```

### 2. Set Up Python Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Neo4j with Docker

```bash
# Start Neo4j container
docker-compose up -d neo4j
```

This will start a Neo4j database with the following default credentials:
- Username: `neo4j`
- Password: `datadays`
- Port: `7687` (Bolt), `7474` (HTTP)

### 4. Configure the SDK

```bash
# Generate default configuration
python -m src.sdk.config --init
```

Edit the generated `config.yaml` file to customize your settings if needed.

### 5. Start the Streamlit Application

```bash
# Start the web application
python main.py
```

The application will be available at `http://localhost:8501`.

## Verification

To verify that the installation was successful:

1. Open your web browser and navigate to `http://localhost:8501`
2. You should see the Data Days dashboard
3. Navigate to the Neo4j Browser at `http://localhost:7474` to verify the database connection

## Troubleshooting

### Common Issues

#### Neo4j Connection Issues
- Ensure Docker is running
- Check if the Neo4j container is up with `docker ps`
- Verify the credentials in your `config.yaml` file

#### Python Dependency Issues
- Try upgrading pip: `pip install --upgrade pip`
- Install dependencies one by one to identify problematic packages

#### Permission Issues
- On Linux/macOS, you might need to run Docker commands with `sudo`
- Ensure your user has permissions to access the required directories

## Next Steps

After installation, we recommend:

1. Following the [Overview](overview.md) to understand the system
2. Exploring the [Demo Workflows](../demos/README.md) to see the SDK in action
3. Reading the appropriate [User Guide](user_guide_trainees.md) for your role

## Support

If you encounter any issues during installation, please:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Refer to the [FAQ](faq.md) for common questions
3. Contact the Data Days team at datadays@mit.edu

---

[Back to Documentation Home](README.md)
