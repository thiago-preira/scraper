import re
from bs4 import BeautifulSoup


class DaftParser:
    def __init__(self, page):
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('li', {'data-testid': re.compile(r'result.*')})
        places = extract_results(results)
        self.places = places

    def get_places(self):
        return self.places


def extract_results(results):
    output = []
    for res in results:
        link = res.select('li a')
        desc = res.find_all('p', {'data-testid': 'address'})[0].get_text()
        price = res.find_all('div', {'data-testid': 'price'})[0].get_text()
        info_tags = res.find_all('div', {'data-testid': 'card-info'})
        infos = [p.get_text() for p in info_tags]
        place = {'link': 'https://www.daft.ie' + link[0]['href'], 'desc': desc, 'price': price, 'infos': infos}
        output.append(place)
    return output
