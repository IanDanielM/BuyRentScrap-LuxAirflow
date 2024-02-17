import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_data(url):
    new_url = url
    houses_list = []
    for i in range(1, 101):
        try:
            if i > 1:
                url = new_url+"?page={}".format(i)
            else:
                url = url

            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            houses_for_rent = soup.find_all('div', 'listing-card')
            for houses in houses_for_rent:
                titles = houses.find(
                    "span", "relative top-[2px] hidden md:inline").get_text(strip=True)
                location = houses.find(
                    "p", "ml-1 truncate text-sm font-normal capitalize text-grey-650").get_text(strip=True)
                size_ft = houses.find(
                    "div", "flex h-6 items-center rounded-full bg-highlight px-3 text-xs font-normal leading-4 text-grey-550 lg:text-sm")
                if size_ft:
                    square_ft = size_ft.get_text(strip=True)
                else:
                    square_ft = None
                bedrooms = houses.find(
                    "div", "flex h-6 items-center rounded-full bg-highlight px-3 text-xs font-medium leading-5")
                if bedrooms:
                    bedrooms = bedrooms.get_text(strip=True)
                else:
                    bedrooms = None
                bathrooms = houses.find(
                    "div", "flex h-6 items-center rounded-full bg-highlight px-3 text-xs font-medium leading-5")
                if bathrooms:
                    bathrooms = bathrooms.get_text(strip=True)
                else:
                    bathrooms = None
                house_prices = houses.find(
                    "div", "hidden justify-between md:flex").get_text(strip=True)
                prices = house_prices.replace('KSh ', '').replace(
                    '/ month', '').replace(',', '')
                link = houses.find(
                    attrs={'data-cy': 'listing-title-link'})['href']

                houses_list.append((titles, location, square_ft,
                                   bedrooms, bathrooms, prices, link))
        except Exception as e:
            print(e)
            continue

        return houses_list


def load_data(data, file_name):
    columns = ['Title', 'Location', 'Size',
               'Bedrooms', 'Bathrooms', 'Price', 'Link']
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(file_name, index=False)
