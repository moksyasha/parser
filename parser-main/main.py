import requests
from bs4 import BeautifulSoup
import fake_useragent
import csv

user = fake_useragent.UserAgent().random
headers = {
    'user-agent': user
}


def get_html(url):
    r = requests.get(url, headers=headers)
    return r


def get_content(html):
    catalog = []
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='card-inner')
    for i in items:
        price = i.find('span', class_='price').get_text()
        price = price.replace(' ', '').replace('руб', '')
        name = i.find('img', class_='product-image')
        name = name["alt"]
        print("Name price ", name, price)
        if name is None:
            continue
        catalog.append({
            'name': name,
            'price': price,
        })
    return catalog


def main():
    filename = 'minons.csv'
    with open(filename, 'w', encoding='utf8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Название', 'Цена'])

    for URL in ['https://toyszone.ru/collection/gadkiy-ya-minony?page='+str(i) for i in range(1, 8)]:
        html = get_html(URL)
        contents = []
        if html.status_code == 200:
            contents = get_content(html.text)
        else:
            print('Error')

        with open(filename, 'a+', encoding='utf8', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            for item in contents:
                writer.writerow([item['name'], item['price']])


if __name__ == '__main__':
    main()
