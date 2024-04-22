#-----------Importing Data----------------------
import pandas as pd
import numpy as np
dataset = pd.read_csv('./archive/ikea.csv')
dataset.drop(dataset.columns[0], axis=1, inplace=True)
dataset['image_paths'] = [None]*len(dataset)

print(dataset)

#----------Function for saving images----------
import os
import requests

def download_images(image_urls, save_folder):

    file_names = []

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                file_name = f'image{i+1}.jpg'
                file_path = os.path.join(save_folder, file_name)
                file_names.append(file_name)
                
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                #print(f"Downloaded {file_path}")
            else:
                print(f"Failed to download image from {url}")
        except requests.RequestException as e:
            print(f"Error downloading {url}: {e}")

    return file_names

#-----------Scraping Data----------------------
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--headless')  # Run headless Chrome
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--log-level=3')  # This attempts to suppress most console messages
options.set_capability('goog:loggingPrefs', {'browser': 'OFF'})  # Try to suppress browser logs

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

import tqdm

for i in tqdm.tqdm(range(0,len(dataset))):
    #url = 'https://www.ikea.com/sa/en/p/norberg-wall-mounted-drop-leaf-table-white-30180504/'
    url = dataset.iloc[i]['link']
    item_id = dataset.iloc[i]['item_id']
    driver.get(url)

    import time
    #time.sleep(10)

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    file_names = []

    if soup is not None:
        main_section = soup.find('main')
        if main_section is not None:
            div1 = main_section.find('div', class_='pip-page-container')
            if div1 is not None:
                div2 = div1.find('div', class_='pip-page-container__inner')
                if div2 is not None:
                    div3 = div2.find('div', class_='pip-page-container__main')
                    if div3 is not None:
                        div4 = div3.find('div', class_='pip-product__subgrid product-pip js-product-pip')
                        if div4 is not None:
                            div5 = div4.find('div', class_='pip-product__left-top pip-product-gallery__left-top')
                            if div5 is not None:
                                div6 = div5.find('div', class_='js-product-gallery pip-product-gallery')
                                if div6 is not None:
                                    div7 = div6.find('div', class_='pip-product-gallery__thumbnails')
                                    if div7 is not None:
                                        images = div7.find_all('img')
                                        image_urls = [img['src'] for img in images if 'src' in img.attrs]
                                        if image_urls is not None:
                                            file_names = download_images(image_urls, f'./images/{item_id}')
                                            dataset.at[i, 'image_paths'] = file_names

    if len(file_names) == 0:
        print(f'Error occured when trying to download images for item: {item_id}')

driver.quit()


print(dataset[:11])