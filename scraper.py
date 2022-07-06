from enum import auto
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time



class Scraper:
       
    def __init__(self):
        self.property_list = []


        
    def accept_cookies(self, driver):
        time.sleep(3)
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
        time.sleep(1)
        search_bar = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@class="c-voGFy"]')))
        search_bar.click()
        search_bar.send_keys('NG8  Nottingham, Wollaton, Aspley')
        search_bar.send_keys(Keys.RETURN)
        return driver


    def get_property_links(self, driver):
        time.sleep(3)
        properties = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class= "css-1itfubx er561h10"]/div')))
        property_list = []
        for property in properties:
            a_tag = property.find_element(By.TAG_NAME, 'a')
            property_link = a_tag.get_attribute('href')
            property_list.append(property_link)
        print(len(property_list))

    def get_property_info(self, driver):
        pass
    pass



def start(driver, URL):
    driver.get(URL)
    driver.maximize_window()
    auto = Scraper()
    driver = auto.accept_cookies(driver)
    driver = auto.search_ng8(driver)
    auto.get_property_links(driver)

if __name__ == '__main__':
    driver = webdriver.Chrome()
    URL = 'https://www.zoopla.co.uk/'
    start(driver, URL)

