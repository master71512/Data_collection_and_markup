from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import urllib.parse
import time
import json
import pandas as pd


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
url = "https://eu-market.ru"
chrome_option = Options()
chrome_option.add_argument(f'{user_agent=}')
driver = webdriver.Chrome(options=chrome_option)
driver.get(url)


search_box = driver.find_element(
    By.ID, 'title-search-input-1')
search_box.send_keys("крышка")
search_box.submit()

show_all = driver.find_element(By.XPATH,
                               "//a[text()='Показать все товары']")
show_all.click()
response = requests.get(driver.current_url)
driver.close()
soup = BeautifulSoup(response.content, 'html.parser')
items = soup.find_all(
    'a', ('class', 'catalog-item-wrapper item-top-wrapper image-link'))
items_links = [urllib.parse.urljoin(url, item.get('href')) for item in items]

result = []
for i in range(10):
    soup = BeautifulSoup(requests.get(items_links[i]).content, 'html.parser')
    vendor_code = soup.find('span', ('class', 'code')).text
    name = soup.find('h1').text
    price = float(soup.find('div', ('class', 'current-price')
                            ).find('span').text.strip())
    link = items_links[i]
    result.append({'vendor_code': vendor_code,
                   'name': name,
                   'price': price,
                   'link': link})
    time.sleep(2)

with open("result.json", 'w', encoding="U8") as f:
    json.dump(result, f, ensure_ascii=False)

df = pd.DataFrame(result)
df.to_csv("em_parse.csv", mode='a', index=False)
