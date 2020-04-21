# -*- coding: utf-8 -*-

import time
from datetime import datetime

class datetimeManager:

    def __init__(self):
        super().__init__()

    def getTimeStamp(self):
        return time.time()

    def getTimeStampFromString(self, dateString):
        timeFormat = '%Y/%m/%d %H:%M:%S'
        return datetime.strptime(dateString, timeFormat).timestamp()

    def getDateString(self, sep=''):
        today = time.strftime('%Y' + sep + '%m' + sep + '%d', time.localtime())
        return today

    def getDateTimeString(self):
        ts = self.getTimeStamp()
        timeFormat = '%Y/%m/%d %H:%M:%S'
        timeString = time.strftime(timeFormat, time.localtime(ts))
        return timeString
    
    def getDuration(self, start_ts, end_ts):
        duration = round(end_ts - start_ts, 4)
        return duration

    def isWeekday(self):
        """
        是否是周一至周五
        """
        today = datetime.now()
        dayOfWeek = today.isoweekday()
        # 只有周一至周五
        return dayOfWeek >=1 and dayOfWeek <= 5

    def isHoliday(self):
        """
        判断今天是否是法定假日，即虽然是周一至周五，但是不开盘。这个函数一年更新一次就行了。
        """
        now = datetime.now()
        dateStr = datetime.now().strftime('%Y%m%d')
        year = now.year
        print(now.month, now.day)
        # if now.month == 1 and now.day == 1:
            # 元旦发邮件，提醒更新函数
            # self.sendMessage(title = '新年注意更新 gridTradeMonitor 项目的 isHoliday 函数之假期数组', msg='今年是 {0} 年，请更新 isHoliday 函数，祝今年投资成功！'.format(year))
        holidays = []
        # 5.1 - 5.5 劳动节
        [holidays.append('{0}050{1}'.format(year, x)) for x in range(1, 6)]
        # 6.25 - 6.27 劳动节
        [holidays.append('{0}06{1}'.format(year, x)) for x in range(25, 28)]
        # 10.1 - 10.8 国庆节、中秋节
        [holidays.append('{0}100{1}'.format(year, x)) for x in range(1, 9)]
        return dateStr in holidays