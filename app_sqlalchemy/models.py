from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

Base = declarative_base()

#事例一：用于单表操作
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    name = Column(String(32),index=True,nullable=False)


#事例二：外键操作

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True)
    name = Column(String(32),index=True,nullable=False)
    depart_id = Column(Integer,ForeignKey('depart.id'))     #depart表名

    #只在程序上作两表关联，用于查询：具体看rela_table3
    dp = relationship('Depart',backref='pers')

class Depart(Base):
    __tablename__ = 'depart'
    id = Column(Integer,primary_key=True)
    title = Column(String(32),index=True,nullable=False)


#事例三：多对多

class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer,primary_key=True)
    name = Column(String(32),index=True,nullable=False)

    #关联其他表
    course_list = relationship('Course',secondary = 'student2course',backref='student_list')

class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer,primary_key=True)
    title = Column(String(32),index=True,nullable=False)

class Student2Course(Base):
    __tablename__ = 'student2course'
    id = Column(Integer,primary_key=True,autoincrement=True)
    student_id = Column(Integer,ForeignKey('student.id'))
    course_id = Column(Integer,ForeignKey('course.id'))

    #联合唯一索引
    __table_args__ = (
        UniqueConstraint('student_id','course_id',name='uix_stu_cou'),
        #Index('ix_stu_cou','name','extra'),        联合索引
    )

#对数据表操作
def create_all():
    engine = create_engine(
        'mysql+pymysql://root:123456@127.0.0.1:3306/sqlalchemy?charset=utf8',
        max_overflow = 0,       #超过连接池大小外，最多创建的链接
        pool_size = 5,          #连接池大小
        pool_timeout = 30,      #池中没有线程最多等待的时间，否则报错
        pool_recycle = -1,       #多久之后对线程中的线程进行一次连接回收（重置）
    )
    Base.metadata.create_all(engine)

def drop_all():
    engine = create_engine(
        'mysql+pymysql://root:123456@127.0.0.1:3306/sqlalchemy?charset=utf8',
        max_overflow=0,  # 超过连接池大小外，最多创建的链接
        pool_size=5,  # 连接池大小
        pool_timeout=30,  # 池中没有线程最多等待的时间，否则报错
        pool_recycle=-1,  # 多久之后对线程中的线程进行一次连接回收（重置）
    )
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    create_all()