from functions import get_pages, get_property_link, get_property, get_all_properties
import requests
import time


if __name__ == '__main__':
        
    page_list = get_pages("https://search.albertare.com/real-estate/calgary_ab")

    t1 = time.time()

    mdf = get_all_properties(page_list[:5]) #concurrency is working, need to work on the rest of the plan in the bottom of functions.py

    elapse = time.time() - t1
    print(elapse)