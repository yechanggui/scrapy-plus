## 关于  

### commmands  
复制scrapy/commands/startproject.py，另存为commands/ruyi.py，增加功能如下：  
- 默认带有result和log目录、.gitignore等
- 集成工具包，包括hz_data_verification.py、run_spider.py等  
- 集成middlewares，包括UserAgentMiddleware，ProxyPoolMiddleware等  
- 集成pipelines，包括MongoDBPipleline  
- 修改settings.py

### templates
新增自定义爬虫模板 templates/spiders/list.tmpl  
后续会继续增加模板，比如table.tmpl

### install.py  
把commmands和templates中的文件copy到scrapy库中

## 安装  
- make install

## 用法   
- scrapy ruyi project_name
- cd project_name
- scrapy genspider -t template spider_name host

## 例子  
- scrapy ruyi example
- cd example
- scrapy genspider -t list example example.com
