#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if nvcc is installed
if ! command_exists nvcc; then
    echo "CUDA is not installed or nvcc is not found in PATH."
    exit 1
fi

# Get the CUDA version
echo "Checking CUDA version..."
CUDA_VERSION=$(nvcc --version | grep -oP "release \K[0-9]+\.[0-9]+")
if [ -z "$CUDA_VERSION" ]; then
    echo "Unable to detect CUDA version."
    exit 1
fi
echo "CUDA version detected: $CUDA_VERSION"

# Adjust CUDA version format for PyTorch compatibility
CUDA_VERSION=${CUDA_VERSION//./} # Remove the dot, e.g., 12.1 -> 121

# Check if conda is installed
if ! command_exists conda; then
    echo "Conda is not installed or not found in PATH."
    exit 1
fi

# Create the Conda environment
echo "Creating Conda environment '3DGETD' with Python 3.12, numpy, pillow, PySide6, and torch (cuda enabled)..."
python3 -m venv 3DGETD
source 3DGETD/bin/activate
pip install PySide6==6.8.0.2
pip install numpy pillow torch --index-url https://download.pytorch.org/whl/cu"$CUDA_VERSION"

if [ $? -ne 0 ]; then
    echo "Failed to create Conda environment or install packages."
    exit 1
fi

echo "Environment '3DGETD' setup completed successfully!"
