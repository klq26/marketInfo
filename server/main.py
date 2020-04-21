# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import Response
# 跨域
from flask_cors import *

from cacheManager import cacheManager
from requestManager import requestsManager
from parseManager import parseManager
from datetimeManager import datetimeManager
from databaseManager import databaseManager


app = Flask(__name__)
CORS(app, supports_credentials=True)

cm = cacheManager()

# ////////////////////////////////////////////////////////////////////////////////////////
# 请求资金数据（两市成交额，融资融券，两市资金净流入，沪港通，沪深通净流入，板块资金）
# ////////////////////////////////////////////////////////////////////////////////////////

@app.route('/api/moneyinfo', methods=['GET'])
def getMoneyInfo_deprecated():
    return getMoneyInfo()

@app.route('/marketinfo/api/moneyinfo', methods=['GET'])
def getMoneyInfo():
    start_ts = datetimeManager().getTimeStamp()
    if cm.cacheAvailable(start_ts, request.path):
        data = cm.getCache(start_ts, request.path)
        return Response(data, status=200, mimetype='application/json')
    responseTexts = requestsManager().getMoneyInfo()
    data = parseManager().parseMoneyInfo(start_ts, responseTexts)
    cm.saveCache(request.path, data)
    return Response(data, status=200, mimetype='application/json')

# ////////////////////////////////////////////////////////////////////////////////////////
# 请求 A 股涨跌平数据
# ////////////////////////////////////////////////////////////////////////////////////////

@app.route('/api/zdpinfo', methods=['GET'])
def getZDPInfo_deprecated():
    return getZDPInfo()

@app.route('/marketinfo/api/zdpinfo', methods=['GET'])
def getZDPInfo():
    start_ts = datetimeManager().getTimeStamp()
    if cm.cacheAvailable(start_ts, request.path):
        data = cm.getCache(start_ts, request.path)
        return Response(data, status=200, mimetype='application/json')
    responseTexts = requestsManager().getZDPInfo()
    data = parseManager().parseZDPInfo(start_ts, responseTexts)
    cm.saveCache(request.path, data)
    return Response(data, status=200, mimetype='application/json')

# ////////////////////////////////////////////////////////////////////////////////////////
# 请求指数数据 china asian euro america australia
# ////////////////////////////////////////////////////////////////////////////////////////
@app.route('/api/indexs/<string:area>', methods=['GET'])
def getIndexInfos_deprecated(area):
    return getIndexInfos(area)

@app.route('/marketinfo/api/indexs/<string:area>', methods=['GET'])
def getIndexInfos(area):
    start_ts = datetimeManager().getTimeStamp()
    sortType = request.args.get('sort', '')
    if not sortType:
        sortType = 1
        # 目前，带 sort 的都不命中缓存，这块后续还得想想办法 TODO
        if cm.cacheAvailable(start_ts, request.path):
            data = cm.getCache(start_ts, request.path)
            return Response(data, status=200, mimetype='application/json')
    else:
        sortType = int(sortType)
    areaGroup = ['china', 'asian', 'euro', 'america','australia']
    if area == '' or area.lower() not in areaGroup:
        return {}
    else:
        continent = ''
        if area.lower() == 'china':
            # 请求中国数据
            continent = '中国'
        elif area.lower() == 'asian':
            # 请求亚洲数据
            continent = '亚洲'
        elif area.lower() == 'euro':
            # 请求欧洲数据
            continent = '欧洲'
        elif area.lower() == 'america':
            # 请求美洲数据
            continent = '美洲'
        elif area.lower() == 'australia':
            # 请求澳洲数据
            continent = '澳洲'
        names, codes = getSequence(continent, sortType)
        responseText = requestsManager().getIndexInfos(area, codes)
        data = parseManager().parseIndexInfos(start_ts, area, names, responseText)
        cm.saveCache(request.path, data)
        return Response(data, status=200, mimetype='application/json')

# 根据 sort 类型和目标大陆返回指数名称和指数代码数组
def getSequence(continent, sortType):
    db = databaseManager()
    if sortType == 2:
        return db.sequenceByDealTime(continent)
    elif sortType == 3:
        return db.sequenceByAverageGDP(continent)
    elif sortType == 4:
        return db.sequenceByPopulation(continent)
    elif sortType == 5:
        return db.sequenceByArea(continent)
    else:
        # 等于 1 和非法数字都给默认 GDP 降序
        return db.sequenceByGDP(continent)

# ////////////////////////////////////////////////////////////////////////////////////////
# 请求期货&外汇数据
# ////////////////////////////////////////////////////////////////////////////////////////

@app.route('/api/goods_and_exchanges', methods=['GET'])
def getGoodsAndExchangeInfo_deprecated():
    return getGoodsAndExchangeInfo()

@app.route('/marketinfo/api/goods_and_exchanges', methods=['GET'])
def getGoodsAndExchangeInfo():
    start_ts = datetimeManager().getTimeStamp()
    if cm.cacheAvailable(start_ts, request.path):
        data = cm.getCache(start_ts, request.path)
        return Response(data, status=200, mimetype='application/json')
    responseTexts = requestsManager().getGoodsAndExchangeInfo()
    data = parseManager().parseGoodsAndExchangeInfo(start_ts, responseTexts)
    cm.saveCache(request.path, data)
    return Response(data, status=200, mimetype='application/json')

# ////////////////////////////////////////////////////////////////////////////////////////
# 请求债券数据
# ////////////////////////////////////////////////////////////////////////////////////////

@app.route('/api/bondinfo', methods=['GET'])
def getBondInfo_deprecated():
    return getBondInfo()

@app.route('/marketinfo/api/bondinfo', methods=['GET'])
def getBondInfo():
    start_ts = datetimeManager().getTimeStamp()
    if cm.cacheAvailable(start_ts, request.path):
        data = cm.getCache(start_ts, request.path)
        return Response(data, status=200, mimetype='application/json')
    responseTexts = requestsManager().getBondInfo()
    data = parseManager().parseBondInfo(start_ts, responseTexts)
    cm.saveCache(request.path, data)
    return Response(data, status=200, mimetype='application/json')

# ////////////////////////////////////////////////////////////////////////////////////////
# 请求指数所属国家的信息
# ////////////////////////////////////////////////////////////////////////////////////////

@app.route('/api/countryinfo/<string:indexName>', methods=['GET'])
def getCountryinfo_deprecated(indexName):
    return getCountryinfo(indexName)

@app.route('/marketinfo/api/countryinfo/<string:indexName>', methods=['GET'])
def getCountryinfo(indexName):
    start_ts = datetimeManager().getTimeStamp()
    if cm.cacheAvailable(start_ts, request.path):
        data = cm.getCache(start_ts, request.path)
        return Response(data, status=200, mimetype='application/json')
    responseText = requestsManager().getCountryinfo(indexName)
    data = parseManager().parseCountryinfo(start_ts, indexName, responseText)
    cm.saveCache(request.path, data)
    return Response(data, status=200, mimetype='application/json')

# ////////////////////////////////////////////////////////////////////////////////////////
# 请求指数历史数据
# ////////////////////////////////////////////////////////////////////////////////////////

@app.route('/api/indexhistory/<string:indexName>', methods=['GET'])
def getIndexHistory_deprecated(indexName):
    return getIndexHistory(indexName)

@app.route('/marketinfo/api/indexhistory/<string:indexName>', methods=['GET'])
def getIndexHistory(indexName):
    start_ts = datetimeManager().getTimeStamp()
    if cm.cacheAvailable(start_ts, request.path):
        data = cm.getCache(start_ts, request.path)
        return Response(data, status=200, mimetype='application/json')
    responseText = requestsManager().getIndexHistory(indexName)
    data = parseManager().parseIndexHistory(start_ts, indexName, responseText)
    cm.saveCache(request.path, data)
    return Response(data, status=200, mimetype='application/json')

# ////////////////////////////////////////////////////////////////////////////////////////
# 是否工作日
# ////////////////////////////////////////////////////////////////////////////////////////

@app.route('/api/today', methods=['GET'])
def dayType_deprecated():
    return dayType()

@app.route('/marketinfo/api/today', methods=['GET'])
def dayType():
    start_ts = datetimeManager().getTimeStamp()
    if cm.cacheAvailable(start_ts, request.path):
        data = cm.getCache(start_ts, request.path)
        return Response(data, status=200, mimetype='application/json')
    responseText = requestsManager().getDayType()
    data = parseManager().parseDayType(start_ts, responseText)
    cm.saveCache(request.path, data)
    return Response(data, status=200, mimetype='application/json')

# debug
if __name__ == '__main__':
    app.run(port=5000, debug=True)