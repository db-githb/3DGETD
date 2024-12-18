#!/bin/bash

# Define the log file
log_file="log.txt"

# Check if the log file exists
if [[ -f "$log_file" ]]; then
    # load the log file to load the variable into the current script
    package_manager=$(grep "^package_manager=" "$log_file" | cut -d '=' -f 2)
    operating_system=$(grep "^operating_system=" "$log_file" | cut -d '=' -f 2)

else
    echo "Log file $log_file that stores user's package_manager choice does not exist.  Did you run setup_script.sh?"
    sleep 1s
    exit 1
fi

echo -n "Activating virtual environment..."
if [[ $package_manager == "conda" ]]; then

    # >>> Conda Initialize >>>
    # !! Contents within this block are managed by 'conda init' !!
    if command -v conda &> /dev/null; then
        eval "$(conda shell.bash hook)"
    else
        echo "Conda is not installed or not in your PATH."
        sleep 1s
        return 1
    fi
    # <<< Conda Initialize <<<

    conda activate 3DGETD
    echo " ✔"

elif [[ $package_manager == "pip" && $operating_system == "linux" ]]; then
    source 3DGETD/bin/activate
    echo " ✔"
elif [[ $package_manager == "pip" && $operating_system == "windows" ]]; then
    source 3DGETD/Scripts/activate
    echo " ✔"
else
    echo "✘"
    echo "Failed to activate environment.  Have you run setup_3dgetd.sh?"
    sleep 1s
    exit 1
fi

# Run the Python script in the background
python 3dgetd.py & pid=$! # Process Id of the previous running command

spin=('[    ]' '[=   ]' '[==  ]' '[=== ]' '[ ===]' '[  ==]' '[   =]')

i=0
while kill -0 $pid 2>/dev/null; do
  # Use the current frame from the spinner array
  echo -ne "\rRunning 3DGETD ${spin[i]}"
  
  # Increment and reset the spinner index
  i=$(( (i + 1) % ${#spin[@]} ))
  
  # Add a delay
  sleep 0.2
done
echo
# Deactivate virtual environment
echo -n "Deactivating virtual environment..."
if [[ $package_manager == "conda" ]]; then
    conda deactivate
    echo " ✔"
elif [[ $package_manager == "pip" ]]; then
    deactivate
    echo " ✔"
else
    echo "Failed to deactivate virtual environment"
    echo -e "\rDeactivating virtual environment... ✘"
fi
echo "Goodbye!"
