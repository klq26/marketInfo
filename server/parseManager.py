# -*- coding: utf-8 -*-

import re
import json

import numpy as np

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
        end_ts = self.dm.getTimeStamp()
        duration = self.dm.getDuration(start_ts, end_ts)
        data = self.packDataWithCommonInfo(duration = duration, data = parsedData)
        return data

    # 沪深两市成交额
    def parse_hslscje(self, name, symbol, text):
        jsonResult = text.replace('callback(', '').replace(');', '')
        jsonData = json.loads(jsonResult)
        datalist = jsonData.get('data', {}).get('diff', [])
        if len(datalist) == 2:
            shanghaiDealMoney = round(float(datalist[0]['f6']) / 100000000, 1)
            shenzhenDealMoney = round(float(datalist[1]['f6']) / 100000000, 1)
        else:
            shanghaiDealMoney = 0.0
            shenzhenDealMoney = 0.0
        totalDealMoney = round(shanghaiDealMoney + shenzhenDealMoney, 1)
        # 结果
        inlandDealMoneyData = [{'name' : '沪', 'value' : shanghaiDealMoney},{'name' : '深', 'value' : shenzhenDealMoney},{'name' : '总', 'value' : totalDealMoney}]
        return {'name': name,'symbol':symbol, 'value':inlandDealMoneyData}

    # 融资融券
    def parse_rzrqye(self, name, symbol, text):
        jsonData = json.loads(text.replace('cb(','').replace(');',''))['result']
        rzrqData = []
        if jsonData['data'] and len(jsonData['data']) > 0:
            lastestData = jsonData['data'][0]
            # ts = int(lastestData['dim_date'])/1000  # python 只处理秒
            # timeTuple = time.localtime(ts)
            # rzrqyeDate = time.strftime("%Y-%m-%d", timeTuple)
            rzrqyeValue = round(lastestData['RZRQYE']/(10000 * 10000), 1)
            rzyeValue = round(lastestData['RZYE']/(10000 * 10000), 1)
            rqyeValue = round(lastestData['RQYE']/(10000 * 10000), 1)
            
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
        # 不要大单和特大单了，为了 UI
        inlandMoneyFlowData.pop(-1)
        inlandMoneyFlowData.pop(-1)
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
        finalResult.append({'name':'北向资金','symbol':'bxzjjlr', 'value':hongkongS2NFlowData})
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
        finalResult.append({'name':'南向资金','symbol':'nxzjjlr', 'value':hongkongN2SFlowData})
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
    # 解析 A 股涨跌平数据
    # ////////////////////////////////////////////////////////////////////////////////////////

    def parseZDPInfo(self, start_ts, texts):
        symbols = []
        names = []
        parsedData = []
        [symbols.append(item['symbol']) for item in self.cm.zdpinfo]
        [names.append(item['name']) for item in self.cm.zdpinfo]
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
        end_ts = self.dm.getTimeStamp()
        duration = self.dm.getDuration(start_ts, end_ts)
        data = self.packDataWithCommonInfo(duration = duration, data = parsedData)
        return data

    def parse_zdfb_zdt(self, name, symbol, text):
        finalResult = []
        jsonResult = text.replace('callback(', '').replace(');', '')
        jsonData = json.loads(jsonResult)
        data = jsonData['data']['fenbu']
        print(data)
        fenbu = {}
        for x in data:
            # 高效合并两个字典
            fenbu = dict(fenbu, **x)
        zdfb = []
        # 下跌（把 -10 和 -9 合并成 -10% ~ -8%，下同。这里的 -9 实际上是 -8%）
        fall_keys = np.arange(-10, 0, 1).reshape(5, -1).tolist()
        for group in fall_keys:
        #     print(group)
            total = 0
            for x in group:
                total += fenbu[str(x)]
            zdfb.append(total)
        # 上涨（把 1 和 2 合并成 0% ~ 2%）
        raise_keys = np.arange(1, 11, 1).reshape(5, -1).tolist()
        for group in raise_keys:
        #     print(group)
            total = 0
            for x in group:
                total += fenbu[str(x)]
        #     print(total)
            zdfb.append(total)

        finalResult.append({'name' : '涨跌分布','symbol' : 'zdfb', 'value' : zdfb[::-1]})
        finalResult.append({'name' : '涨跌停','symbol' : 'zdt', 'value' : [{'name' : '涨停','symbol' : 'zt', 'value' : fenbu['11']},{'name' : '跌停','symbol' : 'dt', 'value' : fenbu['-11']+fenbu['-10']}]})
        return finalResult

    def parse_zszdp(self, name, symbol, text):
        finalResult = []
        results = []
        jsonResult = text.replace('callback(', '').replace(');', '')
        jsonData = json.loads(jsonResult)
        datalist = jsonData.get('data', {}).get('diff', [])
        if len(datalist) == 9:
            allMarkets = ['000002','000003','399107','399108']
            indexMapping = {'399102':'创业板综','000016':'上证50','000300':'沪深300','399905':'中证500','000852':'中证1000'}
            allUp = 0
            allEqual = 0
            allDown = 0
            for item in datalist:
                if item['f12'] in allMarkets:
                    allUp = allUp + int(item['f104'])
                    allEqual = allEqual + int(item['f106'])
                    allDown = allDown + int(item['f105'])
                else:
                    name = indexMapping[item['f12']]
                    up = int(item['f104'])
                    equal = int(item['f106'])
                    down = int(item['f105'])
                    if up + equal + down > 0: # 中证1000有点问题，3个都是0，先忽略错误数据吧
                        results.append({'name' : name, 'symbol' : item['f12'], 'z':up, 'p':equal, 'd':down})
            results.insert(0, {'name' : '全市场', 'symbol' : 'all', 'z':allUp, 'p':allEqual, 'd':allDown})
            # print(results)
            finalResult.append({'name' : '指数涨跌平','symbol' : 'zdp', 'value' : results})
        return finalResult
    
    # ////////////////////////////////////////////////////////////////////////////////////////
    # 解析指数数据 china asian euro america australia
    # ////////////////////////////////////////////////////////////////////////////////////////

    def parseIndexInfos(self, start_ts, area, names, text):
        # 可选区域
        areaGroup = ['china', 'asian', 'euro', 'america', 'australia']
        if area == '' or area.lower() not in areaGroup:
            return {}
        else:
            parsedData = {}
            if area.lower() == 'china':
                # 解析中国数据
                parsedData = self.parseChinaIndexs(text)
            elif area.lower() == 'asian':
                # 解析亚洲数据
                parsedData = self.parseAsianIndexs(text, names)
            elif area.lower() == 'euro':
                # 解析欧洲数据
                parsedData = self.parseEuroIndexs(text, names)
            elif area.lower() == 'america':
                # 解析美洲数据
                parsedData = self.parseAmericaIndexs(text, names)
            elif area.lower() == 'australia':
                # 解析澳洲数据
                parsedData = self.parseAustraliaIndexs(text)
            end_ts = self.dm.getTimeStamp()
            duration = self.dm.getDuration(start_ts, end_ts)
            data = self.packDataWithCommonInfo(duration = duration, data = parsedData)
            return data
    
    # 清洗&重组中国数据
    def parseChinaIndexs(self, text):
        return self.parseEastmoney100Data(u'中国', json.loads(text))

    def parseAsianIndexs(self, text, countryNames):
        return self.parseEastmoney87Data(u'亚洲',countryNames, json.loads(text))

    def parseEuroIndexs(self, text, countryNames):
        return self.parseEastmoney87Data(u'欧洲',countryNames, json.loads(text))

    def parseAmericaIndexs(self, text, countryNames):
        return self.parseEastmoney87Data(u'美洲',countryNames, json.loads(text))

    def parseAustraliaIndexs(self, text):
        countryNames = ['澳大利亚','新西兰']
        return self.parseEastmoney87Data(u'澳洲',countryNames, json.loads(text))

    # 清洗东方财富亚洲数据（100.eastmoney）
    def parseEastmoney100Data(self, indexArea, jsonData):
        datalist = jsonData['data']['diff']
        result = []
        for key in datalist.keys():
            item = datalist[key]
            index = indexModel()
            index.indexCode = item['f12']
            index.indexName = item['f14'].replace(' ','')
            if index.indexName == u'国证Ａ指':
                index.indexName = u'国证A指'
            if index.indexName == u'中国互联网50':
                index.indexName = u'海外互联'
            if index.indexName == u'恒生科技指数':
                index.indexName = u'恒生科技'
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
    def parseEastmoney87Data(self, indexArea, customNames, jsonData):
        datalist = jsonData['data']['diff']
        result = []
        count = 0
        # {"f2":1129217,"f3":-124,"f4":-14145,"f6":0.0,"f12":"TWII","f14":"台湾加权","f18":1143362}
        for item in datalist:
            index = indexModel()
            index.indexCode = item['f12']
            index.indexName = item['f14']
            if len(customNames) > count:
                # 对输出项的名称进行干预
                index.indexName = customNames[count]
            index.indexArea = indexArea
            index.sequence = count
            if index.indexName == u'离岸汇率':
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

    # ////////////////////////////////////////////////////////////////////////////////////////
    # 解析期货&外汇数据
    # ////////////////////////////////////////////////////////////////////////////////////////
    
    def parseGoodsAndExchangeInfo(self, start_ts, texts):
        symbols = []
        names = []
        parsedData = []
        [symbols.append(item['symbol']) for item in self.cm.goods_and_exchanges]
        [names.append(item['name']) for item in self.cm.goods_and_exchanges]
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
                    # 2022年2月10日10:00:58：去掉单独请求离岸人民币的接口后，这块应该永远不会走了，仅做backup
                    parsedData.append(data)
            else:
                parsedData.append({'name' : name, 'symbol' : symbol, 'value' : []})

        # 离岸人民币
        USDCNH = parsedData[11] # 2022年4月13日15:35:07：这样写很不好，以后指数期货增加了，还得改！但是比for循环效率高
        # print(USDCNH)
        # COMEX 黄金
        COMEX_GC = parsedData[0]
        # print(COMEX_GC)
        # COMEX 白银
        COMEX_SI = parsedData[1]
        # print(COMEX_SI)
        # COMEX 黄金白银的单位是金衡盎司，1金衡盎司 = 31.1034768克
        # 期货新增工行纸黄金
        cnGold = indexModel()
        cnGold.indexCode = 'GOLD'
        cnGold.indexName = '工行黄金'
        cnGold.indexArea = '期货'
        cnGold.current = round(float(COMEX_GC['current']) / 31.1034768 * float(USDCNH['current']), 4)
        cnGold.lastClose = round(float(COMEX_GC['lastClose']) / 31.1034768 * float(USDCNH['lastClose']), 4)
        cnGold.dailyChangRate = '{0:.2f}%'.format(
                    round(float((cnGold.current / cnGold.lastClose - 1) * 100), 2))
        cnGold.dailyChangValue = round(float(cnGold.current - cnGold.lastClose), 4)
        cnGold.dealMoney = 0.0
        cnGold.sequence = 0
        # 纸黄金挪到第三位
        parsedData.insert(2, cnGold.__dict__)
        # 期货新增工行纸白银
        cnSilver = indexModel()
        cnSilver.indexCode = 'SILVER'
        cnSilver.indexName = '工行白银'
        cnSilver.indexArea = '期货'
        cnSilver.current = round(float(COMEX_SI['current']) / 31.1034768 * float(USDCNH['current']), 4)
        cnSilver.lastClose = round(float(COMEX_SI['lastClose']) / 31.1034768 * float(USDCNH['lastClose']), 4)
        cnSilver.dailyChangRate = '{0:.2f}%'.format(
                    round(float((cnSilver.current / cnSilver.lastClose - 1) * 100), 2))
        cnSilver.dailyChangValue = round(float(cnSilver.current - cnSilver.lastClose), 4)
        cnSilver.dealMoney = 0.0
        cnSilver.sequence = 0
        # 纸白银挪到第四位
        parsedData.insert(3, cnSilver.__dict__)
        # 分组（goods & exchanges）
        goods = parsedData[0:13]
        for i in range(0,len(goods)):
            goods[i]['sequence'] = i
        exchanges = parsedData[13:len(parsedData)]
        for i in range(0,len(exchanges)):
            exchanges[i]['sequence'] = i

        end_ts = self.dm.getTimeStamp()
        duration = self.dm.getDuration(start_ts, end_ts)
        data = self.packDataWithCommonInfo(duration = duration, data = {'goods': goods, 'exchanges':exchanges})
        return data
    
    def parse_goods_and_exchanges(self, name, symbol, text):
        jsonResult = text.replace('callback(', '').replace(');', '')
        jsonData = json.loads(jsonResult)
        datalist = jsonData.get('data', {}).get('diff', [])
        if len(datalist) > 0:
            count = 0
            # 期货接口key&name
            goodKeys = ['GC00Y', 'SI00Y', 'CL00Y', 'CN00Y', 'IHFI', 'IFFI', 'ICFI', 'HSI_M', 'HSIM2', 'HSIU2', 'HSIZ2']
            goodNames = ['纽约黄金', '纽约白银', '纽约原油', 'A50期货', 'IH50期货', 'IF300期货', 'IC500期货', '恒生期货', '恒06期货', '恒09期货', '恒12期货']
            # 外汇接口key&name
            exchangeKeys = ['USDCNH', 'USDCNYC', 'CADCNYC', 'GBPCNYC', 'EURCNYC', 'AUDCNYC', 'HKDCNYC', 'JPYCNYC', 'CNYKRWC']
            exchangeNames = ['离岸汇率', '美元汇率', '加元汇率', '英镑汇率', '欧元汇率', '澳元汇率', '港元汇率', '日元汇率', '韩元汇率']
            # 结果
            results = []
            # 解析期货
            for i, key in enumerate(goodKeys):
                for item in datalist:
                    if item['f12'] == key:
                        index = indexModel()
                        index.indexCode = key
                        index.indexName = goodNames[i]
                        index.indexArea = '期货'
                        index.current = round(float(item['f2']), 4)
                        index.lastClose = round(float(item['f18']), 4)
                        index.dailyChangRate = '{0}%'.format(round(float(item['f3']), 4))
                        index.dailyChangValue = round(float(item['f4']), 4)    
                        index.dealMoney = 0.0
                        index.sequence = count
                        count = count + 1
                        results.append(index.__dict__)
                        break
            # 解析外汇
            for i, key in enumerate(exchangeKeys):
                for item in datalist:
                    if item['f12'] == key:
                        index = indexModel()
                        if 'CNH' in key:
                            # 离岸人民币代码是USDCNH，不带C
                            index.indexCode = key
                        else:
                            index.indexCode = key[0:len(key)-1]
                        index.indexName = exchangeNames[i]
                        index.indexArea = '外汇'
                        index.current = round(float(item['f2']), 4)
                        index.lastClose = round(float(item['f18']), 4)
                        index.dailyChangRate = '{0}%'.format(round(float(item['f3']), 4))
                        index.dailyChangValue = round(float(item['f4']), 4)    
                        index.dealMoney = 0.0
                        index.sequence = count
                        count = count + 1
                        # 针对日元做修正
                        if index.indexCode == 'JPYCNY':
                            index.current = round(index.current / 100, 4)
                            index.lastClose = round(index.lastClose / 100, 4)
                            index.dailyChangValue = round(index.dailyChangValue / 100, 4)    
                        # 针对韩元做修正
                        if index.indexCode == 'CNYKRW':
                            index.indexCode = 'KRWCNY'
                            index.current = round(1 / index.current, 4)
                            index.lastClose = round(1 / index.lastClose, 4)
                            index.dailyChangValue = round(index.current - index.lastClose, 4)  
                        results.append(index.__dict__)
                        break
        return results

    # ////////////////////////////////////////////////////////////////////////////////////////
    # 请求债券数据
    # ////////////////////////////////////////////////////////////////////////////////////////

    def parseBondInfo(self, start_ts, texts):
        symbols = []
        names = []
        parsedData = []
        [symbols.append(item['symbol']) for item in self.cm.bondinfo]
        [names.append(item['name']) for item in self.cm.bondinfo]
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
        # 调用了三次蛋卷 plan，需要重新组织数据结构
        non_plan = parsedData[0:2]
        plans = parsedData[2:len(parsedData)]
        grouped_plans = []
        for i in range(0,len(plans)):
            plans[i]['value']['sequence'] = i
            grouped_plans.append(plans[i]['value'])
        new_plans = {'name' : plans[0]['name'], 'symbol' : plans[0]['symbol'], 'value' : grouped_plans}
        finalResult = []
        [finalResult.append(x) for x in non_plan]
        finalResult.append(new_plans)
        end_ts = self.dm.getTimeStamp()
        duration = self.dm.getDuration(start_ts, end_ts)
        data = self.packDataWithCommonInfo(duration = duration, data = finalResult)
        return data

    def parse_bond(self, name, symbol, text):
        jsonData = json.loads(text)
        finalResult = []
        # workDate = jsonData['worktime']
        # 5 7 10 年国债
        bond5year = 0.0
        bond7year = 0.0
        bond10year = 0.0
        if len(jsonData) >= 1:
            values = jsonData[0]['seriesData']
            for valueArray in values:
                if valueArray[0] == 5.0:
                    bond5year = '{0}%'.format(round(float(valueArray[1]),2))
                elif valueArray[0] == 7.0:
                    bond7year = '{0}%'.format(round(float(valueArray[1]),2))
                elif valueArray[0] == 10.0:
                    bond10year = '{0}%'.format(round(float(valueArray[1]),2))
            result5year = { 'indexName' : u'5年国债', 'indexCode' : '5YEAR','indexArea' : '债券', 'sequence' : 0, 'current' : bond5year, 'lastClose' : bond5year,'dailyChangValue' : 0.000, 'dealMoney' : 0.000, 'dailyChangRate' : '0.00%', 'year' : 5}
            result7year = { 'indexName' : u'7年国债', 'indexCode' : '7YEAR','indexArea' : '债券', 'sequence' : 1, 'current' : bond7year, 'lastClose' : bond7year,'dailyChangValue' : 0.000, 'dealMoney' : 0.000, 'dailyChangRate' : '0.00%', 'year' : 7}
            result10year = { 'indexName' : u'10年国债', 'indexCode' : '10YEAR','indexArea' : '债券', 'sequence' : 2, 'current' : bond10year, 'lastClose' : bond10year,'dailyChangValue' : 0.000, 'dealMoney' : 0.000, 'dailyChangRate' : '0.00%', 'year' : 10}
        finalResult.append({'name': name, 'symbol' : symbol, 'value' : [result5year, result7year, result10year]})
        return finalResult

    def parse_fund(self, name, symbol, text):
        data = json.loads(text)['data']
        finalResult = []
        current = '{0}%'.format(round(float(data['fund_derived']['annual_yield7d']),2))
        value = { 'indexName' : u'天天利B', 'indexCode' : '003474','indexArea' : '货基', 'sequence' : 0, 'current' : current, 'lastClose' : current,'dailyChangValue' : 0.000, 'dealMoney' : 0.000, 'dailyChangRate' : '0.00%'}
        finalResult.append({'name': name, 'symbol' : symbol, 'value' : [value]})
        return finalResult

    def parse_plan(self, name, symbol, text):
        data = json.loads(text)['data']
        finalResult = []
        count = 0
        # index = indexModel()
        planName = data['plan_name']
        if u'稳稳' in planName:
            planName = '稳稳幸福'
        if u'90' in planName:
            planName = '钉钉宝90'
        if u'365' in planName:
            planName = '钉钉宝365'
        current = round(float(data['yield_middle']),2)
        nav = round(float(data['plan_derived']['unit_nav']),4)
        dailyChangeRate = round(float(data['plan_derived']['nav_grtd']),2)
        lastClose = round(float(nav / (1 + dailyChangeRate / 100)),4)
        dailyChangeValue = round(nav - lastClose,4)
        
        value = { 'nav' : nav, 'indexName' : planName, 'indexCode' : data['plan_code'],'indexArea' : '组合', 'sequence' : count, 'current' : "{0:.2f}%".format(current), 'lastClose' : 0,'dailyChangValue' : dailyChangeValue, 'dealMoney' : 0.000, 'dailyChangRate' : "{0}%".format(dailyChangeRate)}
        count = count + 1
        finalResult.append({'name': name, 'symbol' : symbol, 'value' : value})
        return finalResult
    
    # ////////////////////////////////////////////////////////////////////////////////////////
    # 解析指数排序数据 china asian euro america australia
    # ////////////////////////////////////////////////////////////////////////////////////////
    def parseIndexSortInfos(self, start_ts, area, type, datalist):
        # 本地数据库查询结果，直接打包
        end_ts = self.dm.getTimeStamp()
        duration = self.dm.getDuration(start_ts, end_ts)
        data = self.packDataWithCommonInfo(duration = duration, data = datalist)
        return data

    # ////////////////////////////////////////////////////////////////////////////////////////
    # 解析今日类型（开盘日：0 周末：1 节假日：2
    # ////////////////////////////////////////////////////////////////////////////////////////

    def parseDayType(self, start_ts, text):
        jsonData = text
        dayType = jsonData[self.dm.getDateString()]
        weekday = '0'
        weekend = '0'
        holiday = '0'
        if dayType == '0':
            weekday = '1'
            weekend = '0'
            holiday = '0'
        elif dayType == '1':
            weekday = '0'
            weekend = '1'
            holiday = '0'
        elif dayType == '2':
            weekday = '0'
            weekend = '0'
            holiday = '1'
        parsedData = {'weekday' : weekday, 'weekend' : weekend, 'holiday' : holiday }
        # 结束时间
        end_ts = self.dm.getTimeStamp()
        duration = self.dm.getDuration(start_ts, end_ts)
        data = self.packDataWithCommonInfo(duration = duration, data = parsedData)
        return data

    # ////////////////////////////////////////////////////////////////////////////////////////
    # 解析国家信息
    # ////////////////////////////////////////////////////////////////////////////////////////
    def parseCountryinfo(self, start_ts, indexName, datalist):
        # 本地数据库查询结果，直接打包
        end_ts = self.dm.getTimeStamp()
        duration = self.dm.getDuration(start_ts, end_ts)
        datalist[0]['area'] = self.numToUnitType(datalist[0]['area'], '平方公里')
        datalist[0]['gdpRMB'] = self.numToUnitType(datalist[0]['gdpRMB'], '元')
        datalist[0]['population'] = self.numToUnitType(datalist[0]['population'], '人')
        datalist[0]['gdpPersonAvg'] = self.numToUnitType(datalist[0]['gdpPersonAvg'], '元')
        summerTime = datalist[0]['summerTime']
        if summerTime == 'NA':
            summerTime = '无'
        else:
            summerTime = ' - '.join([x.replace(' ','') + '月' for x in summerTime.split('-')])
        datalist[0]['summerTime'] = summerTime
        dealTime = datalist[0]['dealTime']
        values = dealTime.split('-')
        close = values[1]
        close_hour, close_minute = close.split(':')
        if int(close_hour) >= 24:
            close_hour = str(int(close_hour) - 24)
        close = close_hour + ':' + close_minute
        datalist[0]['dealTime'] = '{0} - {1}'.format(values[0], close)
        datalist[0]['breakTime'] = datalist[0]['breakTime'].replace('-',' - ')
        data = self.packDataWithCommonInfo(duration = duration, data = datalist)
        return data
    
    def numToUnitType(self, num, unit):
        length = len(str(int(num)))
        result = ''
        if length > 12:
            result = '{0}{1}{2}'.format(round(float(num) / 1000000000000, 2),'万亿',unit)
        elif length > 8:
            result = '{0}{1}{2}'.format(round(float(num) / 100000000, 2),'亿',unit)
        elif length > 4:
            result = '{0}{1}{2}'.format(round(float(num) / 10000, 2),'万',unit)
        return result
        # 9600000
        # 99086500000000
        # 1400000000


    # ////////////////////////////////////////////////////////////////////////////////////////
    # 解析指数历史数据
    # ////////////////////////////////////////////////////////////////////////////////////////
    def parseIndexHistory(self, start_ts, indexName, datalist):
        # 本地数据库查询结果，直接打包
        end_ts = self.dm.getTimeStamp()
        duration = self.dm.getDuration(start_ts, end_ts)
        if len(datalist) > 0:
            result = []
            historyInfos = datalist[0]['indexHistory'].split('-')
            count = len(historyInfos)
            if count == 10:
                yearData = historyInfos[count - 10].split(',')
                result.append({'name':'十年', 'open':yearData[1], 'count': 10, 'year': yearData[0]})
            if count >= 5:
                yearData = historyInfos[count - 5].split(',')
                result.append({'name':'五年', 'open':yearData[1], 'count': 5, 'year': yearData[0]})
            if count >= 3:
                yearData = historyInfos[count - 3].split(',')
                result.append({'name':'三年', 'open':yearData[1], 'count': 3, 'year': yearData[0]})
            if count >= 1:
                yearData = historyInfos[-1].split(',')
                result.append({'name':'今年', 'open':yearData[1], 'count': 1, 'year': yearData[0]})
            datalist[0]['indexHistory'] = result
        data = self.packDataWithCommonInfo(duration = duration, data = datalist)
        return data

    