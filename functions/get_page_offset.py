import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import urllib.parse as urlparse
from urllib.parse import parse_qs


def page_offset():
    # getting the page offset

    target_list_url = "https://www.sahibinden.com/en/for-sale/owner?pagingSize=50&address_region=1&viewType=List&price_min=300000&address_town=435&address_town=436"
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
    response = requests.request("GET", target_list_url, headers=headers, data=payload)
    # Using BeautifulSoup for getting data
    soup = BeautifulSoup(response.text, 'lxml')
    page_offset = soup.find('ul', class_='pageNaviButtons').find_all("li")
    counter = 0
    for counter, offset in enumerate(page_offset):
        offset = offset.find("a")
        if counter == len(page_offset) - 2:
            offset = offset["href"]
            parsed = urlparse.urlparse(offset)
            a_string = "".join(parse_qs(parsed.query)['pagingOffset'])
            return a_string