import re
from bs4 import BeautifulSoup


class MyHomeParser:
    def __init__(self, page):
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('app-mh-property-listing-card')
        places = extract_results(results)
        self.places = places

    def get_places(self):
        return self.places


def extract_results(results):
    output = []
    for res in results:
        listing_card = res.find('div', {'class': re.compile(r'PropertyListingCard__ImageContainer.*')})
        link = listing_card.select('a')
        desc = res.find_all('a', {'class': re.compile(r'PropertyListingCard__Addres.*')})[0].get_text()
        price = res.find_all('div', {'class': re.compile(r'PropertyListingCard__Price.*')})[0].get_text()
        info_tags = res.find_all('div', {'class': re.compile(r'PropertyInfoStrip.*')})
        print(info_tags)
        infos = [p.get_text() for p in info_tags]
        place = {'link': 'https://myhome.ie' + link[0]['href'], 'desc': desc, 'price': price, 'infos': infos}
        output.append(place)
    return output
