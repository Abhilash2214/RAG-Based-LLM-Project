#!/bin/bash

echo "Setting up RAG Backend API..."

# Create virtual environment
python -m venv venv

# Activate virtual environment
if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate  # Windows
else
    source venv/bin/activate      # Linux/Mac
fi

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p uploads
mkdir -p users_data

echo "Setup complete! Run 'python app.py' to start the server."