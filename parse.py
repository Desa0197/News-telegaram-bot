import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime

# headers для того чтоб сайт не подумал, что я бот
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.148 YaBrowser/22.7.2.748 (beta) Yowser/2.5 Safari/537.36',
    'accept': '*/*'
}

URL = 'https://www.cybersport.ru/?sort=-publishedAt'


def get_html(url: str):
    # отправляю запрос на сайт
    response = requests.get(url, headers=HEADERS)
    return response


def get_content(html):
    # список для новостей
    list_news = []
    # создал объйкт soup для работы с html файлом
    soup = bs(html, 'html.parser')
    # получаем все блоки с новостями
    blocks_news = soup.find_all('a', class_='link_CocWY')
    # пробегаю по всем блокам с новостями
    for block in blocks_news[:10]:
        # достаю ссылку
        link = f'https://www.cybersport.ru{block.get("href")}'
        # достаю название
        title = block.find('h3', class_='title_nSS03').text.strip()
        # достаю время в формате unix timestamp
        block_date_time = block.find('time').get('datetime')
        unix_date_time = datetime.fromisoformat(block_date_time)
        # перевел в человечский вид
        date_time = datetime.strftime(unix_date_time, '%d-%m-%Y %H:%M')
        # добавил словарь с иноформацие о новости в список
        list_news.append({
            'link': link,
            'title': title,
            'date_time': date_time
        })
    # перевернул список
    list_news.reverse()
    return list_news


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        content = get_content(html.content)
        return content
    else:
        print('Error')
