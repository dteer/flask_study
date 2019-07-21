from models import User,Depart
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#数据库连接
engine = create_engine(
        'mysql+pymysql://root:123456@127.0.0.1:3306/sqlalchemy?charset=utf8',
        max_overflow = 0,       #超过连接池大小外，最多创建的链接
        pool_size = 5,          #连接池大小
        pool_timeout = 30,      #池中没有线程最多等待的时间，否则报错
        pool_recycle = -1,       #多久之后对线程中的线程进行一次连接回收（重置）
    )
SessionFactory = sessionmaker(bind=engine)
session = SessionFactory()


#方式一
def one():
    cursor = session.execute('INSERT INTO users(name) VALUES(:value)',params={'value':'瑞思'})
    session.commit()
    session.close()


#方式二
def two():
    conn = engine.raw_connection()
    cursor = conn.cursor()
    cursor.execute("select * from t1")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
















