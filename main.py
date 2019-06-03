import requests
from bs4 import BeautifulSoup as bs
from multiprocessing.dummy import Pool as ThreadPool
import re

page_all = ['http://gov.tuva.ru/press_center/news/?PAGEN_1=%s' % i for i in range(1,405)]

def clear(str):
    str = re.sub( '\n', '', str )
    str = re.sub( '\t', '', str )
    str = re.sub( '\xa0', '', str )
    return str

def page_parser(page_url):
    url_page = []
    r = requests.get(page_url)
    soup = bs(r.text, 'lxml' )
    tag = (soup.findAll( "div",{"class": "news-item"}))
    for i in tag:
        url = ('http://gov.tuva.ru'+i.find("a").get('href'))
        url_page.append(url)
    return url_page

def get_page(page):
    r = requests.get(page)
    soup = bs(r.text, 'lxml')
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

with open( 'd:/AnacodaProgect/2019_may/govtuva.txt', 'a', encoding='utf8') as file:
    pool = ThreadPool(5)
    for page_url in page_all:
        try:
            news = pool.map(get_page, page_parser(page_url))
        except:
            print ('error page')
        for i in news:
            try:
                print (i)
                file.write(str(i)+'\n')
            except:
                print ('error news')
file.close()

