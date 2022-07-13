from multiprocessing.sharedctypes import Value
from plistlib import UID
from selenium import webdriver
import uuid
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import os
import shutil


class Scraper:
       
    def __init__(self, url):
        self.page_count = 0
        self.big_list = []
        self.driver = webdriver.Chrome()
        self.url = url
        self.info_dict = {'Link' : [], 'Price' : [], 'Bedrooms' : [], 'Bathrooms' : [], 'Address' : [], 'IMG links' : [], 'UID' : [], 'UUID' : []}
        


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


    def close_email_popup(self):
        close_button = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@class= "css-e4jnh6-CancelButton e13xjwxo6"]')))
        close_button.click()


    def get_property_links(self):
        property_list = []
        properties = WebDriverWait(self.driver, 100).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="css-1itfubx et6shp90"]/div[position() < 3]')))
        # Change position value for number of links
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        #
        property_list.clear()
        for property in properties:
            a_tag = property.find_element(By.TAG_NAME, 'a')
            property_link = a_tag.get_attribute('href')
            property_list.append(property_link)
        print('got links')
        return property_list




    def get_unique_id(self):
        unique_id = self.url.split('/')[5]
        self.info_dict['UID'].append(unique_id)



    def get_uuid(self):
        universally_uid = str(uuid.uuid4())
        self.info_dict['UUID'].append(universally_uid)




    def get_property_img(self):
        property_img_list = []
        property_imgs = self.driver.find_elements(By.XPATH, '//main/div/div/section//li')
        for img in property_imgs:
            img_tag = img.find_element(By.XPATH, '//img')
            src_link = img_tag.get_attribute('src')
            property_img_list.append(src_link)
        self.info_dict['IMG links'].append(property_img_list)





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



    def change_page(self):
        next_page = self.driver.find_element(By.XPATH, '//*[@class= "css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2"]')
        next_page.click()



    def create_raw_data_folder(self):
        try:
            dir = '/home/muaz/Desktop/AiCore/Data_Collection_Pipeline/raw_data/'
            shutil.rmtree(dir)
        except:
            pass
        directory = 'raw_data'
        parent_dir = '/home/muaz/Desktop/AiCore/Data_Collection_Pipeline/'
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        print('raw_data directory created')




    def create_id_folders(self, folder_counter):
        parent_dir = '/home/muaz/Desktop/AiCore/Data_Collection_Pipeline/raw_data/'
        directory = self.info_dict['UID'][folder_counter]
        uid_directory = os.path.join(parent_dir, directory)
        os.mkdir(uid_directory)
        return uid_directory




    def create_data_files(self, uid_directory, folder_counter):
        data = open(os.path.join(uid_directory, 'data.json'), 'a')
        for key in self.info_dict:
            data.write(f'{key} = {self.info_dict[key][folder_counter]}\n')





    def start(self):
        self.driver.get(self.url)
        # self.driver.maximize_window()
        time.sleep(2)
        self.accept_cookies()
        self.search_ng8()
        page_counter = 0
        while page_counter < 4:
            if page_counter == 1:
                self.close_email_popup()
            property_list = self.get_property_links()
            self.big_list.extend(property_list)
            self.change_page()
            page_counter += 1
        property_list = self.get_property_links()
        self.big_list.extend(property_list)
        print(len(self.big_list))
        time.sleep(3)
        property_counter = 0
        for property in self.big_list:
            self.info_dict['Link'].append(property)
            self.url = property
            self.driver.get(self.url)
            time.sleep(1)
            self.get_property_info()
            self.get_property_img()
            self.get_unique_id()
            self.get_uuid()
            property_counter += 1
            print(f'Got info for property {property_counter}')
        self.create_raw_data_folder()
        folder_counter = 0
        while folder_counter < len(self.big_list):
            uid_directory = self.create_id_folders(folder_counter)
            self.create_data_files(uid_directory, folder_counter)
            folder_counter += 1
        print('Folders created and data stored')


if __name__ == '__main__':
    p = Scraper('https://www.zoopla.co.uk/')
    p.start()