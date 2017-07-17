import requests
import json
import jieba
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


# 获取新闻标题
def get_title(url):
    title = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Cookie': 'aliyungf_tc=AQAAAM2wy2fVBgcAIVuVJCb1oNqwn0ue; xq_a_token=0a52c567442f1fdd8b09c27e0abb26438e274a7e; xq_a_token.sig=dR_XY4cJjuYM6ujKxH735NKcOpw; xq_r_token=43c6fed2d6b5cc8bc38cc9694c6c1cf121d38471; xq_r_token.sig=8d4jOYdZXEWqSBXOB9N5KuMMZq8; u=771499919053313; device_id=766809662fb787b3417926e7e917fb94; Hm_lvt_1db88642e346389874251b5a1eded6e3=1499919055; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1499921390; Hm_lvt_9d483e9e48ba1faa0dfceaf6333de846=1499919055; Hm_lpvt_9d483e9e48ba1faa0dfceaf6333de846=1499921390',
        'X-Requested-With': 'XMLHttpRequest',
    }
    r = requests.get(url, headers=headers)
    # 返回的数据是json，用json解析
    json1 = json.loads(r.text)
    for i in range(0, 15):
        json2 = json.loads(json1['list'][i]['data'])
        if json2['title'] == '':
            continue
        title.append(json2['title'])
    return title


# 获取页面数
def get_num(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Cookie': 'aliyungf_tc=AQAAAM2wy2fVBgcAIVuVJCb1oNqwn0ue; xq_a_token=0a52c567442f1fdd8b09c27e0abb26438e274a7e; xq_a_token.sig=dR_XY4cJjuYM6ujKxH735NKcOpw; xq_r_token=43c6fed2d6b5cc8bc38cc9694c6c1cf121d38471; xq_r_token.sig=8d4jOYdZXEWqSBXOB9N5KuMMZq8; u=771499919053313; device_id=766809662fb787b3417926e7e917fb94; Hm_lvt_1db88642e346389874251b5a1eded6e3=1499919055; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1499921390; Hm_lvt_9d483e9e48ba1faa0dfceaf6333de846=1499919055; Hm_lpvt_9d483e9e48ba1faa0dfceaf6333de846=1499921390',
        'X-Requested-With': 'XMLHttpRequest',
    }
    r = requests.get(url, headers=headers)

    next_id = json.loads(r.text)
    return next_id['next_id']


# 获取页面
def get_url(next_id):
    url = []
    base_url = 'https://xueqiu.com/v4/statuses/public_timeline_by_category.json?'
    # 构建id
    num = range(next_id, 20190000, -15)
    for i in num:
        params = {'since_id': -1,
                  'max_id': i,
                  'count': 15,
                  'category': -1}
        r = requests.get(base_url, params=params)
        url.append(r.url)
    return url


# 保存标题
def save_title(title):
    with open('title.txt', 'a', encoding='utf-8') as f:
        f.write(title + '\n')


# 提取关键词显示词云
def extract_words():
    text = open('title.txt', 'r', encoding='utf-8').read()
    # 禁用词表
    stopwords = set(STOPWORDS)
    # jieba精确模式分词
    word_jieba = jieba.cut(text, cut_all=False)
    word_split = " ".join(word_jieba)
    wordcloud = WordCloud(font_path='simhei.ttf', max_words=200, width=1600, height=800, stopwords=stopwords).generate(
        word_split)
    plt.imshow(wordcloud)
    plt.axis('off')
    wordcloud.to_file('wordcloud.jpg')
    plt.show()


if __name__ == '__main__':
    url = 'https://www.xueqiu.com/v4/statuses/public_timeline_by_category.json?since_id=-1&max_id=-1&count=5&category=-1'
    next_id = get_num(url)
    for url in get_url(next_id):
        for title in get_title(url):
            save_title(title)
    extract_words()
