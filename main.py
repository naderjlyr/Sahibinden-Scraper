from functions.get_apartments import get_apartments
from functions.get_single_apartment import single_apartment
from functions.get_single_apartment import single_apartment
from functions.get_page_offset import page_offset

#first of all comment out 6,7,8 to get the page offset and the apartments list.
extracted_offset = page_offset()
print("total offset number : ", extracted_offset)
get_apartments(extracted_offset)

#data will be saved in data.json file. and after that comment out the line below,
#to start scraping apartment data.

# single_apartment()
