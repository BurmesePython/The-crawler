import requests
from bs4 import BeautifulSoup
import time
import pymongo


def get_urls(url):    # 获取子页面链接
    url_list = []
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    urls = soup.select('div.hd a')
    for i in urls:
        url_list.append(i['href'])
    return url_list


def get_page_info(url):    # 获取子页面信息
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    try:
        info_data = {
            '''
            name:电影名称, img:电影图片链接, year:上映时间, director:导演,
            starring：主演, release_date:上映时间, running_times:片长,
            rating_values:评分, evaluations:评价数
            '''
            'name': soup.select('h1 span:nth-of-type(1)')[0].text,
            'img': [i['src'] for i in soup.select('a.nbgnbg img')][0],
            'year': soup.select('#content > h1 > span.year')[0].text,
            'director': soup.select('#info > span:nth-of-type(1) > span.attrs > a')[0].text,
            'starring': [i.text for i in soup.select('span.actor span  a')],
            'release_date': [i.text for i in soup.find_all('span', property="v:initialReleaseDate")],
            'running_times': soup.find_all('span', property="v:runtime")[0].text,
            'rating_values': soup.select('div.rating_self.clearfix > strong')[0].get_text(),
            'evaluations': soup.select('a.rating_people span')[0].text
        }
        return info_data
    except:
        pass


def get_pages():    # 爬取的页数
    page = []
    for i in range(0, 250, 25):
        url = 'https://movie.douban.com/top250?start={}'.format(i)
        page.append(url)
    return page


if __name__ == '__main__':
    client = pymongo.MongoClient('localhost', 27017)
    dianying = client['dianying']
    sheet = dianying['sheet']

    for i in get_pages():
        for j in get_urls(i):
            data = get_page_info(j)
            if data == None:    #子页面信息为None时，跳过存储
                continue
            else:
                sheet.insert_one(get_page_info(j))
                print(data)
            time.sleep(1)
    print('已完成')


