

说明：

sql 这个模块并非是 server 端代码。而是自行整理的国家信息（country_info）与指数历史数据（index_history），这些内容是生成 MySQL 数据库的原始信息。

1. 国家信息和指数历史数据先各自拿到原始信息。（index_history_spider.py 去东方财富，回来生成 index_history.txt，这个后续会被 db_helper 按顺序读入内存并写入对应的数据库条目，country_info_baidu_helper 去百度遍历提取，生成文件，逐一手工更新后续提到的 xlsx 文件）。
2. 手工把数据填写到对应的 xlsx 文件里面。
3. 把 xlsx 内容复制粘贴到 csv。（这一步需要“国家信息”注意把全局逗号替换为空，防止数据库不认识。“指数信息”不需要，因为历史数据是 py 脚本操作 txt 文件直接插入数据库的），国家信息中，大陆，香港，美国由于监控了多只指数，所以结构是“指数1-指数2-指数3”这样用短横线分割。指数历史信息也采用了类似的方式，其结构是（2012,open,close-2013,open,close...）
4. *_db_helper.py 是把 *.csv 文件插入到云端数据库表的脚本。记得插入之前，云端需要 truncated 一下对应的 table 以免因为 unique key 导致操作失败。
5. finance.sql 是初版本数据库的一个备份。