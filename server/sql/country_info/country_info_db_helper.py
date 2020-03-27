import os
import sys
import pymysql

# 打开数据库
ip_address = ''
if sys.platform.startswith('win'):
    ip_address = '112.125.25.230'
elif sys.platform.startswith('linux'):
    ip_address = '127.0.0.1'
db = pymysql.connect(ip_address,'klq26','abc123!@#==','finance')
cursor = db.cursor()

# 创建表 SQL 代码
# CREATE TABLE `country_info` (
# 	`id` INT(3) NOT NULL,
# 	`country` VARCHAR(10) NOT NULL COLLATE 'utf8_unicode_ci',
# 	`country_code` VARCHAR(2) NOT NULL COLLATE 'utf8_unicode_ci',
# 	`capital` VARCHAR(10) NOT NULL COLLATE 'utf8_unicode_ci',
# 	`trading_market` VARCHAR(30) NOT NULL COLLATE 'utf8_unicode_ci',
# 	`market_code` VARCHAR(8) NOT NULL COLLATE 'utf8_unicode_ci',
# 	`index_name` VARCHAR(200) NOT NULL COLLATE 'utf8_unicode_ci',
# 	`index_code` VARCHAR(200) NOT NULL COLLATE 'utf8_unicode_ci',
# 	`continent` VARCHAR(4) NOT NULL COLLATE 'utf8_unicode_ci',
# 	`timezone` VARCHAR(6) NOT NULL COLLATE 'utf8_unicode_ci',
# 	`deal_time` VARCHAR(12) NOT NULL COLLATE 'utf8_unicode_ci',
# 	`break_time` VARCHAR(12) NOT NULL COLLATE 'utf8_unicode_ci',
# 	`population` BIGINT(14) NOT NULL,
# 	`population_count_year` INT(4) NOT NULL,
# 	`area` BIGINT(14) NOT NULL,
# 	`gdp` BIGINT(14) NOT NULL,
# 	`gdp_count_year` INT(4) NOT NULL,
# 	`gdp_currency` VARCHAR(4) NOT NULL COLLATE 'utf8_unicode_ci',
# 	`gdp_currency_rate` DOUBLE NULL DEFAULT NULL,
# 	`gdp_person_avg` DOUBLE NULL DEFAULT NULL,
# 	`inland_currency` VARCHAR(12) NOT NULL COLLATE 'utf8_unicode_ci',
# 	`currency_code` VARCHAR(3) NOT NULL COLLATE 'utf8_unicode_ci',
# 	`summer_time` VARCHAR(6) NOT NULL COLLATE 'utf8_unicode_ci',
# 	PRIMARY KEY (`id`),
# 	UNIQUE INDEX `country` (`country`),
# 	UNIQUE INDEX `country_code` (`country_code`)
# )
# COLLATE='utf8_unicode_ci'
# ENGINE=InnoDB;


# 从 countryinfo.csv 中读取数据，插入数据库（如果之前有数据，应该 truncated 一下，把所有数据删除）
with open('countryinfo.csv','r',encoding='utf-8') as f:
    all_values = f.readlines()
    # SQL 字段名
    sql_keys = all_values.pop(0).replace('\n','').split('\t')
    # dict(zip(list1,list2))
    for line in all_values:
        sql_values = line.replace('\n','').split('\t')
        d = dict(zip(sql_keys, sql_values))
        # 查看字典
        print(d)
        # 字段超多时（本例中 22 个字段，用下面方法配合字典插入）
        sql = '''insert into country_info(%s) values (%s)'''
        key_list = []
        value_list= []
        for k, v in d.items():
            key_list.append(k)
            value_list.append('%%(%s)s' % k)
        sql = sql % (','.join(key_list),','.join(value_list))
        cursor.execute(sql, d)
    db.commit()
    cursor.close()
    db.close()