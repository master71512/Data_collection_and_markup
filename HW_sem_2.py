import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import json

# получаем контент страницы
url = "https://books.toscrape.com/"
books_info = list()
for i in range(2):
    website = requests.get(url)
    html = website.content
    init_soup = BeautifulSoup(html, "html.parser")
    # на странице посмотрели имя нужного класса
    image_containers = init_soup.find_all('div', ('class', 'image_container'))
    rel_links = [container.find('a').get('href')
                 for container in image_containers]  # ищем все ссылки
    # склеиваем абсолютную и относительную ссылку, сохранем в список
    abs_links = [urllib.parse.urljoin(url, rel_link) for rel_link in rel_links]
    for abs_link in abs_links:  # открываем каждую ссылку из списка и парсим необходимые данные
        soup = BeautifulSoup(requests.get(abs_link).content, 'html.parser')
        div = soup.find('div', ('class', 'col-sm-6 product_main'))
        title = div.find('h1').text
        price_str = div.find('p', ('class', 'price_color')).text
        available = div.find('p', ('class', 'instock availability')).text
        available = int(re.findall(r'\b\d+\b', available)[0])
        description = soup.find("meta", attrs={"name": "description"})[
            "content"].strip()
        # сохраняем все данные в словарь и добавляем в список
        books_info.append({"title": title, "price": price_str,
                          "available": available, "description": description})
        print(books_info[i])
    # ищем ссылку на следующую страницу
    next_li = init_soup.find('li', ('class', 'next'))
    if not next_li:
        break  # если ссылки нет - останавливаем цикл
    # если ссылка есть - сохраняем url и в ледующей итерации парсим ее
    next_link = next_li.find('a')['href']
    url = urllib.parse.urljoin(url, next_link)

with open("books.json", "w") as file:
    json.dump(books_info, file)  # сохраняем данные в файл
