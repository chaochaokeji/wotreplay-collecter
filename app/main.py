
from pymongo import MongoClient
from wotreplay import Wotreplay
from download import Download
import time
import requests

client = MongoClient('mongodb://mongo:27017')

# 入口函数
def main():
    init()
    while True:
        getDownloadUrl()
        getPlayerInfo()

# 初始化
def init():
    print('初始化')
    dblist = client.list_database_names()
    if 'wotreplay-collecter' not in dblist:
        client['wotreplay-collecter']['configs'].insert_many([
            { 'server': 'ru', 'version': 79, 'page': 100 },
            { 'server': 'eu', 'version': 84, 'page': 100 }
        ])

# 获取下载连接
def getDownloadUrl():
    print('获取下载连接')
    configsCol = client['wotreplay-collecter']['configs']
    print('获取配置')
    for config in configsCol.find():
        print(config['server'] + '服务器')
        download = Download(config['server'], config['version'])
        flag = False
        for page in range(config['page']):
            print('获取第{0}页下载url'.format(page+1))
            downloadsCol = client['wotreplay-collecter']['downloads']
            for url in download.downloadUrlList(page+1):
                if downloadsCol.find_one({ 'url': url }):
                    flag = True
                    break
                else:
                    downloadsCol.insert_one({ 'url': url, 'isDownload': 0 })
            if flag:
                break    

# 获取玩家信息
def getPlayerInfo():                
    print('获取玩家信息')
    downloadsCol = client['wotreplay-collecter']['downloads']      
    for downloadInfo in downloadsCol.find({ 'isDownload': 0 }):
        print('下载{0}的文件'.format(downloadInfo['url']))
        f = requests.get(downloadInfo['url'])
        timeStamp = int(time.time())
        filePath = './wotreplayFiles/{0}.wotreplay'.format(timeStamp)
        with open(filePath, 'wb') as code:
            code.write(f.content)
        print('开始解析{0}'.format(filePath))
        replay = Wotreplay(filePath, True)
        print('插入玩家数据到数据库')
        client['wotreplay-collecter']['players'].insert_many(replay.playerList)
        downloadsCol.update_one( { 'url': downloadInfo['url'] }, { '$set': { 'isDownload': 1 } } )

if __name__ == '__main__':
    main()