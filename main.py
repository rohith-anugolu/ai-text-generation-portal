import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.scrapethissite.com/pages/simple/"

def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print("Exception occured while requesting the url.\n", e)

    content = BeautifulSoup(response.text, "html.parser")
    return content

def extract_countries(html_content: BeautifulSoup):
    countries = []
    countries_html = html_content.find_all('div', class_="country")

    for country in countries_html:
        country_name = country.find("h3", class_="country-name").get_text(strip=True)
        capital = country.find("span", class_="country-capital").get_text(strip=True)
        population = country.find("span", class_="country-population").get_text(strip=True)
        area = country.find("span", class_="country-area").get_text(strip=True)

        # print(country_name, capital, population, area)
        countries.append({
            "Name": country_name,
            "Capital": capital,
            "Population": population,
            "Area": area
        })

    df = pd.DataFrame(countries)
    return df


def main():
    html_content = get_html_content(URL)
    countries_df = extract_countries(html_content)
    # write df content to csv
    countries_df.to_csv('countries.csv', index=False)

if __name__ == "__main__":
    main()
