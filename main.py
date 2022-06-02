
import requests

from fastapi import FastAPI

from daft_parser import DaftParser
from myhome_parser import MyHomeParser

app = FastAPI()


def request_page(url):
    page = requests.get(url)
    if page.status_code != 200:
        raise Exception(f"Error requesting url {url}")
    return page


def extract_results(result_list):
    output = []
    for res in result_list:
        link = res.select('li a')
        desc = res.find_all('p', {'data-testid': 'address'})[0].get_text()
        price = res.find_all('div', {'data-testid': 'price'})[0].get_text()
        info_tags = res.find_all('div', {'data-testid': 'card-info'})
        infos = [p.get_text() for p in info_tags]
        place = {'link': 'https://www.daft.ie' + link[0]['href'], 'desc': desc, 'price': price, 'infos': infos}
        output.append(place)
    return output


@app.get("/")
def status():
    return [{"daft": "call /daft for daft places"},
            {"myhome": "call /myhome for myhome.ie places"}]


@app.get("/daft")
async def root():
    requested_page = request_page(
        'https://www.daft.ie/property-for-rent/ireland?rentalPrice_from=1200&rentalPrice_to=2500&numBeds_from=2&firstPublishDate_from=now-1d%2Fd')
    paser = DaftParser(requested_page)
    return paser.get_places()

@app.get("/myhome")
async def root():
    requested_page = request_page(
        'https://www.myhome.ie/rentals/dublin/property-to-rent?minenergyrating=90&minprice=1500&maxprice=2500&minbeds=1')
    paser = MyHomeParser(requested_page)
    return paser.get_places()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)
