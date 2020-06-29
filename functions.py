import re
import requests
from soup import get_by_selector, get_prop_details
from bs4 import BeautifulSoup


def get_pages(search_url):
    #get how many properties are pulled up
    response = requests.get(search_url)
    page = "https://search.albertare.com/api/properties?city=Calgary&page="
    soup = BeautifulSoup(response.text, 'html.parser')
    property_count = soup.select(".search-results-count")[0].text
    
    for i in property_count:
        result = bool(re.search('[0-9]', i))
        if not result:
            property_count = property_count.replace(i, '')
    
    page_list = []
    
    for i in range(int(property_count)):
        page_list.append(page + str(i + 1))
    
    return page_list

def get_property_link(page_url):
    #go through the json info, make a dict
    property_links = []
    prop_link = {}
    data = requests.get(page_url).json()
    for link in data['data']:
        prop_link['id'] = link['id']
        for att, val in link['attributes'].items():
            prop_link[att] = val
        prop_link['status'] = link['status']['data']['text']
        prop_link['buyer_agent'] = link['buyerAgent']
        prop_link['url'] = link['meta']['data']['url']
        property_links.append(prop_link)
    return property_links

def get_property(data):
    #iterate each page link, get the individual property links and access
    #receives dictionary of one property
    base_url = "https://search.albertare.com/homedetails"
    end_url = data['url']
    full_url = base_url + end_url
    response = requests.get(full_url)
    soup = BeautifulSoup(response.text, 'html.parser')


    prop_details = get_prop_details(soup)
    print(prop_details)
    
    




#soup the contents, return a dataframe

#save into excel file

