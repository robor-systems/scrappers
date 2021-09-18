import json
import pprint
import xlsxwriter
import time
import csv

import pprint
import sys
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

import re 

import os
from dotenv import load_dotenv

load_dotenv() # read .env file

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome('chromedriver.exe') 
df = pd.DataFrame(columns=['website','phone numbers'])

def searchRegex(page_src, url):
    global df
    pattern = re.compile(r"(\([0-9]{3}\)\s?|[0-9]{3}-)[0-9]{3}-[0-9]{4}")
    phone_num = re.search(pattern, page_src)

    if phone_num: 
        print(f'Found: ${phone_num.group()} from ${url} using regex')
        
        new_row = {'website': url, 'phone numbers': phone_num.group()}
        df = df.append(new_row, ignore_index=True)
    else:
        print(f'NOT FOUND at ${url} using regex')
        new_row = {'website': url, 'phone numbers': 'NOT FOUND'}
        df = df.append(new_row, ignore_index=True)

def main(): 
    global df
    f = open('websites.json')
    data = json.load(f)

    websites = data['websites']

    for url in websites:
        print(url)
        driver.get(url)
        try:
            phone_num_elem = driver.find_element_by_css_selector('a[href^="tel:"')
            phone_num = phone_num_elem.get_attribute('href')
            # phone_num = phone_num_elem.get_attribute('innerText')

        except NoSuchElementException:
            print("can't find phone number using a tag")
            searchRegex(driver.page_source, url)
            continue

        else:
            print(f'Found: ${phone_num} from ${url} using css selector')

            new_row = {'website': url, 'phone numbers': phone_num}
            df = df.append(new_row, ignore_index=True)


    pprint.pprint(df)
    df.to_excel("websites_data.xlsx")
    driver.quit()

if __name__ == "__main__":
    main()