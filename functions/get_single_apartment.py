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
from functions.check_file_header import checkFileHeader
from functions.get_images import getImages
from functions.get_info import getInfo
from functions.write_to_file import writeFile


class FlowException(Exception):
    pass


def single_apartment():
    header_added = False
    jsonData, header_added = checkFileHeader(header_added)
    apartment_options = defaultdict(dict)
    # print(header_added)
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
                print(headers)
                soup = BeautifulSoup(response.text, 'lxml')
                apartment_content = soup.find("div", {"id": "classifiedDetail"})
            except Exception as e:
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                raise FlowException("coudldn't get the classifiedDetail DIV",
                                    "Process Exception in line {}".format(line),
                                    e)
            try:
                if apartment_content is not None:
                    apartment_options = {
                        ad_post_id: {"location": "", "ad": "", "ad_date": "", "real_estate": "", "real_estate_type": "",
                                     "m²_(brüt)": "", "m²_(net)": "", "number_of_rooms": "",
                                     "age_of_building": "", "floor_number": "", "number_of_floors": "",
                                     "heating": "", "number_of_bathrooms": "", "balcony": "",
                                     "furnished": "", "user_status": "",
                                     "within_a_building_complex": "", "apartment_complex_name": "",
                                     "dues": "", "eligible_for_bank_credit": "", "from": "",
                                     "available_for_viewing_with_video_call": "", "exchangeable": "",
                                     "Frontage": "", "Interior Properties": "",
                                     "External Properties": "", "Nearliness ": "", "Transportation": "",
                                     "Scene": "", "Residence Type": "", "Accessible Housing": "",
                                     "price": "", "map_lat": "", "map_lon": "", "owner_name": "",
                                     "owner_phone": "", "owner_registration_date": "", "images": "", }}
                    image_urls_string = getImages(apartment_content, ad_post_id)
            except Exception as e:
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                raise FlowException("getImages has faced a problem, check it out!")
            try:
                if apartment_content is not None:
                    apartment_options_final = getInfo(response, apartment_content, apartment_options, ad_post_id,
                                                      image_urls_string)
                    header_names = list(apartment_options[ad_post_id].keys())
                    writeFile(header_names, header_added, apartment_options_final, ad_post_id)
                    time.sleep(randint(100, 200))
            except Exception as e:
                trace_back = sys.exc_info()[2]
                line = trace_back.tb_lineno
                raise FlowException("couldn't get the apartment info!check the related file.")
        except Exception as e:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            raise FlowException("coudldn't get the classifiedDetail DIV",
                                "Process Exception in line {}".format(line),
                                e)
            pass
