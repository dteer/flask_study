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


#连表查询
class Link_find():
    #1.查询所有用户+所属部门名称    ===> inner join
    def link_table(self):
        res = session.query(User.id,User.name,Depart.title).join(Depart,User.depart_id==Depart.id).all()
        print(res)
        for row in res:
            print(row.id,row.name,row.title)

    #2.查询所有用户+所属部门名称    ===> left join
    def link_table2(self):
        res = session.query(User.id,User.name,Depart.title).join(Depart,User.depart_id==Depart.id,isouter=True).all()
        print(res)
        for row in res:
            print(row.id,row.name,row.title)

    #对于relationship字段跨表操作  =====》正向
    def rela_table1(self):
        res = session.query(User).all()
        for row in res:
            print(row.id,row.name,row.dp.title)

    #对于relationship字段跨表操作  =====》反向
    def rela_table2(self):
        res = session.query(Depart).filter(Depart.title == '软件部').first()
        for row in res.pers:
            print(row.id, row.name, res.title)

#连表创建
class Link_add():

    #需求一：IT部门，在该部门中添加员工：天收

    #方式一
    def link_add1(self):
        d1 = Depart(title='IT')
        session.add(d1)
        session.commit()

        u1 = User(name='天收',depart_id=d1.id)
        session.add(u1)
        session.commit()

    # 方式二       ====> 关联relationship
    def link_add2(self):
        u1 = User(name='天收',dp=Depart(title='IT'))
        session.add(u1)
        session.commit()

    #需求二：创建部门：王者荣耀，在该部门添加员工：A/B/C

    #方式一        ====> 关联relationship
    def link_Madd1(self):
        session.add_all([
            User(name='A',dp=Depart(title='王者荣耀')),
            User(name='B',dp=Depart(title='王者荣耀')),
            User(name='C',dp=Depart(title='王者荣耀')),
        ])

    #方式二    ====> 关联relationship
    def link_Madd2(self):
        d1 = Depart(title='王者荣耀')
        d1.pers = [User(name='A'),User(name='B'),User(name='C')]
        session.add(d1)
        session.commit()

session.close()