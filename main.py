import requests
from bs4 import BeautifulSoup as bs
from multiprocessing.dummy import Pool as ThreadPool
import re

SAVE_FILE = 'govtuva.txt'

def clear(str):
    str = re.sub( '\n', '', str)
    str = re.sub( '\t', '', str)
    str = re.sub( '\xa0', '', str)
    return str

def page_parser(page_url):
    '''Paginaion funcion'''
    url_page = []
    req = requests.get(page_url)
    soup = bs(req.text, 'lxml' )
    tag = (soup.findAll( "div",{"class": "news-item"}))
    for page_in in tag:
        url = ('http://gov.tuva.ru{}'.format(page_in.find("a").get('href')))
        url_page.append(url)
    return url_page

def get_page(page):
    '''Parser page'''
    req = requests.get(page)
    soup = bs(req.text, 'lxml')
    tag = (soup.findAll( "td", {"class": "main-column"} ))
    for i in tag:
        cat = i.find("ul", {"class": "breadcrumb-navigation"}).text.split('>')[-1][1:]
        title = i.find("h1").text
        title = clear(title)
        date = i.find("span", {"class": "news-date-time"}).text
        url = page
        content = i.find("div", {"class": "news-text"}).text
        content = clear(content)
        image = 'http://gov.tuva.ru'+i.find("div", {"class": "news-picture"}).find('img').get('src')
        item = [title,date,cat,content,url,image]
        news = {'title': title, 'content': content, 'cat': cat,'image': image, 'date': date, 'url': url,}
    return news

page_all = ['http://gov.tuva.ru/press_center/news/?PAGEN_1=%s' % i for i in range(1,405)]
with open(SAVE_FILE, 'a', encoding='utf8') as file:
    pool = ThreadPool(5)
    for page_url in page_all:
        try:
            news_pool = pool.map(get_page, page_parser(page_url))
        except Exception as e:
            print (e)
        for i in news_pool:
            file.write(str(i)+'\n')

file.close()
