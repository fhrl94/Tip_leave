from query import Query


class ServerQuery(Query):

    def __init__(self):
        """
        初始化
        """
        self._get_emp()

        pass


    # def _transform(self):
    #     """
    #     将查询的结果进行转换
    #     :return:
    #     """
    #     pass

    def _get_data(self):
        """
        通过工号查询未阅读的消息，并将数据存储
        :return:
        """
        pass

    def run(self):
        """
        如果 self._code 为空,报错
        每次运行时，先通过 _get_query_uid() 将 code 转换为 Uid
        通过调用 _get_data() 查询金蝶数据库中 msg 前50条
        # 调用 _transform() 转换为可阅读文本 （将所有的 Uid 转换为 name、code）
        然后返回数据 dict
        将 self._code 置空
        :return:
        """


        pass
    #
    # def _get_emp_info(self):
    #     """
    #     _transform() 调用前置，将 _get_data() 获取的数据转换
    #     通过 Uid 转 code、name
    #     :return:
    #     """
    #     pass

    def _get_query_uid(self):
        """
        _get_data() 调用前置,将code 转换为 Uid
        :return:
        """
        pass

    def _get_emp(self):
        """
        获取金蝶系统中所有人员的 Uid、code、emp_id、name，存储至数据库
        :return:
        """
        pass

    @property
    def code(self):
        return self._code


    @code.setter
    def code(self, code):
        assert len(code) == 10 and isinstance(code, str), "输入工号错误"
        self._code = code