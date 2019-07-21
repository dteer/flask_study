from models import Student
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker  # 单线程版
from sqlalchemy.orm import scoped_session  # 多线程版
from threading import Thread

# 数据库连接
engine = create_engine(
    'mysql+pymysql://root:123456@127.0.0.1:3306/sqlalchemy?charset=utf8',
    max_overflow=0,  # 超过连接池大小外，最多创建的链接
    pool_size=5,  # 连接池大小
    pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
    pool_recycle=-1,  # 多久之后对线程中的线程进行一次连接回收（重置）
)

"""
注意点：session = SessionFactory()
 代表从连接池获取一个连接，如果作为全局变量，无法实现多线程连接
"""


# 方式一：使用session = SessionFactory()
class Link_1():
    SessionFactory = sessionmaker(bind=engine)

    def task(self):
        # 去连接池中获取一个连接
        session = self.SessionFactory()
        res = session.query(Student).all()
        print(res)
        # 将连接交给连接池
        session.close()

    def run(self):
        for i in range(20):
            t = Thread(target=self.task)
            t.start()


# 方式二：使用session = scoped_session(SessionFactory)
class Link_2():
    SessionFactory = sessionmaker(bind=engine)
    # 内部用thearding.local()实现多线程,原理如一
    session = scoped_session(SessionFactory)

    def task(self):
        res = self.session.query(Student).all()
        print(res)
        # 将连接交给连接池
        self.session.remove()

    def run(self):
        for i in range(20):
            t = Thread(target=self.task)
            t.start()
