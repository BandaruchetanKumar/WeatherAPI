
# Real-Time Weather Monitoring System

This project implements a real-time data processing system to monitor weather conditions and provide summarized insights using rollups and aggregates. The system utilizes data from the OpenWeatherMap API.

## Features

1. Continuous retrieval of weather data for Indian metros (Delhi, Mumbai, Chennai, Bangalore, Kolkata, Hyderabad)
2. Daily weather summaries with aggregates (average, maximum, minimum temperatures, dominant weather condition)
3. Alerting system for user-configurable temperature thresholds
4. Visualization of daily weather summaries and historical trends
5. Centralized configuration file for easy customization
6. Comprehensive test suite
7. Logging system for better debugging and monitoring
8. Web interface for easy visualization of weather data

## Project Structure

- `config.py`: Central configuration file for the entire system
- `weather_monitoring.py`: Main script for fetching and storing weather data
- `data_processing.py`: Script for processing daily summaries and aggregates
- `visualizations.py`: Script for generating weather visualizations
- `alert_system.py`: Script for checking and sending weather alerts
- `test_weather_system.py`: Unit tests for the weather monitoring system
- `run_weather_system.sh`: Shell script to run all components of the system
- `web_interface.py`: Flask web application for visualizing weather data

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/weather-monitoring-system.git
   cd weather-monitoring-system
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up MongoDB:
   - Install MongoDB on your system
   - Start the MongoDB service

4. Configure the system:
   - Open `config.py` and update the following:
     - OpenWeatherMap API key
     - MongoDB connection details
     - Email configuration for alerts
     - Temperature threshold for alerts
     - List of cities to monitor

## Running the System

To run the entire weather monitoring system, use the provided shell script:

```
chmod +x run_weather_system.sh
./run_weather_system.sh
```

This script will:
1. Start the weather monitoring system
2. Wait for initial data collection
3. Process daily summaries
4. Generate visualizations
5. Check and send alerts
6. Run the test suite
7. Start the web interface
8. Stop the weather monitoring system

The script includes logging, and all messages will be written to `weather_system.log`.

## Running Individual Components

You can also run individual components of the system:

1. Weather Monitoring:
   ```
   python weather_monitoring.py
   ```

2. Data Processing:
   ```
   python data_processing.py
   ```

3. Visualizations:
   ```
   python visualizations.py
   ```

4. Alert System:
   ```
   python alert_system.py
   ```

5. Tests:
   ```
   python test_weather_system.py
   ```

6. Web Interface:
   ```
   python web_interface.py
   ```

After starting the web interface, you can access the dashboard at `http://localhost:5000`.

## Customization

To customize the system's behavior, edit the `config.py` file. You can modify:

- API key
- MongoDB connection details
- List of cities to monitor
- Temperature threshold for alerts
- Email settings for alerts

## Future Improvements

1. Add support for more weather parameters (e.g., humidity, wind speed)
2. Implement machine learning models for weather prediction
3. Enhance the alerting system with more customizable rules
4. Improve the web interface with more interactive features and real-time updates

## License

This project is licensed under the MIT License - see the LICENSE file for details.
