# -*- coding: utf-8 -*-

import re
import json

from configManager import configManager
from datetimeManager import datetimeManager
from indexModel import indexModel

class parseManager:

    def __init__(self):
        super().__init__()
        self.cm = configManager()
        self.dm = datetimeManager()
    
    # ////////////////////////////////////////////////////////////////////////////////////////
    # 解析资金数据（两市成交额，融资融券，两市资金净流入，沪港通，沪深通净流入，板块资金）
    # ////////////////////////////////////////////////////////////////////////////////////////

    def parseMoneyInfo(self, start_ts, texts):
        symbols = []
        names = []
        parsedData = []
        [symbols.append(item['symbol']) for item in self.cm.moneyinfo]
        [names.append(item['name']) for item in self.cm.moneyinfo]
        for i in range(0,len(texts)):
            name = names[i]
            symbol = symbols[i]
            text = texts[i]
            if hasattr(parseManager, 'parse_' + symbol):
                # 反射机制调用对应解析函数
                func = getattr(parseManager, 'parse_' + symbol)
                data = func(self, name, symbol, text)
                if type(data) == type(list()):
                    [parsedData.append(x) for x in data]
                else:
                    parsedData.append(data)
            else:
                parsedData.append({'name' : name, 'symbol' : symbol, 'value' : []})
        # print(parsedData)
        self.dm = datetimeManager()
        end_ts = self.dm.getTimeStamp()
        duration = self.dm.getDurationString(start_ts, end_ts)
        data = self.packDataWithCommonInfo(duration = duration, data = parsedData)
        return data
        pass

    # 沪深两市成交额
    def parse_hslscje(self, name, symbol, text):
        indexInfos = text.split(';')
        # 接口返回的最后一项是个 '\n'
        indexInfos.pop(-1)
        shanghaiDealMoney = 0
        shenzhenDealMoney = 0
        pattern = re.compile('var hq_str_(.*?)="(.*?)"')
        for item in indexInfos:
            result = re.findall(pattern, item)
            if len(result) > 0:
                if result[0][0] == 'sh000002':
                    values = result[0][1].split(',')
                    shanghaiDealMoney = round(float(result[0][1].split(',')[9]) / 100000000,1)
                elif result[0][0] == 'sz399107':
                    shenzhenDealMoney = round(float(result[0][1].split(',')[9]) / 100000000,1)
        totalDealMoney = shanghaiDealMoney + shenzhenDealMoney
        # 结果
        inlandDealMoneyData = [{'name' : '沪', 'value' : shanghaiDealMoney},{'name' : '深', 'value' : shenzhenDealMoney},{'name' : '总', 'value' : totalDealMoney}]
        return {'name': name,'symbol':symbol, 'value':inlandDealMoneyData}

    # 融资融券
    def parse_rzrqye(self, name, symbol, text):
        jsonData = json.loads(text)
        rzrqData = []
        if jsonData['data'] and len(jsonData['data']) > 0:
            lastestData = jsonData['data'][0]
            # ts = int(lastestData['dim_date'])/1000  # python 只处理秒
            # timeTuple = time.localtime(ts)
            # rzrqyeDate = time.strftime("%Y-%m-%d", timeTuple)
            rzrqyeValue = round(lastestData['rzrqye']/(10000 * 10000), 1)
            rzyeValue = round(lastestData['rzye']/(10000 * 10000), 1)
            rqyeValue = round(lastestData['rqye']/(10000 * 10000), 1)
            
            rzrqData.append({'name' : '资', 'value' : rzyeValue})
            rzrqData.append({'name' : '券', 'value' : rqyeValue})
            rzrqData.append({'name' : '总', 'value' : rzrqyeValue})
        return {'name': name,'symbol': symbol, 'value':rzrqData}

    # 沪深资金净流入
    def parse_hszjjlr(self, name, symbol, text):
        inlandMoneyFlowData = []
        data = text.replace('updateMoneyFlow(','').replace(');','')
        jsonData = json.loads(data)
        klines = jsonData["data"]["klines"]
        if len(klines) > 0:
            lastestData = klines[-1].split(',')
        else:
            lastestData = ["0","0","0","0","0","0"]
        # print(lastestData)
        # 取值
        # ["2020-02-21 15:00", "-25845607550.0", "27224361803.0", "-1378753893.0", "-18919648215.0", "-6925959335.0"]
        # 时间，主力净流入（亿），小单净流入（亿），中单净流入（亿），大单净流入（亿），超大单净流入（亿）,都要除以 100000000
        sequencesIndex = [2, 3, 1, 4, 5]
        sequencesName = ['小','中','主','大','特']
        nameIdx = 0
        for idx in sequencesIndex:
            num = round(float(lastestData[idx]) / 100000000,1)
            if num > 0:
                num = '+{0}'.format(num)
            else:
                num = '{0}'.format(num)
            inlandMoneyFlowData.append({'name' : sequencesName[nameIdx], 'value' : num})
            nameIdx = nameIdx + 1
        return {'name':name,'symbol':symbol, 'value':inlandMoneyFlowData}

    # 沪港通深港通资金情况
    def parse_hgtsgtzjqk(self, name, symbol, text):
        finalResult = []
        hongkongS2NFlowData = []
        hongkongN2SFlowData = []
        data = text.replace('updateHKMoneyFlow(','').replace(');','')
        jsonData = json.loads(data)
        # ["15:00", "-88205.65", "5288205.65", "273623.63", "4926376.37", "185417.98"]
        # 时间，沪股通净流入（万），余额（万），深股通净流入（万），余额（万），两市净流入（万）
        sequencesIndex = [1, 3, 5]
        sequencesName = ['沪','深','总']
        # 北向资金
        S2N = jsonData["data"]["s2n"]
        lastestS2N = 0
        for item in S2N:
            dataInfo = item.split(",")
            if dataInfo[1] == '-':
                break
            lastestS2N = dataInfo
        # 赋值
        nameIdx = 0
        for idx in sequencesIndex:
            num = round(float(lastestS2N[idx]) / 10000,1)
            if num > 0:
                num = '+{0}'.format(num)
            else:
                num = '{0}'.format(num)
            hongkongS2NFlowData.append({'name' : sequencesName[nameIdx], 'value' : num})
            nameIdx = nameIdx + 1
        # print(hongkongS2NFlowData)
        finalResult.append({'name':'北向资金净流入（亿）','symbol':'bxzjjlr', 'value':hongkongS2NFlowData})
        # 南向资金
        N2S = jsonData["data"]["n2s"]
        lastestN2S = 0
        for item in N2S:
            dataInfo = item.split(",")
            if dataInfo[1] == '-':
                break
            lastestN2S = dataInfo
        nameIdx = 0
        for idx in sequencesIndex:
            num = round(float(lastestN2S[idx]) / 10000,1)
            if num > 0:
                num = '+{0}'.format(num)
            else:
                num = '{0}'.format(num)
            hongkongN2SFlowData.append({'name' : sequencesName[nameIdx], 'value' : num})
            nameIdx = nameIdx + 1
        # print(hongkongN2SFlowData)
        finalResult.append({'name':'南向资金净流入（亿）','symbol':'nxzjjlr', 'value':hongkongN2SFlowData})
        return finalResult

    # 行业资金净流入
    def parse_hyzjjlr(self, name, symbol, text):
        jsonResult = text.replace('callback(', '').replace(');', '')
        jsonData = json.loads(jsonResult)
        count = jsonData['data']['total']
        datalist = jsonData['data']['diff']
        nameKey = 'f14'
        valueKey = 'f62'
        moneyOuts = []
        # 升序 -100，-90
        # {'f12': 'BK0473', 'f14': '券商信托', 'f62': 2857139456.0}
        moneyOuts.append({ 'name' : datalist['0'][nameKey], 'value' : round(float(datalist['0'][valueKey])/100000000,1)})
        moneyOuts.append({ 'name' : datalist['1'][nameKey], 'value' : round(float(datalist['1'][valueKey])/100000000,1)})
        moneyOuts.append({ 'name' : datalist['2'][nameKey], 'value' : round(float(datalist['2'][valueKey])/100000000,1)})
        moneyOuts.append({ 'name' : datalist['3'][nameKey], 'value' : round(float(datalist['3'][valueKey])/100000000,1)})
        moneyOuts.append({ 'name' : datalist['4'][nameKey], 'value' : round(float(datalist['4'][valueKey])/100000000,1)})
        moneyIns = []
        # 降序 100 90
        moneyIns.append({ 'name' : datalist['{0}'.format(count-1)][nameKey], 'value' : round(float(datalist['{0}'.format(count-1)][valueKey])/100000000,1)})
        moneyIns.append({ 'name' : datalist['{0}'.format(count-2)][nameKey], 'value' : round(float(datalist['{0}'.format(count-2)][valueKey])/100000000,1)})
        moneyIns.append({ 'name' : datalist['{0}'.format(count-3)][nameKey], 'value' : round(float(datalist['{0}'.format(count-3)][valueKey])/100000000,1)})
        moneyIns.append({ 'name' : datalist['{0}'.format(count-4)][nameKey], 'value' : round(float(datalist['{0}'.format(count-4)][valueKey])/100000000,1)})
        moneyIns.append({ 'name' : datalist['{0}'.format(count-5)][nameKey], 'value' : round(float(datalist['{0}'.format(count-5)][valueKey])/100000000,1)})

        return {'name':'行业资金净流入（亿）','symbol':'hyzjjlr', 'value': {'money_in' : moneyIns, 'money_out' : moneyOuts}}

    # ////////////////////////////////////////////////////////////////////////////////////////
    # 解析指数数据 china asian euro america
    # ////////////////////////////////////////////////////////////////////////////////////////

    def parseIndexInfos(self, start_ts, area, text):
        # 可选区域
        areaGroup = ['china', 'asian', 'euro', 'america']
        if area == '' or area.lower() not in areaGroup:
            return {}
        else:
            parsedData = {}
            self.dm = datetimeManager()
            if area.lower() == 'china':
                # 解析中国数据
                parsedData = self.parseChinaIndexs(text)
            elif area.lower() == 'asian':
                # 解析亚洲数据
                parsedData = self.parseAsianIndexs(text)
            elif area.lower() == 'euro':
                # 解析欧洲数据
                parsedData = self.parseEuroIndexs(text)
            elif area.lower() == 'america':
                # 解析美洲数据
                parsedData = self.parseAmericaIndexs(text)
            end_ts = self.dm.getTimeStamp()
            duration = self.dm.getDurationString(start_ts, end_ts)
            data = self.packDataWithCommonInfo(duration = duration, data = parsedData)
            return data
    
    # 清洗&重组中国数据
    def parseChinaIndexs(self, text):
        return self.parseEastmoney100Data(u'中国', json.loads(text))

    def parseAsianIndexs(self, text):
        return self.parseEastmoney87Data(u'亚洲', json.loads(text))

    def parseEuroIndexs(self, text):
        return self.parseEastmoney87Data(u'欧洲', json.loads(text))

    def parseAmericaIndexs(self, text):
        return self.parseEastmoney87Data(u'美洲', json.loads(text))

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

    # 清洗东方财富欧美数据（87.eastmoney）
    def parseEastmoney87Data(self, indexArea, jsonData):
        datalist = jsonData['data']['diff']
        result = []
        count = 0
        # {"f2":1129217,"f3":-124,"f4":-14145,"f6":0.0,"f12":"TWII","f14":"台湾加权","f18":1143362}
        for item in datalist:
            index = indexModel()
            index.indexCode = item['f12']
            index.indexName = item['f14']
            if index.indexName.find(u'新加坡') > 0:
                index.indexName = '新加坡STI'
            if index.indexName == "印度孟买SENSEX":
                index.indexName = '印度SENSEX'
            if index.indexName.find(u'ETF') > 0:
                index.indexName = '油气XOP'
            if index.indexName.find(u'离岸') > 0:
                index.indexName = u'离岸人民币'
            if index.indexName == u"巴西BOVESPA":
                index.indexName = u'巴西BVSP'
            index.indexArea = indexArea
            index.sequence = count
            if index.indexName == u'离岸人民币':
                index.current = round(float(item['f2'])/10000,4)
                index.lastClose = round(float(item['f18'])/10000,4)
                index.dailyChangValue = round(float(item['f4'])/10000,4)
            else:
                index.current = round(float(item['f2'])/100,2)
                index.lastClose = round(float(item['f18'])/100,2)
                index.dailyChangValue = round(float(item['f4'])/100,2)           
            index.dailyChangRate = '{0:.2f}%'.format(round(float(item['f3'])/100,2))
            index.dealMoney = round(float(item['f6']),2)
            result.append(index.__dict__)
            count = count + 1
        return result

    # 添加公共返回值
    def packDataWithCommonInfo(self, isCache = False, isSuccess = True, msg = "success", duration = '0', data = {}):
        code = 0
        if not isSuccess:
            code = -1
        result = {'code' : code, 'msg' : msg, 'isCache' : False, 'aliyun_date' : datetimeManager().getDateTimeString(), 'data' : data, 'duration' : duration}
        return json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True)