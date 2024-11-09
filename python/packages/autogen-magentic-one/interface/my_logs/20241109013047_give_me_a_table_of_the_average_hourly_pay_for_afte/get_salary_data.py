# filename: get_salary_data.py
import requests

def get_salary_data(city):
    url = "https://api.indeed.com/ads/apisearch"
    params = {
        "q": "afterschool educator",
        "l": city + ", TX",
        "userip": "1.2.3.4",  # Use a dummy IP
        "useragent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "format": "json",
        "v": "2",  # Version of the API
        "publisher": "YOUR_PUBLISHER_ID_HERE",  # Replace with your Indeed Publisher ID
        }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        jobs = data.get("results", [])
        total_salary = 0
        salary_count = 0
        for job in jobs:
            if 'salary' in job and job['salary']:
                try:
                    salary = int(job['salary'].replace('$', '').replace(',', ''))
                    total_salary += salary
                    salary_count += 1
                except ValueError:
                    continue
        if salary_count > 0:
            return total_salary / salary_count
        else:
            return "No salary data found"
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"

cities = ["Houston", "Dallas", "Austin", "San Antonio", "Fort Worth", "El Paso"]

for city in cities:
    average_salary = get_salary_data(city)
    print(f"The average hourly pay for afterschool educators in {city} is: {average_salary}")