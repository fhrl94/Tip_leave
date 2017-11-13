import json
import pymssql

from leave_stone import Emp_Info
from query import Query


class ServerQuery(Query):

    def __init__(self, conf, stone, logger):
        """
        初始化
        """
        self._conf = conf
        self._stone = stone
        self._logger = logger
        self._conn = pymssql.connect(self._conf.get('server', 'ip'), self._conf.get('server', 'user'),
                                     self._conf.get('server', 'password'), database=self._conf.get('server', 'database'))
        self._cur = self._conn.cursor()
        self._code = None
        self._uid = None
        self._logger.info("初始化人员信息")
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
        self._logger.debug("查询开始")
        # TODO 新消息查询，待修改
        sql = """
        select top 100 RecieverID,SenderID,Subject,MsgType,RecDate,ReadDate,IsRead,IsDeal,SourceID
        from MS_Message 
        where MsgType = 1 and IsDeal = 0 and RecieverID = '{uid}'
        """.format(uid=self._uid)
        self._cur.execute(sql)
        # emp_cols = ('receiver_id', 'sender_id', 'subject', 'message_type', 'receive_date', 'read_date', 'is_read',
        #             'is_deal', 'flow_object_id', )
        # for one in self._cur.fetchall():
        #     msg_info = Message_primitive()
        #     for count, col in enumerate(emp_cols):
        #         if col in ('receiver_id', 'sender_id', 'flow_object_id', ):
        #             setattr(msg_info, col, str(one[count]))
        #         else:
        #             setattr(msg_info, col, one[count])
        #     self._stone.add(msg_info)
        # self._stone.commit()
        self.result = self._cur.fetchall()
        self._logger.debug("查询完成")
        pass

    def run(self, code):
        """
        如果 self._code 为空,报错
        每次运行时，先通过 _get_query_uid() 将 code 转换为 Uid
        通过调用 _get_data() 查询金蝶数据库中 msg 前100条
        # 调用 _transform() 转换为可阅读文本 （将所有的 Uid 转换为 name、code）
        然后返回数据 dict
        将 self._code 置空
        :return:
        """
        self.code = code
        self._get_query_uid()
        self._get_data()
        if self.result:
            print(self._get_msg_json())
            return self._get_msg_json()
        pass

    def _get_msg_json(self):
        """
        将 self.result 中的 subject(3)，receive_date(5) 以json数据格式返回
        :return:
        """
        result = []
        for one in self.result:
            temp = {"subject": one[2], "receive_date": one[4].strftime('%Y-%m-%d %H:%M:%S'), }
            # print(temp)
            result.append(temp)
        return json.dumps(result)
        pass

    def _get_query_uid(self):
        """
        _get_data() 调用前置,将code 转换为 self._uid
        :return:
        """
        uid = self._stone.query(Emp_Info.uid).filter(Emp_Info.code == self.code).one_or_none()
        if uid is None:
            self._get_emp()
            uid = self._stone.query(Emp_Info).filter(Emp_Info.code == self.code).one_or_none()
            try:
                assert uid is not None, "UID获取错误"
            except AssertionError:
                self._logger.warning("UID获取错误,工号是{code}".format(code=self.code))
                raise TypeError("无此工号")
        self._logger.debug("查询的工号是{code},uid 为{uid}".format(code=self.code, uid=list(uid)[0]))
        self._uid = list(uid)[0]
        pass

    def _get_emp(self):
        """
        获取金蝶系统中所有人员的 Uid、code、emp_id、name，存储至数据库
        :return:
        """
        self._stone.query(Emp_Info).delete()
        self._stone.commit()
        sql = """
                select hbu.ID, hbu.Account, hbu.FEmpID,he.Name
                from HR_Base_User as hbu
                join HM_Employees as he on hbu.FEmpID = he.EM_ID
                where Deleted = 0  
                order by FUserID
                """
        self._cur.execute(sql)
        emp_cols = ('uid', 'code', 'em_id', 'name',)
        for one in self._cur.fetchall():
            empinfo = Emp_Info()
            for count, col in enumerate(emp_cols):
                if col in ('uid', 'em_id', ):
                    setattr(empinfo, col, str(one[count]))
                else:
                    setattr(empinfo, col, one[count])
            self._stone.add(empinfo)
        self._stone.commit()
        pass

    @property
    def code(self):
        return self._code


    @code.setter
    def code(self, code):
        try:
            assert len(code) == 10 and isinstance(code, str), "输入工号错误"
        except AssertionError:
            self._logger.info("工号输入错误{code}".format(code=code))
            raise TypeError("无此工号")
        self._code = str(code)

