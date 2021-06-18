import sys
from collections import defaultdict

from bs4 import BeautifulSoup
class FlowException(Exception):
    pass
def getInfo(response,apartment_content, apartment_options, ad_post_id, image_urls_string):
    try:
        # Extracting Contents
        print("going for:" + ad_post_id)
        apartment_title_price = apartment_content.find('div', class_="classifiedInfo")
        apartment_location_names = apartment_title_price.find("h2").findChildren("a")
        del apartment_location_names[0]
        location_string = ','.join([location_name.text.strip().replace('.', '') for location_name in apartment_location_names])
        print(location_string)
        apartment_options[ad_post_id]["location"] = location_string
        apartment_price = apartment_title_price.find('input',{"id": "priceHistoryFlag"}).previousSibling.strip().replace(' TL','').replace(',', '')
        apartment_details = apartment_content.find('ul', class_="classifiedInfoList")
        apartment_owner = apartment_content.find('div', class_="classifiedUserContent")
        owner_registration_date = apartment_owner.find("p", class_="userRegistrationDate").findChild("span").text.strip()
        apartment_owner_name = apartment_owner.findChild('h5').text
        mapsoup = BeautifulSoup(response.text, 'lxml')
        apartment_location_map = mapsoup.find("div", {"data-lat": True})
        apartment_latitude = apartment_location_map['data-lat']
        apartment_longitude = apartment_location_map['data-lon']
        try:
            apartment_owner_phone = apartment_owner.find('span', class_="pretty-phone-part").text.replace('(','').replace(')', '').replace(' ', '')
        except:
            apartment_owner_phone = ''
        items = apartment_details.findChildren("li", {"class": False}, recursive=False)
        apartment_features = {}
        for item in items:
            item_title = item.find("strong").text.strip().replace(' ', '_').lower()
            item_value = item.find("span").text.lower().strip()
            apartment_options[ad_post_id][item_title] = item_value
        apartment_amenities_soup = mapsoup.find('div', {"id": "classifiedProperties"})
        apartment_amenities_headings = apartment_amenities_soup.find_all("h3")
        headings = {}
        for heading in apartment_amenities_headings:
            heading = heading.text
            headings.update({heading: ''})
        for item_h in headings:
            amenity_ul = apartment_amenities_soup.find("h3", text=item_h).find_next_sibling("ul").findChildren("li",class_="selected")
            amenity_ul_string = ','.join([item_li.text.strip() for item_li in amenity_ul])
            # print(item_h + ':' + amenity_ul_string)
            apartment_options[ad_post_id][item_h] = amenity_ul_string
        apartment_options[ad_post_id]["price"] = int(apartment_price)
        apartment_options[ad_post_id]["map_lat"] = apartment_latitude
        apartment_options[ad_post_id]["map_lon"] = apartment_longitude
        apartment_options[ad_post_id]["owner_name"] = apartment_owner_name
        apartment_options[ad_post_id]["owner_phone"] = apartment_owner_phone
        apartment_options[ad_post_id]["owner_registration_date"] = owner_registration_date
        apartment_options[ad_post_id]["images"] = image_urls_string
        print(apartment_options)
        return apartment_options
    except Exception as e:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        raise FlowException("coudldn't get the content",
                            "Process Exception in line {}".format(line),
                            e)
        pass

