from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


#class Scraper:


def load_page() -> webdriver.Firefox:
    driver = webdriver.Firefox()
    URL = 'https://www.zoopla.co.uk/'
    driver.get(URL)
    accept_cookies(driver)
    
def accept_cookies(driver):
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id= "gdpr-consent-notice"]')))
        print('Found pop-up')
        driver.switch_to.frame('gdpr-consent-notice')
        accept_cookies_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id= "save"]')))
        accept_cookies_button.click()
        print('Button Clicked')
    except TimeoutException:
        print('Button not found')

load_page()
