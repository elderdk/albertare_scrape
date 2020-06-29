import re
import requests
from soup import get_by_selector, get_prop_details
from bs4 import BeautifulSoup
import threading
import concurrent.futures


thread_local = threading.local()

def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

def get_pages(search_url):
    # retrieve the number of pagination pages to create
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
    #iterate each page link, get the individual property links and access
    #receives dictionary of one property
    base_url = "https://search.albertare.com"
    end_url = url
    full_url = base_url + end_url
    data = {}
    print(f"getting {end_url}")
    session = get_session()
    response = session.get(full_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    prop_details = get_prop_details(soup)
    
    for k, v in prop_details.items():
        data[k] = v

    return data

def get_property_link(page_url):
    session = get_session()
    #go through the json info, make a list of dict
    property_links = []
    data = session.get(page_url).json()
    for link in data['data']:
        prop_link = {}
        prop_link['id'] = link['id']
        for att, val in link['attributes'].items():
            prop_link[att] = val
        prop_link['status'] = link['status']['data']['text']
        prop_link['buyer_agent'] = link['buyerAgent']
        prop_link['url'] = link['meta']['data']['url']

        #access the site and get the feature information
        features = get_property(prop_link['url'])

        for k, v in features.items():
            prop_link[k] = v

        property_links.append(prop_link)

    return property_links

def get_all_properties(links):

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(get_property_link, links)


#soup the contents, return a dataframe

#save into excel file

