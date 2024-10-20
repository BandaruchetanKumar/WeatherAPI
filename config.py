
# OpenWeatherMap API configuration
#API_KEY = 'c58dd38a02712c6285ab806d0043d670'
#BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# MongoDB configuration
#MONGO_URI = 'mongodb+srv://Hello:NAjILWe6evsp7QP8@cluster0.s2q4o.mongodb.net/'
#DB_NAME = 'Hello'

# OpenWeatherMap API configuration
API_KEY = 'your_api_key'  # Replace with your valid OpenWeatherMap API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# MongoDB configuration
MONGO_URI = 'mongodb+srv://<username>:<password>@cluster0.mongodb.net'  # Replace <username> and <password> with actual credentials
DB_NAME = 'weather_db'  # Change 'weather_db' to a more relevant name if required

# List of Indian metros
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

# Alert configuration
TEMP_THRESHOLD = 35  # Celsius
CONSECUTIVE_ALERTS = 2  # Number of consecutive high-temperature alerts before sending an email

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'bandaruchetankumar@gmail.com'  # Replace with your email
SENDER_PASSWORD = 'Chetankumar891#'  # Replace with an app-specific password (Google requires this if you have 2FA enabled)
RECIPIENT_EMAIL = 'bandaruchetan16@example.com'  # Replace with the recipient's email

# Data update interval (in seconds)
UPDATE_INTERVAL = 300  # 5 minutes
