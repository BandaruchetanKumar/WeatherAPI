import requests
import time
from datetime import datetime
from pymongo import MongoClient
import config

# Function to fetch weather data from OpenWeatherMap API
def fetch_weather_data(city):
    params = {
        'q': city,
        'appid': config.API_KEY,
        'units': 'metric'  # Return temperature in Celsius
    }
    try:
        response = requests.get(config.BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for 4XX/5XX errors
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for {city}: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred for {city}: {err}")
    return None

# Function to store weather data into MongoDB
def store_weather_data(data):
    try:
        client = MongoClient(config.MONGO_URI)
        db = client[config.DB_NAME]
        collection = db['weather_data']
        collection.insert_one(data)
        client.close()
    except Exception as e:
        print(f"Error storing data: {str(e)}")

# Function to process and save weather data for each city
def process_weather_data():
    for city in config.CITIES:
        weather_data = fetch_weather_data(city)
        if weather_data:
            try:
                processed_data = {
                    'city': city,
                    'main': weather_data['weather'][0]['main'],
                    'temp': weather_data['main']['temp'],
                    'feels_like': weather_data['main']['feels_like'],
                    'dt': datetime.fromtimestamp(weather_data['dt']),
                }
                store_weather_data(processed_data)
                print(f"Stored weather data for {city}")
            except KeyError as e:
                print(f"Missing data in response for {city}: {str(e)}")
        else:
            print(f"No weather data returned for {city}")

# Main function to continuously update weather data
def main():
    while True:
        process_weather_data()
        print("Waiting for the next update...")
        time.sleep(config.UPDATE_INTERVAL)

# Run the main function
if __name__ == "__main__":
    main()
