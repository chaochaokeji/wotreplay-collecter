
from pymongo import MongoClient
from wotreplay import Wotreplay
from download import Download

# 入口函数
def main():
    init()
    collect()

def init():
    client = MongoClient('mongodb://mongo:27017')
    dblist = client.list_database_names()
    if 'wotreplay-collecter' not in dblist:
        client['wotreplay-collecter']['configs'].insert_many([
            { 'server': 'ru', 'version': 79, 'page': 1 },
            { 'server': 'eu', 'version': 84, 'page': 1 }
        ])

def collect():
    print('连接数据库')
    client = MongoClient('mongodb://mongo:27017')
    configsCol = client['wotreplay-collecter']['configs']
    print('获取配置')
    for config in configsCol.find():
        print(config['server'] + '服务器')
        download = Download(config['server'], config['version'])
        flag = False
        for page in range(config['page']):
            print('获取第{0}页下载url'.format(page+1))
            for url in download.downloadUrlList(page+1):
                filePath = download.downloadReplay(url)
                print('下载{0}的文件'.format(url))
                if filePath == '':
                    flag = True
                    break
                print('开始解析{0}'.format(filePath))
                replay = Wotreplay(filePath, True)
                players = client['wotreplay-collecter']['players']
                print('插入玩家数据到数据库')
                players.insert_many(replay.playerList)
            if flag:
                break

if __name__ == '__main__':
    main()