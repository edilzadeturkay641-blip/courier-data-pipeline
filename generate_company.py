import json
import random

cities = [
    "Baku",
    "Ganja",
    "Sumgait",
    "Mingachevir",
    "Shaki"
]

company_names = [
    "Bravo",
    "Araz",
    "Kontakt Home",
    "Irshad",
    "Wolt",
    "Bolt Food",
    "Starex",
    "Limak"
]

companies = []

for i, company_name in enumerate(company_names, start=1):

    company = {
        "company_id": i,
        "company_name": company_name,
        "city": random.choice(cities)
    }

    companies.append(company)

with open("data/companies.json", "w", encoding="utf-8") as file:
    json.dump(companies, file, indent=4, ensure_ascii=False)