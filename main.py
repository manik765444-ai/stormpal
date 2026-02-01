**main.py**
```python
import argparse
import logging
from weather_client import WeatherClient

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Weather CLI tool")
    parser.add_argument("-c", "--city", type=str, help="City to retrieve weather for")
    parser.add_argument("-u", "--units", type=str, default="metric", choices=["metric", "imperial"], help="Units to display temperature in")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    return parser.parse_args()

def configure_logging(verbose):
    """Configure logging."""
    logging.basicConfig(level=logging.INFO if not verbose else logging.DEBUG)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

def main():
    """Main entry point of the application."""
    args = parse_args()
    configure_logging(args.verbose)

    try:
        client = WeatherClient()
        weather = client.get_weather(args.city, args.units)
        print(f"Weather in {args.city}:")
        print(f"  Temperature: {weather['temperature']}{weather['unit']}")
        print(f"  Description: {weather['description']}")
        print(f"  Humidity: {weather['humidity']}%")
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    main()
```

**weather_client.py**
```python
import logging
import requests

API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # replace with your own API key

class WeatherClient:
    """Client for retrieving weather data from OpenWeatherMap."""

    def __init__(self):
        """Initialize the client."""
        self.session = requests.Session()

    def get_weather(self, city, units):
        """Retrieve weather data for a given city."""
        params = {
            "q": city,
            "appid": API_KEY,
            "units": units
        }

        response = self.session.get(API_URL, params=params)
        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error retrieving weather data: {e}")
            raise

        data = response.json()
        temperature = data["main"]["temp"]
        unit = "°C" if units == "metric" else "°F"
        description = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]

        return {
            "temperature": temperature,
            "unit": unit,
            "description": description,
            "humidity": humidity
        }
```

**requirements.txt**
```
requests