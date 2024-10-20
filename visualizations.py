import matplotlib.pyplot as plt
from pymongo import MongoClient
from datetime import datetime, timedelta
import config

def convert_date(date_obj):
    """Convert a datetime.date to datetime.datetime."""
    return datetime.combine(date_obj, datetime.min.time())

def get_data_for_visualization(days=7):
    # Use context manager to ensure MongoClient is properly closed
    with MongoClient(config.MONGO_URI) as client:
        db = client[config.DB_NAME]
        collection = db['daily_summaries']

        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)

        # Convert dates to datetime for MongoDB query
        start_date = convert_date(start_date)
        end_date = convert_date(end_date)

        pipeline = [
            {
                '$match': {
                    'date': {'$gte': start_date, '$lte': end_date}
                }
            },
            {
                '$sort': {'date': 1}
            }
        ]

        try:
            results = list(collection.aggregate(pipeline))
            return results
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return []

def plot_temperature_trends(data):
    for city in config.CITIES:
        city_data = [item for item in data if item['city'] == city]
        dates = [item['date'] for item in city_data]
        avg_temps = [item['avg_temp'] for item in city_data]
        max_temps = [item['max_temp'] for item in city_data]
        min_temps = [item['min_temp'] for item in city_data]

        plt.figure(figsize=(10, 6))
        plt.plot(dates, avg_temps, label='Average Temperature')
        plt.plot(dates, max_temps, label='Maximum Temperature')
        plt.plot(dates, min_temps, label='Minimum Temperature')
        
        plt.title(f'Temperature Trends for {city}')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig(f'{city}_temperature_trends.png')
        plt.close()

def plot_weather_conditions(data):
    for city in config.CITIES:
        city_data = [item for item in data if item['city'] == city]
        conditions = [item['dominant_weather'] for item in city_data]
        
        condition_counts = {}
        for condition in conditions:
            condition_counts[condition] = condition_counts.get(condition, 0) + 1

        plt.figure(figsize=(8, 8))
        plt.pie(condition_counts.values(), labels=condition_counts.keys(), autopct='%1.1f%%')
        plt.title(f'Dominant Weather Conditions for {city}')
        
        plt.savefig(f'{city}_weather_conditions.png')
        plt.close()

def generate_visualizations():
    data = get_data_for_visualization()
    if data:  # Check if data is not empty
        plot_temperature_trends(data)
        plot_weather_conditions(data)
        print("Visualizations generated successfully.")
    else:
        print("No data available for visualizations.")

if __name__ == "__main__":
    generate_visualizations()
