from __future__ import absolute_import
import time
import random

def create_data(start_id):
    """Generate a dictionary containing weather-related metrics for a location."""

    weather_data = {
        'id': start_id,
        'location': 'Central Park',
        'time': time.asctime(),
        'temperature': round(random.gauss(20, 2), 2), 
        'humidity': int(random.gauss(50, 10)),
        'wind_speed': round(random.gauss(10, 3), 2), 
        'barometric_pressure': round(random.gauss(1015, 5), 2),
        'precipitation': round(random.uniform(0, 20), 2), 
        'weather_condition': random.choice(['Sunny', 'Rainy', 'Cloudy', 'Snowy', 'Foggy'])
    }
    return weather_data

def print_data(data):
    """Print the data in a human-readable format."""
    print(f"Data ID: {data['id']}")
    print(f"Location: {data['location']}")
    print(f"Time: {data['time']}")
    print(f"Temperature: {data['temperature']}°C")
    print(f"Humidity: {data['humidity']}%")
    print(f"Wind Speed: {data['wind_speed']} km/h")
    print(f"Barometric Pressure: {data['barometric_pressure']} mbar")
    print(f"Precipitation: {data['precipitation']} mm")
    print(f"Weather Condition: {data['weather_condition']}")


if __name__ == "__main__":
    data = create_data()
    print_data(data)
