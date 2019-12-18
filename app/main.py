from pymongo import MongoClient
from wotreplay import Wotreplay
from download import Download
import time
import requests

client = MongoClient('mongodb://127.0.0.1:27017')

# 入口函数
def main():
    init()
    while True:
        getDownloadUrl()
        getPlayerInfo()

# 初始化
def init():
    message('初始化')
    dblist = client.list_database_names()
    if 'wotreplay-collecter' not in dblist:
        client['wotreplay-collecter']['configs'].insert_many([
            { 'server': 'ru', 'version': 80, 'page': 1 },
            { 'server': 'eu', 'version': 85, 'page': 1 }
        ])

# 获取下载连接
def getDownloadUrl():
    message('获取下载连接')
    configsCol = client['wotreplay-collecter']['configs']
    message('获取配置')
    for config in configsCol.find():
        message(config['server'] + '服务器')
        download = Download(config['server'], config['version'])
        flag = False
        for page in range(config['page']):
            message('获取第{0}页下载url'.format(page+1))
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
    message('获取玩家信息')
    downloadsCol = client['wotreplay-collecter']['downloads']      
    for downloadInfo in downloadsCol.find({ 'isDownload': 0 }):
        message('下载{0}的文件'.format(downloadInfo['url']))
        f = requests.get(downloadInfo['url'])
        timeStamp = int(time.time())
        filePath = './wotreplayFiles/{0}.wotreplay'.format(timeStamp)
        with open(filePath, 'wb') as code:
            code.write(f.content)
        try:
            message('开始解析{0}'.format(filePath))
            replay = Wotreplay(filePath, True)
            message('插入玩家数据到数据库')
            client['wotreplay-collecter']['players'].insert_many(replay.playerList)
            downloadsCol.update_one( { 'url': downloadInfo['url'] }, { '$set': { 'isDownload': 1 } } )
        except:
            downloadsCol.update_one( { 'url': downloadInfo['url'] }, { '$set': { 'isDownload': 2 } } )   

# 消息
def message(text):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '   ' + text)

if __name__ == '__main__':
    main()