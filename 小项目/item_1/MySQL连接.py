import pymysql

conn = pymysql.Connect(host='127.0.0.1',user='',password='',database='',charset='utf8')
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

#方式一：
# cursor.execute('select * from userinfo where user=%s and pwd=%s',('小明','ghjkhjkjk'))
#方式二：
cursor.execute('select * from userinfo where user=%(us)s and pwd=%(pw)s',('小明','ghjkhjkjk'))

data = cursor.fetchone()
cursor.close()
