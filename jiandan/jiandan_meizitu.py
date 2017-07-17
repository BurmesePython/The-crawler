# Filename :
# author by :

import requests
from bs4 import BeautifulSoup
import os


def url_open(url):    # 解析网页
    kv = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    r = requests.get(url, headers=kv)
    r.encoding = r.apparent_encoding
    return r.text


def get_page(url):
    html = url_open(url)
    soup = BeautifulSoup(html, 'html.parser')
    page_num = soup.find('span', 'current-comment-page')
    page_num = int(page_num.string.strip('[]'))
    return page_num


def find_imgs(url):    # 获取图片地址
    html = url_open(url)
    img_addrs = []
    soup = BeautifulSoup(html, 'html.parser')
    for i in soup.find_all('img')[0:-1]:
        img_addrs.append('http:' + i['src'])
    return img_addrs


def save_imgs(folder, img_addrs):    # 下载图片
    for each in img_addrs:
        r = requests.get(each)
        filename = each.split('/')[-1]
        with open(filename, 'wb') as f:
            f.write(r.content)


def main(folder=r'C:\Users\Arthas\Desktop\OOXX', pages=5):   # 设置默认下载5页
    os.mkdir(folder)   # 创建文件夹
    os.chdir(folder)
    url = 'http://jandan.net/ooxx/'
    page_num = int(get_page(url))
    for i in range(pages):
        page_num -= 1
        page_url = url + 'page-' + str(page_num) + '#comments'
        img_addrs = find_imgs(page_url)
        save_imgs(folder, img_addrs)

if __name__ == "__main__":
    main()

