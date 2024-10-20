
# OpenWeatherMap API configuration
API_KEY = 'c58dd38a02712c6285ab806d0043d670'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# MongoDB configuration
MONGO_URI = 'mongodb://localhost:27017/'
DB_NAME = 'weather_monitoring'

# List of Indian metros
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

# Alert configuration
TEMP_THRESHOLD = 35  # Celsius
CONSECUTIVE_ALERTS = 2

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your_email@gmail.com'
SENDER_PASSWORD = 'your_app_password'
RECIPIENT_EMAIL = 'recipient_email@example.com'

# Data update interval (in seconds)
UPDATE_INTERVAL = 300  # 5 minutes