
# OpenWeatherMap API configuration
#API_KEY = 'c58dd38a02712c6285ab806d0043d670'
#BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# MongoDB configuration
#MONGO_URI = 'mongodb+srv://Hello:NAjILWe6evsp7QP8@cluster0.s2q4o.mongodb.net/'
#DB_NAME = 'Hello'

# OpenWeatherMap API configuration
API_KEY = 'c58dd38a02712c6285ab806d0043d670'  # Replace with your valid OpenWeatherMap API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# MongoDB configuration
MONGO_URI = 'mongodb+srv://Hello:NAjILWe6evsp7QP8@cluster0.s2q4o.mongodb.net'  # Replace <username> and <password> with actual credentials
DB_NAME = 'Cluster0'  # Change 'Hello' to a more relevant name if required

# List of Indian metros
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

# Alert configuration
TEMP_THRESHOLD = 35  # Celsius
CONSECUTIVE_ALERTS = 2  # Number of consecutive high-temperature alerts before sending an email

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your_email@gmail.com'  # Replace with your email
SENDER_PASSWORD = 'your_app_password'  # Replace with an app-specific password (Google requires this if you have 2FA enabled)
RECIPIENT_EMAIL = 'recipient_email@example.com'  # Replace with the recipient's email

# Data update interval (in seconds)
UPDATE_INTERVAL = 300  # 5 minutes
