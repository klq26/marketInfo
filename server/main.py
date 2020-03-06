# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import Response

from cacheManager import cacheManager
from requestManager import requestsManager
from parseManager import parseManager
from datetimeManager import datetimeManager

app = Flask(__name__)

cm = cacheManager()

# ////////////////////////////////////////////////////////////////////////////////////////
# 请求资金数据（两市成交额，融资融券，两市资金净流入，沪港通，沪深通净流入，板块资金）
# ////////////////////////////////////////////////////////////////////////////////////////

@app.route('/api/moneyinfo', methods=['GET'])
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
# 请求指数数据 china asian euro america
# ////////////////////////////////////////////////////////////////////////////////////////
@app.route('/api/indexs/<string:area>', methods=['GET'])
def getIndexInfos(area):
    start_ts = datetimeManager().getTimeStamp()
    if cm.cacheAvailable(start_ts, request.path):
        data = cm.getCache(start_ts, request.path)
        return Response(data, status=200, mimetype='application/json')
    responseText = requestsManager().getIndexInfos(area)
    data = parseManager().parseIndexInfos(start_ts, area, responseText)
    cm.saveCache(request.path, data)
    return Response(data, status=200, mimetype='application/json')

# ////////////////////////////////////////////////////////////////////////////////////////
# 请求期货&外汇数据
# ////////////////////////////////////////////////////////////////////////////////////////

@app.route('/api/goods_and_exchanges', methods=['GET'])
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
# 是否工作日
# ////////////////////////////////////////////////////////////////////////////////////////

@app.route('/api/today', methods=['GET'])
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