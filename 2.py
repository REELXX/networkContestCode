#导入sqllite3模块
import sqlite3

# 1.硬盘上创建连接
con = sqlite3.connect('db.sqlite3')
# 获取cursor对象
cur = con.cursor()
# 执行sql创建表
sql = 'select * from Home_userinfo'
try:
    cur.execute(sql)
    # 获取所有数据
    person_all = cur.fetchall()
    # print(person_all)
    # 遍历
    for p in person_all:
        print(p)


except Exception as e:
    print(e)
    print('查询失败')
finally:
    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()
