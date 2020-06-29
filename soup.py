from bs4 import BeautifulSoup

def get_by_selector(soup, selector):
    try:
        elem = soup.select(selector)
        return elem
    except:
        return 'None'

def get_prop_details(soup):

    details = {}

    selector = {
        "com_features": "div.property-feature-group:nth-child(2) > ul",
        "ext_features": "div.property-feature-group:nth-child(3) > ul",
        "int_features": "div.property-feature-group:nth-child(4) > ul",
        "style": "div.property-feature-group:nth-child(5) > ul"
    }    

    for k, v in selector.items():
        details[k] = get_by_selector(soup, v)
    
    return details