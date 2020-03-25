# -*- coding: utf-8 -*-

class countryInfoModel:
    """
    国情
    """

    def __init__(self, data=None):
        country_info_model_keys = ['id','country','countryCode','capital','tradingMarket','marketCode','indexName','indexCode','continent','timezone','dealTime','breakTime','population','area','gdpRMB','gdpPersonAvg','inlandCurrency','inlandCurrencyCode','summerTime']
        self.id = 0
        self.country = u'中国大陆'
        self.countryCode = u'CN'
        self.capital = u'北京'
        self.tradingMarket = u'上海证券交易所'
        self.marketCode = u'SSE'
        self.indexName = u'上证指数'
        self.indexCode = u'0000001'
        self.continent = u'亚洲'
        self.timezone = u'UTC+8'
        self.dealTime = '09:25-15:00'
        self.breakTime = '11:30-13:00'        
        self.population = 1400000000
        self.area = 9600000  # 单位：平方公里
        self.gdpRMB = 99086500000000  # 单位：元
        self.gdpPersonAvg = 70776.07    # 单位：元
        self.inlandCurrency = '人民币'
        self.inlandCurrencyCode = 'CNY'
        self.summerTime = 'NA'

        if data:
            self.__dict__ = data

    def __str__(self):
        """
        输出对象
        """
        return str(self.__dict__)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)
