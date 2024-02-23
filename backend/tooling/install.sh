#!/bin/bash

# Check if python3 is installed
if ! [ -x "$(command -v python3)" ]; then
    echo "Error: python3 is not installed." >&2
    exit 1
fi

# Check if docker is installed
if ! [ -x "$(command -v docker)" ]; then
    echo "Error: docker is not installed." >&2
    exit 1
fi

# Create venv
echo "Creating venv"
cd ..
python3 -m venv backend
if [ $? -ne 0 ]; then
    echo "Error: Failed to create python venv." >&2
    exit 1
fi
source backend/bin/activate
cd backend

# Install requirements
echo "Installing python requirements"
pip install -r requirements.txt 
if [ $? -ne 0 ]; then
    echo "Error: Failed to install python requirements." >&2
    exit 1
fi
echo "Requirements installed successfully"

# Make docker image for code api
cd codeapi/docker
echo "Building docker image for codeapi/docker"
docker build -t codeapi .
if [ $? -ne 0 ]; then
    echo "Error: Failed to build docker image for codeapi." >&2
    exit 1
fi
echo "Docker image for codeapi built."


echo "Backend installed successfully"
