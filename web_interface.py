
from flask import Flask, render_template_string, jsonify
from pymongo import MongoClient
import config
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def get_mongo_client():
    return MongoClient(config.MONGO_URI)

@app.route('/')
def index():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather Monitoring Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h1>Weather Monitoring Dashboard</h1>
        <div>
            <h2>Latest Weather Data</h2>
            <ul id="latest-data"></ul>
        </div>
        <div>
            <h2>Temperature Trends</h2>
            <canvas id="tempChart"></canvas>
        </div>
        <script>
            function fetchLatestData() {
                fetch('/api/latest')
                    .then(response => response.json())
                    .then(data => {
                        const ul = document.getElementById('latest-data');
                        ul.innerHTML = '';
                        data.forEach(item => {
                            ul.innerHTML += `<li>${item.city}: ${item.temp}°C, ${item.main}</li>`;
                        });
                    });
            }

            function fetchTempTrends() {
                fetch('/api/temp_trends')
                    .then(response => response.json())
                    .then(data => {
                        const ctx = document.getElementById('tempChart').getContext('2d');
                        new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: data.dates,
                                datasets: data.cities.map(city => ({
                                    label: city,
                                    data: data.temps[city],
                                    fill: false
                                }))
                            },
                            options: {
                                responsive: true,
                                title: {
                                    display: true,
                                    text: 'Temperature Trends'
                                },
                                scales: {
                                    x: {
                                        display: true,
                                        title: {
                                            display: true,
                                            text: 'Date'
                                        }
                                    },
                                    y: {
                                        display: true,
                                        title: {
                                            display: true,
                                            text: 'Temperature (°C)'
                                        }
                                    }
                                }
                            }
                        });
                    });
            }

            fetchLatestData();
            fetchTempTrends();
            setInterval(fetchLatestData, 300000); // Update every 5 minutes
        </script>
    </body>
    </html>
    """)

@app.route('/api/latest')
def get_latest_data():
    client = get_mongo_client()
    db = client[config.DB_NAME]
    collection = db['weather_data']
    
    latest_data = list(collection.find(
        {},
        {'_id': 0, 'city': 1, 'temp': 1, 'main': 1}
    ).sort([('dt', -1)]).limit(len(config.CITIES)))
    
    client.close()
    return jsonify(latest_data)

@app.route('/api/temp_trends')
def get_temp_trends():
    client = get_mongo_client()
    db = client[config.DB_NAME]
    collection = db['daily_summaries']
    
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    
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
    
    results = list(collection.aggregate(pipeline))
    client.close()
    
    dates = list(set([r['date'].strftime('%Y-%m-%d') for r in results]))
    dates.sort()
    
    temps = {city: [] for city in config.CITIES}
    for date in dates:
        for city in config.CITIES:
            city_data = next((r for r in results if r['date'].strftime('%Y-%m-%d') == date and r['city'] == city), None)
            temps[city].append(city_data['avg_temp'] if city_data else None)
    
    return jsonify({
        'dates': dates,
        'cities': config.CITIES,
        'temps': temps
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
