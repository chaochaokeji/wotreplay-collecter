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
