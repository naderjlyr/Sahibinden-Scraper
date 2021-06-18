import sys

from bs4 import BeautifulSoup


def getImages(apartment_content, ad_post_id):
    try:
        print("going for getting images of : " + ad_post_id)
        apartment_images = apartment_content.find('div', {'class': 'classifiedDetailMainPhoto'})
        if apartment_images is not None:
            children = apartment_images.findChildren('label', {"id": lambda x: x and x.startswith('label_images')},recursive=False)[:4]
            image_urls_list = []
            for counter, image in enumerate(children):
                image_urls = image.find('img', {'alt': True})
                if image_urls.has_attr('class'):
                    image_urls['data-src'] = image_urls['src']
                image_urls_list.append(image_urls['data-src'].replace("x5_", "big_"))
            image_urls_string = ','.join(image_urls_list)
            return image_urls_string
    except Exception as e:
        trace_back = sys.exc_info()[2]
        line = trace_back.tb_lineno
        print("couldn't get the Images,the add is either deleted or doesn't have pictures!")
        return image_urls_string
