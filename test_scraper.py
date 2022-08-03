from cmath import exp
from scraper import Scraper
from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import os
import json
import boto3

class ScraperTestCase(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper('https://www.zoopla.co.uk/', webdriver.Chrome())
        self.scraper.driver.get(self.scraper.url)
        time.sleep(1)
        self.scraper.accept_cookies()
        self.scraper.search_ng8()
        time.sleep(2)
        property_list = self.scraper.get_property_links()
        self.scraper.big_list.extend(property_list)


    def test_accept_cookies(self):
        try:
            self.scraper.driver.find_element(By.XPATH, '//*[@id= "gdpr-consent-notice"]')
        except NoSuchElementException:
            assert True

    def test_search_ng8(self):
        expected = 'https://www.zoopla.co.uk/for-sale/property/ng8/?q=NG8%20%20Nottingham%2C%20Wollaton%2C%20Aspley&search_source=home'
        actual = self.scraper.driver.current_url
        self.assertEqual(expected, actual)

    def test_change_page(self):
        self.scraper.change_page()
        time.sleep(2)
        expected = 'https://www.zoopla.co.uk/for-sale/property/ng8/?q=NG8%20%20Nottingham%2C%20Wollaton%2C%20Aspley&search_source=home&pn=2'
        actual = self.scraper.driver.current_url
        self.assertEqual(expected, actual)

    def test_close_email_popup(self):
        self.scraper.change_page()
        self.scraper.close_email_popup()
        try:
            self.scraper.driver.find_element(By.XPATH, '//*[@class= "e1urp9zt0 css-1i01by8-StyledModal e13xjwxo11"]')
        except NoSuchElementException:
            assert True

    def test_data_file_contents(self):
        self.scraper.url = self.scraper.big_list[0]
        time.sleep(2)
        self.scraper.driver.get(self.scraper.url)
        time.sleep(2) 
        uid = self.scraper.get_unique_id
        uid_directory = f'/home/muaz/Desktop/AiCore/Data_Collection_Pipeline/raw_data/{uid}'
        with open (f'{uid_directory}/data.json') as json_file:
            data = json.load(json_file)
        if 'Link' and 'Price' and 'Description' and 'Bathrooms' and 'Address' and 'IMG links' and 'UID' and 'UUID' in data:
            assert True
        else:
            assert False
        
    def test_images_downloaded(self):
        self.scraper.url = self.scraper.big_list[0]
        time.sleep(2)
        self.scraper.driver.get(self.scraper.url) 
        time.sleep(2)
        price, description, bathrooms, address, img, uid, uni_uid = self.scraper.get_info()
        current_property = {'Link' : self.scraper.url, 'Price' : price, 'Description' : description, 'Bathrooms' : bathrooms,
        'Address' : address, 'IMG links' : img, 'UID' : uid, 'UUID' : uni_uid}
        uid_directory = f'/home/muaz/Desktop/AiCore/Data_Collection_Pipeline/raw_data/{current_property["UID"]}'
        img_dir = f'{uid_directory}/Images/'
        expected = len(current_property['IMG links'])
        actual = len([name for name in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, name))])
        self.assertEqual(expected, actual)

    def test_bucket_contents(self):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('muazaicoredcp')
        bucket_list = []
        for obj in bucket.objects.all():
            bucket_list.append(obj)
        dir = '/home/muaz/Desktop/AiCore/Data_Collection_Pipeline/raw_data/'
        names = [n for n in os.listdir(dir) if os.path.isdir(os.path.join(dir, n))]
        img_file_count = 0
        data_file_count = 0
        for name in names:
            img_dir = f'{dir}{name}/Images'
            img_file_count += len([f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))])
            data_file_count += 1
        expected = img_file_count + data_file_count
        actual = len(bucket_list)
        self.assertEqual(expected, actual)







unittest.main(argv=[''], verbosity=2)