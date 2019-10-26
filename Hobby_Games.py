
import requests
from bs4 import BeautifulSoup
import csv
import os


os.remove('Hobby_Games.csv')

with open('Hobby_Games.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(('title', 'price', 'status', 'url'))

def get_html(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='paginate').find('a', class_='last').get('href')
    total_pages = pages.split('=')[1].split('&')[0]

    return int(total_pages)

def write_csv(data):
    with open('Hobby_Games.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'],
                         data['price'],
                         data['status'],
                         data['url']))

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    ads = soup.find('div', class_='row products-container').find_all('div', class_='col-lg-4 col-md-6 col-sm-6 col-xs-12')
    for ad in ads:
        try:
            title = ad.find('div', class_='name-desc').find('a').get('title')
        except:
            title = ''
        try:
            price = ad.find('div', class_='buttons product-cart').find('span', class_='price').text.strip()
        except:
            price = ''
        try:
            status = ad.find('div', class_='buttons product-cart').find('span', class_='in-cart text hidden').text.strip()
            if status == 'Оформить заказ':
                status = 'В наличии'
            else:
                status = 'Нет в наличии'
        except:
            status = 'Нет в наличии'
        try:
            url = ad.find('div', class_='name-desc').find('a', class_='name').get('href')
        except:
            url = ''
        data = {
            'title': title,
            'price': price,
            'status': status,
            'url': url
        }
        write_csv(data)

def main():
    url = 'https://hobbygames.ru/armii'
    base_url = 'https://hobbygames.ru/armii?page='
    page_part = '&parameter_type=0'

    total_pages = get_total_pages(get_html(url))

    for i in range(1, total_pages+1):
        url_gen = base_url + str(i) + page_part
        html = get_html(url_gen)
        get_page_data(html)

if __name__ == '__main__':
    main()
