import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import json

# получаем контент страницы
url = "https://books.toscrape.com/"
books_info = list()
while True:
    website = requests.get(url)
    html = website.content
    init_soup = BeautifulSoup(html, "html.parser")
    # на странице посмотрели имя нужного класса
    image_containers = init_soup.find_all('div', ('class', 'image_container'))
    rel_links = [container.find('a').get('href') for container in image_containers] # ищем все ссылки
    abs_links = [urllib.parse.urljoin(url, rel_link) for rel_link in rel_links] # склеиваем абсолютную и относительную ссылку, сохранем в список
    for abs_link in abs_links: # открываем каждую ссылку из списка и парсим необходимые данные
        soup = BeautifulSoup(requests.get(abs_link).content, 'html.parser')
        div = soup.find('div', ('class', 'col-sm-6 product_main'))
        title = div.find('h1').text
        price_str = div.find('p', ('class', 'price_color')).text
        available = div.find('p', ('class', 'instock availability')).text
        available = int(re.findall(r'\b\d+\b', available)[0])
        description = soup.find("meta", attrs={"name": "description"})["content"].strip()
        books_info.append({"title": title, "price": price_str, "available": available, "description": description}) # сохраняем все данные в словарь и добавляем в список
    next_li = init_soup.find('li', ('class', 'next')) # ищем ссылку на следующую страницу
    if not next_li:
        break # если ссылки нет - останавливаем цикл
    next_link = next_li.find('a')['href'] # если ссылка есть - сохраняем url и в ледующей итерации парсим ее
    url = urllib.parse.urljoin(url, next_link)
with open("books.json", "w") as file:
    json.dump(books_info, file) # сохраняем данные в файл
