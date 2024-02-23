#!/bin/bash

# Create venv
echo "Creating venv"
cd ..
python3 -m venv backend
source backend/bin/activate
cd backend

# Install requirements
echo "Installing requirements"
pip install -r requirements.txt

echo "Backend installed successfully"
