from cmath import exp
from scraper import Scraper
from selenium import webdriver
import unittest
import uuid
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import os
import shutil
import urllib.request
import tempfile


class ScraperTestCase(unittest.TestCase):

    def setUp(self):
        self.scraper = Scraper('https://www.zoopla.co.uk/', webdriver.Chrome())
        self.scraper.driver.get(self.scraper.url)
        time.sleep(1)
        self.scraper.accept_cookies()
        self.scraper.search_ng8()
        time.sleep(2)


    # def test_accept_cookies(self):
    #     try:
    #         self.scraper.driver.find_element(By.XPATH, '//*[@id= "gdpr-consent-notice"]')
    #     except NoSuchElementException:
    #         assert True

    # def test_search_ng8(self):
    #     expected = 'https://www.zoopla.co.uk/for-sale/property/ng8/?q=NG8%20%20Nottingham%2C%20Wollaton%2C%20Aspley&search_source=home'
    #     actual = self.scraper.driver.current_url
    #     self.assertEqual(expected, actual)
        
    # def test_links_per_page(self):
    #     expected = 25
    #     actual = len(self.scraper.get_property_links())
    #     self.assertEqual(expected, actual)

    # def test_change_page(self):
    #     self.scraper.change_page()
    #     time.sleep(2)
    #     expected = 'https://www.zoopla.co.uk/for-sale/property/ng8/?q=NG8%20%20Nottingham%2C%20Wollaton%2C%20Aspley&search_source=home&pn=2'
    #     actual = self.scraper.driver.current_url
    #     self.assertEqual(expected, actual)

    # def test_close_email_popup(self):
    #     self.scraper.change_page()
    #     self.scraper.close_email_popup()
    #     try:
    #         self.scraper.driver.find_element(By.XPATH, '//*[@class= "e1urp9zt0 css-1i01by8-StyledModal e13xjwxo11"]')
    #     except NoSuchElementException:
    #         assert True
        
    # def test_number_of_links_in_big_list(self):
    #     counter = 0
    #     while counter < 2:
    #         if counter == 1:
    #             self.scraper.close_email_popup()
    #         property_list = self.scraper.get_property_links()
    #         self.scraper.big_list.extend(property_list)
    #         self.scraper.change_page()
    #         counter += 1
    #         time.sleep(2)
    #     expected = 50
    #     actual = len(self.scraper.big_list)
    #     self.assertEqual(expected, actual)

    def test_data_file_contents(self):
        self.scraper.create_raw_data_folder()
        proplist = self.scraper.get_property_links()
        time.sleep(2)
        self.scraper.info_dict['Link'].append(proplist[0])
        property_counter = 0
        self.scraper.url = proplist[0]
        print(proplist[0])
        self.scraper.driver.get(self.scraper.url)
        time.sleep(2)
        self.scraper.get_property_info()
        self.scraper.get_property_img()
        self.scraper.get_unique_id()
        self.scraper.get_uuid()
        uid_directory = self.scraper.create_id_folders(property_counter)
        data = self.scraper.create_data_files(uid_directory, property_counter)
        data.seek(0)
        content = data.read()
        print(content)

        






unittest.main(argv=[''], verbosity=2)