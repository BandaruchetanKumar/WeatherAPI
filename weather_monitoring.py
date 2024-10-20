
import requests
import time
from datetime import datetime
from pymongo import MongoClient
import config

def fetch_weather_data(city):
    params = {
        'q': city,
        'appid': config.API_KEY,
        'units': 'metric'  # This will return temperature in Celsius
    }
    response = requests.get(config.BASE_URL, params=params)
    return response.json()

def store_weather_data(data):
    client = MongoClient(config.MONGO_URI)
    db = client[config.DB_NAME]
    collection = db['weather_data']
    collection.insert_one(data)
    client.close()

def process_weather_data():
    for city in config.CITIES:
        try:
            weather_data = fetch_weather_data(city)
            processed_data = {
                'city': city,
                'main': weather_data['weather'][0]['main'],
                'temp': weather_data['main']['temp'],
                'feels_like': weather_data['main']['feels_like'],
                'dt': datetime.fromtimestamp(weather_data['dt'])
            }
            store_weather_data(processed_data)
            print(f"Stored weather data for {city}")
        except Exception as e:
            print(f"Error processing data for {city}: {str(e)}")

def main():
    while True:
        process_weather_data()
        time.sleep(config.UPDATE_INTERVAL)

if __name__ == "__main__":
    main()
