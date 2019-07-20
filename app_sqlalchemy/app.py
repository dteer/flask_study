from models import Users
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



#根据Users类对users表进行基本增删改查
class Base_opra():
    #单条增加
    def add_one(self):
        obj = Users(name='alex')
        session.add(obj)
        session.commit()
        session.close()

    #多条增加
    def add_many(self):
        obj1 = Users(name='小明')
        obj2 = Users(name='小米')
        session.add_all([
            obj1,obj2
        ])
        session.commit()

    #查找
    def search(self):
        res = session.query(Users).all()
        for row in res:
            print(row.id,row.name)

    #添加条件查找
    def search_filter(self):
        res = session.query(Users).filter(Users.id > 2)
        for row in res:
            print(row.id,row.name)

    #取有限条数据
    def search_limit(self):
        #obj.first()
        res = session.query(Users).filter(Users.id > 2)[:2]
        for row in res:
            print(row.id,row.name)

    #删除
    def delete(self):
        session.query(Users).filter(Users.id >=3).delete()
        session.commit()

    #改数据库
    def update(self):
        #方式一
        session.query(Users).filter(Users.id ==1).update({'name':'小北'})
        #方式二
        session.query(Users).filter(Users.id ==2).update({Users.name:'东北'})
        #方式三   在原基础上添加内容
        session.query(Users).filter(Users.id ==2).update({'name':Users.name+'正美'},synchronize_session=False)    #默认数值计算
        session.commit()

#sqlalchemy常用操作
class comm_use():

    #根据字段获取数据
    def feild(self):
        res = session.query(Users.id,Users.name).all()
        for item in res:
            print('表现形式(类似元组)：',item,type(item))
            print(item[0],item.name)

    #转换成原生态sql语句
    def sql(self):
        query = session.query(Users.id,Users.name)
        print(query)

    #对字段重命名 as
    def new_feild(self):
        res = session.query(Users.id, Users.name.label('cname'))
        print(res)


#条件查询
def filter():
    # and条件
    session.query(Users).filter(Users.id>1,Users.name =='elix').all()

    #between条件
    session.query(Users).filter(Users.id.between(1,3),Users.name =='elix').all()

    #in条件
    session.query(Users).filter(Users.id.in_([1,3,4])).all()

    #不在in中
    session.query(Users).filter(~Users.id.in_([1,3,4])).all()

    #子查询
    session.query(Users).filter(Users.id.in_(session.query(Users.id).filter(Users.name=='eric'))).all()

    # and 和 or
    from sqlalchemy import and_ , or_
    session.query(Users).filter(and_(Users.id>3,Users.name=='eric')).all()
    session.query(Users).filter(or_(Users.id<3,Users.name=='eric')).all()

    session.query(Users).filter(
        or_(
            Users.id < 2,
            and_(Users.name == 'eric', Users.id > 3),
            Users.extra != ''
        )
    ).all()

    #filter_by
    session.query(Users).filter_by(name='alex').all()

    # 通配符 like
    session.query(Users).filter(~Users.name.like('e%')).all()

    #限制，切片
    session.query(Users)[1:2]