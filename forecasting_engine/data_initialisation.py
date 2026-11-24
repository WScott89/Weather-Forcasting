from dataclasses import dataclass

@dataclass
class WeatherData:
    """Class for storing weather data. Holds temperature, humidity, wind_speed,
    wind_direction, precipitation and air_pressure."""
    temperature: int
    humidity: int
    wind_speed: int
    wind_direction: int
    precipitation: int
    pressure: int

@dataclass
class WeatherNode:
    """Stores the position and weather data for a given Node."""
    longitude: str
    latitude: str
    height: str
    name: str = None
    node_id: int
    weather_data: WeatherData
