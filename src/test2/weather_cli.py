import os
from openweathermap.api import CityNotFoundError, NotAuthorizedError, OpenWeatherMapAPI


def main():
    API_KEY = os.environ["OPENWEATHERMAP_KEY"]

    welcome_message = """Weather CLI App
Shows current weather in your city. Powered by OpenWeatherMap
"""
    print(welcome_message)
    city = input("Enter your city: ")

    api = OpenWeatherMapAPI(API_KEY)

    try:
        weather = api.get_weather_for_city(city)

        print(f"It is currently {weather.temperature}°C in {weather.city}")
        if weather.description:
            print(f"Weather: {weather.description}")
    except CityNotFoundError:
        print("ERROR: Requested city was not found")
        exit(1)
    except NotAuthorizedError:
        print(
            "ERROR: Not authorized. Make sure you provide a valid OpenWeatherMap "
            + "token via OPENWEATHERMAP_KEY environment variable"
        )
        exit(1)


if __name__ == "__main__":
    main()
