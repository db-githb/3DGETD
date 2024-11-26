# Define the log file
log_file="log.txt"

# Check if the log file exists
if [[ -f "$log_file" ]]; then
    # Source the log file to load the variable into the current script
    pm=$(grep "^package_manager=" "$log_file" | cut -d '=' -f 2)

    # Use the retrieved value
    echo "Retrieved value: $pm"
else
    echo "Log file $log_file does not exist."
    exit 1
fi

