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
        country_info_db_keys = ['id','country','country_code','capital','continent','timezone','deal_time','break_time','population','area','gdp_rmb','gdp_person_avg','inland_currency','currency_code','summer_time']
        country_info_model_keys = ['id','country','countryCode','capital','continent','timezone','dealTime','breakTime','population','area','gdpRMB','gdpPersonAvg','inlandCurrency','inlandCurrencyCode','summerTime']
        self.country_info_keymapping = dict(zip(country_info_db_keys, country_info_model_keys))

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
    
    def getCountryByIndexCode(self, continent='亚洲', code='N225'):
        historyList = self.getIndexHistorysByContinent(continent)
        for item in historyList:
            if item['indexCode'] == code:
                return {'country': item['country'], 'countryCode': item['countryCode'], 'indexCode':code}
        return {'country': 'NA', 'countryCode': 'NA', 'indexCode':code}

    # 按大洲查询国家数据（默认 GDP 降序排列）
    def getCountryInfosByContinent(self, continent=u'中国', orderby='gdp_rmb'):
        db = pymysql.connect(self.ip_address,'klq26','abc123!@#==','finance')
        cursor = db.cursor()
        # 数据库字段名
        db_keys = self.country_info_keymapping.keys()
        # 模型字段名
        model_keys = self.country_info_keymapping.values()
        sql = "SELECT {0} FROM country_info WHERE continent = '{1}' ORDER BY {2} DESC".format(','.join(db_keys), continent, orderby)
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
    
    def sequenceByDealTime(self, continent=u'亚洲'):
        key = 'deal_time'
        countrylist = db.getCountryInfosByContinent(continent, key)
        countrylist = reversed(countrylist)
        self.assignSequence(countrylist, self.country_info_keymapping[key])

    def sequenceByGDP(self, continent=u'亚洲'):
        key = 'gdp_rmb'
        countrylist = db.getCountryInfosByContinent(continent, key)
        self.assignSequence(countrylist, self.country_info_keymapping[key])

    def sequenceByAverageGDP(self, continent=u'亚洲'):
        key = 'gdp_person_avg'
        countrylist = db.getCountryInfosByContinent(continent, key)
        self.assignSequence(countrylist, self.country_info_keymapping[key])

    def sequenceByPopulation(self, continent=u'亚洲'):
        key = 'population'
        countrylist = db.getCountryInfosByContinent(continent, key)
        self.assignSequence(countrylist, self.country_info_keymapping[key])

    def sequenceByArea(self, continent=u'亚洲'):
        key = 'area'
        countrylist = db.getCountryInfosByContinent(continent, key)
        self.assignSequence(countrylist, self.country_info_keymapping[key])

    # 根据数据库返回结果，统一生成 sequence 数组供客户端排序（同时附上排序字段供客户端 debug）
    def assignSequence(self, countrylist, sortKey='id'):
        result = []
        index = 1
        for item in countrylist:
            countryInfo = countryInfoModel()
            countryInfo.__dict__ = item
            result.append({'country' : countryInfo.country, 'countryCode': countryInfo.countryCode,'{0}'.format(sortKey): countryInfo[sortKey], 'sequence': index})
            index += 1
        [print(x) for x in result]
        print()
        pass

if __name__ == "__main__":
    db = databaseManager()
    # 测试历史年 K
    result = db.getIndexHistorysByContinent('澳洲')
    for item in result:
        indexHistory = indexHistoryModel()
        indexHistory.__dict__ = item
        print(indexHistory)
    
    # 测试根据指数 symbol 获取指数国家的功能
    print(db.getCountryByIndexCode(code='PSI'))

    # 测试国家数据
    db.sequenceByGDP()
    db.sequenceByAverageGDP()
    db.sequenceByDealTime()
    db.sequenceByPopulation()
    db.sequenceByArea()

    pass
