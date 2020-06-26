import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def make_driver(headless):

    dirname = os.path.dirname(os.path.realpath(__file__))
    chromedriver = os.path.join(dirname, 'library/chromedriver.exe') #Point to the directory containing chromedriver.exe
    options = Options()
    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    options.add_argument('user-agent={userAgent}')
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.headless = headless #True for headless mode
    driver = webdriver.Chrome(chromedriver, options=options)

    return driver