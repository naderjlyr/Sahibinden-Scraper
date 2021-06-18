import os.path
import csv
import time
from random import randint


class FlowException(Exception):
    pass


def writeFile(header_names, header_added, apartment_options_final, ad_post_id):
    with open(os.path.dirname(__file__) + '/../file.csv', mode="a+", encoding='utf-8', newline='') as writeFileCsv:
        dict_writer = csv.DictWriter(writeFileCsv, header_names)
        if not header_added:
            dict_writer.writeheader()
            header_added = True
        dict_writer.writerow(apartment_options_final[ad_post_id])
        print(ad_post_id, "is being written to the file.", "waiting for 20-100, and going for the rest:")
        # time.sleep(randint(100, 200))
