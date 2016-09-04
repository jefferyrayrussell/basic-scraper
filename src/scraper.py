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
    """ Makes a request to the King County Server, fetches
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
    """ Sets up HTML as DOM nodes for
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
    """ Takes an element as an argument, returns true if the element is 
    both a <tr> and contains two <td> elements within it.
    """

    element_is_tablerow = element.name == 'tr'
    element_has_tabledata_children = elem.find_all('td', recursive=False)
    element_has_two_tabledata = len(element_has_tabledata_children) == 2
    return element_is_tablerow and element_has_two_tabledata


def clean_data(td):
    """ Cleans up values received from cells."""

    data = td.string
    try:
        return data.strip(" \n:-")
    except AttributeError:
        return u""


def extract_restaurant_metadata(element):
    """ Puts data into a dictionary to represent a single restaurant."""
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


def is_inspection_row(element):
    """ Filter function extracts correct rows to build inspection data."""

    element_is_tablerow = elem.name == 'tr'
    if not is_tr:
        return False
    element_has_tabledata_children = elem.find_all('td', recursive=False)
    has_four = len(td_children) == 4
    this_text = clean_data(td_children[0]).lower()
    contains_word = 'inspection' in this_text
    does_not_start = not this_text.startswith('inspection')
    return is_tr and has_four and contains_word and does_not_start


def extract_score_data(element):
    """ Builds aggregated data."""

    inspection_rows = element.find_all(is_inspection_row)
    samples = len(inspection_rows)
    total = high_score = average = 0
    for row in inspection_rows:
        strval = clean_data(row.find_all('td')[2])
        try:
            intval = int(strval)
        except (ValueError, TypeError):
            samples -= 1
        else:
            total += intval
            high_score = intval if intval > high_score else high_score
    if samples:
        average = total/float(samples)
    data = {
        u'Average Score': average,
        u'High Score': high_score,
        u'Total Inspections': samples
    }
    return data


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
        score_data = extract_score_data(listing)
            print score_data
