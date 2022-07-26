from cmath import exp
from scraper import Scraper
from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import os
import json


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
        uid_directory = self.scraper.get_info()
        with open (f'{uid_directory}/data.json') as json_file:
            data = json.load(json_file)
        if 'Link' and 'Price' and 'Description' and 'Bathrooms' and 'Address' and 'IMG links' and 'UID' and 'UUID' in data:
            assert True
        else:
            assert False
        
    def test_images_downloaded(self):
        uid_directory = self.scraper.get_info()
        self.scraper.get_images(uid_directory)
        img_dir = f'{uid_directory}/Images/'
        expected = len(self.scraper.property_dict['Property'][-1]['IMG links'])
        actual = (len([name for name in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, name))]))
        self.assertEqual(expected, actual)






unittest.main(argv=[''], verbosity=2)