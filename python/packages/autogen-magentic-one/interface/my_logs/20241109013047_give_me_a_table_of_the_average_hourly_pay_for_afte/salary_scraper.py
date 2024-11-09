# filename: salary_scraper.py

import requests
from bs4 import BeautifulSoup

def scrape_salary_data(city):
    url = f"https://www.glassdoor.com/Salaries/{city}-afterschool-educator-salary-SRCH_IL.0,7_IM{city_id}.htm"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    salary_info = soup.find_all('div', class_='css-1bluz6i e1wijj242')
    if salary_info:
        salary_text = salary_info[0].text.strip()
        print(f"{city}: {salary_text}")
    else:
        print(f"Salary data for {city} not found.")

cities = {
    "Houston": "1126943",
    "San-Antonio": "1139761",
    "Dallas": "1139977",
    "Austin": "1139761",
    "Fort-Worth": "1140202",
    "El-Paso": "1140176",
    "Arlington": "1140028",
    "Corpus-Christi": "1140113",
    "Plano": "1140181",
    "Laredo": "1139886"
}

for city, city_id in cities.items():
    scrape_salary_data(city)