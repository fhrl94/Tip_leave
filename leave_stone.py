# 导入:
import sqlite3

import sys
from sqlalchemy import Column, create_engine, Date, String, Integer, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

cx = sqlite3.connect(sys.path[0] + "/emp.sqlite3")
engine = create_engine("sqlite:///" + sys.path[0] + "/emp.sqlite3", echo=True)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# 创建对象的基类:
Base = declarative_base()
# 连接数据库
session = DBSession()


# class MessageInfo(Base):
#     """
#     消息表：
#     表结构：
#     工号、接受人姓名、发送人姓名、主题、消息类型（区分是否是流程）、
#     接受时间、阅读时间、是否阅读、是否处理、流程对象姓名
#     """
#     # 表的名字:
#     __tablename__ = 'MessageInfo'
#
#     # 表的结构:
#     id = Column(Integer(), primary_key=True)
#     receiver_code = Column(String(10))
#     receiver_name = Column(String(10))
#     sender_name = Column(String(10))
#     subject = Column(String(200))
#     message_type = Column(Integer())
#     receive_date = Column(Date())
#     read_date = Column(Date())
#     is_read = Column(Boolean())
#     is_deal = Column(Boolean())
#     flow_object_name = Column(String(10))
#
#
#     def __str__(self):
#         return self.id


class User_info(Base):
    # 表的名字:
    __tablename__ = 'User_info'

    # 表的结构:
    id = Column(Integer(), primary_key=True)
    code = Column(String(10))
    ip_address = Column(String(16))
    on_status = Column(Boolean())
    # TODO 动态密码，适用于短信获取
    # password = Column(String(6))
    # TODO 手机号码
    # Tel = Column(String(11))
    # TODO 计算机名称


    def __str__(self):
        return self.id

class Message_primitive(Base):

    # 表的名字:
    __tablename__ = 'Message_primitive'

    # 表的结构:
    id = Column(Integer(), primary_key=True)
    receiver_id = Column(String(36))
    sender_id = Column(String(36))
    subject = Column(String(200))
    message_type = Column(Integer())
    receive_date = Column(Date())
    read_date = Column(Date())
    is_read = Column(Boolean())
    is_deal = Column(Boolean())
    flow_object_id = Column(String(36))


    def __str__(self):
        return self.id

class Emp_Info(Base):
    """
    全局id、工号、empty_id、名称
    """
    # 表的名字:
    __tablename__ = 'Emp_Info'

    # 表的结构:
    id = Column(Integer(), primary_key=True)
    uid = Column(String(36))
    code = Column(String(10))
    em_id = Column(String(36))
    name = Column(String(10))

    def __str__(self):
        return self.id
# 如果没有创建表，则创建
Base.metadata.create_all(engine)


def stoneobject():
    return session
