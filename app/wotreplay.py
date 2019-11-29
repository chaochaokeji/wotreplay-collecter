# wotreplay类

import os
import re
import json

class Wotreplay:
    
    def __init__(self, path, delFile = False):
        # 打开wotreplay文件
        f = open(path, mode = 'r', encoding = 'utf-8', errors = 'ignore')
        
        # 读取文件内容
        rTxt = f.read()

        # 截取文件内容转为字典
        searchObj = re.search(r'{".*"playerName".*"}', rTxt)
        if searchObj:
            self.__rDict = json.loads(searchObj.group())

        # 截取文件内容转为列表
        searchObj = re.search(r'\[{"arenaUniqueID".*"frags".*}}\]', rTxt)
        if searchObj:
            self.__rList = json.loads(searchObj.group())

        # 关闭文件
        f.close()
        
        # 删除文件
        if delFile:
            os.remove(path)

    # 玩家昵称
    @property
    def playerName(self):
        return self.__rDict['playerName']

    # 玩家使用车辆
    @property
    def playerVehicle(self):
        return self.__rDict['playerVehicle']

    # 服务器
    @property
    def serverName(self):
        return self.__rDict['serverName']
    
    # 地区代码
    @property
    def regionCode(self):
        return self.__rDict['regionCode']

    # 游戏时间
    @property
    def dateTime(self):
        return self.__rDict['dateTime']

    # 玩家列表
    @property
    def playerList(self):
        list = []
        vehicles = self.__rDict['vehicles']
        for id in vehicles:
            list.append({
                'id': id,
                'name': vehicles[id]['name'],
                'clan': vehicles[id]['clanAbbrev'],
                'serverName': self.__rDict['serverName'],
                'vehicle': vehicles[id]['vehicleType'].replace(':', '-'),
                'dateTime': self.__rDict['dateTime']
            })
        return list