import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import ssl
import json

index_codes = ['0008321','0000011','3990012','3990062','0000151','0009221','0000161','0003001','3999052','0008521','0008421','3990052','0009911','0009921','3999752','3999862','3998122','3999712','0008271','HSI5','HSCEI5','HSCCI5','TWII_UI','N225_UI','KS11_UI','STI_UI','SENSEX_UI','KLSE_UI','SET_UI','PSI_UI','KSE100_UI','VNINDEX_UI','JKSE_UI','CSEALL_UI','ATX_UI','FTSE_UI','ASE_UI','FCHI_UI','BFX_UI','PX_UI','ISEQ_UI','GDAXI_UI','RTS_UI','AEX_UI','PSI20_UI','MIB_UI','ICEXI_UI','HEX_UI','OSEBX_UI','IBEX_UI','OMXC20_UI','WIG_UI','SSMI_UI','OMXSPI_UI','BVSP_UI','MXX_UI','TSX_UI','DJIA_UI','SPX_UI','NDX_UI','NZ50_UI','AORD_UI']

index_names = ['中证转债','上证指数','深证成指','创业板指','红利指数','中证红利','上证50','沪深300','中证500','中证1000','800等权','中小板指','全指医药','全指金融','证券公司','中证银行','养老产业','中证传媒','中证环保','恒生指数','国企指数','红筹指数','台湾加权','日经225','韩国KOSPI','富时新加坡海峡时报','印度孟买SENSEX','富时马来西亚KLCI','泰国SET','菲律宾马尼拉','巴基斯坦卡拉奇','越南胡志明','印尼雅加达综合','斯里兰卡科伦坡','奥地利ATX','英国富时100','希腊雅典ASE','法国CAC40','比利时BFX','布拉格指数','爱尔兰综合','德国DAX30','俄罗斯RTS','荷兰AEX','葡萄牙PSI20','富时意大利MIB','冰岛ICEX','芬兰赫尔辛基','挪威OSEBX','西班牙IBEX35','OMX哥本哈根20','波兰WIG','瑞士SMI','瑞典OMXSPI','巴西BOVESPA','墨西哥BOLSA','加拿大S&P/TSX','道琼斯','标普500','纳斯达克','新西兰50','澳大利亚普通股']

# 生成 code - name 对字典
params = dict(zip(index_codes, index_names))
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 按照 index_codes names 的顺序从上至下写入独立文件，粘贴到 csv 或 excel 即可
result = []
for fundCode in params.keys():
    print(fundCode)
    url = 'http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id={0}&TYPE=yk'.format(fundCode)
    response = requests.get(url, verify=False)
    dataList = response.text.split('\r\n')
    data = []
    for item in dataList:
        values = str(item).replace('(','').split(',')
        if len(values) < 3:
            continue
        data.append('{0},{1},{2}'.format(values[0][0:4],values[1],values[2]))
    # 只取最后 10 年（含不足 10 年）
    year_count = len(data)
    if year_count >= 10:
        data = data[year_count - 10: year_count]
    # 用分隔符 “-” 分隔
    info = '-'.join(data)
    # print(info)
    result.append(info)

with open('index_history.txt','w+',encoding='utf-8') as f:
    for line in result:
        f.write(line + '\n')