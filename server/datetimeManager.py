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
