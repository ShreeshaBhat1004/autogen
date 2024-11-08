# filename: save_seattle_weather.py

weather_info = """
Current Seattle Weather:
- Condition: Partly sunny
- Temperature: 59°F
- Wind: 8 MPH
- Humidity: 59%
"""

with open("seattle_weather.txt", "w") as file:
    file.write(weather_info)

print("Weather information saved to seattle_weather.txt")