import pymysql

import datetime

import messageSystem


con = pymysql.connect(host="39.106.49.30", user="root",
                          password="123456", db="message",
                      port=3306, charset='utf8')


def login():
    """登录"""
    while True:
        uname = input('请输入用户名：')
        pword = input('请输入密码：')
        flag = False
        with con.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            result = cursor.execute(
                'select uname as uname, pword as pword from tb_user'
                )
            for row in cursor.fetchall():
                if row['uname'] == uname:
                    flag = True
                    if row['pword'] == pword:
                        print('登录成功')
                        messageSystem.current_uname = uname
                        messageSystem.show_mess_system()
                    else:
                        print('密码输入错误')
            if not flag:
                print('该用户名不存在')


def fill_info():
    """填写注册信息"""
    while True:
        uname = input('请输入用户名(不超过10位)：')
        if 0 <= len(uname) <= 10:
            break
        else:
            print('输入有误，用户名不能超过10位')
    while True:
        pword = input('请输入密码(不超过8位)：')
        if 0 <= len(pword) <= 8:
            break
        else:
            print('输入有误，密码不能超过8位')
    with con.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
        result = cursor.execute(
            'select uname as uname from tb_user'
        )
        flag = False
        for row in cursor.fetchall():
            if row['uname'] == uname:
                flag = True
                print('该用户名已经注册')
        if not flag:
            try:
                with con.cursor() as cursor1:
                    result2 = cursor1.execute(
                        'insert into tb_user values (%s, %s, %s)',
                        (uname, pword, datetime.datetime.now())
                    )
                    if result2 == 1:
                        print('注册成功')
                con.commit()
            except pymysql.MySQLError as err:
                print(err)
                con.rollback()


def register():
    value = input('1.填写信息注册\n2.返回上级\n请选择：')
    if value == '1':
        fill_info()
    elif value == '2':
        return


def show_home_page():
    """主页"""
    while True:
        value = input('1.登录\n2.注册\n3.退出\n请选择：')
        if value == '1':
            login()
        elif value == '2':
            register()
        elif value == '3':
            con.close()
            exit()
        else:
            print('输入有误')


if __name__ == '__main__':
    show_home_page()
