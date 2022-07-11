from selenium import webdriver
import uuid
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
        self.info_dict = {'Link' : [], 'Price' : [], 'Bedrooms' : [], 'Bathrooms' : [], 'Address' : [], 'IMG link' : [], 'UID' : [], 'UUID' : []}
        


    def accept_cookies(self):
        try:
            WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id= "gdpr-consent-notice"]')))
            self.driver.switch_to.frame('gdpr-consent-notice')
            accept_cookies_button = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id= "save"]')))
            accept_cookies_button.click()
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
        properties = WebDriverWait(self.driver, 100).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="css-1itfubx emu4sxi0"]/div')))
        self.property_list.clear()
        for property in properties:
            a_tag = property.find_element(By.TAG_NAME, 'a')
            property_link = a_tag.get_attribute('href')
            self.property_list.append(property_link)
        print('got links')
        return self.property_list




    def get_unique_id(self):
        unique_id = self.url.split('/')[5]
        self.info_dict['UID'].append(unique_id)
        return self.info_dict


    def get_uuid(self):
        universally_uid = uuid.uuid4()
        self.info_dict['UUID'].append(universally_uid)
        return self.info_dict



    def get_property_img(self):
        property_img = self.driver.find_element(By.XPATH, '//main/div/div//li[2]//img').get_attribute('src')
        self.info_dict['IMG link'].append(property_img)
        return self.info_dict




    def get_property_info(self):
        error_msg = 'Not Applicable'
        info_container = self.driver.find_element(By.XPATH, '//*[@data-testid= "listing-summary-details"]')
        price = info_container.find_element(By.XPATH, '//*[@data-testid= "price"]').text
        self.info_dict['Price'].append(price)
        bedroom = info_container.find_element(By.XPATH, './div[position() > 3]//*[text()[contains(., "bed")]]').text
        self.info_dict['Bedrooms'].append(bedroom)
        try:
            bathroom = info_container.find_element(By.XPATH, './div//*[text()[contains(., "bath")]]').text
            self.info_dict['Bathrooms'].append(bathroom)
        except:
            self.info_dict['Bathrooms'].append(error_msg)
        address = info_container.find_element(By.XPATH, '//*[@data-testid= "address-label"]').text
        self.info_dict['Address'].append(address)
        return self.info_dict


    def change_page(self):
        next_page = self.driver.find_element(By.XPATH, '//*[@class= "css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2"]')
        next_page.click()




    def start(self):
        page_counter = 0
        self.driver.get(self.url)
        # self.driver.maximize_window()
        time.sleep(3)
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
        time.sleep(3)
        for property in self.big_list:
            self.info_dict['Link'].append(property)
            self.url = property
            self.driver.get(self.url)
            time.sleep(2)
            self.get_property_info()
            self.get_property_img()
            self.get_unique_id()
            self.get_uuid()
        print(self.info_dict)

if __name__ == '__main__':
    p = Scraper('https://www.zoopla.co.uk/')
    p.start()