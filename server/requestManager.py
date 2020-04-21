# -*- coding: utf-8 -*-

import grequests
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import ssl

from configManager import configManager
from indexModel import indexModel
from datetimeManager import datetimeManager

from databaseManager import databaseManager

class requestsManager:

    def __init__(self):
        super().__init__()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
        self.cm = configManager()
    
    # ////////////////////////////////////////////////////////////////////////////////////////
    # 请求资金数据（两市成交额，融资融券，两市资金净流入，沪港通，沪深通净流入，板块资金）
    # ////////////////////////////////////////////////////////////////////////////////////////

    def getMoneyInfo(self):
        urls = []
        responseTexts = []
        [urls.append(item['url']) for item in self.cm.moneyinfo]
        # 并发
        request_list = [grequests.get(url,headers=self.headers) for url in urls]
        response_list = grequests.map(request_list)
        for response in response_list:
            if response.status_code == 200:
                responseTexts.append(response.text)
            else:
                responseTexts.append('{}')
        return responseTexts

    # ////////////////////////////////////////////////////////////////////////////////////////
    # 请求 A 股涨跌平数据
    # ////////////////////////////////////////////////////////////////////////////////////////

    def getZDPInfo(self):
        urls = []
        responseTexts = []
        [urls.append(item['url']) for item in self.cm.zdpinfo]
        # 并发
        request_list = [grequests.get(url,headers=self.headers) for url in urls]
        response_list = grequests.map(request_list)
        for response in response_list:
            if response.status_code == 200:
                responseTexts.append(response.text)
            else:
                responseTexts.append('{}')
        return responseTexts

    # ////////////////////////////////////////////////////////////////////////////////////////
    # 请求指数数据 china asian euro america australia
    # ////////////////////////////////////////////////////////////////////////////////////////

    def getIndexInfos(self, area, codes):
        # 可选区域
        areaGroup = ['china', 'asian', 'euro', 'america','australia']
        if area == '' or area.lower() not in areaGroup:
            return {}
        else:
            responseText = ''
            if area.lower() == 'china':
                # 请求中国数据
                responseText = self.requestChinaIndexs()
            elif area.lower() == 'asian':
                # 请求亚洲数据
                responseText = self.requestAsianIndexs(codes)
            elif area.lower() == 'euro':
                # 请求欧洲数据
                responseText = self.requestEuroIndexs(codes)
            elif area.lower() == 'america':
                # 请求美洲数据
                responseText = self.requestAmericaIndexs(codes)
            elif area.lower() == 'australia':
                # 请求澳洲数据
                responseText = self.requestAustraliaIndexs()
            return responseText
    
    # 请求中国
    def requestChinaIndexs(self):
        url = "http://10.push2.eastmoney.com/api/qt/clist/get?cb=updateIndexInfos&pn=1&pz=30&fs=i:1.000832,i:1.000001,i:0.399001,i:0.399006,i:1.000015,i:1.000922,i:1.000016,i:1.000300,i:0.399905,i:1.000852,i:1.000842,i:0.399005,i:1.000991,i:1.000992,i:0.399975,i:0.399986,i:0.399812,i:0.399971,i:1.000827,i:100.HSI,i:100.HSCEI,i:124.HSCCI&fields=f14,f12,f2,f4,f3,f18,f6"
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            # print(response.text)
            result = response.text.replace('updateIndexInfos(', '').replace(');', '')
            return result
        else:
            return ''
    
    # 请求亚洲
    def requestAsianIndexs(self, codes):
        # 根据 2019.12 最新 GDP 排名降序请求
        # http://www.southmoney.com/paihangbang/201912/4612448.html
        url = "http://87.push2.eastmoney.com/api/qt/ulist.np/get?cb=updateIndexInfos&np=1&pi=0&pz=40&po=1&secids={0}&fields=f14,f12,f2,f4,f3,f18,f6".format('%2C'.join(codes))
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            # print(response.text)
            result = response.text.replace('updateIndexInfos(','').replace(');','')
            return result
        else:
            return ''

    # 请求欧洲
    def requestEuroIndexs(self, codes):
        # 根据 2019.12 最新 GDP 排名降序请求
        # http://www.southmoney.com/paihangbang/201912/4612514.html
        url = "http://87.push2.eastmoney.com/api/qt/ulist.np/get?cb=updateIndexInfos&np=1&pi=0&pz=40&po=1&secids={0}&fields=f14,f12,f2,f4,f3,f18,f6".format('%2C'.join(codes))
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            # print(response.text)
            result = response.text.replace('updateIndexInfos(','').replace(');','')
            return result
        else:
            return ''

    # 请求美洲
    def requestAmericaIndexs(self, codes):
        url = "http://87.push2.eastmoney.com/api/qt/ulist.np/get?cb=updateIndexInfos&np=1&pi=0&pz=40&po=1&secids={0}&fields=f14,f12,f2,f4,f3,f18,f6".format('%2C'.join(codes))
        print('美国',url)
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            # print(response.text)
            result = response.text.replace('updateIndexInfos(','').replace(');','')
            return result
        else:
            return ''
    
    # 请求澳洲
    def requestAustraliaIndexs(self):
        url = "http://87.push2.eastmoney.com/api/qt/ulist.np/get?cb=updateIndexInfos&np=1&pi=0&pz=40&po=1&secids=100.AORD%2C100.NZ50&fields=f14,f12,f2,f4,f3,f18,f6"
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            # print(response.text)
            result = response.text.replace('updateIndexInfos(','').replace(');','')
            return result
        else:
            return ''

    # ////////////////////////////////////////////////////////////////////////////////////////
    # 请求期货&外汇数据
    # ////////////////////////////////////////////////////////////////////////////////////////
    
    def getGoodsAndExchangeInfo(self):
        urls = []
        responseTexts = []
        [urls.append(item['url']) for item in self.cm.goods_and_exchanges]
        # 并发
        request_list = [grequests.get(url,headers=self.headers) for url in urls]
        response_list = grequests.map(request_list)
        for response in response_list:
            if response.status_code == 200:
                responseTexts.append(response.text)
            else:
                responseTexts.append('{}')
        return responseTexts

    # ////////////////////////////////////////////////////////////////////////////////////////
    # 请求债券数据
    # ////////////////////////////////////////////////////////////////////////////////////////

    def getBondInfo(self):
        urls = []
        responseTexts = []
        [urls.append(item['url']) for item in self.cm.bondinfo]
        # 并发
        request_list = [grequests.get(url,headers=self.headers) for url in urls]
        response_list = grequests.map(request_list)
        for response in response_list:
            if response.status_code == 200:
                responseTexts.append(response.text)
            else:
                responseTexts.append('{}')
        return responseTexts
    
    # ////////////////////////////////////////////////////////////////////////////////////////
    # 请求指数排序数据 china asian euro america australia
    # ////////////////////////////////////////////////////////////////////////////////////////
    def getIndexSortInfos(self, area, type):
        # 可选区域
        areaGroup = ['asian', 'euro', 'america']
        if area == '' or area.lower() not in areaGroup:
            return {}
        else:
            continent = ''
            if area.lower() == 'asian':
                continent = u'亚洲'
            if area.lower() == 'euro':
                continent = u'欧洲'
            if area.lower() == 'america':
                continent = u'美洲'
            response = {}
            if type.lower() == u'gdp' or type == '1':
                response = {'name': '产值', 'value': databaseManager().sequenceByGDP(continent=continent)}
            if type.lower() == u'dealtime' or type == '2':
                response = {'name': '时区', 'value': databaseManager().sequenceByDealTime(continent=continent)}
            if type.lower() == u'avg_gdp' or type == '3':
                response = {'name': '人均', 'value': databaseManager().sequenceByAverageGDP(continent=continent)}
            if type.lower() == u'population' or type == '4':
                response = {'name': '人口', 'value': databaseManager().sequenceByPopulation(continent=continent)}
            if type.lower() == u'area' or type == '5':
                response = {'name': '国土', 'value': databaseManager().sequenceByArea(continent=continent)}
            
            return response

    # ////////////////////////////////////////////////////////////////////////////////////////
    # 请求今日类型（开盘日：0 周末：1 节假日：2
    # ////////////////////////////////////////////////////////////////////////////////////////

    def getDayType(self):
        dm = datetimeManager()
        today = dm.getDateString()
        if dm.isHoliday():
            return {today: '2'}
        elif dm.isWeekday():
            return {today: '0'}
        else:
            return {today: '1'}
        # 第三方接口老挂，不搞了
        # url = "http://www.easybots.cn/api/holiday.php?d=" + today
        # response = requests.get(url, headers=self.headers, verify=False)
        # if response.status_code == 200:
        #     return response.text

    

    # ////////////////////////////////////////////////////////////////////////////////////////
    # 请求国家信息
    # ////////////////////////////////////////////////////////////////////////////////////////
    def getCountryinfo(self, indexName):
        result = []
        db = databaseManager()
        # 先尝试按国家名称找
        result = db.getSingleCountryInfo('country', indexName)
        if len(result) == 0:
            # 国家名称没有，说明是一个国家对应多个指数（如中美），此时应该进行 index_code 查询
            result = databaseManager().getSingleCountryInfo('index_name', indexName)
        return result

    # ////////////////////////////////////////////////////////////////////////////////////////
    # 请求指数历史数据
    # ////////////////////////////////////////////////////////////////////////////////////////
    def getIndexHistory(self, indexName):
        result = []
        db = databaseManager()
        # 先尝试按国家名称找
        result = db.getSingleIndexHistory('country', indexName)
        if len(result) == 0:
            # 国家名称没有，说明是一个国家对应多个指数（如中美），此时应该进行 index_code 查询
            result = databaseManager().getSingleIndexHistory('index_name', indexName)
        return result