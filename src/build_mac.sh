#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Installing Python..."
    brew install python@3.12  # Adjust Python version if needed
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip is not installed. Installing pip..."
    python3 -m ensurepip
fi

# Check if virtualenv is installed
if ! command -v virtualenv &> /dev/null; then
    echo "virtualenv is not installed. Installing virtualenv..."
    pip3 install virtualenv
fi

# Create and activate virtual environment
echo "Creating and activating virtual environment..."
if [ ! -d "myenv" ]; then
    virtualenv -p python3 myenv
fi
source myenv/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install -r requirements.txt

# Install Nuitka
echo "Installing Nuitka..."
pip install nuitka

# Build the Python application using Nuitka
echo "Building application with Nuitka..."
python -m nuitka \
    --standalone \
    --macos-create-app-bundle \
    --macos-app-icon=mac.icns \
    main.py

# Clean up
deactivate
echo "Build completed."
