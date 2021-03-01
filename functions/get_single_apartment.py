import csv
import json
import os.path
import sys
import time
from collections import defaultdict
from random import randint
import pandas as pd
import requests
from bs4 import BeautifulSoup
from random_user_agent.params import SoftwareName, OperatingSystem
from random_user_agent.user_agent import UserAgent


class FlowException(Exception):
    pass

def single_apartment():
    header_added = False
    with open(os.path.dirname(__file__) + '/../data.json', encoding='utf-8') as readData:
        jsonData = list(json.loads(readData.read()).keys())
        try:
            currentData = pd.read_csv('file.csv', usecols=["ad"]).stack().to_numpy().tolist()
            if currentData:
                for item in currentData:
                    if str(item) in jsonData:
                        print("found!")
                        jsonData.remove(str(item))
                        header_added = True
        except Exception as e:
            pass
    apartment_options = defaultdict(dict)
    for apt_number, ad_post_id in enumerate(jsonData):
        try:
            software_names = [SoftwareName.CHROME.value]
            operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
            user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems,
                                           limit=100)
            # Get Random User Agent String.
            user_agent = user_agent_rotator.get_random_user_agent()
            url = "https://www.sahibinden.com/en/kelime-ile-arama?query_text=" + ad_post_id
            headers = {
                "Host": "www.sahibinden.com",
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": user_agent,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
                "referer": "https://www.google.com/",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9,tr-TR;q=0.8,tr;q=0.7",
                "Cookie": "vid=357; cdid=wTYNHg2d19h06lQY5fd35232; MS1=https://www.google.com/; __gads=ID=25c6356a74bc7524:T=1610112088:S=ALNI_Mb8hkwgxObsjo7D2UFWCJXenDZ1Lg; _fbp=fb.1.1610112087601.193556605; _ga=GA1.2.909703944.1610112087; showPremiumBanner=false; userLastSearchSplashClosed=true; showCookiePolicy=true; nwsh=fct; myPriceHistorySplashClosed=1; segIds=; _gid=GA1.2.1315204118.1610873259; geoipCity=""; geoipIsp=ovh_sas; xsrf-token=1a6b3bfa546787ced2a2ad1e22d14981a2515521; st=a5455d420a9564d3987eeabf43e8290290fbdfd216a189a7ce98e52e8fdfa217e51bf836ec6e8aebe5c28e0ca1acc612509239d57321aeeb6; dp=1536*864-landscape; ulfuid=null; searchType=TEXT/ENTER/CLASSIC; _dc_gtm_UA-235070-1=1; _gali=searchSuggestionForm",
            }
            try:
                response = requests.request("GET", url, headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')
                apartment_content = soup.find("div", {"id": "classifiedDetail"})
                # Extracting Image URLs
                # print(apt_number,ad_post_id)
            except Exception as e:
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                raise FlowException("coudldn't get the classifiedDetail DIV",
                                    "Process Exception in line {}".format(line),
                                    e)
            try:
                apartment_images = apartment_content.find('div', {'class': 'classifiedDetailMainPhoto'})
                children = apartment_images.findChildren('label', {"id": lambda x: x and x.startswith('label_images')},
                                                         recursive=False)[:4]
                image_urls_list = []
                # print(ad_post_id)
                for counter, image in enumerate(children):
                    image_urls = image.find('img', {'alt': True})
                    if image_urls.has_attr('class'):
                        image_urls['data-src'] = image_urls['src']
                    image_urls_list.append(image_urls['data-src'].replace("x5_","big_"))
                image_urls_string = ','.join(image_urls_list)
                print(image_urls_string)
            except Exception as e:
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                print("couldn't get the Images,the add is either deleted or doesn't have pictures!")
                pass

            try:
                # Extracting Contents
                apartment_title_price = apartment_content.findChild('div', class_="classifiedInfo")
                apartment_location_names = apartment_title_price.find("h2").findChildren("a")
                del apartment_location_names[0]
                location_string = ','.join(
                    [location_name.text.strip().replace('.', '') for location_name in apartment_location_names])
                apartment_options[ad_post_id]["location"] = location_string
                # print(apartment_options)
                apartment_price = apartment_title_price.find('input',
                                                             {"id": "priceHistoryFlag"}).previousSibling.strip().replace(
                    ' TL',
                    '').replace(
                    ',', '')
                apartment_details = apartment_content.find('ul', class_="classifiedInfoList")
                apartment_owner = apartment_content.find('div', class_="classifiedUserContent")
                owner_registration_date = apartment_owner.find("p", class_="userRegistrationDate").findChild(
                    "span").text.strip()
                # print(owner_registration_date)
                apartment_owner_name = apartment_owner.findChild('h5').text

                try:
                    apartment_owner_phone = apartment_owner.find('span', class_="pretty-phone-part").text.replace('(',
                                                                                                                  '').replace(
                        ')', '').replace(' ', '')
                except:
                    apartment_owner_phone = ''
                apartment_location_map = apartment_content.find("div", {"data-lat": True})
                apartment_latitude = apartment_location_map['data-lat']
                apartment_longitude = apartment_location_map['data-lon']
                items = apartment_details.findChildren("li", {"class": False}, recursive=False)
                apartment_features = {}
                for item in items:
                    item_title = item.find("strong").text.strip().replace(' ', '_').lower()
                    item_value = item.find("span").text.lower().strip()
                    apartment_features.update({item_title: item_value})
                    apartment_options[ad_post_id][item_title] = item_value
                # print(apartment_options)
                apartment_amenities_soup = apartment_content.find('div', {"id": "classifiedProperties"})
                apartment_amenities_headings = apartment_amenities_soup.find_all("h3")
                headings = {}
                for heading in apartment_amenities_headings:
                    heading = heading.text
                    headings.update({heading: ''})
                for item_h in headings:
                    amenity_ul = apartment_amenities_soup.find("h3", text=item_h).find_next_sibling("ul").findChildren("li",
                                                                                                                       class_="selected")
                    amenity_ul_string = ','.join([item_li.text.strip() for item_li in amenity_ul])
                    apartment_options[ad_post_id][item_h] = amenity_ul_string
                apartment_options[ad_post_id]["price"] = int(apartment_price)
                apartment_options[ad_post_id]["map_lat"] = apartment_latitude
                apartment_options[ad_post_id]["map_lon"] = apartment_longitude
                apartment_options[ad_post_id]["owner_name"] = apartment_owner_name
                apartment_options[ad_post_id]["owner_phone"] = apartment_owner_phone
                apartment_options[ad_post_id]["owner_registration_date"] = owner_registration_date
                apartment_options[ad_post_id]["images"] = image_urls_string
                # print(apartment_options)
                header_names = list(apartment_options[ad_post_id].keys())
                # print(apartment_options)
                with open(os.path.dirname(__file__) + '/../file.csv', mode="a+", encoding='utf-8', newline='') as writeFile:
                    dict_writer = csv.DictWriter(writeFile, header_names)
                    if not header_added:
                        dict_writer.writeheader()
                        header_added = True
                    dict_writer.writerow(apartment_options[ad_post_id])
                    print(ad_post_id, "is being written to the file.","waiting for 20-100, and going for the rest:")
                    time.sleep(randint(100, 200))
            except Exception as e:
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                print("couldn't get the ad,the add is deleted!",ad_post_id)
                time.sleep(randint(100, 200))
                pass
        except Exception as e:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            raise FlowException("coudldn't get the classifiedDetail DIV",
                                "Process Exception in line {}".format(line),
                                e)
            pass
