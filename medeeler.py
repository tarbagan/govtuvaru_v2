import requests
from bs4 import BeautifulSoup as bs
import csv

SAVE_FILE = r'e:\PythonProgect\Test\govtuva.csv'

def requests_get(url):
    """# get request html from url"""
    # предусмотреть возможность получения разных header
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/71.0.3578.98 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r.text
    except Exception as e:
        return e

def search_url_page(html):
    try:
        url_part = []
        soup = bs(html, 'lxml')
        root_html = (soup.find('div', {'class': 'news-list'}))
        url_page = (root_html.findAll('p', {'class': 'news-item'}))
        for i in url_page:
            url =  'http://gov.tuva.ru' + i.find("a").get('href')
            if url:
                url_part.append(url)
        return url_part
    except:
        pass

def get_content(html):
    try:
        soup = bs(html, 'lxml')
        root_html = (soup.find('div', {'class': 'news-detail'}))
        text = root_html.text
        text = ''.join(text.split('\n')[3:])
        if text:
            return text
    except:
        pass

with open(SAVE_FILE, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    page_all = ['http://gov.tuva.ru/press_center/tyva_news/?PAGEN_1=%s' % i for i in range( 1, 178 )]
    for url in page_all:
        html = requests_get(url)
        try:
            for num, url_page in enumerate(search_url_page(html)):
                html_page = requests_get(url_page)
                text = get_content(html_page)
                if text:
                    print (text[0:200])
                    writer.writerow({'id': num, 'text': text})
        except:
            pass
