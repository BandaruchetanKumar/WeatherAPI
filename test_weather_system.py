import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import visualizations  # Ensure your visualizations module is correctly imported

class TestWeatherMonitoringSystem(unittest.TestCase):

    @patch('visualizations.plot_temperature_trends')
    @patch('visualizations.plot_weather_conditions')
    def test_generate_visualizations(self, mock_plot_weather_conditions, mock_plot_temperature_trends):
        # Mock data
        weather_data = [
            {'city': 'Delhi', 'temperature': 30, 'humidity': 60, 'description': 'Clear', 'timestamp': datetime.now()},
            {'city': 'Mumbai', 'temperature': 28, 'humidity': 70, 'description': 'Cloudy', 'timestamp': datetime.now()}
        ]
        
        # Call the function
        visualizations.generate_visualizations(weather_data)
        
        # Assert that the mocked functions were called
        mock_plot_temperature_trends.assert_called_once()
        mock_plot_weather_conditions.assert_called_once()

    def test_get_daily_summary(self):
        # Mock data
        mock_data = [
            {'city': 'Delhi', 'temperature': 30, 'humidity': 60, 'description': 'Clear', 'timestamp': datetime(2024, 10, 13, 12, 0)},
            {'city': 'Mumbai', 'temperature': 28, 'humidity': 70, 'description': 'Cloudy', 'timestamp': datetime(2024, 10, 13, 12, 0)}
        ]
        
        # Call the function
        summary = visualizations.get_daily_summary(mock_data)
        
        # Assert the result
        self.assertIsInstance(summary, str)
        self.assertIn('Delhi', summary)
        self.assertIn('Mumbai', summary)

    @patch('visualizations.send_email')
    def test_process_alerts(self, mock_send_email):
        # Mock data
        mock_data = [
            {'city': 'Delhi', 'temperature': 36, 'humidity': 60, 'description': 'Clear', 'timestamp': datetime.now()},
            {'city': 'Mumbai', 'temperature': 37, 'humidity': 70, 'description': 'Cloudy', 'timestamp': datetime.now()}
        ]
        
        # Call the function
        visualizations.process_alerts(mock_data)
        
        # Assert that send_email was called
        mock_send_email.assert_called_once()

    @patch('visualizations.MongoClient')
    def test_store_weather_data(self, mock_mongo_client):
        # Mock data
        mock_data = {'city': 'Delhi', 'temperature': 30, 'humidity': 60, 'description': 'Clear', 'timestamp': datetime.now()}
        
        # Mock MongoDB client
        mock_client = MagicMock()
        mock_mongo_client.return_value.__enter__.return_value = mock_client
        mock_db = mock_client['Cluster0']
        mock_collection = mock_db['weather_data']
        
        # Call the function
        visualizations.store_weather_data(mock_data)
        
        # Assert that insert_one was called with the mock data
        mock_collection.insert_one.assert_called_once_with(mock_data)

if __name__ == "__main__":
    unittest.main()