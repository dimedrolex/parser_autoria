import requests
from bs4 import BeautifulSoup


URL = 'https://auto.ria.com/uk/car/lincoln/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0', 'accept': '*/*'}
HOST = 'https://auto.ria.com'


# Функция get-запрос к серверу 
# params - определение числа страниц
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)      
    return r


# Функция сбора данных с сайта
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('section', class_='ticket-item')
    # print(items)
    cars = []
    for item in items[:3]:
        cars.append({
            'title': item.find('a', class_='address').get_text(strip=True),
            'link': HOST + item.find('a', class_='address').get('href'),
            'usd_price': item.find('span', class_='bold green size22').get_text(strip=True) + '$',
            'uah_price': item.find('span', class_='i-block').get_text(strip=True),
            'picture': item.find('a', class_='photo-185x120').get('href'),
            'city': item.find('li', class_ = 'item-char view-location js-location').get_text(strip=True),
        })
    for present in cars:
        print(f'{present["title"]} -> Link: {present["link"]} \nPicture: {present["picture"]}\nLocation: {present["city"]}\nPrice_USD: {present["usd_price"]} == Price_UAH: {present["uah_price"]}\n')


# Основная функция парсинга страницы
def parse():
    html = get_html(URL)
    # Проверяем связь со страицей
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')   

parse()
