# -*- coding: utf-8 -*-

class configManager:

    def __init__(self):
        super().__init__()
        self.server_url = 'http://112.125.25.230/'
        # 反射机制信息注册
        self.moneyinfo = [
            {'name' : '沪深两市成交额（亿）', 'symbol' : 'hslscje', 'url' : 'https://hq.sinajs.cn/?list=sh000002,sz399107', 'requester' : '', 'parser' : ''},
            {'name' : '融资融券余额（亿）', 'symbol' : 'rzrqye', 'url' : 'http://api.dataide.eastmoney.com/data/get_rzrq_lshj?orderby=dim_date&order=desc&pageindex=1&pagesize=240', 'requester' : '', 'parser' : ''},
            {'name' : '沪深资金净流入（亿）', 'symbol' : 'hszjjlr', 'url' : 'http://push2.eastmoney.com/api/qt/stock/fflow/kline/get?lmt=0&klt=1&secid=1.000001&secid2=0.399001&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63&cb=updateMoneyFlow', 'parser' : ''},
            {'name' : '沪港通深港通资金情况', 'symbol' : 'hgtsgtzjqk', 'url' : 'http://push2.eastmoney.com/api/qt/kamt.rtmin/get?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55,f56&cb=updateHKMoneyFlow', 'requester' : '', 'parser' : ''},
            {'name' : '行业资金净流入（亿）', 'symbol' : 'hyzjjlr', 'url' : 'http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=500&fields=f12,f14,f62&fid=f62&fs=m:90+t:2&cb=callback', 'requester' : '', 'parser' : ''}
        ]

        self.goods_and_exchanges = [
            {'name' : '离岸人民币', 'symbol' : 'larmb', 'url' : 'http://87.push2.eastmoney.com/api/qt/ulist.np/get?cb=updateIndexInfos&np=1&pi=0&pz=40&po=1&secids=133.USDCNH&fields=f14,f12,f2,f4,f3,f18,f6', 'requester' : '', 'parser' : ''},
            {'name' : '期货和汇率', 'symbol' : 'goods_and_exchanges', 'url' : 'https://hq.sinajs.cn/?list=hf_CHA50CFD,hf_GC,hf_SI,hf_CL,USDCNY,CADCNY,GBPCNY,EURCNY,AUDCNY,HKDCNY,TWDCNY,fx_sjpycny,fx_skrwcny', 'requester' : '', 'parser' : ''}
        ]

        # {'name' : '', 'symbol' : '', 'url' : '', 'requester' : '', 'parser' : ''},