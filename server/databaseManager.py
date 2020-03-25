# -*- coding: utf-8 -*-
import sys

import pymysql

from indexHistoryModel import indexHistoryModel
from countryInfoModel import countryInfoModel

class databaseManager:

    def __init__(self):
        super().__init__()
        # 打开数据库
        self.ip_address = ''
        if sys.platform.startswith('win'):
            self.ip_address = '112.125.25.230'
        elif sys.platform.startswith('linux'):
            self.ip_address = '127.0.0.1'
        # 数据库与 model 模型的 key 匹配
        country_info_db_keys = ['id','country','country_code','capital','trading_market','market_code','index_name','index_code','continent','timezone','deal_time','break_time','population','area','gdp_rmb','gdp_person_avg','inland_currency','currency_code','summer_time']
        country_info_model_keys = ['id','country','countryCode','capital','tradingMarket','marketCode','indexName','indexCode','continent','timezone','dealTime','breakTime','population','area','gdpRMB','gdpPersonAvg','inlandCurrency','inlandCurrencyCode','summerTime']
        self.country_info_keymapping = dict(zip(country_info_db_keys, country_info_model_keys))

        index_history_db_keys = ['id','country','country_code','continent','index_name','index_code','index_history']
        index_history_model_keys = ['id','country','countryCode','continent','indexName','indexCode','indexHistory']
        self.index_history_keymapping = dict(zip(index_history_db_keys, index_history_model_keys))

    # 按大洲查询指数历史数据
    def getIndexHistorysByContinent(self, continent=u'中国', orderby='id'):
        db = pymysql.connect(self.ip_address,'klq26','abc123!@#==','finance')
        cursor = db.cursor()
        # 数据库字段名
        db_keys = ['id','country','country_code','continent','index_name','index_code','index_history']
        # 模型字段名
        model_keys = ['id','country','countryCode','continent','indexName','indexCode','indexHistory']
        sql = "SELECT {0} FROM index_history WHERE continent = '{1}'".format(','.join(db_keys), continent)
        # print(sql)
        cursor.execute(sql)
        db.commit()
        datalist = list(cursor.fetchall())
        result = []
        for item in datalist:
            result.append(dict(zip(model_keys, list(item))))
        cursor.close()
        db.close()
        return result
    
    def getCountryByIndexCode(self, continent='美洲', code='N225'):
        historyList = self.getIndexHistorysByContinent(continent)
        for item in historyList:
            if item['indexCode'] == code:
                return {'country': item['country'], 'countryCode': item['countryCode'], 'indexCode':code}
        return {'country': 'NA', 'countryCode': 'NA', 'indexCode':code}

    # 按大洲查询国家数据（默认 GDP 降序排列）
    def getCountryInfosByContinent(self, continent=u'中国', orderby='gdp_rmb', desc='DESC'):
        db = pymysql.connect(self.ip_address,'klq26','abc123!@#==','finance')
        cursor = db.cursor()
        # 数据库字段名
        db_keys = self.country_info_keymapping.keys()
        # 模型字段名
        model_keys = self.country_info_keymapping.values()
        sql = "SELECT {0} FROM country_info WHERE continent = '{1}' ORDER BY {2} {3}".format(','.join(db_keys), continent, orderby, desc)
        # print(sql)
        cursor.execute(sql)
        db.commit()
        datalist = list(cursor.fetchall())
        result = []
        for item in datalist:
            result.append(dict(zip(model_keys, list(item))))
        cursor.close()
        db.close()
        return result

    ####################
    # 按国情指标降序排序 #
    ####################
    
    def sequenceByDealTime(self, continent=u'美洲'):
        key = 'deal_time'
        countrylist = self.getCountryInfosByContinent(continent, key, desc="ASC")
        return self.assignSequence(countrylist, self.country_info_keymapping[key])

    def sequenceByGDP(self, continent=u'美洲'):
        key = 'gdp_rmb'
        countrylist = self.getCountryInfosByContinent(continent, key)
        return self.assignSequence(countrylist, self.country_info_keymapping[key])

    def sequenceByAverageGDP(self, continent=u'美洲'):
        key = 'gdp_person_avg'
        countrylist = self.getCountryInfosByContinent(continent, key)
        return self.assignSequence(countrylist, self.country_info_keymapping[key])

    def sequenceByPopulation(self, continent=u'美洲'):
        key = 'population'
        countrylist = self.getCountryInfosByContinent(continent, key)
        return self.assignSequence(countrylist, self.country_info_keymapping[key])

    def sequenceByArea(self, continent=u'美洲'):
        key = 'area'
        countrylist = self.getCountryInfosByContinent(continent, key)
        return self.assignSequence(countrylist, self.country_info_keymapping[key])

    # 根据数据库返回结果，统一生成 sequence 数组供客户端排序（同时附上排序字段供客户端 debug）
    def assignSequence(self, countrylist, sortKey='id'):
        # print(sortKey)
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

    # 根据字段获取单个国家
    def getSingleCountryInfo(self, db_key, value):
        db = pymysql.connect(self.ip_address,'klq26','abc123!@#==','finance')
        cursor = db.cursor()
        # 数据库字段名
        db_keys = self.country_info_keymapping.keys()
        # 模型字段名
        model_keys = self.country_info_keymapping.values()
        sql = "SELECT {0} FROM country_info WHERE {1} LIKE '%{2}%'".format(','.join(db_keys), db_key, value)
        # print(sql)
        cursor.execute(sql)
        db.commit()
        datalist = list(cursor.fetchall())
        result = []
        for item in datalist:
            result.append(dict(zip(model_keys, list(item))))
        cursor.close()
        db.close()
        return result

    # 根据字段获取单个国家
    def getSingleIndexHistory(self, db_key, value):
        db = pymysql.connect(self.ip_address,'klq26','abc123!@#==','finance')
        cursor = db.cursor()
        # 数据库字段名
        db_keys = self.index_history_keymapping.keys()
        # 模型字段名
        model_keys = self.index_history_keymapping.values()
        sql = "SELECT {0} FROM index_history WHERE {1} LIKE '%{2}%'".format(','.join(db_keys), db_key, value)
        # print(sql)
        cursor.execute(sql)
        db.commit()
        datalist = list(cursor.fetchall())
        result = []
        for item in datalist:
            result.append(dict(zip(model_keys, list(item))))
        cursor.close()
        db.close()
        return result

if __name__ == "__main__":
    db = databaseManager()
    # 测试历史年 K
    # result = db.getIndexHistorysByContinent('澳洲')
    # for item in result:
    #     indexHistory = indexHistoryModel()
    #     indexHistory.__dict__ = item
    #     print(indexHistory)
    
    # 测试根据指数 symbol 获取指数国家的功能
    # print(db.getCountryByIndexCode(code='PSI'))

    # 测试国家数据
    db.sequenceByGDP()
    db.sequenceByAverageGDP()
    db.sequenceByDealTime()
    db.sequenceByPopulation()
    db.sequenceByArea()

    pass
