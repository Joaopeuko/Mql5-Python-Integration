#!/bin/bash

# Script to build documentation for MQPy

# Export Python path to include the project root directory
export PYTHONPATH=$(pwd)

# Install required packages if needed
if [ "$1" == "--install" ]; then
    echo "Installing required packages..."
    pip install mkdocs mkdocs-material mkdocstrings mkdocs-gen-files mkdocs-literate-nav mkdocs-section-index mkdocstrings-python mkdocs-jupyter
fi

# Create necessary directories
mkdir -p docs/reference
mkdir -p docs/css

# Build the documentation
echo "Building documentation..."
mkdocs build

# If the build was successful, optionally serve
if [ $? -eq 0 ]; then
    echo "Documentation built successfully."
    
    if [ "$1" == "--serve" ] || [ "$2" == "--serve" ]; then
        echo "Serving documentation at http://localhost:8000"
        mkdocs serve
    fi
else
    echo "Error building documentation."
fi 