import re
import os
import requests
from soup import get_by_selector, get_prop_details
from bs4 import BeautifulSoup
import threading
import concurrent.futures
import pandas as pd


thread_local = threading.local()
mdf = pd.DataFrame()

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

def get_pages(search_url):
    # retrieve the number of pagination pages to create
    # https://search.albertare.com/api/properties?city=Calgary&page=1
    # https://search.albertare.com/api/properties?city=Calgary&page=2
    # https://search.albertare.com/api/properties?city=Calgary&page=3

    response = requests.get(search_url)
    page = "https://search.albertare.com/api/properties?city=Calgary&page="
    soup = BeautifulSoup(response.text, 'html.parser')
    property_count = soup.select(".search-results-count")[0].text
    
    for i in property_count:
        result = bool(re.search('[0-9]', i))
        if not result:
            property_count = property_count.replace(i, '')
    
    property_count = int(property_count)

    if property_count // 10 == 0:
        property_count //= 10
    else:
        property_count = (property_count // 10) + 1

    page_list = []
    
    for i in range(property_count):
        page_list.append(page + str(i + 1))
    
    return page_list

def get_property(url):
    #access the individual property site and pull features
    #like com_ int_ ext_features and style

    base_url = "https://search.albertare.com"
    end_url = url

    full_url = base_url + end_url
    data = {}
    session = get_session()
    response = session.get(full_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    prop_details = get_prop_details(soup)
    
    for k, v in prop_details.items():
        data[k] = v

    return data

def get_property_link(page_url):
    #iterate each link from get_page, make dict for each property (10 in each page)
    #use get_prop_details to get the features and make complete dict set for each property

    global mdf
    session = get_session()
    property_data = []
    data = session.get(page_url).json()
    for link in data['data']:
        prop_link = {}
        prop_link['id'] = link['id']
        for att, val in link['attributes'].items():
            prop_link[att] = val
        prop_link['status'] = link['status']['data']['text']
        prop_link['url'] = link['meta']['data']['url']
        prop_link.pop('location', None)

        #access the site and get the feature information
        features = get_property(prop_link['url'])

        for k, v in features.items():
            prop_link[k] = v

        property_data.append(prop_link)

    mdf = make_dataframe(property_data)
    
    return mdf

def make_dataframe(property_data):
    global mdf
    for prop in property_data:
        df = pd.DataFrame([prop]) #without [] this raises scalar value error. But dictionary doesn't contain any list. So why?
        print(f"Scraped {len(df)} from {prop['url']}")
        mdf = mdf.append(df)
        print(len(mdf))

    return mdf

def write_to_excel(mdf):
    dirname = os.path.dirname(os.path.realpath(__file__))
    fname = os.path.join(dirname, 'result.xlsx')

    if not os.path.isfile(fname):
        import openpyxl
        wb = openpyxl.Workbook()
        wb.save(fname)
    
    with pd.ExcelWriter(fname, mode="a", engine="openpyxl") as writer:
        mdf.to_excel(writer)
    

def get_all_properties(links):
    #master concurrency function

    global mdf

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor: #seems multiple workers can't write to a global variable at the same time
        executor.map(get_property_link, links)

    write_to_excel(mdf)