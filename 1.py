import sqlite3

userList = []
passwdList = []
nameAndPasswd = {}
con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
sql = 'select username,email from Home_userinfo'
try:
    # 修改
    a = input("输入姓名")
    b = input("修改邮箱")

    cur.execute('UPDATE Home_userinfo set email=? where username=? ',(b,a))

    # 提交事务
    con.commit()
    print('修改成功')

    cur.execute(sql)
    # 获取所有数据
    person_all = cur.fetchall()
    # print(person_all)
    # 遍历
    for p in person_all:
        peopleInfo = {p[0]: p[1]}
        nameAndPasswd.update(peopleInfo)
        # userList.append(p[0])
        # passwdList.append(p[1])
        # print(p)
except Exception as e:
    print(e)
    print('查询失败')
finally:
    # 关闭游标
    cur.close()
    # 关闭连接
    con.close()

# a = input("zhanghao:")
# b = input("mima:")
# if nameAndPasswd.get(a) == b:
#     print("密码正确")
# else:
#     print("密码错误")

print(nameAndPasswd)
