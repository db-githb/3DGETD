#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

compare_versions() {
    if [ "$(printf '%s\n' "$1" "$2" | sort -V | head -n1)" = "$2" ]; then
        return 0  # v1 >= v2
    else
        return 1  # v1 < v2
    fi
}

# Get user input for package manager
while true; do
	read -p "Choose package manager (pip or conda): " package_manager
	if [[ "$package_manager" == "pip" || "$package_manager" == "conda" ]]; then
		package_manager=${package_manager}
		echo "Selected package manager: $package_manager"
		break
	else
		echo "Invalid input. Try again. (Note: Ensure all lowercase.)"
    fi
done

OS=$(uname)

# Detect OS
if [[ "$OS" == "Linux" ]]; then
	OS="linux"
    echo "Linux system detected."
elif [[ "$OS" == "Darwin" ]]; then
    echo "MacOS system detected. This tool is unavailable for MacOS. Please use Linux or Windows."
	exit 1
elif [[ "$OS" == "CYGWIN"* || "$OS" == "MINGW"* ]]; then
	OS="windows"
    echo "Windows system detected."
else
    echo "Unknown operating system: $OS.  Please use Linux or Windows."
	exit 1
fi

echo "operating_system="$OS > log.txt

# Store package manager selection in log file for executable script
echo "package_manager=$package_manager" >> log.txt

# Construct the script name
script_name="./env_setup_scripts/${package_manager}_setup_${OS}.sh"

# Check if nvcc is installed
if ! command_exists nvcc; then
    echo "CUDA is not installed or nvcc is not found in PATH."
    exit 1
fi

# Get the CUDA version
CUDA_VERSION=$(nvcc --version | grep -oP "release \K[0-9]+\.[0-9]+")
if [ -z "$CUDA_VERSION" ]; then
    echo "Unable to detect CUDA version."
    exit 1
fi
echo "CUDA version detected: $CUDA_VERSION"

# Adjust CUDA version format for PyTorch compatibility
CUDA_VERSION=${CUDA_VERSION}

# Retrieve Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+\.\d+')
echo "Python version detected: $PYTHON_VERSION"

TORCH_VERSION=2.5

# Ensure compatible Torch and CUDA versions

# torch >=3.9 AND CUDA >= 11.8 AND !(CUDA >=12.4)
if compare_versions "$PYTHON_VERSION" "3.9" && \
   compare_versions "$CUDA_VERSION" "11.8" && \
   ! compare_versions "$CUDA_VERSION" "12.4"; then
    TORCH_VERSION=2.5
	echo "Using pytorch: 2.5"
elif compare_versions "$PYTHON_VERSION" "3.8" && \
     compare_versions "$CUDA_VERSION" "11.8" && \
     ! compare_versions "$CUDA_VERSION" "12.1"; then
    TORCH_VERSION=2.4
	echo "Using pytorch: 2.4"
elif compare_versions "$PYTHON_VERSION" "3.8" && \
	 ! compare_versions "$PYTHON_VERSION" "3.11" && \
     compare_versions "$CUDA_VERSION" "11.7"; then
    TORCH_VERSION=2.4
	echo "Using pytorch: 2.5"
elif ! compare_versions "$PYTHON_VERSION" "3.8"; then
    echo "Python $PYTHON_VERSION incompatible; must be >= 3.8"
	sleep 2s
    exit 1
elif ! compare_versions "$CUDA_VERSION" "11.8"; then
    echo "CUDA $CUDA_VERSION incompatible; must be >= 11.7"
	sleep 2s
    exit 1
else
    echo "Configuration not supported."
	sleep 5s
    exit 1
fi

echo "Using Torch version: $TORCH_VERSION"

if [[ "$package_manager" == "conda" ]]; then
	# Check if conda is installed
	if ! command_exists conda; then
	    echo "Conda is not installed or not found in PATH."
		sleep 5s
	    exit 1
	fi

	# Create the Conda environment
	echo "Creating Conda environment '3DGETD' with Python $PYTHON_VERSION, numpy, pillow, PySide6, pytorch=$TORCH_VERSION, pytorch-cuda=$CUDA_VERSION"
	conda create -n 3DGETD python="$PYTHON_VERSION" numpy pillow conda-forge::pyside6 pytorch="$TORCH_VERSION" pytorch-cuda="$CUDA_VERSION" -c pytorch -c nvidia -y
	if [ $? -ne 0 ]; then
	    echo "Failed to create Conda environment or install packages."
	    exit 1
	fi

	echo "Environment '3DGETD' setup completed successfully!"

elif [[ "$package_manager" == "pip" ]]; then

	# Check if Pip is installed
	if ! command_exists pip; then
	    echo "Pip is not installed or not found in PATH."
	    exit 1
	fi

	# Create the Pip environment
	CUDA_VERSION=${CUDA_VERSION//./} # Remove the dot, e.g., 12.1 -> 121
	echo "Creating virtual environment '3DGETD' with Python $PYTHON_VERSION, numpy, pillow, PySide6==6.8.0.2, and torch (cuda enabled) from https://download.pytorch.org/whl/cu$CUDA_VERSION"
	python3 -m venv 3DGETD
	source 3DGETD/bin/activate
	pip install PySide6==6.8.0.2
	pip install numpy pillow torch --index-url https://download.pytorch.org/whl/cu"$CUDA_VERSION"

	if [ $? -ne 0 ]; then
	    echo "Failed to create environment or install packages."
	    exit 1
	fi

	echo "Environment '3DGETD' setup completed successfully!"
fi

# Ensure run scripts is executable
chmod +x run_3dgetd.sh 






	
