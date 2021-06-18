import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
import pandas as pd
from functions.get_single_apartment import single_apartment


# Specifying the target url from SAHIBINDEN
def get_apartments(pagingOffset):
    # getting the page offset
    target_list_url = ''
    for counter, offset in enumerate(range(0, int(pagingOffset), 50)):
        if counter == 0:
            target_list_url = "https://www.sahibinden.com/en/for-sale/owner?pagingSize=50&address_region=1&viewType=List&price_min=300000&address_town=431&address_city=34"
        else:
            target_list_url = "https://www.sahibinden.com/en/for-sale/owner?pagingOffset=" + str(
                offset) + "&pagingSize=50&address_region=1&viewType=List&price_min=300000&address_town=431&address_city=34"
        payload = {}
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,tr-TR;q=0.8,tr;q=0.7",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": "vid=357; cdid=wTYNHg2d19h06lQY5fd35232; MS1=https://www.google.com/; __gads=ID=25c6356a74bc7524:T=1610112088:S=ALNI_Mb8hkwgxObsjo7D2UFWCJXenDZ1Lg; _fbp=fb.1.1610112087601.193556605; _ga=GA1.2.909703944.1610112087; showPremiumBanner=false; userLastSearchSplashClosed=true; showCookiePolicy=true; nwsh=fct; myPriceHistorySplashClosed=1; acc_type=bireysel_uye; kno=a5RXpJxy-5frrTYih2w2LLg; st=a4cabe82b5e5c4f8d942fd2ce672c1207de55842925f8f24e793838c076cad9c2e392c1f837dd6a7564a0025967684c246e460e0ac1371f90; segIds=; _gid=GA1.2.1315204118.1610873259",
            "Host": "www.sahibinden.com",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        }
        time.sleep(15)
        response = requests.request("GET", target_list_url, headers=headers, data=payload)
        # Using BeautifulSoup for getting data
        soup = BeautifulSoup(response.text, 'lxml')
        apartment_ad = soup.find_all('tr', class_='searchResultsItem listView')
        my_apartment = {}
        with open("mapping/locations.json", encoding='utf-8') as locations:
            location = json.load(locations)
        with open('data.json', encoding='utf-8') as f:
            temp = json.load(f).keys()
        # Loop for going through received data from properties list
        for apartment_item in apartment_ad:
            # Checking if Apartment exists in json file
            apartment_id = apartment_item['data-id']
            if apartment_id in temp:
                print("Apartment Exists with id : ", apartment_id)
            else:
                apartment_title = apartment_item.find("a", class_="classifiedTitle").text.strip()
                apartment_price = int(
                    apartment_item.find("td", class_="searchResultsPriceValue").text.strip().replace('TL', '')
                        .replace(',', '').replace(' ', ''))
                apartment_date_string = apartment_item.find("td", class_="searchResultsDateValue").text.strip()
                apartment_date_datetime = datetime.strptime(apartment_date_string, '%d %B %Y')
                apartment_location_district = apartment_item.find("td", class_="searchResultsLocationValue").contents[
                    0].strip()
                print(apartment_location_district)
                my_apartment[apartment_id] = {"title": apartment_title, "price": apartment_price,
                                              "date": str(apartment_date_datetime),
                                              "location": apartment_location_district
                                              }
                print("New Apartment Found with id : ", apartment_id)
            # Writing data into a json file.
        with open("data.json", "r+", encoding="utf-8") as json_file:
            data = json.load(json_file)
            data.update(my_apartment)
            json_file.seek(0)
            json.dump(data, json_file, indent=4, ensure_ascii=False)
