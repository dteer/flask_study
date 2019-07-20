# SQLAlchemy

## sqlalchemy基础配置

* 配置文件及运行

  * ```python
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column
    from sqlalchemy import *
    
    Base = declarative_base()
    
    #创建表结构
    class Users(Base):
        __tablename__ = 'users'
        id = Column(Integer,primary_key=True)
        name = Column(String(32),index=True,nullable=False)
    #配置文件
    from sqlalchemy import 
    create_engineengine = create_engine(    'mysql+pymysql://root:123456@127.0.0.1:3306/sqlalchemy?charset=utf8',    max_overflow = 0,       #超过连接池大小外，最多创建的链接    
     pool_size = 5,          #连接池大小    
     pool_timeout = 30,      #池中没有线程最多等待的时间，否则报错    
     pool_recycle = -1,       #多久之后对线程中的线程进行一次连接回收（重置）)
    
    #创建数据表
    Base.metadata.create_all(engine)		
    ```