from dataclasses import dataclass
import json
from typing import Literal
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen


@dataclass
class Weather:
    city: str
    temperature: int
    description: str | None


class CityNotFoundError(Exception):
    pass


class NotAuthorizedError(Exception):
    pass


class OpenWeatherMapAPI:
    def __init__(self, api_key: str, units: Literal["standard", "metric", "imperial"] = "metric"):
        self._api_key = api_key
        self._units = units

    def get_weather_for_city(self, city: str) -> Weather:
        endpoint = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": self._api_key, "units": self._units}

        try:
            with urlopen(endpoint + "?" + urlencode(params)) as res:
                data = json.load(res)
                return Weather(
                    city=data["name"],
                    temperature=int(data["main"]["temp"]),
                    description=None if len(data["weather"]) == 0 else data["weather"][0]["description"],
                )
        except HTTPError as e:
            if e.code == 404:
                raise CityNotFoundError()
            elif e.code == 401:
                raise NotAuthorizedError()
            raise
