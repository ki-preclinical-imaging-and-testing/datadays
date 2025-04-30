"""
Science Data Kit (SDK) - File Scanner Module

This module provides functionality for scanning directories and organizing research data files.
It identifies file types, extracts basic metadata, and creates file entities in the knowledge graph.
"""

import os
import logging
import datetime
import mimetypes
from typing import Dict, List, Any, Optional

# Configure logging
logger = logging.getLogger('sdk.scanner')

class FileScanner:
    """
    Scanner for research data files.
    
    This class provides methods for scanning directories, identifying file types,
    extracting basic metadata, and organizing files into collections.
    """
    
    def __init__(self, graph_connector=None):
        """
        Initialize the FileScanner.
        
        Args:
            graph_connector: Connection to the Neo4j graph database
        """
        self.graph_connector = graph_connector
        # Initialize mimetypes
        mimetypes.init()
        # Add additional mimetypes for research data files
        self._add_research_mimetypes()
        
    def _add_research_mimetypes(self):
        """Add research-specific mimetypes that may not be in the standard library."""
        # Microscopy formats
        mimetypes.add_type('image/tiff', '.ome.tiff')
        mimetypes.add_type('image/tiff', '.ome.tif')
        # Flow cytometry formats
        mimetypes.add_type('application/octet-stream', '.fcs')
        # Sequencing formats
        mimetypes.add_type('application/octet-stream', '.fastq')
        mimetypes.add_type('application/octet-stream', '.fastq.gz')
        mimetypes.add_type('application/octet-stream', '.bam')
        
    def scan_directory(self, directory: str, recursive: bool = True, 
                      file_types: List[str] = None, exclude_patterns: List[str] = None,
                      extract_basic_metadata: bool = True) -> Dict[str, Any]:
        """
        Scan a directory for research data files.
        
        Args:
            directory: Path to the directory to scan
            recursive: Whether to scan subdirectories
            file_types: List of file types to include (e.g., ['image', 'table'])
            exclude_patterns: List of patterns to exclude (e.g., ['.git', '__pycache__'])
            extract_basic_metadata: Whether to extract basic metadata during scan
            
        Returns:
            Dictionary containing scan results:
            {
                'files': List of file dictionaries,
                'file_type_counts': Dictionary of file type counts
            }
        """
        logger.info(f"Scanning directory: {directory}")
        
        # Initialize results
        files = []
        file_type_counts = {}
        
        # Default file types if not specified
        if file_types is None:
            file_types = ['image', 'table', 'document', 'sequence', 'other']
            
        # Default exclude patterns if not specified
        if exclude_patterns is None:
            exclude_patterns = ['.git', '__pycache__', '.ipynb_checkpoints']
        
        # Check if directory exists
        if not os.path.isdir(directory):
            logger.error(f"Directory does not exist: {directory}")
            return {'files': [], 'file_type_counts': {}}
        
        # Walk through the directory
        for root, dirs, filenames in os.walk(directory):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
            
            # Process files in this directory
            for filename in filenames:
                # Skip excluded files
                if any(pattern in filename for pattern in exclude_patterns):
                    continue
                
                # Get full file path
                file_path = os.path.join(root, filename)
                
                # Determine file type
                file_type = self._determine_file_type(file_path)
                
                # Skip if not in requested file types
                if file_type not in file_types and 'other' not in file_types:
                    continue
                
                # Extract basic metadata if requested
                metadata = {}
                if extract_basic_metadata:
                    metadata = self._extract_basic_metadata(file_path)
                
                # Create file dictionary
                file_dict = {
                    'file_id': self._generate_file_id(file_path),
                    'path': file_path,
                    'file_type': file_type,
                    'directory': root,
                    'filename': filename,
                    **metadata
                }
                
                # Add to results
                files.append(file_dict)
                
                # Update file type counts
                file_type_counts[file_type] = file_type_counts.get(file_type, 0) + 1
            
            # Stop if not recursive
            if not recursive:
                break
        
        logger.info(f"Scan completed. Found {len(files)} files.")
        
        return {
            'files': files,
            'file_type_counts': file_type_counts
        }
    
    def _determine_file_type(self, file_path: str) -> str:
        """
        Determine the type of a file based on its extension and content.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File type: 'image', 'table', 'document', 'sequence', or 'other'
        """
        # Get mimetype based on extension
        mimetype, _ = mimetypes.guess_type(file_path)
        
        # Default to 'other' if mimetype not found
        if mimetype is None:
            return 'other'
        
        # Determine file type based on mimetype
        if mimetype.startswith('image/'):
            return 'image'
        elif mimetype in ['text/csv', 'application/vnd.ms-excel', 
                         'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
            return 'table'
        elif mimetype in ['application/pdf', 'application/msword',
                         'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                         'text/plain']:
            return 'document'
        elif mimetype == 'application/octet-stream':
            # Check extension for sequence data
            ext = os.path.splitext(file_path)[1].lower()
            if ext in ['.fastq', '.fq', '.fastq.gz', '.fq.gz', '.bam', '.sam', '.fcs']:
                return 'sequence'
            return 'other'
        else:
            return 'other'
    
    def _extract_basic_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract basic metadata from a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary of metadata
        """
        metadata = {}
        
        try:
            # Get file stats
            stats = os.stat(file_path)
            
            # File size
            metadata['size_bytes'] = stats.st_size
            
            # Creation and modification times
            metadata['creation_date'] = datetime.datetime.fromtimestamp(
                stats.st_ctime).strftime('%Y-%m-%d')
            metadata['modified_date'] = datetime.datetime.fromtimestamp(
                stats.st_mtime).strftime('%Y-%m-%d')
            
        except Exception as e:
            logger.warning(f"Error extracting metadata from {file_path}: {e}")
        
        return metadata
    
    def _generate_file_id(self, file_path: str) -> str:
        """
        Generate a unique ID for a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Unique file ID
        """
        # In a real implementation, this would generate a more sophisticated ID
        # For now, we'll just use a hash of the file path
        return f"file_{hash(file_path) % 10000:04d}"
    
    def create_collection(self, name: str, description: str = None, 
                         file_ids: List[str] = None) -> Dict[str, Any]:
        """
        Create a collection of files in the knowledge graph.
        
        Args:
            name: Name of the collection
            description: Description of the collection
            file_ids: List of file IDs to include in the collection
            
        Returns:
            Dictionary representing the collection
        """
        logger.info(f"Creating collection: {name}")
        
        # Generate a collection ID
        collection_id = f"collection_{hash(name) % 10000:04d}"
        
        # Create collection dictionary
        collection = {
            'collection_id': collection_id,
            'name': name,
            'description': description or '',
            'file_count': len(file_ids) if file_ids else 0,
            'created_date': datetime.datetime.now().strftime('%Y-%m-%d')
        }
        
        # In a real implementation, this would create the collection in Neo4j
        # and establish relationships to the files
        if self.graph_connector and file_ids:
            logger.info(f"Adding {len(file_ids)} files to collection {name}")
            # This would be implemented to add files to the collection in Neo4j
        
        return collection

# Example usage
if __name__ == "__main__":
    # This code will only run if the module is executed directly
    scanner = FileScanner()
    results = scanner.scan_directory(".")
    print(f"Found {len(results['files'])} files")
    for file_type, count in results['file_type_counts'].items():
        print(f"  - {file_type}: {count}")