# -*- coding: utf-8 -*-

# import grequests
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
    
    def getIndexInfos(self, area):
        # 可选区域
        areaGroup = ['china', 'asian', 'euro', 'america']
        if area == '' or area.lower() not in areaGroup:
            return {}
        else:
            if area.lower() == 'china':
                # 请求中国数据
                responseText = self.requestChinaIndexs()
                return responseText
    
    # 请求中国
    def requestChinaIndexs(self):
        url = "http://10.push2.eastmoney.com/api/qt/clist/get?cb=updateIndexInfos&pn=1&pz=30&fs=i:1.000832,i:1.000001,i:0.399001,i:0.399006,i:1.000015,i:1.000922,i:1.000016,i:1.000300,i:0.399905,i:1.000852,i:1.000842,i:0.399005,i:1.000991,i:1.000992,i:0.399975,i:0.399986,i:0.399812,i:0.399971,i:1.000827,i:100.HSI,i:100.HSCEI,i:124.HSCCI&fields=f14,f12,f2,f4,f3,f18,f6"
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url, headers=self.headers, verify=False)
        if response.status_code == 200:
            # print(response.text)
            result = response.text.replace(
                'updateIndexInfos(', '').replace(');', '')
            return result
        else:
            return ''