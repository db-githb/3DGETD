#!/bin/bash

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

# Get user input for package manager
while true; do
	read -p "Choose package manager (pip or conda): " package_manager
	if [[ "$package_manager" == "pip" || "$package_manager" == "conda" ]]; then
		package_manager=${package_manager}
		echo $package_manager
		break
	else
		echo "Invalid input. Try again."
    fi
done

# Store package manager selection in log file for executable script
"package_manager="$package_manager > log.txt

# Construct the script name
script_name="./env_setup_scripts/${package_manager}_setup_${OS}.sh"

# Check if the script exists
if [[ -f "$script_name" ]]; then
    echo "Running script: $script_name"
    chmod +x "$script_name"  # Ensure the script is executable
    $script_name           # Execute the script
else
    echo "Error: Script '$script_name' not found."
    exit 1
fi

# Ensure run scripts is executable
chmod +x run_3dgetd.sh 






	
