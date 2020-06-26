from sele import make_driver
from tools import check_for_load
import os
import time


url = "https://search.albertare.com/real-estate/calgary_ab"

dirname = os.path.dirname(os.path.realpath(__file__))
property_link_list = os.path.join(dirname, 'test.txt')

driver = make_driver(headless = False)
driver.get(url)


start_time = time.time()

with open(property_link_list, 'a', encoding='utf-8') as f:

    pulled_list = []

    while True:
        
        #scroll down to the bottom
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        driver.execute_script(f"window.scrollTo(0, {scroll_height});")
        time.sleep(1)

        #click if 'load more' button appears
        load_button = check_for_load(driver)
        if load_button:
            load_button.click()

        #get number of currently loaded entries
        loaded_properties = driver.find_elements_by_css_selector("div.property")
        print(f"Properties on the screen: {len(loaded_properties)}")
        for property in loaded_properties:
            link = property.find_element_by_css_selector("a").get_attribute('href')
            link = link.split('/')[-2:]
            link = '/'.join(link)

        #delete the nodes to free up memory and maintain scraping speed
        # for _ in range(len(loaded_properties)):
        #     driver.execute_script("document.getElementsByClassName('property')[0].remove();")


end_time = time.time()

print("Elapsed time: " + end_time - start_time)

# #save the list of property links to csv
# for property in loaded_properties:
#     property_link = property.find_element_by_css_selector('a')[0].get_attribute('href')
#     print(property_link)
    
# if property_link not in pulled_list:
#     pulled_list.append(property_link)
#     f.write(property_link)