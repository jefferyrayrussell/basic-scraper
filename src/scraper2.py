"""A Python script to extract restaurant health inspection data."""

from bs4 import BeautifulSoup
import requests
import sys
import re

INSPECTION_DOMAIN = 'http://info.kingcounty.gov'
INSPECTION_PATH = '/health/ehs/foodsafety/inspections/Results.aspx'
INSPECTION_PARAMS = {
    'Output': 'W',
    'Business_Name': "Ivar's Salmon House",
    'Business_Address': '401 NE NORTHLAKE WAY',
    'Longitude': '',
    'Latitude': '',
    'City': 'Seattle',
    'Zip_Code': '98105',
    'Inspection_Type': 'All',
    'Inspection_Start': '',
    'Inspection_End': '',
    'Inspection_Closed_Business': 'A',
    'Violation_Points': '',
    'Violation_Red_Points': '',
    'Violation_Descr': '',
    'Fuzzy_Search': 'N',
    'Sort': 'B'
}


def get_inspection_page(**kwargs):
    """Return content and encoding of query from server."""
    url = INSPECTION_DOMAIN + INSPECTION_PATH
    params = INSPECTION_PARAMS.copy()
    for key, val in kwargs.items():
        if key in INSPECTION_PARAMS:
            params[key] = val
    resp = requests.get(url, params=params)
    write_inspection_page(resp)
    resp.raise_for_status()
    return resp.content, resp.encoding


def write_inspection_page(results):
    """Write results of query to file on local disk."""
    file = open('results.html', 'w')
    file.write(str(results.encoding))
    file.write(str(results.content))
    file.close()


def load_inspection_page(file_to_load):
    """Read above file on local disk and return content and encoding."""
    file = open(file_to_load, 'r')
    encoding = file.readline()
    content = file.read()
    encoding = encoding[0:5]
    return content, encoding


def parse_source(html, encoding='utf-8'):
    """Set up HTML as DOM nodes for scraping and further processing."""
    parsed = BeautifulSoup(html, 'html5lib', from_encoding=encoding)
    return parsed


def extract_data_listings(html):
    """Return a list of listing container nodes."""
    id_finder = re.compile(r'PR[\d]+~')
    return html.find_all('div', id=id_finder)


if __name__ == '__main__':
    kwargs = {
        'Inspection_Start': '2/1/2014',
        'Inspection_End': '2/1/2015',
        'Zip_Code': '98105'
    }
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = load_inspection_page('results.html')
    else:
        html, encoding = get_inspection_page(**kwargs)
        doc = parse_source(html, encoding)
        listings = extract_data_listings(doc)
    # print len(listings)
    # print listings[0].prettify()
