requestManager 负责所有的接口请求。
parseManager 负责所有的 response 解析并返回 json 数据。
cacheManager 负责决定哪些接口需要进行缓存以及缓存多久等策略。
configManager 负责确定一些便于迁移的配置，例如阿里云服务器地址（三年后到期等因素）。
dateManager 负责处理时间戳相关的功能。
indexModel 是指数型数据的公共模型，方便客户端渲染。
main 是 uwsgi application 主入口，应该是很轻量级的文件。