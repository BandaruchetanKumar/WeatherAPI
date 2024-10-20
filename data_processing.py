#NAjILWe6evsp7QP8
from pymongo import MongoClient
from datetime import datetime, timedelta
import config

def get_daily_summary(date):
    client = MongoClient(config.MONGO_URI)
    db = client[config.DB_NAME]
    collection = db['weather_data']

    start_date = datetime.combine(date, datetime.min.time())
    end_date = start_date + timedelta(days=1)

    pipeline = [
        {
            '$match': {
                'dt': {'$gte': start_date, '$lt': end_date}
            }
        },
        {
            '$group': {
                '_id': '$city',
                'avg_temp': {'$avg': '$temp'},
                'max_temp': {'$max': '$temp'},
                'min_temp': {'$min': '$temp'},
                'weather_conditions': {'$push': '$main'}
            }
        }
    ]

    results = list(collection.aggregate(pipeline))

    for result in results:
        # Find the dominant weather condition
        weather_counts = {}
        for condition in result['weather_conditions']:
            weather_counts[condition] = weather_counts.get(condition, 0) + 1
        dominant_weather = max(weather_counts, key=weather_counts.get)

        result['dominant_weather'] = dominant_weather
        del result['weather_conditions']

    client.close()
    return results

def store_daily_summary(date, summary):
    client = MongoClient(config.MONGO_URI)
    db = client[config.DB_NAME]
    collection = db['daily_summaries']

    for city_summary in summary:
        document = {
            'date': date,
            'city': city_summary['_id'],
            'avg_temp': city_summary['avg_temp'],
            'max_temp': city_summary['max_temp'],
            'min_temp': city_summary['min_temp'],
            'dominant_weather': city_summary['dominant_weather']
        }
        collection.insert_one(document)

    client.close()

def process_daily_summaries():
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    summary = get_daily_summary(yesterday)
    store_daily_summary(yesterday, summary)
    print(f"Processed and stored daily summary for {yesterday}")

if __name__ == "__main__":
    process_daily_summaries()
