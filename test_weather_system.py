
import unittest
from unittest.mock import patch, MagicMock
from pymongo import MongoClient
from datetime import datetime
import config
import weather_monitoring
import data_processing
import visualizations
import alert_system

class TestWeatherMonitoringSystem(unittest.TestCase):

    def setUp(self):
        self.mongo_client = MongoClient(config.MONGO_URI)
        self.db = self.mongo_client[config.DB_NAME + '_test']

    def tearDown(self):
        self.mongo_client.drop_database(config.DB_NAME + '_test')
        self.mongo_client.close()

    @patch('weather_monitoring.requests.get')
    def test_fetch_weather_data(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'weather': [{'main': 'Clear'}],
            'main': {'temp': 25, 'feels_like': 26},
            'dt': 1622555555
        }
        mock_get.return_value = mock_response

        result = weather_monitoring.fetch_weather_data('TestCity')
        self.assertEqual(result['weather'][0]['main'], 'Clear')
        self.assertEqual(result['main']['temp'], 25)

    def test_store_weather_data(self):
        test_data = {
            'city': 'TestCity',
            'main': 'Clear',
            'temp': 25,
            'feels_like': 26,
            'dt': datetime.now()
        }
        weather_monitoring.store_weather_data(test_data)

        stored_data = self.db['weather_data'].find_one({'city': 'TestCity'})
        self.assertIsNotNone(stored_data)
        self.assertEqual(stored_data['main'], 'Clear')

    def test_get_daily_summary(self):
        # Insert test data
        test_data = [
            {'city': 'TestCity', 'main': 'Clear', 'temp': 25, 'dt': datetime(2023, 6, 1, 12, 0)},
            {'city': 'TestCity', 'main': 'Cloudy', 'temp': 22, 'dt': datetime(2023, 6, 1, 18, 0)}
        ]
        self.db['weather_data'].insert_many(test_data)

        summary = data_processing.get_daily_summary(datetime(2023, 6, 1).date())
        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0]['_id'], 'TestCity')
        self.assertAlmostEqual(summary[0]['avg_temp'], 23.5)

    @patch('alert_system.send_email')
    def test_process_alerts(self, mock_send_email):
        test_data = [
            {'city': 'HotCity', 'temp': config.TEMP_THRESHOLD + 1, 'dt': datetime.now()},
            {'city': 'CoolCity', 'temp': config.TEMP_THRESHOLD - 1, 'dt': datetime.now()}
        ]
        self.db['weather_data'].insert_many(test_data)

        alert_system.process_alerts()
        mock_send_email.assert_called_once()

    @patch('matplotlib.pyplot.savefig')
    def test_generate_visualizations(self, mock_savefig):
        test_data = [
            {'date': datetime(2023, 6, 1).date(), 'city': 'TestCity', 'avg_temp': 25, 'max_temp': 30, 'min_temp': 20, 'dominant_weather': 'Clear'},
            {'date': datetime(2023, 6, 2).date(), 'city': 'TestCity', 'avg_temp': 26, 'max_temp': 31, 'min_temp': 21, 'dominant_weather': 'Cloudy'}
        ]
        self.db['daily_summaries'].insert_many(test_data)

        visualizations.generate_visualizations()
        self.assertEqual(mock_savefig.call_count, len(config.CITIES) * 2)  # Two plots for each city

if __name__ == '__main__':
    unittest.main()
