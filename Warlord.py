
import requests
from bs4 import BeautifulSoup
import csv
import os

os.remove('Warlord.csv')

with open('Warlord.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(('fraction', 'title', 'price', 'status', 'url'))

def get_html(url):
    r = requests.get(url)
    return r.text

def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('p', style='text-align: left;').find_all('a')
    links = []
    for td in tds:
        a = td.href
        link = a
        links.append(link)
    return links

def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('ul', class_='pagination')
    if pages is None:
        total_pages = '1'
    else:
        pages = soup.find('li', class_='pagination-item').find_all('a', title='В конец').get('href')
        total_pages = pages.split('=')[1]

    return int(total_pages)

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    try:
        fraction = soup.find('div', class_= 'collection-content float-xl-9 float-lg-12').find('h1').text.strip()
    except:
        fraction = ''

    ads = soup.find('div', class_='collection-products row-flex').find_all('div', class_='product-card flex-xl-4 flex-lg-4 flex-md-6 flex-xs-12')
    for ad in ads:
        try:
            title = ad.find('div', class_='product-image').find('a').get('title')
        except:
            title = ''
        try:
            price = ad.find('div', class_='price').find('span', class_='price-number').text.strip()
        except:
            price = ''
        try:
            status = ad.find('div', class_='product-toolbar').find('a', class_='btn button inverted btn-more-info').text.strip()
            if status == 'В корзину':
                status = 'В наличии'
            else:
                status = 'Нет в наличии'
        except:
            status = 'Нет в наличии'
        try:
            url = ad.find('div', class_='product-image').find('a').get('href')
        except:
            url = ''

        data = {'fraction': fraction,
            'title': title,
            'price': price,
            'status': status,
            'url': url}
        write_csv(data)

def write_csv(data):
    with open('Warlord.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['fraction'],
                         data['title'],
                         data['price'],
                         data['status'],
                         data['url']))


def main():
    url = 'https://warlord.ru/collection/WH40K'

    all_links = get_all_links(get_html(url))

    for link in all_links:
        html = get_html(link)

        total_pages = get_total_pages(html)

        for i in range(1, total_pages+1):
            url_gen = link + '?page=' + str(i)
            html = get_html(url_gen)
            get_page_data(html)


if __name__ == '__main__':
    main()