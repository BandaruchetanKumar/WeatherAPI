import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pymongo import MongoClient
from datetime import datetime, timedelta
import config

def get_latest_weather_data():
    client = MongoClient(config.MONGO_URI)
    db = client[config.DB_NAME]
    collection = db['weather_data']

    pipeline = [
        {'$sort': {'dt': -1}},
        {'$group': {
            '_id': '$city',
            'latest_data': {'$first': '$$ROOT'}
        }},
        {'$replaceRoot': {'newRoot': '$latest_data'}}
    ]

    results = list(collection.aggregate(pipeline))
    client.close()
    return results

def check_alerts(data):
    alerts = []
    for city_data in data:
        if city_data['temp'] > config.TEMP_THRESHOLD:
            alerts.append(f"Alert: {city_data['city']} temperature ({city_data['temp']}°C) exceeds {config.TEMP_THRESHOLD}°C")
    return alerts

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = config.SENDER_EMAIL
    msg['To'] = config.RECIPIENT_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
        server.starttls()
        server.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

def process_alerts():
    latest_data = get_latest_weather_data()
    alerts = check_alerts(latest_data)

    if alerts:
        subject = "Weather Alert Notification"
        body = "\n".join(alerts)
        send_email(subject, body)
        print("Alerts processed and email sent")
    else:
        print("No alerts to process")

if __name__ == "__main__":
    process_alerts()
