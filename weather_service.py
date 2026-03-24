import requests

class WeatherService:
    """
    Connects to the weather API to get temperature information.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast"

    def get_forecast_scores(self, city_name, days=3):
        """Gets weather for a few days and converts it to a 1-5 score."""
        params = {'q': city_name, 'appid': self.api_key, 'units': 'metric'}
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            daily_scores = []
            # The API gives weather every 3 hours (8 times a day)
            for i in range(0, days * 8, 8):
                if i < len(data['list']):
                    temp = data['list'][i]['main']['temp']
                    daily_scores.append(self._convert_to_score(temp))
            return daily_scores
        except Exception as e:
            print(f"Error fetching forecast: {e}")
            return None

    def get_weather_score(self, city_name):
        """Gets the weather score for just today."""
        scores = self.get_forecast_scores(city_name, days=1)
        return scores[0] if scores else None

    def _convert_to_score(self, temp):
        """
        Changes real temperature numbers into a simple 1 to 5 scale.
        1 is very cold, 5 is very hot.
        """
        if temp < 10: return 1
        elif temp < 18: return 2
        elif temp < 25: return 3
        elif temp < 30: return 4
        else: return 5