import os
import pytest
from src.test2.openweathermap.api import CityNotFoundError, NotAuthorizedError, OpenWeatherMapAPI


if not os.environ.get("OPENWEATHERMAP_KEY"):
    pytest.skip("set OPENWEATHERMAP_KEY environment variable to test weather functions", allow_module_level=True)


def test_openweathermap_api():
    api = OpenWeatherMapAPI(os.environ["OPENWEATHERMAP_KEY"])
    weather = api.get_weather_for_city("London")

    assert weather.city == "London"


def test_openweathermap_api_wrong_key():
    api = OpenWeatherMapAPI("a")
    with pytest.raises(NotAuthorizedError):
        api.get_weather_for_city("London")


def test_openweathermap_api_no_city():
    assume_this_city_does_not_exist = "afdsghfgdhfshgfgjvmjhxcgvyuxfu"
    api = OpenWeatherMapAPI(os.environ["OPENWEATHERMAP_KEY"])
    with pytest.raises(CityNotFoundError):
        api.get_weather_for_city(assume_this_city_does_not_exist)
