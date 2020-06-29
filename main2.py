from functions import get_pages, get_property_link, get_property, get_all_properties
import requests
import time


if __name__ == '__main__':
        
    search_url = "https://search.albertare.com/real-estate/calgary_ab"
    page_list = get_pages(search_url)

    t1 = time.time()

    # link_pages = (page_list[0]) #capped at 1 for testing

    get_all_properties(page_list[:10]) #concurrency is working, need to work on the rest of the plan in the bottom of functions.py

    elapse = time.time() - t1
    print(elapse)