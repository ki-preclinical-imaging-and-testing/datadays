#!/usr/bin/env python3
"""
Science Data Kit (SDK) - Main Application

This is the entry point for the Science Data Kit application, which provides tools for
organizing research data using a knowledge graph approach.

Usage:
    python main.py [--help] [--version] [--config CONFIG_FILE]

Options:
    --help          Show this help message and exit
    --version       Show version information and exit
    --config        Specify a custom configuration file path
"""

import os
import sys
import argparse
import logging
from datetime import datetime

# Configure logging
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'sdk_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger('sdk')

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Science Data Kit (SDK) - Research Data Organization Tool')
    parser.add_argument('--version', action='store_true', help='Show version information')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    return parser.parse_args()

def show_version():
    """Display version information."""
    version = "0.1.0"  # Update this with actual version
    print(f"Science Data Kit (SDK) version {version}")
    print("MIT Koch Institute - Data Days Initiative")
    print("https://github.com/mit-koch/datadays")

def load_configuration(config_path=None):
    """Load configuration from file or use defaults."""
    # Default configuration
    config = {
        'neo4j': {
            'uri': 'bolt://localhost:7687',
            'username': 'neo4j',
            'password': 'datadays'
        },
        'streamlit': {
            'port': 8501,
            'theme': 'light'
        },
        'data_dir': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    }

    # If config file is specified, load it
    if config_path and os.path.exists(config_path):
        try:
            import yaml
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                # Update default config with user config
                for section, values in user_config.items():
                    if section in config:
                        config[section].update(values)
                    else:
                        config[section] = values
            logger.info(f"Configuration loaded from {config_path}")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")

    # Ensure data directory exists
    os.makedirs(config['data_dir'], exist_ok=True)

    return config

def launch_streamlit_app(config):
    """Launch the Streamlit web application."""
    try:
        import streamlit.web.cli as stcli

        # Prepare Streamlit arguments
        streamlit_args = [
            "streamlit", "run", 
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "app", "app.py"),
            "--server.port", str(config['streamlit']['port']),
            "--theme.base", config['streamlit']['theme']
        ]

        # Set environment variables for configuration
        os.environ['SDK_CONFIG'] = str(config)

        logger.info(f"Launching Streamlit app on port {config['streamlit']['port']}")
        sys.argv = streamlit_args
        stcli.main()

    except ImportError:
        logger.error("Streamlit is not installed. Please install it with: pip install streamlit")
        print("\nError: Streamlit is not installed.")
        print("Please install it with: pip install streamlit")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error launching Streamlit app: {e}")
        print(f"\nError launching application: {e}")
        sys.exit(1)

def check_dependencies():
    """Check if required dependencies are installed."""
    missing_deps = []

    try:
        import streamlit
    except ImportError:
        missing_deps.append("streamlit")

    try:
        import neo4j
    except ImportError:
        missing_deps.append("neo4j")

    try:
        import pandas
    except ImportError:
        missing_deps.append("pandas")

    try:
        import yaml
    except ImportError:
        missing_deps.append("pyyaml")

    if missing_deps:
        logger.warning(f"Missing dependencies: {', '.join(missing_deps)}")
        print("\nWarning: Some dependencies are missing.")
        print(f"Please install them with: pip install {' '.join(missing_deps)}")
        return False

    return True

def main():
    """Main entry point for the application."""
    # Parse command line arguments
    args = parse_arguments()

    # Show version and exit if requested
    if args.version:
        show_version()
        return

    # Check dependencies
    if not check_dependencies():
        return

    # Load configuration
    config = load_configuration(args.config)

    # Launch the Streamlit app
    launch_streamlit_app(config)

if __name__ == '__main__':
    try:
        logger.info("Starting Science Data Kit application")
        main()
    except KeyboardInterrupt:
        logger.info("Application terminated by user")
        print("\nApplication terminated by user.")
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        print(f"\nError: {e}")
        sys.exit(1)
