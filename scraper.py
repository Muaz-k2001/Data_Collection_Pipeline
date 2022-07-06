from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
URL = 'https://www.zoopla.co.uk/'

class Scraper:
       
        


        
    def accept_cookies(self, driver):
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id= "gdpr-consent-notice"]')))
            print('Found pop-up')
            driver.switch_to.frame('gdpr-consent-notice')
            accept_cookies_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id= "save"]')))
            accept_cookies_button.click()
            print('Button Clicked')
            return driver
        except TimeoutException:
            print('Button not found')




    def search_ng8(self, driver):
        search_bar = driver.find_element('xpath', '//*[@class="c-voGFy"]')
        search_bar.click()
        search_bar.send_keys('NG8  Nottingham, Wollaton, Aspley')
        search_bar.send_keys(Keys.RETURN)
        print('hello')

def start(driver, URL):
    driver.get(URL)
    r = Scraper()
    r.accept_cookies(driver)
    r.search_ng8(driver)


start(driver, URL)

