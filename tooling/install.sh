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
python3 -m venv api
if [ $? -ne 0 ]; then
    echo "Error: Failed to create python venv." >&2
    exit 1
fi

# Install requirements
echo "Installing python requirements"
source api/bin/activate
echo "Current working directory: $(pwd)"
pip install -r requirements.txt 
if [ $? -ne 0 ]; then
    echo "Error: Failed to install python requirements." >&2
    exit 1
fi
echo "Requirements installed successfully"

# Get user input for the codeapi, ask if they want to build or pull from dockerhub
echo "Do you want to build the codeapi from source or pull from dockerhub?"
echo "Building from source allows you to install custom python, nodejs & apt packages, modify the files in codeapi/docker for that. Building will take several minutes."
echo "Pulling from dockerhub will pull the latest image from dockerhub."
echo "1. Build from source"
echo "2. Pull from dockerhub"
read -p "Enter your choice: " choice

if [ $choice -eq 1 ]; then
    # Make docker image for code api
    cd codeapi/docker
    echo "Building docker image for codeapi/docker"
    docker build -t codeapi .
    if [ $? -ne 0 ]; then
        echo "Error: Failed to build docker image for codeapi." >&2
        exit 1
    fi
    echo "Docker image for codeapi built."
    cd ../../
else
    echo "Pulling codeapi from dockerhub"
    docker pull martianhannah/codeapi
    docker tag martianhannah/codeapi codeapi
    if [ $? -ne 0 ]; then
        echo "Error: Failed to pull codeapi from dockerhub." >&2
        exit 1
    fi
    echo "Codeapi pulled from dockerhub"
fi

# Setting up Vue
echo "Setting up Vue"
cd magma
npm install
if [ $? -ne 0 ]; then
    echo "Error: Failed to install npm requirements." >&2
    exit 1
fi
cd ..

echo "Backend installed successfully"

echo "To start the backend, run the following commands:"
echo "source api/bin/activate"
echo "cd api && python3 api/app.py"
echo "To start the frontend, run the following commands:"
echo "cd magma && npm run dev"
