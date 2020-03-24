# -*- coding: utf-8 -*-


class indexHistoryModel:
    """
    指数年K
    """

    def __init__(self, data=None):
        self.id = 0
        self.country = u'中国大陆'
        self.countryCode = u'CN'
        self.continent = u'亚洲'
        self.indexName = u'上证指数'
        self.indexCode = u'000001'
        self.indexHistory = u'2020,1000,1500'

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
