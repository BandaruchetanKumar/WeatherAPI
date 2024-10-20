#!/bin/bash

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> weather_system.log
}

# Start the weather monitoring system
log_message "Starting weather monitoring system"
python3 weather_monitoring.py &
WEATHER_PID=$!

# Wait for 10 minutes to collect some data
log_message "Waiting for 10 minutes to collect initial data"
sleep 600

# Process daily summaries
log_message "Processing daily summaries"
if python3 data_processing.py; then
    log_message "Daily summaries processed successfully"
else
    log_message "Error processing daily summaries"
fi

# Generate visualizations
log_message "Generating visualizations"
if python3 visualizations.py; then
    log_message "Visualizations generated successfully"
else
    log_message "Error generating visualizations"
fi

# Check and send alerts
log_message "Checking and sending alerts"
if python3 alert_system.py; then
    log_message "Alerts processed successfully"
else
    log_message "Error processing alerts"
fi

# Run tests
log_message "Running tests"
if python3 test_weather_system.py; then
    log_message "All tests passed successfully"
else
    log_message "Some tests failed"
fi

# Start the web interface
log_message "Starting web interface"
python3 web_interface.py &
WEB_PID=$!

log_message "Web interface started. Access it at http://localhost:5000"

# Wait for user input to stop the system
read -p "Press Enter to stop the weather monitoring system and web interface..."

# Stop the weather monitoring system and web interface
log_message "Stopping weather monitoring system and web interface"
kill $WEATHER_PID
kill $WEB_PID

log_message "Weather monitoring system tasks completed"
