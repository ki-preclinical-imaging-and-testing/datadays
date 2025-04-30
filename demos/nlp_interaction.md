# Natural Language Interaction with Science Data Kit

This document demonstrates how to use the Science Data Kit (SDK) to interact with your knowledge graph using natural language. We'll cover:

1. Understanding natural language interaction capabilities
2. Setting up the NLP environment
3. Basic natural language queries
4. Advanced query techniques
5. Building a conversational interface
6. Customizing the NLP engine for domain-specific terminology

## Prerequisites

Before following this tutorial, ensure you have:
- Installed the Science Data Kit following the [Installation Guide](../docs/installation.md)
- Completed the [Data Scanning](data_scanning.md) and [Metadata Extraction](metadata_extraction.md) tutorials
- A Neo4j database populated with research data and metadata

## 1. Understanding Natural Language Interaction Capabilities

The Science Data Kit provides natural language processing (NLP) capabilities that allow you to:

- Query your knowledge graph using plain English
- Translate natural language questions into Cypher queries
- Extract entities and relationships from text
- Generate summaries and insights from your data
- Build conversational interfaces for your research data

These capabilities make it easier for researchers without graph database expertise to explore and analyze their data.

## 2. Setting Up the NLP Environment

First, let's set up our environment for natural language processing:

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
        from science_data_kit.graph import GraphConnector
        from science_data_kit.nlp import NLPProcessor, QueryTranslator
    else:
        # Fall back to internal src.sdk if external repository is not available
        from src.sdk.graph import GraphConnector
        from src.sdk.nlp import NLPProcessor, QueryTranslator
except ImportError:
    # If both imports fail, raise an error
    raise ImportError("Could not import SDK modules. Please ensure either the science_data_kit repository is cloned alongside this repo or the src.sdk modules are available.")

# Connect to the Neo4j database
graph = GraphConnector(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="datadays"
)

# Initialize the NLP processor
nlp_processor = NLPProcessor()

# Initialize the query translator
query_translator = QueryTranslator(graph_connector=graph)
```

## 3. Basic Natural Language Queries

Let's start with some basic natural language queries:

```python
# Function to process natural language queries
def process_query(query_text):
    """
    Process a natural language query and return results

    Parameters:
    -----------
    query_text : str
        The natural language query

    Returns:
    --------
    dict
        Dictionary containing query results and metadata
    """
    print(f"Query: {query_text}")

    # Process the query text
    processed_query = nlp_processor.process_text(query_text)

    # Translate to Cypher
    cypher_query, params = query_translator.translate_to_cypher(processed_query)

    print(f"Translated Cypher: {cypher_query}")

    # Execute the query
    if cypher_query:
        results = graph.run_query(cypher_query, parameters=params)

        # Convert results to a DataFrame for easier handling
        if results:
            df = pd.DataFrame([dict(record) for record in results])
            return {
                'original_query': query_text,
                'cypher_query': cypher_query,
                'results': df,
                'success': True
            }
        else:
            return {
                'original_query': query_text,
                'cypher_query': cypher_query,
                'results': None,
                'success': False,
                'message': 'No results found'
            }
    else:
        return {
            'original_query': query_text,
            'cypher_query': None,
            'results': None,
            'success': False,
            'message': 'Could not translate query to Cypher'
        }

# Example basic queries
basic_queries = [
    "Show me all image files",
    "How many files do we have in total?",
    "What are the different file types in the database?",
    "Show me files created in the last month",
    "Which files have metadata?"
]

# Process each query
for query in basic_queries:
    result = process_query(query)

    if result['success'] and result['results'] is not None:
        print("\nResults:")
        display(result['results'].head(10))  # Display first 10 rows
        print(f"Total results: {len(result['results'])}")
    else:
        print(f"\nError: {result.get('message', 'Unknown error')}")

    print("\n" + "-"*50 + "\n")
```

### Understanding Query Translation

Let's examine how natural language queries are translated to Cypher:

```python
# Function to explain query translation
def explain_translation(query_text):
    """
    Explain how a natural language query is translated to Cypher

    Parameters:
    -----------
    query_text : str
        The natural language query
    """
    print(f"Original query: {query_text}")

    # Process the query text
    processed_query = nlp_processor.process_text(query_text)

    # Get entities and intents
    entities = processed_query.get('entities', [])
    intents = processed_query.get('intents', [])

    print("\nIdentified entities:")
    for entity in entities:
        print(f"  - {entity['type']}: {entity['text']}")

    print("\nIdentified intents:")
    for intent in intents:
        print(f"  - {intent}")

    # Translate to Cypher
    cypher_query, params = query_translator.translate_to_cypher(processed_query)

    print(f"\nTranslated Cypher: {cypher_query}")
    if params:
        print("\nParameters:")
        for key, value in params.items():
            print(f"  - {key}: {value}")

    # Explain the translation
    explanation = query_translator.explain_translation(processed_query)

    print("\nExplanation:")
    print(explanation)

# Example query to explain
explain_translation("Show me all image files created by Alice in the last week")
```

## 4. Advanced Query Techniques

Now let's explore more advanced natural language queries:

```python
# Advanced queries
advanced_queries = [
    "Show me all microscopy images with exposure time greater than 100ms",
    "Find files that contain data about protein expression in cancer cells",
    "Which experiments have the most complete metadata?",
    "Show me the relationship between file size and creation date",
    "Find all files related to experiment EXP-2023-001 and show their metadata"
]

# Process each advanced query
for query in advanced_queries:
    result = process_query(query)

    if result['success'] and result['results'] is not None:
        print("\nResults:")
        display(result['results'].head(10))  # Display first 10 rows
        print(f"Total results: {len(result['results'])}")

        # For some queries, create visualizations
        if "relationship between" in query.lower():
            if 'file_size' in result['results'].columns and 'creation_date' in result['results'].columns:
                plt.figure(figsize=(10, 6))
                plt.scatter(result['results']['creation_date'], result['results']['file_size'])
                plt.title('Relationship between File Size and Creation Date')
                plt.xlabel('Creation Date')
                plt.ylabel('File Size (bytes)')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
    else:
        print(f"\nError: {result.get('message', 'Unknown error')}")

    print("\n" + "-"*50 + "\n")
```

### Combining Natural Language with Filters

We can combine natural language queries with specific filters:

```python
# Function to query with filters
def query_with_filters(base_query, filters):
    """
    Combine a natural language query with specific filters

    Parameters:
    -----------
    base_query : str
        The base natural language query
    filters : dict
        Dictionary of filters to apply

    Returns:
    --------
    dict
        Dictionary containing query results and metadata
    """
    print(f"Base query: {base_query}")
    print("Filters:")
    for key, value in filters.items():
        print(f"  - {key}: {value}")

    # Process the base query
    processed_query = nlp_processor.process_text(base_query)

    # Add filters to the processed query
    processed_query['filters'] = filters

    # Translate to Cypher
    cypher_query, params = query_translator.translate_to_cypher(processed_query)

    print(f"\nTranslated Cypher: {cypher_query}")

    # Execute the query
    if cypher_query:
        results = graph.run_query(cypher_query, parameters=params)

        # Convert results to a DataFrame for easier handling
        if results:
            df = pd.DataFrame([dict(record) for record in results])
            return {
                'original_query': base_query,
                'filters': filters,
                'cypher_query': cypher_query,
                'results': df,
                'success': True
            }
        else:
            return {
                'original_query': base_query,
                'filters': filters,
                'cypher_query': cypher_query,
                'results': None,
                'success': False,
                'message': 'No results found'
            }
    else:
        return {
            'original_query': base_query,
            'filters': filters,
            'cypher_query': None,
            'results': None,
            'success': False,
            'message': 'Could not translate query to Cypher'
        }

# Example query with filters
base_query = "Show me files"
filters = {
    "file_type": "image",
    "creation_date_after": "2023-01-01",
    "size_greater_than": 1000000  # 1MB
}

filtered_result = query_with_filters(base_query, filters)

if filtered_result['success'] and filtered_result['results'] is not None:
    print("\nResults:")
    display(filtered_result['results'].head(10))
    print(f"Total results: {len(filtered_result['results'])}")
else:
    print(f"\nError: {filtered_result.get('message', 'Unknown error')}")
```

## 5. Building a Conversational Interface

Now let's build a simple conversational interface for interacting with our knowledge graph:

```python
# Conversation context manager
class ConversationContext:
    def __init__(self):
        self.context = {
            'entities': {},
            'previous_queries': [],
            'current_focus': None
        }

    def update_context(self, query_text, processed_query, results):
        # Store the query
        self.context['previous_queries'].append({
            'text': query_text,
            'processed': processed_query,
            'results': results
        })

        # Update entities in context
        if 'entities' in processed_query:
            for entity in processed_query['entities']:
                self.context['entities'][entity['type']] = entity['text']

        # Update current focus if results contain specific types
        if results is not None and not results.empty:
            if 'file_type' in results.columns:
                self.context['current_focus'] = 'files'
            elif 'collection_name' in results.columns:
                self.context['current_focus'] = 'collections'
            elif 'experiment_id' in results.columns:
                self.context['current_focus'] = 'experiments'

    def get_context_for_query(self, query_text):
        # Process the new query
        processed_query = nlp_processor.process_text(query_text)

        # Check for references to previous context
        has_context_reference = any(word in query_text.lower() for word in ['these', 'those', 'them', 'it', 'this'])

        # If the query references previous context, add relevant information
        if has_context_reference and self.context['current_focus']:
            processed_query['context'] = {
                'focus': self.context['current_focus'],
                'entities': self.context['entities']
            }

        return processed_query

# Initialize conversation context
conversation = ConversationContext()

# Function to process a conversational query
def process_conversation(query_text):
    """
    Process a query in a conversational context

    Parameters:
    -----------
    query_text : str
        The natural language query

    Returns:
    --------
    dict
        Dictionary containing query results and metadata
    """
    print(f"You: {query_text}")

    # Get context-aware processed query
    processed_query = conversation.get_context_for_query(query_text)

    # Translate to Cypher
    cypher_query, params = query_translator.translate_to_cypher(processed_query)

    # Execute the query
    if cypher_query:
        print(f"System (thinking): Executing Cypher: {cypher_query}")
        results = graph.run_query(cypher_query, parameters=params)

        # Convert results to a DataFrame
        if results:
            df = pd.DataFrame([dict(record) for record in results])

            # Update conversation context
            conversation.update_context(query_text, processed_query, df)

            # Generate a natural language response
            if len(df) == 0:
                response = "I couldn't find any results matching your query."
            elif len(df) == 1:
                response = f"I found 1 result matching your query."
            else:
                response = f"I found {len(df)} results matching your query."

            # Add details about the results
            if len(df) > 0:
                if 'file_type' in df.columns:
                    file_types = df['file_type'].value_counts()
                    file_type_str = ", ".join([f"{count} {file_type} files" for file_type, count in file_types.items()])
                    response += f" This includes {file_type_str}."

            print(f"System: {response}")

            # Display results
            if not df.empty:
                display(df.head(5))
                if len(df) > 5:
                    print(f"... and {len(df) - 5} more results.")

            return {
                'original_query': query_text,
                'cypher_query': cypher_query,
                'results': df,
                'response': response,
                'success': True
            }
        else:
            response = "I couldn't find any results matching your query."
            print(f"System: {response}")
            return {
                'original_query': query_text,
                'cypher_query': cypher_query,
                'results': None,
                'response': response,
                'success': False,
                'message': 'No results found'
            }
    else:
        response = "I'm sorry, I couldn't understand your query. Could you rephrase it?"
        print(f"System: {response}")
        return {
            'original_query': query_text,
            'cypher_query': None,
            'results': None,
            'response': response,
            'success': False,
            'message': 'Could not translate query to Cypher'
        }

# Example conversation
conversation_queries = [
    "Show me all microscopy images",
    "How many of them have metadata?",
    "Which ones are the largest?",
    "Show me the metadata for the largest one",
    "Are there any other files related to the same experiment?"
]

# Process the conversation
for query in conversation_queries:
    result = process_conversation(query)
    print("\n")
```

## 6. Customizing the NLP Engine for Domain-Specific Terminology

Research data often contains domain-specific terminology. Let's customize the NLP engine to better understand these terms:

```python
# Function to add domain-specific terminology to the NLP engine
def add_domain_terminology(nlp_processor, terminology_dict):
    """
    Add domain-specific terminology to the NLP engine

    Parameters:
    -----------
    nlp_processor : NLPProcessor
        The NLP processor to customize
    terminology_dict : dict
        Dictionary mapping terms to their entity types
    """
    print("Adding domain-specific terminology:")
    for term, entity_type in terminology_dict.items():
        print(f"  - {term}: {entity_type}")
        nlp_processor.add_entity(term, entity_type)

    # Retrain the NLP model with the new entities
    nlp_processor.retrain()

    print("NLP engine updated with domain-specific terminology")

# Example domain-specific terminology for microscopy
microscopy_terms = {
    "confocal": "microscope_type",
    "widefield": "microscope_type",
    "TIRF": "microscope_type",
    "STED": "microscope_type",
    "two-photon": "microscope_type",
    "objective": "microscope_component",
    "40x": "magnification",
    "63x": "magnification",
    "100x": "magnification",
    "NA": "numerical_aperture",
    "exposure time": "acquisition_parameter",
    "z-stack": "acquisition_mode",
    "time-lapse": "acquisition_mode",
    "DAPI": "fluorophore",
    "GFP": "fluorophore",
    "mCherry": "fluorophore",
    "Alexa488": "fluorophore",
    "Alexa594": "fluorophore",
    "Alexa647": "fluorophore"
}

# Add the terminology to the NLP processor
add_domain_terminology(nlp_processor, microscopy_terms)

# Test the customized NLP engine with domain-specific queries
domain_queries = [
    "Show me all confocal microscopy images",
    "Find images with 63x magnification",
    "Which files contain GFP and DAPI channels?",
    "Show me all time-lapse experiments",
    "Find images with exposure time less than 100ms"
]

# Process each domain-specific query
for query in domain_queries:
    # Process the query text to see entity recognition
    processed_query = nlp_processor.process_text(query)

    print(f"\nQuery: {query}")
    print("Recognized entities:")
    for entity in processed_query.get('entities', []):
        print(f"  - {entity['text']}: {entity['type']}")

    # Translate and execute
    result = process_query(query)

    if result['success'] and result['results'] is not None:
        print("\nResults:")
        display(result['results'].head(5))
        print(f"Total results: {len(result['results'])}")
    else:
        print(f"\nError: {result.get('message', 'Unknown error')}")

    print("\n" + "-"*50 + "\n")
```

## Summary

In this tutorial, we've demonstrated how to:

1. Set up the NLP environment for natural language interaction with your knowledge graph
2. Process basic natural language queries and translate them to Cypher
3. Use advanced query techniques for more complex questions
4. Build a conversational interface that maintains context
5. Customize the NLP engine for domain-specific terminology

Natural language interaction makes your knowledge graph more accessible to researchers who may not be familiar with graph query languages like Cypher. By providing an intuitive interface for querying and exploring research data, you can help researchers gain insights more quickly and efficiently.

## Next Steps

To continue exploring the Science Data Kit, check out these additional tutorials:

- [Advanced Graph Queries](graph_queries.md): Write and execute advanced queries against the knowledge graph
- [Data Visualization](data_visualization.md): Create interactive visualizations of your research data
- [Custom NLP Development](custom_nlp.md): Develop custom NLP models for specific research domains

You can also refer to the [User Guide for Trainees](../docs/user_guide_trainees.md) for more information on using natural language interaction with your research data.
