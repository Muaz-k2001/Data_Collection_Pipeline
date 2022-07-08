from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time



class Scraper:
       
    def __init__(self, url):
        self.property_list = []
        self.page_count = 0
        self.big_list = []
        self.driver = webdriver.Chrome()
        self.url = url

        


    def accept_cookies(self):
        time.sleep(3)
        try:
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id= "gdpr-consent-notice"]')))
            print('Found pop-up')
            self.driver.switch_to.frame('gdpr-consent-notice')
            accept_cookies_button = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id= "save"]')))
            accept_cookies_button.click()
            print('Button Clicked')
            return self.driver
        except TimeoutException:
            print('Button not found')




    def search_ng8(self):
        time.sleep(1)
        search_bar = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@class="c-voGFy"]')))
        search_bar.click()
        search_bar.send_keys('NG8  Nottingham, Wollaton, Aspley')
        search_bar.send_keys(Keys.RETURN)
        return self.driver



    def get_property_links(self):
        try:
            close_button = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@class= "css-e4jnh6-CancelButton e13xjwxo6"]')))
            close_button.click()
        except:
            pass
        properties = WebDriverWait(self.driver, 100).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class= "css-1itfubx e34pn540"]/div')))
        self.property_list.clear()
        for property in properties:
            a_tag = property.find_element(By.TAG_NAME, 'a')
            property_link = a_tag.get_attribute('href')
            self.property_list.append(property_link)
        print('got links')
        return self.property_list




    def get_property_info(self):
        pass
    pass




    def change_page(self):
        next_page = self.driver.find_element(By.XPATH, '//*[@class= "css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2"]')
        next_page.click()




    def start(self):
        page_counter = 0
        self.driver.get(self.url)
        # self.driver.maximize_window()
        self.accept_cookies()
        self.search_ng8()
        while page_counter < 4:
            page_counter += 1
            self.get_property_links()
            self.big_list.extend(self.property_list)
            self.change_page()
        if page_counter == 4:
            self.get_property_links()
            self.big_list.extend(self.property_list)
        print(len(self.big_list))

if __name__ == '__main__':
    p = Scraper('https://www.zoopla.co.uk/')
    p.start()