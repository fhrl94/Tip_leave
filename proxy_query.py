
from query import Query
from server_query import ServerQuery


class ProxyQuery(Query):
    def __init__(self, conf, stone, logger):
        """

        """
        # TODO 后期涉及到多进程
        self.server_query = ServerQuery(conf=conf, stone=stone, logger=logger)

        pass

    def _get_data(self, code):
        """

        :return:
        """
        # TODO 异常处理
        self.query = self.server_query.run(code)
        pass

    def run(self):
        """
        将 self.query 转换为 json
        :return:
        """

        pass

    pass
