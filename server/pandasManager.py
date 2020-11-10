# -*- coding: utf-8 -*-
import sys
import os
import json

import pandas as pd
import numpy as np

from indexHistoryModel import indexHistoryModel
from countryInfoModel import countryInfoModel

"""
用于替代 databaseManager。之后有关国家信息和指数历史年 K 数据，不再走云端 mysql 软件
只维护本地 csv 或 xlsx 数据即可。
"""
class pandasManager:

    def __init__(self):
        super().__init__()
        self.folder = os.path.abspath(os.path.dirname(__file__))
        # 加载数据
        self.df_country_info = pd.read_csv(os.path.join(self.folder, 'data', 'country_info', 'country_info.csv'), sep='\t')
        self.df_index_history = pd.read_csv(os.path.join(self.folder, 'data', 'index_history', 'index_history.csv'), sep='\t')
        pass

    # 按大洲查询指数历史数据
    def getIndexHistorysByContinent(self, continent=u'中国', orderby='id'):
        df = self.df_index_history
        # 有下划线的字段列，都不是前端需要的
        keys = [x for x in df.columns if '_' not in x]
        df_continent = df[df['continent'] == continent]
        df_continent = df_continent[keys]
        return json.loads(df_continent.to_json(orient='records', force_ascii=False, indent=4))

    def getCountryByIndexCode(self, code='N225'):
        df = self.df_index_history
        df = df[df['indexCode'] == code]
        if len(df) > 0:
            return {'country': df.country.values[0], 'countryCode': df.countryCode.values[0], 'indexCode':code}
        else:
            return {'country': 'NA', 'countryCode': 'NA', 'indexCode':code}

    # 按大洲查询国家数据（默认 GDP 降序排列）
    def getCountryInfosByContinent(self, continent=u'中国', orderby='gdpRMB', ascending=True):
        df = self.df_country_info
        # 有下划线的字段列，都不是前端需要的
        keys = [x for x in df.columns if '_' not in x]
        df_continent = df[df['continent'] == continent]
        df_continent.sort_values(by=orderby, ascending=ascending, inplace=True)
        df_continent = df_continent[keys]
        return json.loads(df_continent.to_json(orient='records', force_ascii=False, indent=4))

    ####################
    # 按国情指标降序排序 #
    ####################
    
    def sequenceByDealTime(self, continent=u'美洲'):
        key = 'dealTime'
        countrylist = self.getCountryInfosByContinent(continent=continent, orderby=key, ascending=False)
        return self.assignSequence(countrylist)

    def sequenceByGDP(self, continent=u'美洲'):
        key = 'gdpRMB'
        countrylist = self.getCountryInfosByContinent(continent=continent, orderby=key, ascending=False)
        return self.assignSequence(countrylist)
    
    def sequenceByAverageGDP(self, continent=u'美洲'):
        key = 'gdpPersonAvg'
        countrylist = self.getCountryInfosByContinent(continent=continent, orderby=key, ascending=False)
        return self.assignSequence(countrylist)
    
    def sequenceByPopulation(self, continent=u'美洲'):
        key = 'population'
        countrylist = self.getCountryInfosByContinent(continent=continent, orderby=key, ascending=False)
        return self.assignSequence(countrylist)
    
    def sequenceByArea(self, continent=u'美洲'):
        key = 'area'
        countrylist = self.getCountryInfosByContinent(continent=continent, orderby=key, ascending=False)
        return self.assignSequence(countrylist)
    
    # 根据数据库返回结果，统一生成 sequence 数组供客户端排序（同时附上排序字段供客户端 debug）
    def assignSequence(self, countrylist):
        db_countrys = [x['country'] for x in countrylist]
        db_names = [x['indexName'] for x in countrylist]
        db_codes = [x['indexCode'] for x in countrylist]

        names = []
        codes = []
        # 指数换国家
        for i in range(0,len(db_countrys)):
            country = db_countrys[i]
            code = db_codes[i]
            name = db_names[i]
            # 当该国只有一只观察指数时
            if '-' not in name:
                names.append(country)
                codes.append(code.replace('i:',''))
            else:
                indexNames = name.split('-')
                indexCodes = code.split('-')
                [names.append(x) for x in indexNames]
                [codes.append(x.replace('i:','')) for x in indexCodes]
        # print(names)
        # print(codes)
        return (names, codes)
    
    # 根据字段获取单个国家（同一国家，多个指数的情况下，会需要二次查询）
    def getSingleCountryInfo(self, key, value):
        df = self.df_country_info
        # 有下划线的字段列，都不是前端需要的
        keys = [x for x in df.columns if '_' not in x]
        if key == 'index_name':
            # 兼容 requestManager 旧代码
            key = 'indexName'
        df_continent = df[df[key].str.contains(value)]
        df_continent = df_continent[keys]
        return json.loads(df_continent.to_json(orient='records', force_ascii=False, indent=4))
    
    # 根据字段获取单个国家（同一国家，多个指数的情况下，会需要二次查询）
    def getSingleIndexHistory(self, key, value):
        df = self.df_index_history
        # 有下划线的字段列，都不是前端需要的
        keys = [x for x in df.columns if '_' not in x]
        if key == 'index_name':
            # 兼容 requestManager 旧代码
            key = 'indexName'
        df_continent = df[df[key].str.contains(value)]
        df_continent = df_continent[keys]
        return json.loads(df_continent.to_json(orient='records', force_ascii=False, indent=4))

if __name__ == "__main__":
    db = pandasManager()
    # 测试历史年 K
    # result = db.getIndexHistorysByContinent('美洲')
    # for item in result:
    #     indexHistory = indexHistoryModel()
    #     indexHistory.__dict__ = item
    #     print(indexHistory)
    
    # 测试根据指数 symbol 获取指数国家的功能
    # print(db.getCountryByIndexCode(code='N225'))
    
    # 测试国家数据
    # print(db.sequenceByGDP(continent='美洲'))
    # print(db.sequenceByAverageGDP(continent='中国'))
    # print(db.sequenceByDealTime(continent='美洲'))
    # print(db.sequenceByPopulation(continent='欧洲'))
    # print(db.sequenceByArea(continent='亚洲'))

    # 测试单个指数的数据
    # print(db.getSingleIndexHistory('country', '日本'))
    # print(db.getSingleIndexHistory('index_name', '标普500'))
    # print()
    # print(db.getSingleCountryInfo('country', '日本'))
    # print(db.getSingleCountryInfo('index_name', '标普500'))