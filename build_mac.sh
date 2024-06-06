#!/bin/bash

# Define variables
PYTHON_VERSION=3.12
VENV_DIR=myenvmac
REQUIREMENTS_FILE=requirements.txt
SETUP_SCRIPT=mac-setup.py

# Get the directory of the script
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Full path to the requirements file
REQUIREMENTS_PATH="$SCRIPT_DIR/$REQUIREMENTS_FILE"
SETUP_SCRIPT_PATH="$SCRIPT_DIR/$SETUP_SCRIPT"

# Function to check if a command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# Function to install Python using Homebrew
install_python_with_brew() {
    local version=$1
    if ! command_exists brew; then
        echo "Homebrew not found. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        # Add Homebrew to PATH
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi

    echo "Installing Python $version via Homebrew..."
    brew install python@$version
}

# Function to install Python from python.org
install_python_from_web() {
    local version=$1
    local py_installer="python-$version-macosx10.9.pkg"

    echo "Downloading Python $version installer from python.org..."
    curl -O "https://www.python.org/ftp/python/$version/$py_installer"

    echo "Installing Python $version..."
    sudo installer -pkg $py_installer -target /

    echo "Cleaning up installer..."
    rm $py_installer
}

# Function to check and install Python
install_python() {
    local version=$1

    # Try installing with Homebrew first
    if command_exists brew; then
        install_python_with_brew $version
    else
        echo "Homebrew not available. Attempting to install Python from python.org..."
        install_python_from_web $version
    fi
}

# Check if Python is installed
if ! command_exists python3; then
    echo "Python3 could not be found. Installing Python $PYTHON_VERSION..."
    install_python $PYTHON_VERSION
else
    echo "Python3 is already installed."
fi

# Ensure the correct Python version is used
export PATH="/usr/local/opt/python@$PYTHON_VERSION/bin:$PATH"
if ! command_exists python3; then
    echo "Failed to install Python. Exiting."
    exit 1
fi

# Check if virtual environment exists, if not, create it
if [ ! -d "$SCRIPT_DIR/$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$SCRIPT_DIR/$VENV_DIR"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$SCRIPT_DIR/$VENV_DIR/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies from requirements.txt
if [ -f "$REQUIREMENTS_PATH" ]; then
    echo "Installing dependencies from $REQUIREMENTS_PATH..."
    if ! pip install -r "$REQUIREMENTS_PATH"; then
        echo "Error installing dependencies from $REQUIREMENTS_PATH. Please check the file for errors."
        deactivate
        exit 1
    fi
else
    echo "$REQUIREMENTS_PATH not found. Ensure it is in the same directory as this script."
    deactivate
    exit 1
fi

# Run the setup script to build the macOS installer
if [ -f "$SETUP_SCRIPT_PATH" ]; then
    echo "Running setup script..."
    pushd "$SCRIPT_DIR" > /dev/null  # Change to the script's directory
    python "$SETUP_SCRIPT" bdist_mac
    popd > /dev/null  # Return to the original directory
else
    echo "$SETUP_SCRIPT_PATH not found. Ensure it is in the same directory as this script."
    deactivate
    exit 1
fi

echo "Build process completed."
deactivate
