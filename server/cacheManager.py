# -*- coding: utf-8 -*-

import os
import sys

import json

from datetimeManager import datetimeManager

class cacheManager:

    def __init__(self):
        super().__init__()
        self.dm = datetimeManager()
        self.cachConfig = [
            # 资金数据，缓存 30 秒
            {'path' : '/api/moneyinfo', 'cache_duration' : 30},
            # 涨跌平数据，缓存 30 秒
            {'path' : '/api/zdpinfo', 'cache_duration' : 30},
            # 指数数据，缓存 10 秒
            {'path' : '/api/indexs/china', 'cache_duration' : 10},
            {'path' : '/api/indexs/asian', 'cache_duration' : 10},
            {'path' : '/api/indexs/euro', 'cache_duration' : 10},
            {'path' : '/api/indexs/america', 'cache_duration' : 10},
            # 期货及外汇，缓存 10 秒
            {'path' : '/api/goods_and_exchanges', 'cache_duration' : 10},
            # 债券及投资组合，缓存 60 秒
            {'path' : '/api/bondinfo', 'cache_duration' : 60},
            # 是否工作日，缓存 60 秒
            {'path' : '/api/today', 'cache_duration' : 60}
        ]
        self.cache_folder = os.path.join(os.getcwd(),'cache')
        if not os.path.exists(self.cache_folder):
            os.makedirs(self.cache_folder)

    # 缓存文件路径
    def filepathOfUrl(self, url_path):
        return os.path.join(self.cache_folder, url_path.replace('/','.')[1:len(url_path)] + '.json')

    # 获取 path 对应的有效时长（如 10s，60s）
    def getCacheDurationOfPath(self,url_path):
        for item in self.cachConfig:
            if item['path'] == url_path:
                return float(item['cache_duration'])
        return 0

    # 判断缓存是否可用（有文件，且 aliyun_date 与当前时间的间隔在缓存有效期之内
    def cacheAvailable(self, start_ts, url_path):
        paths = [x['path'] for x in self.cachConfig]
        if url_path not in paths:
            return False
        elif os.path.exists(self.filepathOfUrl(url_path)):
            with open(self.filepathOfUrl(url_path), 'r', encoding='utf-8') as f:
                data = json.loads(f.read())
                ts = float(self.dm.getTimeStampFromString(data['aliyun_date']))
                duration = self.dm.getDuration(ts, start_ts)
                if duration < self.getCacheDurationOfPath(url_path):
                    return True
                else:
                    return False
        else:
            return False

    # 获取缓存（修改 duration 和 isCache）
    def getCache(self, start_ts, url_path):
        if self.cacheAvailable(start_ts, url_path):
            with open(self.filepathOfUrl(url_path), 'r', encoding='utf-8') as f:
                data = json.loads(f.read())
                data['isCache'] = True
                end_ts = self.dm.getTimeStamp()
                duration = self.dm.getDuration(start_ts, end_ts)
                data['duration'] = duration
                return json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True)
        else:
            return json.dumps({})
    
    # 写入本地缓存文件
    def saveCache(self, url_path, data):
        with open(self.filepathOfUrl(url_path), 'w+', encoding='utf-8') as f:
            f.write(data)
