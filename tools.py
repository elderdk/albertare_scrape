from selenium.common.exceptions import NoSuchElementException


def check_for_load(driver):
    
    try:
        load_button = driver.find_element_by_css_selector("div.load-more.text-center > button")
        return load_button

    except NoSuchElementException:
        return False