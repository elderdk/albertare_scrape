from sele import make_driver
from tools import check_for_load
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = "https://search.albertare.com/real-estate/calgary_ab"

dirname = os.path.dirname(os.path.realpath(__file__))
property_link_list = os.path.join(dirname, 'test.txt')

driver = make_driver(headless = False)
driver.get(url)


start_time = time.time()

with open(property_link_list, 'a', encoding='utf-8') as f:

    pulled_list = []

    while True:
        
        # scroll down to the bottom
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        driver.execute_script(f"window.scrollTo(0, {scroll_height});")

        # click if 'load more' button appears
        load_button = check_for_load(driver)
        if load_button:
            load_button.click()

        # find the properties available on the screen
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.property > a')))
        loaded_properties = driver.find_elements_by_css_selector("div.property > a")
        
        # get the link of each property and delete the node
        for property in loaded_properties:
            # link = property.find_element_by_css_selector("a").get_attribute('href')
            link = property.get_attribute('href')
            link = link.split('/')[-2:]
            link = '/'.join(link)
            link = "/" + link

            # delete the node
            script = f"document.querySelector(\"a[href^=\'{link}\']\").remove()"
            driver.execute_script(script)



end_time = time.time()

print("Elapsed time: " + end_time - start_time)

# successully deleting node
# make it so that a file is created and the links are saved
# use proxy or slow scrape to access each site and scrape the info.