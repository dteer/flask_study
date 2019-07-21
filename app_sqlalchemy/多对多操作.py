from models import Student,Course,Student2Course
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



#创建数据
class Create_data():
    # 创建一个课程，创建2学生，两个学生选新创建的课程
    def create_data1(self):
        obj = Course(title='英语')
        obj.student_list = [
            Student(name='小杰'),
            Student(name='小工'),
        ]
        session.add(obj)
        session.commit()

#查找数据
class Find_data():

    #三表关联
    def find_data(self):
        # join in
        res = session.query(Student2Course.id,Student.name,Course.title).join(Student,Student2Course.id==Student.id).join(Course,Student2Course.course_id==Course.id).order_by(Student2Course.id.asc())

        # left in
        # res = session.query(Student2Course.id,Student.name,Course.title).join(Student,Student2Course.id==Student.id,isouter=True).join(Course,Student2Course.course_id==Course.id,isouter=True)
        for row in res:
            print(row)

    #小东选修的课程       ====》 正向
    def find_data2(self):
        obj = session.query(Student).filter(Student.name=='小东').first()
        for item in obj.course_list:
            print(item.title)
    #选了‘生物’的所有人     ====》反向
    def find_data3(self):
        obj = session.query(Course).filter(Course.title=='生物').first()
        for item in obj.student_list:
            print(item.name)



session.close()








