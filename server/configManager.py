# -*- coding: utf-8 -*-

class configManager:
    # 是否采用测试服务器
    isDebug = False

    def __init__(self):
        super().__init__()
        self.server_url = ''
        if self.isDebug:
            self.server_url = 'http://127.0.0.1:5000/'
        else:
            self.server_url = 'http://112.125.25.230/'
        # 反射机制信息注册（方便并发接口解耦）
        self.moneyinfo = [
            {'name' : '沪深成交', 'symbol' : 'hslscje', 'url' : 'https://push2.eastmoney.com/api/qt/ulist.np/get?cb=callback&fltt=2&secids=1.000002%2C0.399107&fields=f1%2Cf2%2Cf3%2Cf4%2Cf6%2Cf12%2Cf13%2Cf104%2Cf105%2Cf106'},
            {'name' : '融资融券', 'symbol' : 'rzrqye', 'url' : 'http://datacenter.eastmoney.com/api/data/get?type=RPTA_RZRQ_LSHJ&sty=ALL&source=WEB&st=DIM_DATE&sr=-1&p=1&ps=240&callback=cb'},
            {'name' : '沪深资金', 'symbol' : 'hszjjlr', 'url' : 'http://push2.eastmoney.com/api/qt/stock/fflow/kline/get?lmt=0&klt=1&secid=1.000001&secid2=0.399001&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63&cb=updateMoneyFlow', 'parser' : ''},
            {'name' : '沪港通深港通资金情况', 'symbol' : 'hgtsgtzjqk', 'url' : 'http://push2.eastmoney.com/api/qt/kamt.rtmin/get?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55,f56&cb=updateHKMoneyFlow'},
            {'name' : '行业资金净流入（亿）', 'symbol' : 'hyzjjlr', 'url' : 'http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=500&fields=f12,f14,f62&fid=f62&fs=m:90+t:2&cb=callback'}
        ]

        self.zdpinfo = [
            {'name' : '涨跌分布与涨跌停', 'symbol' : 'zdfb_zdt', 'url' : 'http://push2ex.eastmoney.com/getTopicZDFenBu?cb=callback&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wz.ztzt'},
            {'name' : '指数涨跌平', 'symbol' : 'zszdp', 'url' : 'https://push2.eastmoney.com/api/qt/ulist.np/get?cb=callback&fltt=2&secids=1.000002,0.399107,1.000003,0.399108,0.399102,1.000016,1.000300,0.399905,1.000852&fields=f2%2Cf12%2Cf14%2Cf104%2Cf105%2Cf106'},
        ]

        self.goods_and_exchanges = [
            {'name' : '期货和汇率', 'symbol' : 'goods_and_exchanges', 'url' : 'http://65.push2.eastmoney.com/api/qt/clist/get?cb=callback&pn=1&pz=20&po=0&np=1&fltt=2&invt=2&fid=f14&fs=i:104.CN00Y,i:159.IHFI,i:159.IFFI,i:159.ICFI,i:134.HSI_M,i:134.HSIM2,i:134.HSIU2,i:134.HSIZ2,i:101.GC00Y,i:101.SI00Y,i:102.CL00Y,i:133.USDCNH,i:120.USDCNYC,i:120.CADCNYC,i:120.GBPCNYC,i:120.EURCNYC,i:120.AUDCNYC,i:120.HKDCNYC,i:120.JPYCNYC,i:120.CNYKRWC&fields=f2,f3,f4,f12,f13,f14,f18'}
        ]

        self.bondinfo = [
            {'name' : '国债', 'symbol' : 'bond', 'url' : 'http://yield.chinabond.com.cn/cbweb-czb-web/czb/czbChartSearch'},
            {'name' : '货币基金', 'symbol' : 'fund', 'url' : 'https://danjuanapp.com/djapi/fund/003474'},
            {'name' : '混合债券', 'symbol' : 'plan', 'url' : 'https://danjuanapp.com/djapi/plan/CSI1021'},
            {'name' : '混合债券', 'symbol' : 'plan', 'url' : 'https://danjuanapp.com/djapi/plan/CSI1014'},
            {'name' : '混合债券', 'symbol' : 'plan', 'url' : 'https://danjuanapp.com/djapi/plan/CSI1019'},
        ]

        # {'name' : '', 'symbol' : '', 'url' : ''},