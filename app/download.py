# Download类

import time
import requests
from urllib import request
from bs4 import BeautifulSoup
from pymongo import MongoClient

class Download:
    
    def __init__(self, server, version):
        self.__server = server
        self.__version = version
    
    # 获取下载列表
    def downloadUrlList(self, page):
        # 拼接url地址
        self.__url = 'http://wotreplays.{0}/site/index/version/{1}/sort/uploaded_at.desc/page/{2}/'.format(self.__server, self.__version, page)
        
        # 爬取下载地址
        soup = BeautifulSoup(request.urlopen(self.__url), features='html.parser')
        list = []
        for link in soup.find_all('a', 'btn_l-grey'):
            if link.get('href'):
                list.append('http://wotreplays.{0}'.format(self.__server) + link.get('href'))
        return list

    # 下载replay
    def downloadReplay(self, url):
        # 判断url是否在数据库中存在
        client = MongoClient('mongodb://mongo:27017')
        downloadsCol = client['wotreplay-collecter']['downloads']
        doc = downloadsCol.find_one({ 'url': url })
        if doc:
            return ''

        # 下载
        f = requests.get(url)
        timeStamp = int(time.time())
        filePath = './wotreplayFiles/{0}.wotreplay'.format(timeStamp)
        with open(filePath, 'wb') as code:
            code.write(f.content)
        
        # 插入数据库
        downloadsCol.insert_one({ 'url': url })

        return filePath

