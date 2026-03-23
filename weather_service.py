import requests

class WeatherService:
    """
    Handles external communication with the OpenWeatherMap API
    and normalizes meteorological data into a discrete scoring system.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast"

    def get_forecast_scores(self, city_name, days=3):
        """Fetches forecast data and converts raw temperatures into 1-5 suitability scores."""
        params = {'q': city_name, 'appid': self.api_key, 'units': 'metric'}
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            daily_scores = []
            # API returns forecast in 3-hour increments (8 chunks per 24 hours)
            for i in range(0, days * 8, 8):
                if i < len(data['list']):
                    temp = data['list'][i]['main']['temp']
                    daily_scores.append(self._convert_to_score(temp))
            return daily_scores
        except Exception as e:
            print(f"Error fetching forecast: {e}")
            return None

    def get_weather_score(self, city_name):
        """Retrieves current weather score for a single day context."""
        scores = self.get_forecast_scores(city_name, days=1)
        return scores[0] if scores else None

    def _convert_to_score(self, temp):
        """
        Normalizes continuous temperature data into discrete values (1-5).
        1: Freezing | 5: Very Hot
        """
        if temp < 10: return 1
        elif temp < 18: return 2
        elif temp < 25: return 3
        elif temp < 30: return 4
        else: return 5