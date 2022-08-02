from multiprocessing.sharedctypes import Value
from selenium import webdriver
import uuid
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import shutil
import urllib.request
import json
import boto3

s3_client = boto3.client('s3')

class Scraper:
    '''Scrapes a website for desired information
    '''

       
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver
        self.big_list = []
        self.property_dict = {'Property' : []}
        


    def accept_cookies(self):
        '''Clicks the accept cookies button that pops up on inital website visit
        '''
        WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id= "gdpr-consent-notice"]')))
        self.driver.switch_to.frame('gdpr-consent-notice')
        accept_cookies_button = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id= "save"]')))
        accept_cookies_button.click()


    def search_ng8(self):
        '''Types the desired search location and presses enter to commence search
        '''
        search_bar = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@class="c-voGFy"]')))
        search_bar.click()
        search_bar.send_keys('NG8  Nottingham, Wollaton, Aspley')
        search_bar.send_keys(Keys.RETURN)



    def close_email_popup(self):
        '''Closes the email popup on the second page of properties
        '''
        close_button = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@class= "css-e4jnh6-CancelButton e13xjwxo6"]')))
        close_button.click()



    def get_property_links(self):
        '''Gets the links to all the properties on the current page

        Returns:
            list: list of property links
        '''
        property_list = []
        properties = WebDriverWait(self.driver, 100).until(EC.presence_of_all_elements_located((By.XPATH, '//main/div[2]/div/div[position() < 4]')))
        property_list.clear()
        for property in properties:
            a_tag = property.find_element(By.TAG_NAME, 'a')
            property_link = a_tag.get_attribute('href')
            property_list.append(property_link)
        print('got links')
        return property_list
    


    def get_unique_id(self):
        '''Assigns a unique ID for each property from the ID given in the URL and appends to the dictionary

        Returns:
            str: string of numbers to be used as unique identifier
        '''
        unique_id = self.url.split('/')[5]
        return unique_id



    def get_uuid(self):
        '''Generates a random Universally Unique ID (UUID) for each property and appends to the dictionary

        Returns:
            str: string to be used as universally unique identifier
        '''
        uni_uid = str(uuid.uuid4())
        return uni_uid



    def get_property_img(self):
        '''Generates a list of links for all the images for the current property and appends to the dictionary

        Returns:
            list: list of links for each image of property
        '''
        property_img_list = []
        next_img = self.driver.find_element(By.XPATH, '//main/div/div/section//button[@aria-label= "Next image"]')
        property_imgs = self.driver.find_elements(By.XPATH, '//main/div/div/section//li')
        for property in property_imgs[1:-1]:
            displayed_img = property.find_element(By.XPATH, '//main/div/div/section//li[@aria-hidden= "false"]')
            img_tag = displayed_img.find_element(By.XPATH, './/img')
            src_link = img_tag.get_attribute('src')
            property_img_list.append(src_link)
            next_img.click()
        return property_img_list



    def get_price(self, error_msg, info_container):
        '''Gets the price attribute of the property

        Returns:
            str: price of property
        '''
        try:
            price = info_container.find_element(By.XPATH, '//*[@data-testid= "price"]').text
            print(type(price))
            return price
        except:
            return error_msg



    def get_description(self, error_msg, info_container):
        '''Gets description of property
        
        Returns:
            str: description of property
        '''
        try:
            description = info_container.find_element(By.XPATH, './div//*[text()[contains(., "for")]]').text
            return description
        except:
            return error_msg



    def get_bathrooms(self, error_msg, info_container):
        '''Gets number of bathrooms of property
        
        Returns:
            str: number of bathrooms of property
        '''
        try:
            bathroom = info_container.find_element(By.XPATH, './div//*[text()[contains(., "bath")]]').text
            return bathroom
        except:
            return error_msg
        


    def get_address(self, error_msg, info_container):
        '''Gets address of property
        
        Returns:
            str: address of property
        '''
        try:
            address = info_container.find_element(By.XPATH, '//*[@data-testid= "address-label"]').text
            return address
        except:
            return error_msg



    def change_page(self):
        '''Clicks the next button to change to the next page
        '''
        next_page = self.driver.find_element(By.XPATH, '//*[@class= "css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2"]')
        next_page.click()



    def create_raw_data_folder(self):
        '''Deletes existing raw_data folder and generates new one
        '''
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



    def create_id_folders(self, property_counter):
        '''Creates folders in the raw_data folder for each property. The name of each folder is the UID generated earlier

        Args:
            property_counter (int): position of property in order of getting info

        Returns:
            str: path to current property directory
        '''
        parent_dir = '/home/muaz/Desktop/AiCore/Data_Collection_Pipeline/raw_data/'
        directory = self.property_dict['Property'][property_counter]['UID']
        uid_directory = os.path.join(parent_dir, directory)
        os.mkdir(uid_directory)
        return uid_directory



    def create_data_files(self, uid_directory, property_counter):
        '''Inside the relevant property folder, creates a file 'data.json' containing information obtained for the property

        Args:
            uid_directory (str): path to current property directory
            property_counter (int): position of property in order of getting info
        '''
        with open(os.path.join(uid_directory, 'data.json'), 'a+') as outfile:
            json.dump(self.property_dict['Property'][property_counter], outfile, indent= 4)
        s3_client.upload_file(f'{uid_directory}/data.json', 'muazaicoredcp', f'data_{self.property_dict["Property"][property_counter]["UID"]}')



    def make_img_folder(self, uid_directory):
        '''Inside the relevant property folder, creates a folder named 'images' to store property images

        Args:
            uid_directory (str): path to current property directory
        '''
        directory = 'Images'
        img_path = os.path.join(uid_directory, directory)
        os.mkdir(img_path)
        return img_path



    def download_imgs(self, img_directory, property_counter):
        '''Downloads the images for the property as a .jpg file with the image number as the image name

        Args:
            img_directory (str): path to directory in which property images are stored
            property_counter (int): position of property in order of getting info
        '''
        property_img_list = self.property_dict['Property'][-1]['IMG links']
        file_count = 1
        for img in property_img_list:
            urllib.request.urlretrieve(img, f'{img_directory}/img_{file_count}.jpg')
            s3_client.upload_file(f'{img_directory}/img_{file_count}.jpg', 'muazaicoredcp', f'img_{self.property_dict["Property"][property_counter]["UID"]}_{file_count}')
            file_count += 1



    def get_links(self):
        '''Runs the part of the script related to getting property links
        '''
        self.driver.get(self.url)
        # self.driver.maximize_window()
        time.sleep(2)
        self.accept_cookies()
        time.sleep(2)
        self.search_ng8()
        time.sleep(3)
        # page_counter = 1
        # while page_counter < 5:
        #     if page_counter == 2:
        #         self.close_email_popup()
        #     property_list = self.get_property_links()
        #     self.big_list.extend(property_list)
        #     self.change_page()
        #     time.sleep(1)
        #     page_counter += 1
        property_list = self.get_property_links()
        self.big_list.extend(property_list)
        print(len(self.big_list))



    def get_info(self):
        '''Runs the part of the code related to getting the property information. Also calls the get_images() function within the loop
        '''
        property_counter = 0
        error_msg = 'N/A'
        self.create_raw_data_folder()
        for property in self.big_list:
            self.url = property
            time.sleep(1)
            self.driver.get(self.url)
            time.sleep(1)
            info_container = self.driver.find_element(By.XPATH, '//*[@data-testid= "listing-summary-details"]')
            price = self.get_price(error_msg, info_container)
            description = self.get_description(error_msg, info_container)
            bathrooms = self.get_bathrooms(error_msg, info_container)
            address = self.get_address(error_msg, info_container)
            img = self.get_property_img()
            uid = self.get_unique_id()
            uni_uid = self.get_uuid()

            current_property = {'Link' : property, 'Price' : price, 'Description' : description, 'Bathrooms' : bathrooms,
            'Address' : address, 'IMG links' : img, 'UID' : uid, 'UUID' : uni_uid}

            self.property_dict['Property'].append(current_property)

            uid_directory = self.create_id_folders(property_counter)
            self.create_data_files(uid_directory, property_counter)
            # self.get_images(uid_directory, property_counter)
            property_counter += 1
            print(f'Got info for property {property_counter}')
    


    def get_images(self, uid_directory, property_counter):
        '''Runs the part of the code related to downloading property images into their relevant directories

        Args:
            uid_directory (str): path to current property directory
            property_counter (int): position of property in order of getting info
        '''
        img_directory = self.make_img_folder(uid_directory)
        print('Downloading images...')
        self.download_imgs(img_directory, property_counter)
        print('Folders created and data stored')



def scrape(url, driver):
    p = Scraper(url, driver)
    p.get_links()
    p.get_info()



if __name__ == '__main__':
    url = 'https://www.zoopla.co.uk/'
    driver = webdriver.Chrome()
    scrape(url, driver)