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
        end_ts = self.dm.getTimeStamp()
        duration = self.dm.getDurationString(start_ts, end_ts)
        data = self.packDataWithCommonInfo(duration = duration, data = parsedData)
        return data

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
        duration = self.dm.getDurationString(start_ts, end_ts)
        data = self.packDataWithCommonInfo(duration = duration, data = parsedData)
        return data

    def parse_zdfb_zdt(self, name, symbol, text):
        finalResult = []
        jsonData = json.loads(text)
        arr = jsonData['zdfb_data']['zdfb']
        finalResult.append({'name' : '涨跌分布','symbol' : 'zdfb', 'value' : list(reversed(jsonData['zdfb_data']['zdfb']))})
        finalResult.append({'name' : '涨跌停','symbol' : 'zdt', 'value' : [{'name' : '涨停','symbol' : 'zt', 'value' : jsonData['zdt_data']['last_zdt']['ztzs']},{'name' : '跌停','symbol' : 'dt', 'value' : jsonData['zdt_data']['last_zdt']['dtzs']}]})
        return finalResult

    def parse_zszdp(self, name, symbol, text):
        finalResult = []
        zdpRawData = text.split(';')
        # 接口返回的最后一项是个 '\n'
        zdpRawData.pop(-1)
        # 结果集
        results = []
        # 正则匹配集
        rawlist = []
        # 正则匹配
        pattern = re.compile('var hq_str_(.*?)_zdp="(.*?)"')
        for item in zdpRawData:
            # print(item)
            result = re.findall(pattern, item)
            if len(result) > 0:
                rawlist.append(result[0])
        # // e.g.
        # // var hq_str_sh000002_zdp="865,535,97";    沪A
        # // var hq_str_sz399107_zdp="1396,702,95";   深A
        # // var hq_str_sh000003_zdp="26,14,9";       沪B
        # // var hq_str_sz399108_zdp="13,26,7";       深B
        # // var hq_str_sz399102_zdp="559,217,15";    创业
        
        #[('sh000002', '76,1416,5'), ('sz399107', '144,2044,8'), ('sh000003', '1,48,0'), ('sz399108', '3,41,2'), ('sz399102', '48,745,1'), ('sh000016', '2,48,0'), ('sh000300', '17,283,0'), ('sz399905', '20,480,0'), ('sh000852', '54,941,5'), ('sh000842', '37,763,0')]
        allMarkets = ['sh000002','sh000003','sz399107','sz399108']
        indexMapping = {'sz399102':'创业板综','sh000016':'上证50','sh000300':'沪深300','sz399905':'中证500','sh000852':'中证1000','sh000842':'等权800'}
        allUp = 0
        allEqual = 0
        allDown = 0
        for item in rawlist:
            values = item[1].split(',')
            if item[0] in allMarkets:
                allUp = allUp + int(values[0])
                allEqual = allEqual + int(values[2])
                allDown = allDown + int(values[1])
            else:
                name = indexMapping[item[0]]
                up = int(values[0])
                equal = int(values[2])
                down = int(values[1])
                results.append({'name' : name, 'symbol' : item[0], 'z':up, 'p':equal, 'd':down})
        results.insert(0, {'name' : '全市场', 'symbol' : 'all', 'z':allUp, 'p':allEqual, 'd':allDown})
        # print(results)
        finalResult.append({'name' : '指数涨跌平','symbol' : 'zdp', 'value' : results})
        return finalResult
    
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
                    parsedData.append(data)
            else:
                parsedData.append({'name' : name, 'symbol' : symbol, 'value' : []})
        USDCNH = parsedData.pop(0)
        # 离岸人民币挪到第五位
        parsedData.insert(4,USDCNH)
        # 分组（goods & exchanges）
        goods = parsedData[0:4]
        for i in range(0,len(goods)):
            goods[i]['sequence'] = i
        exchanges = parsedData[4:len(parsedData)]
        for i in range(0,len(exchanges)):
            exchanges[i]['sequence'] = i

        end_ts = self.dm.getTimeStamp()
        duration = self.dm.getDurationString(start_ts, end_ts)
        data = self.packDataWithCommonInfo(duration = duration, data = {'goods': goods, 'exchanges':exchanges})
        return data
    
    def parse_larmb(self, name, symbol, text):
        result = text.replace('updateIndexInfos(', '').replace(');', '')
        # 清洗&重组数据
        USDCNH = self.parseEastmoney87Data('外汇', json.loads(result))[0]
        return USDCNH

    def parse_goods_and_exchanges(self, name, symbol, text):
        exchanges = text.split(';')
        # 接口返回的最后一项是个 '\n'
        exchanges.pop(-1)
        # 期货
        # goodKeys = ['hf_CHA50CFD', 'hf_GC', 'hf_SI', 'hf_CL']
        # 外汇
        exchangeKeys = ['USDCNY', 'CADCNY', 'GBPCNY', 'EURCNY', 'AUDCNY', 'HKDCNY', 'TWDCNY','fx_sjpycny', 'fx_skrwcny']
        # 结果
        results = []
        # 正则匹配集
        rawlist = []
        # 正则匹配
        pattern = re.compile('var hq_str_(.*?)="(.*?)"')
        for item in exchanges:
            # print(item)
            result = re.findall(pattern, item)
            if len(result) > 0:
                rawlist.append(result[0])
        # 清洗正则匹配集，产出最终数据
        count = 0
        for item in rawlist:
            index = indexModel()
            # 数据集合
            values = item[1].split(',')
            # 代码
            indexCode = item[0].replace('hf_', '')
            if indexCode in exchangeKeys:
                # 外汇
                # 日元人民币
                if indexCode == 'fx_sjpycny':
                    indexCode = 'JPYCNY'
                    indexName = '日元人民币'
                # 韩元人民币
                elif indexCode == 'fx_skrwcny':
                    indexCode = 'KRWCNY'
                    indexName = '韩元人民币'
                else:
                    indexCode = item[0].replace('hf_', '')
                    indexName = values[9]
                index.indexCode = indexCode
                index.indexName = indexName
                index.indexArea = '外汇'

                index.current = round(float(values[2]), 4)
                index.lastClose = round(float(values[3]), 4)
                index.dailyChangRate = '{0:.2f}%'.format(
                    round(float((index.current / index.lastClose - 1) * 100), 2))
                index.dailyChangValue = round(float(index.current - index.lastClose), 4)
                index.dealMoney = 0.0
                index.sequence = count
                count = count + 1
            else:
                # 期货
                index.indexCode = item[0].replace('hf_', '')
                if item[0] == 'hf_CHA50CFD':
                    index.indexName = '富时A50'
                else:
                    index.indexName = values[-1]
                index.indexArea = '期货'
                index.current = round(float(values[0]), 3)
                index.lastClose = round(float(values[7]), 3)
                index.dailyChangRate = '{0:.2f}%'.format(
                    round(float((index.current / index.lastClose - 1) * 100), 2))
                index.dailyChangValue = round(float(index.current - index.lastClose), 3)
                index.dealMoney = 0.0
                index.sequence = count
                count = count + 1
            results.append(index.__dict__)
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
        duration = self.dm.getDurationString(start_ts, end_ts)
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
        values = jsonData['seriesData']
        for valueArray in values:
            if valueArray[0] == 5.0:
                bond5year = '{0}%'.format(round(float(valueArray[1]),2))
            elif valueArray[0] == 7.0:
                bond7year = '{0}%'.format(round(float(valueArray[1]),2))
            elif valueArray[0] == 10.0:
                bond10year = '{0}%'.format(round(float(valueArray[1]),2))
        result5year = { 'indexName' : u'5年期国债', 'indexCode' : '5YEAR','indexArea' : '债券', 'sequence' : 0, 'current' : bond5year, 'lastClose' : bond5year,'dailyChangValue' : 0.000, 'dealMoney' : 0.000, 'dailyChangRate' : '0.00%', 'year' : 5}
        result7year = { 'indexName' : u'7年期国债', 'indexCode' : '7YEAR','indexArea' : '债券', 'sequence' : 1, 'current' : bond7year, 'lastClose' : bond7year,'dailyChangValue' : 0.000, 'dealMoney' : 0.000, 'dailyChangRate' : '0.00%', 'year' : 7}
        result10year = { 'indexName' : u'10年期国债', 'indexCode' : '10YEAR','indexArea' : '债券', 'sequence' : 2, 'current' : bond10year, 'lastClose' : bond10year,'dailyChangValue' : 0.000, 'dealMoney' : 0.000, 'dailyChangRate' : '0.00%', 'year' : 10}
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
            planName = '稳稳的幸福'
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
    # 解析今日类型（开盘日：0 周末：1 节假日：2
    # ////////////////////////////////////////////////////////////////////////////////////////

    def parseDayType(self, start_ts, text):
        jsonData = json.loads(text)
        dayType = jsonData[self.dm.getDateString()]
        # print(dayType, jsonData)
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
        duration = self.dm.getDurationString(start_ts, end_ts)
        data = self.packDataWithCommonInfo(duration = duration, data = parsedData)
        return data
