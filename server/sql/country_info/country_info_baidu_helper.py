import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from lxml import etree

# 请求 header
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'accept-encoding': 'gzip, deflate, br'}


countrys = ['中国','香港','台湾','日本','韩国','新加坡','印度','马来西亚','泰国','菲律宾','巴基斯坦','越南','印尼','斯里兰卡','奥地利','英国','希腊','法国','比利时','捷克','爱尔兰','德国','俄罗斯','荷兰','葡萄牙','意大利','冰岛','芬兰','挪威','西班牙','丹麦','波兰','瑞士','瑞典','巴西','墨西哥','加拿大','美国','新西兰','澳大利亚']
categorys = ['首都','时区','人口','面积','gdp','货币']
urls_prefix = u'https://www.baidu.com/s?wd='

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

country_count = 0
country_total = len(countrys)

# 从百度搜索 40 个国家及地区的 6 个分类数据，解析返回结果页的第一条回答，存入下面文件
with open('countryinfo.txt','w+',encoding='utf-8') as f:
    for country in countrys:
        for category in categorys:
            url = urls_prefix + country + category
            response = requests.get(url, headers=header, verify=False)
            if response.status_code == 200 and len(response.text) > 0:
                soup = BeautifulSoup(response.text, 'lxml')
                elements = soup.find_all(
                    'div', attrs={'class': 'op_exactqa_s_answer'})
                totalCount = len(elements)
                if totalCount > 0:
                    f.write('{0}\t{1}\t{2}'.format(country,category,elements[0].text.replace(' ','').replace('\n','')) + '\n')
                else:
                    f.write('{0}\t{1}\t{2}'.format(country,category,'NA') + '\n')
        country_count = country_count + 1
        print(country_count, ' / ', country_total)
        f.write('\n')

