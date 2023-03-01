import requests
import pandas as pd
import time


# 爬虫
def crawler():
    re = []
    header = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }
    Cookie = {'Cookie': ''}
    for ii in range(19):
        # 抗疫日记
        url_base = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D60%26q%3' \
                   'D%23%E6%8A%97%E7%96%AB%E6%97%A5%E8%AE%B0%23%26t%3D0&page_type=searchall'
        url = url_base + str(ii + 1)
        html = requests.get(url, headers=header, cookies=Cookie)
        try:
            for jj in range(len(html.json()['data']['cards'])):
                if html.json()['data']['cards'][jj]['mblog']['isLongText'] == False:
                    text=html.json()['data']['cards'][jj]['mblog']['text']
                else:
                    text=html.json()['data']['cards'][jj]['mblog']['longText']['longTextContent']
                fin=""
                flag=False
                for i in text:
                    if i=='<':
                        flag=True
                    if i=='>':
                        flag=False
                    if flag:
                        continue
                    fin+=i
                data1 = [(html.json()['data']['cards'][jj]['mblog']['user']['id'],  # 用户 ID
                html.json()['data']['cards'][jj]['mblog']['user']['screen_name'],  # 用户名
                html.json()['data']['cards'][jj]['mblog']['reposts_count'],  # 转发数
                html.json()['data']['cards'][jj]['mblog']['comments_count'],  # 评论数
                html.json()['data']['cards'][jj]['mblog']['attitudes_count'],  # 点赞数量
                fin,
                html.json()['data']['cards'][jj]['mblog']['created_at'],  # 发表时间
                html.json()['data']['cards'][jj]['mblog']['source'])]  # 来源设备
                data2 = pd.DataFrame(data1)
                data2.to_csv('weibo_content-yq.csv', header=False, index=False, mode='a+',encoding='GBK')
                re.extend(data1)
        except:
            print("抓取失败")
        print('page ' + str(ii + 1) + ' has done')
        time.sleep(3)
    return re


comments = crawler()

