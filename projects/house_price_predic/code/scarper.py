from bs4 import BeautifulSoup


soup = BeautifulSoup()
base_url = 'https://www.olx.uz/oz/nedvizhimost/doma/prodazha/tashkent/'
def filter_url(page):
    return f'?currency=UYE&page={page}&search%5Bfilter_enum_location%5D%5B0%5D=1&search%5Bfilter_enum_private_house_type%5D%5B0%5D=1&search%5Bfilter_enum_private_house_type%5D%5B1%5D=3&search%5Bfilter_enum_private_house_type%5D%5B2%5D=5'

pages = 25

for page in range(pages):
    url = base_url + filter_url(page)