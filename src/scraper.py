import sys
import requests
import re
from bs4 import BeautifulSoup
import io

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


def get_inspection_page(**kwargs):
    """ The function: makes a request to the King County Server, fetches
    search results, takes query parameters as arguments, returns the
    content and encoding, if problem raises an error.
    """

    url = INSPECTION_DOMAIN + INSPECTION_PATH
    params = INSPECTION_PARAMS.copy()
    for key, val in kwargs.items():
        if key in INSPECTION_PARAMS:
            params[key] = val
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.content, response.encoding


def load_inspection_page(**kwargs):
    """ The function: reads the inpection_page.html file; returns
    the content and encoding.
    """

    files = io.open(paths, 'response_body')
    response = files.read()
    files.close()
    encoding = 'utf-8'
    return response, encoding


def parse_source(html, encoding='utf-8'):
    """ The parse_source function: sets up HTML as DOM nodes for
    scraping, takes the response body from the previous function, parses
    it using BeautifulSoup, returns the parsed object for processing.
    """
    parsed = BeautifulSoup(html, 'html5lib', from_encoding=encoding)
    return parsed


def extract_data_listings(html):
    """ Takes parsed HTML and returns a list of the container nodes."""

    id_finder = re.compile(r'PR[\d]+~')
    return html.find_all('div', id=id_finder)


def has_two_tds(element):
    """The has_two_tds function: takes an element as an argument, returns
    true if the element is both a <tr> and contains two <td> elements
    within it.
    """

    element_is_tablerow = element.name == 'tr'
    element_has_tabledata_children = elem.find_all('td', recursive=False)
    element_has_two_tabledata = len(element_has_tabledata_children) == 2
    return element_is_tablerow and element_has_two_tabledata


def clean_data(td):
    """The clean_data function: cleans up values received form cells."""

    data = td.string
    try:
        return data.strip(" \n:-")
    except AttributeError:
        return u""


def extract_restaurant_metadata(element):
    metadata_rows = element.find('tbody').find_all(
        element_has_two_tabledata, recuresive=False
    )
    rdata = {}
    current_label = ''
    for row in metadata_rows:
        key_cell, val_cell = row.find_all('td', recursive=False)
        new_label = clean_data(key_cell)
        current_label = new_label if new_label else current_label
        rdata.setdefault(current_label, [].append(clean_data(val_cell))
    return rdata

if __name__ == '__main__':
    kwargs = {
        'Inspection_Start': '3/1/2013',
        'Inspection_End': '3/1/2015',
        'Zip_Code': '98109'
    }
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = load_inspection_page('inspection_page.html')
    else:
        html, encoding = get_inspection_page(**kwargs)
    doc = parse_source(html, encoding)
    listings = extract_data_listings(doc)
    for listing in listings[:5]:
        metadata = extract_restaurant_metadata(listing)
        print metadata
        print
