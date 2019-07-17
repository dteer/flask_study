import pymysql
from settings import POOL

def fetch_all(sql,args):
    conn = POOL.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,args)
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return result

def insert(sql,args):
    conn = POOL.connection()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    row = cursor.execute(sql, args)
    conn.commit()
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return row