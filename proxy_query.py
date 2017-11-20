from leave_stone import UserInfo
from query import Query
from server_query import ServerQuery


class ProxyQuery(Query):
    def __init__(self, conf, stone, logger):
        """

        """
        # TODO 后期涉及到线程池 or 队列（优化反应速度）
        self.stone = stone
        self.logger = logger
        self.server_query = ServerQuery(conf=conf, stone=stone, logger=logger)

        pass

    def run(self, code=None, ip_addr=None):
        """
        将 self.query 转换为 json
        :return:
        """
        if code is None or ip_addr is None:
            raise UserWarning("请输入工号和ip地址")
        self._security_check(code=code, ip_addr=ip_addr)
        self._get_data(code=code)
        return self.query

        pass

    def _get_data(self, code=None):
        """

        :return:
        """
        # TODO 异常处理
        if code is None:
            raise UserWarning("请输入工号")
        self.query = self.server_query.run(code)
        pass

    def _security_check(self, ip_addr, code):
        """
        查询是否存在 code ，如果不存在则将（code、ip_addr）写入数据库
        存在则比对 ip_addr ，不一致则将状态改为锁死
        读取客户端IP ，存储到数据库中
        :return:
        """
        self.code = code
        result = self.stone.query(UserInfo).filter(UserInfo.code == self.code).one_or_none()
        # 不存在则创建
        if result is None:
            user_info = UserInfo()
            user_info.code = self.code
            user_info.ip_address = ip_addr
            user_info.on_status = True
            self.stone.add(user_info)
            self.stone.commit()
        else:
            # 存在则比对 ip_addr 存储是否一致
            if result.ip_address != ip_addr:
                result.on_status = False
                self.stone.commit()
            # 存在且查询状态不为 True ，抛出异常
            if not result.on_status:
                raise UserWarning("账号锁定，请与管理员联系")
        pass

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        try:
            assert len(code) == 10 and isinstance(code, str), "输入工号错误"
        except AssertionError:
            self.logger.info("工号输入错误{code}".format(code=code))
            raise UserWarning("无此工号")
        self._code = str(code)

    pass
