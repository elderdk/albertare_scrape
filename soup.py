from bs4 import BeautifulSoup

def get_by_selector(soup, selector):
    #soup helper function to search by selector given
    try:
        elem = soup.select(selector)[0].find_all('li')
        elem_list = []
        for e in elem:
            elem_list.append(e.text)
        return ', '.join(elem_list)
    except:
        return 'None'

def get_prop_details(soup):
    #gets prop features from the individual prop site

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