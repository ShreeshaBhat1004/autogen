# filename: save_weather_data.py

weather_data = """Austin, Texas:
66°F
Wind: 10 MPH
Humidity: 68%
Mostly cloudy - Updated at 5:29 PM, Nov 8, 2023."""

with open("austin_weather.txt", "w") as file:
    file.write(weather_data)

print("Weather data saved to austin_weather.txt")