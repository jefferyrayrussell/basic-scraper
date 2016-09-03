INSPECTION_DOMAIN = 'http://info.kingcounty.gov'
INSPECTION_PATH = '/health/ehs/foodsafety/inspections/Results.aspx'
INSPECTION_PARAMS = {
    'Output': 'W',
    'Business_Name': '',
    'Business_Address': '',
    'Longitude': '',
    'Latitude': '',
    'City': '',
    'Zip_Code': '',
    'Inspection_Type': 'All',
    'Inspection_Start': '',
    'Inspection_End': '',
    'Inspection_Closed_Business': 'A',
    'Violation_Points': '',
    'Violation_Red_Points': '',
    'Violation_Descr': '',
    'Fuzzy_Search': 'N',
    'Sort': 'H'
}

import sys
import requests
import re
from bs4 import BeautifulSoup

def get_inspection_page(**kwargs):
    """This function: makes a request to the King County Server, fetches
    search results, takes query parameters as arguments, returns the
    content and encoding, if problem raises an error."""

    url = INSPECTION_DOMAIN + INSPECTION_PATH
    params = INSPECTION_PARAMS.copy()
    for key, val in kwargs.items():
        if key in INSPECTION_PARAMS:
            params[key] = val
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.content, response.encoding


def load_inspection_page(**kwargs):
    """This function: reads the static inpection_page.html file; returns
    the content and encoding.

# add this import at the top
from bs4 import BeautifulSoup

# then add this function lower down
def parse_source(html, encoding='utf-8'):
    parsed = BeautifulSoup(html, 'html5lib', from_encoding=encoding)
    return parsed


if __name__ == '__main__':
    kwargs = {
        'Inspection_Start': '2/1/2013',
        'Inspection_End': '2/1/2015',
        'Zip_Code': '98109'
    }
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # you will likely have something different here, depending on how
        # you implemented the load_inspection_page function.
        html, encoding = load_inspection_page('inspection_page.html')
    else:
        html, encoding = get_inspection_page(**kwargs)
    doc = parse_source(html, encoding)
    print doc.prettify(encoding=encoding)