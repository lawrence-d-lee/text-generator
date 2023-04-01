import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import urllib
import time
import concurrent.futures
import random
import os



def get_json(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    relevant_part = soup.find_all("script")
    json_text = relevant_part[5].text.replace("window.jsonModel = ", "")
    required_json = json.loads(json_text)
    return required_json


def get_region_code(location):
    response = requests.get(
        "https://www.rightmove.co.uk/house-prices/" + location + ".html"
    )
    soup = BeautifulSoup(response.content, "html.parser")
    relevant_part = soup.find_all("script")[3]
    json_text = relevant_part.text.replace("window.__PRELOADED_STATE__ = ", "")
    required_json = json.loads(json_text)
    return required_json["searchLocation"]["locationId"]


def create_url(
    location,
    min_price="",
    max_price="",
    min_bedrooms="",
    max_bedrooms="",
    min_bathrooms="",
    max_bathrooms="",
    radius="",
    property_type="",
    index="",
):
    base_url = "https://www.rightmove.co.uk/property-for-sale/find.html?"
    location_code = get_region_code(location)
    params = {
        "searchType": "SALE",
        "locationIdentifier": "REGION^" + location_code,
        "radius": radius,
        "minPrice": min_price,
        "maxPrice": max_price,
        "minBedrooms": min_bedrooms,
        "maxBedrooms": max_bedrooms,
        "minBathrooms": min_bathrooms,
        "maxBathrooms": "",
        "propertyTypes": property_type,
        "index": index,
    }
    final_url = base_url + urllib.parse.urlencode(params)
    return final_url


def json_to_df(json):
    df = pd.DataFrame(columns=["Summary"])
    for i in range(len(json["properties"])):
        df.loc[i] = [
            json["properties"][i]["summary"],
        ]
    return df


def create_url_list(
    location,
    min_price="",
    max_price="",
    min_bedrooms="",
    max_bedrooms="",
    min_bathrooms="",
    max_bathrooms="",
    radius="",
    property_type="",
):
    def get_index(i):
        return create_url(
            location,
            min_price,
            max_price,
            min_bedrooms,
            max_bedrooms,
            min_bathrooms,
            max_bathrooms,
            radius,
            property_type,
            index=24 * (i - 1),
        )

    url_list = []
    threads = 30
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor = executor.map(get_index, range(43))
        for url in executor:
            url_list.append(url)
    return url_list


def download_jsons(url_list):
    threads = min(30, len(url_list))
    json_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor = executor.map(get_json, url_list)
        for json in executor:
            json_list.append(json)
        return json_list


def create_df(jsons):
    df = pd.DataFrame(columns=["Summary"])
    for json in jsons:
        new_df = json_to_df(json)
        df = pd.concat([df, new_df], ignore_index=True, axis=0)
    return df.drop_duplicates()


def create_table(
    location,
    min_price="",
    max_price="",
    min_bedrooms="",
    max_bedrooms="",
    min_bathrooms="",
    max_bathrooms="",
    radius="",
    property_type="",
):
    return create_df(
        download_jsons(
            create_url_list(
                location,
                min_price,
                max_price,
                min_bedrooms,
                max_bedrooms,
                min_bathrooms,
                max_bathrooms,
                radius,
                property_type,
            )
        )
    )


def create_full_table(city_list):
    df = pd.DataFrame(columns=["Summary"])
    for city in city_list:
        new_df = create_table(city)
        df = pd.concat([df, new_df], ignore_index=True, axis=0)
        time.sleep(random.randint(5, 10))
        print(city + " is loaded")
    return df.drop_duplicates()


city_list = [
    "Aberdeen",
    "Bath",
    "Bangor"
    "Birmingham",
    "Bradford",
    "Brighton",
    "Bristol",
    "Cambridge",
    "Canterbury",
    "Cardiff",
    "Carlisle",
    "Chelmsford",
    "Chester",
    "Chichester",
    "Colchester",
    "Coventry",
    "Derby",
    "Doncaster",
    "Dundee",
    "Dunfermline",
    "Durham",
    "Edinburgh",
    "Ely",
    "Exeter",
    "Glasgow",
    "Gloucester",
    "Hereford",
    "Hull",
    "Inverness",
    "Lancaster",
    "Leeds",
    "Leicester",
    "Lichfield",
    "Lincoln",
    "Liverpool",
    "London",
    "Manchester",
    "Milton-Keynes",
    "Newcastle-upon-Tyne",
    "Newport",
    "Norwich",
    "Nottingham",
    "Oxford",
    "Perth",
    "Peterborough",
    "Plymouth",
    "Portsmouth",
    "Preston",
    "St-Asaph",
    "St-Davids",
    "Stirling",
    "Swansea",
    "Truro",
    "Wakefield",
    "Wells",
    "Winchester",
    "Wolverhampton",
    "Worcester",
    "Wrexham",
    "York",
]

estate_agent_data = create_full_table(city_list)

estate_agent_data.to_csv(os.getcwd() + "estate_agent_data", index=False)
