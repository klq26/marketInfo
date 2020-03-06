# -*- coding: utf-8 -*-

import grequests
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import ssl

from configManager import configManager
from indexModel import indexModel
from datetimeManager import datetimeManager

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
    # 请求指数数据 china asian euro america
    # ////////////////////////////////////////////////////////////////////////////////////////

    def getIndexInfos(self, area):
        # 可选区域
        areaGroup = ['china', 'asian', 'euro', 'america']
        if area == '' or area.lower() not in areaGroup:
            return {}
        else:
            responseText = ''
            if area.lower() == 'china':
                # 请求中国数据
                responseText = self.requestChinaIndexs()
            elif area.lower() == 'asian':
                # 请求亚洲数据
                responseText = self.requestAsianIndexs()
            elif area.lower() == 'euro':
                # 请求欧洲数据
                responseText = self.requestEuroIndexs()
            elif area.lower() == 'america':
                # 请求美洲数据
                responseText = self.requestAmericaIndexs()
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
    def requestAsianIndexs(self):
        # 根据 2019.12 最新 GDP 排名降序请求
        # http://www.southmoney.com/paihangbang/201912/4612448.html
        url = "http://87.push2.eastmoney.com/api/qt/ulist.np/get?cb=updateIndexInfos&np=1&pi=0&pz=40&po=1&secids=100.N225%2C100.SENSEX%2C100.KS11%2C100.JKSE%2C100.TWII%2C100.SET%2C100.KLSE%2C100.STI%2C100.PSI%2C100.VNINDEX&fields=f14,f12,f2,f4,f3,f18,f6"
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            # print(response.text)
            result = response.text.replace('updateIndexInfos(','').replace(');','')
            return result
        else:
            return ''

    # 请求欧洲
    def requestEuroIndexs(self):
        # 根据 2019.12 最新 GDP 排名降序请求
        # http://www.southmoney.com/paihangbang/201912/4612514.html
        url = "http://87.push2.eastmoney.com/api/qt/ulist.np/get?cb=updateIndexInfos&np=1&pi=0&pz=40&po=1&secids=100.GDAXI%2C100.FTSE%2C100.FCHI%2C100.MIB%2C100.RTS%2C100.IBEX%2C100.AEX%2C100.SSMI%2C100.WIG%2C100.OMXSPI&fields=f14,f12,f2,f4,f3,f18,f6"
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            # print(response.text)
            result = response.text.replace('updateIndexInfos(','').replace(');','')
            return result
        else:
            return ''

    # 请求美洲
    def requestAmericaIndexs(self):
        url = "http://87.push2.eastmoney.com/api/qt/ulist.np/get?cb=updateIndexInfos&np=1&pi=0&pz=40&po=1&secids=100.DJIA%2C100.NDX%2C100.SPX%2C107.XOP%2C100.TSX%2C100.MXX%2C100.BVSP&fields=f14,f12,f2,f4,f3,f18,f6"
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            # print(response.text)
            result = response.text.replace('updateIndexInfos(','').replace(');','')
            return result
        else:
            return ''
    
    
