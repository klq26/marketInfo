# -*- coding: utf-8 -*-

import re
import json

from datetimeManager import datetimeManager
from indexModel import indexModel

class parseManager:

    def __init__(self):
        super().__init__()
    
    def parseIndexInfos(self, start_ts, area, text):
        # 可选区域
        areaGroup = ['china', 'asian', 'euro', 'america']
        if area == '' or area.lower() not in areaGroup:
            return {}
        else:
            parsedData = {}
            dm = datetimeManager()
            if area.lower() == 'china':
                # 解析中国数据
                parsedData = self.parseChinaIndexs(text)
            end_ts = dm.getTimeStamp()
            duration = dm.getDurationString(start_ts, end_ts)
            data = self.packDataWithCommonInfo(duration = duration, data = parsedData)
            return data
    
    # 清洗&重组中国数据
    def parseChinaIndexs(self, text):
        return self.parseEastmoney100Data(u'中国', json.loads(text))

    # 清洗东方财富亚洲数据（100.eastmoney）
    def parseEastmoney100Data(self, indexArea, jsonData):
        datalist = jsonData['data']['diff']
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
    
    # 添加公共返回值
    def packDataWithCommonInfo(self, isCache = False, isSuccess = True, msg = "success", duration = '0', data = {}):
        code = 0
        if not isSuccess:
            code = -1
        result = {'code' : code, 'msg' : msg, 'isCache' : False, 'aliyun_date' : datetimeManager().getDateTimeString(), 'data' : data, 'duration' : duration}
        return json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)