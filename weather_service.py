import requests

class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/forecast"

    def get_forecast_scores(self, city_name, days=3):
        """Fetches forecast and converts to 1-5 scores."""
        params = {'q': city_name, 'appid': self.api_key, 'units': 'metric'}
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            daily_scores = []
            # API returns data in 3-hour chunks (8 chunks per day)
            for i in range(0, days * 8, 8):
                if i < len(data['list']):
                    temp = data['list'][i]['main']['temp']
                    daily_scores.append(self._convert_to_score(temp))
            return daily_scores
        except Exception as e:
            print(f"Error fetching forecast: {e}")
            return None

    def get_weather_score(self, city_name):
        """Helper for today's current weather score."""
        scores = self.get_forecast_scores(city_name, days=1)
        return scores[0] if scores else None

    def _convert_to_score(self, temp):
        if temp < 10: return 1
        elif temp < 18: return 2
        elif temp < 25: return 3
        elif temp < 30: return 4
        else: return 5