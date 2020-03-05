# -*- coding: utf-8 -*-

import re
import json

from indexModel import indexModel

class parseManager:

    def __init__(self):
        super().__init__()
    
    def parseIndexInfos(self, area, text):
        # 可选区域
        areaGroup = ['china', 'asian', 'euro', 'america']
        if area == '' or area.lower() not in ['china', 'asian', 'euro', 'america']:
            return {}
        else:
            if area.lower() == 'china':
                # 请求中国数据
                data = self.parseChinaIndexs(text)
                jsonData = json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)
                return jsonData
    
    # 清洗&重组中国数据
    def parseChinaIndexs(self, jsonData):
        return purgeEastmoney100Data(jsonData,u'中国')

    # 清洗东方财富亚洲数据（100.eastmoney）
    def purgeEastmoney100Data(self, jsonData, indexArea):
        datalist = jsonData['data']['diff']
        print(datalist)
        result = []
        for key in datalist.keys():
            item = datalist[key]
            index = indexModel()
            index.indexCode = item['f12']
            index.indexName = item['f14'].replace(' ','')
            index.indexArea = indexArea
            index.sequence = int(key)
            index.current = round(float(item['f2'])/100, 2)
            index.lastClose = round(float(item['f18'])/100, 2)
            index.dailyChangRate = '{0:.2f}%'.format(
                round(float(item['f3'])/100, 2))
            index.dailyChangValue = round(float(item['f4'])/100, 2)
            index.dealMoney = round(float(item['f6']), 2)
            result.append(index.__dict__)
        return result