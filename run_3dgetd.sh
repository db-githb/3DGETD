#!/bin/bash

# >>> Conda Initialize >>>
# !! Contents within this block are managed by 'conda init' !!
if command -v conda &> /dev/null; then
    eval "$(conda shell.bash hook)"
else
    echo "Conda is not installed or not in your PATH."
    return 1
fi
# <<< Conda Initialize <<<

# Define the log file
log_file="log.txt"

# Check if the log file exists
if [[ -f "$log_file" ]]; then
    # load the log file to load the variable into the current script
    package_manager=$(grep "^package_manager=" "$log_file" | cut -d '=' -f 2)
    OS=$(grep "^operating_system=" "$log_file" | cut -d '=' -f 2)

else
    echo "Log file $log_file that stores user's package_manager choice does not exist.  Did you run setup_script.sh?"
    exit 1
fi

echo -n "Activating virtual environment..."
if [[ $package_manager=="conda" ]]; then
    conda activate 3DGETD
    echo -e "\rActivating virtual environment... ✔"

elif [[ $package_manager=="pip" && $OS=="Linux" ]]; then
    source 3DGETD/bin/activate
    echo -e "\rActivating virtual environment... ✔"

elif [[ $package_manager=="pip" && $OS=="Window" ]]; then
    3DGETD\Scripts\activate
    echo -e "\rActivating virtual environment... ✔"

else
    echo "Failed to activate environment."
    echo -e "\rActivating virtual environment... ✘"
fi

# Run the Python script in the background
python 3dgetd.py & pid=$! # Process Id of the previous running command

spin='-\|/'

i=0
while kill -0 $pid 2>/dev/null
do
  i=$(( (i+1) %4 ))
  printf "\rRunning 3DGETD %c" "${spin:$i:1}"
  sleep .1
done
echo
echo "Goodbye!"
