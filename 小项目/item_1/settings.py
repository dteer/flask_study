from DBUtils.PooledDB import PooledDB, SharedDBConnection
import pymysql

POOL = PooledDB(
    creator=pymysql,  # 使用连接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None代表不限制连接数
    mincached=2,  # 初始化时，连接池中至少创建的空闲链接，0代表不创建
    maxcached=5,  # 连接池最多闲置的连接，0和None不限制
    maxshared=3,  # 链接池中最多共享的连接数量，0和None表示全共享，ps：连接模块默认为1，不生效
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待，True等待
    maxusage=None,  # 一个连接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表
    ping=0,  # ping mysql服务端，检查是否服务可用， 0,1,2,3...
    host='127.0.0.1',
    port=3306,
    user='root',
    password='123456',
    database='',
    charset='utf8',
)