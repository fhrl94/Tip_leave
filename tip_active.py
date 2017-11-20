import configparser
import os
import platform

from leave_stone import stoneobject
from mylogger import Logger
from proxy_query import ProxyQuery
from web import Web

if __name__ == '__main__':
    # 记录器 实例
    logname = "金蝶消息提醒"
    log = Logger(logname)
    logger = log.getlogger()
    # 解析器实例
    conf = configparser.ConfigParser()
    path = 'leave.conf'
    assert os.path.exists(path), "{file}不存在".format(file=path)
    if platform.system() == 'Windows':
        conf.read(path, encoding="utf-8-sig")
    else:
        conf.read(path)
    # 数据库实例
    stone = stoneobject()
    # # 服务器实例
    # server = ServerQuery(conf=conf, stone=stone, logger=logger)
    # # 查询
    # string = server.run(str('0201705003'))
    # 解析
    # list = json.loads(string)
    # print(list)
    proxy_query = ProxyQuery(conf=conf, stone=stone, logger=logger)
    web = Web(proxy_handle=proxy_query, logger=logger, port=int(conf.get('web', 'port')))
    web.get_web_install()

    pass
