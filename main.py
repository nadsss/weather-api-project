
import os
import requests

from dotenv import load_dotenv
from dataclasses import dataclass


# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# Class for storing weather information
class Weather:

    def __init__(self, city, temperature, humidity,
                 description, wind_speed):

        self.city = city
        self.temperature = temperature
        self.humidity = humidity
        self.description = description
        self.wind_speed = wind_speed


def get_weather(city: str) -> Weather:

    # Prepare request parameters
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    # Send GET request
    response = requests.get(
        BASE_URL,
        params=params,
        timeout=10
    )

    # Check whether request was successful
    response.raise_for_status()

    # Parse JSON response
    data = response.json()

    # Create Weather object
    weather = Weather(
        city=data["name"],
        temperature=data["main"]["temp"],
        humidity=data["main"]["humidity"],
        description=data["weather"][0]["description"],
        wind_speed=data["wind"]["speed"]
    )

    return weather


def print_weather(weather: Weather):

    print("\n" + "=" * 35)
    print(f"       WEATHER REPORT")
    print("=" * 35)

    print(f"City:        {weather.city}")
    print(f"Temperature: {weather.temperature} °C")
    print(f"Humidity:    {weather.humidity}%")
    print(f"Conditions:  {weather.description}")
    print(f"Wind Speed:  {weather.wind_speed} m/s")

    print("=" * 35)


def main():

    if not API_KEY:
        print("Error: API_KEY is missing from .env")
        return

    city = input("Enter a city name: ")

    try:
        weather = get_weather(city)
        print_weather(weather)

    except requests.exceptions.HTTPError as error:
        print(f"API error: {error}")

    except requests.exceptions.RequestException as error:
        print(f"Connection error: {error}")

    except (KeyError, IndexError, ValueError) as error:
        print(f"Invalid API response: {error}")


if __name__ == "__main__":
    main()
