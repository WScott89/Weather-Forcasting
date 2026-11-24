from dataclasses import dataclass

@dataclass
class WeatherData:
    """Class for storing weather data. Holds temperature, humidity, wind_speed,
    wind_direction, precipitation and air_pressure."""
    temperature: float
    humidity: float
    wind_speed: float
    wind_direction: int
    precipitation: float
    pressure: int

@dataclass
class WeatherNode:
    """Stores the position and weather data for a given Node."""
    longitude: float
    latitude: float
    height: str
    name: str = None
    node_id: int
    weather_data: WeatherData
