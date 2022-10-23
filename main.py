import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os
from tqdm import tqdm
from selenium.webdriver.common.keys import Keys

sleep_between_interactions = 2


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+8 to toggle the breakpoint.

def progress_bar(current, total):
    tqdm(current, total)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    print('Starting...')
    driver = webdriver.Chrome()
    driver.get('https://www.marvel.com/comics/list/623/get_started_with_free_issues')
    results = []
    content = driver.page_source
    soup = BeautifulSoup(content)
    soup_list = soup.find_all(attrs={'class': 'row-item comic-item'})
    total_comics = len(driver.find_elements(by=By.CSS_SELECTOR, value='div.row-item.comic-item'))

    print(f'\t{total_comics} comics have been found')
    if not os.path.exists('csvfile.csv'):
        f = open('csvfile.csv', 'w')
        f.write('title;image\n')
    else:
        f = open('csvfile.csv', 'a')

    # r = open("csvfile.csv", "r")
    os.makedirs(f'./images', exist_ok=True)

    for i in tqdm(range(total_comics)):
        title = soup_list[i].find('a', attrs={'class': 'meta-title'}).text
        title = title.replace("\n", "").replace(" ", "").replace("/", "-")
        with open('csvfile.csv') as r:
            if title in r.read():
                continue
        print(f'\nDownloading comic ({i + 1}/{total_comics}) - {title}')
        driver.find_elements(by=By.CSS_SELECTOR, value='div.row-item.comic-item')[i].click()
        time.sleep(sleep_between_interactions)
        read_now = driver.find_element(by=By.CSS_SELECTOR, value='a.cta-btn.cta-btn--solid.cta-btn--red.active')

        if 'READ NOW' in read_now.text:
            comic_code = read_now.get_attribute('href').split('book/', 1)[1]
            comic_url = f'https://bifrost.marvel.com/v1/catalog/digital-comics/web/assets/{comic_code}?rand={comic_code}'
            response = requests.get(comic_url)
            data = response.json()
            pages = data['data']['results'][0]['pages']
            page_count = 0
            for page in pages:
                page_count += 1
                response = requests.get(page['assets']['source'])
                image_name = f'{title}_{str(page_count).zfill(4)}.jpg'
                file = open(f'./images/{image_name}', 'wb')
                file.write(response.content)
                file.close()
                f.write(f'{title};{image_name}\n')

        driver.execute_script("window.history.go(-1)")
        time.sleep(sleep_between_interactions)

    f.close()

        # pages_menu = driver.find_element(by=By.CSS_SELECTOR, value='span.icon.allPages')
        # pages_menu.click()
        # time.sleep(sleep_between_interactions)
        # total_pages = driver.find_elements(by=By.CSS_SELECTOR, value='div.thumbs-wrap')

    #     time.sleep(sleep_between_interactions)
    #     thumbnail_pages = driver.find_elements(by=By.CSS_SELECTOR, value='div.thumbs.readable.activePage')
    #     for thumbnail_page in thumbnail_pages:
    #         thumbnail_page.click()
    #         possible = driver.find_elements(by=By.XPATH, value="//*[contains(@id, 'SvgjsImage')]")
    #         for item in possible:
    #             width = item.get_attribute('width')
    #             height = item.get_attribute('height')
    #
    #         #actual_image = driver.find_element(by=By.CLASS_NAME, value='svg-el')
    #         #content = actual_image.find_element(by=By.TAG_NAME, value='image')
    #         #href = content.get_attribute('id')
    #         #print(href)
    #         #soup = BeautifulSoup(content)
    #         time.sleep(sleep_between_interactions)
    #         print()
    #
    # content = driver.page_source
    # soup = BeautifulSoup(content)
    # for element in soup.find_all(attrs={'class': 'row-item comic-item'}):
    #     image_url = element.find('a', attrs={'class': 'row-item-image-url'})
    #     link = image_url['href']
    #     title = element.find('a', attrs={'class': 'meta-title'}).text
    #
    #     print(link)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
