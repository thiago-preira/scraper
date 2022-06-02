
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
