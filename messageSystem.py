import pymysql

import datetime

import homePage

current_uname = ''

con = pymysql.connect(host="39.106.49.30", user="root",
                          password="123456", db="message",
                      port=3306, charset='utf8')


def send_mes():
    """发送信息"""
    titles = input('请输入短信标题：')
    contents = input('请输入短信内容：')
    receiver = input('请输入需要发送的人：')
    flag = False
    with con.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
        result2 = cursor.execute(
            'select uname as uname from tb_user'
        )
        for row in cursor.fetchall():
            if row['uname'] == receiver:
                flag = True
                try:
                    with con.cursor(cursor=pymysql.cursors.DictCursor) as cursor1:
                        result = cursor1.execute(
                            'insert into tb_sms (sender, receiver, title, content, uname) \
                                values (%s, %s, %s, %s, %s)',
                            (current_uname, receiver, titles, contents, current_uname),
                            )
                        result2 = cursor1.execute(
                            'insert into tb_sms (sender, receiver, title, content, sread, uname) \
                                values (%s, %s, %s, %s, %s, %s)',
                            (current_uname, receiver, titles, contents, 1, receiver),
                        )
                        if result > 0:
                            print('发送成功')
                    con.commit()
                except pymysql.MySQLError as err:
                    print(err)
                    con.rollback()
        if not flag:
            print('没有该接收者')
    show_mess_system()


def read_mes():
    """显示账户所有未读信息"""
    with con.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
        result2 = cursor.execute(
            'select sno as sno, sender as sender,'
            'sdate as sdate from tb_sms where sread=0 and uname=%s and sremove=1' % current_uname
        )
        if result2 == 0:
            print('该账户没有未读信息')
        else:
            print('以下是未读的信息')
            print('编号', '发送者', '日期', sep='\t')
            for row in cursor.fetchall():
                print(row['sno'], row['sender'], row['sdate'], sep='\t\t')


def find_mes():
    """显示账户所有信息"""
    with con.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
        result2 = cursor.execute(
            'select sno as sno, sender as sender,'
            'sdate as sdate from tb_sms where uname=%s and sremove=1' % current_uname
        )
        if result2 == 0:
            print('该账户没有可读信息')
        else:
            print('以下是该账户全部的信息')
            print('编号', '发送者', '日期', sep='\t')
            for row in cursor.fetchall():
                print(row['sno'], row['sender'], row['sdate'], sep='\t\t')


def read_check():
    while True:
        value = input('1.按短信编号查看未读信息\n2.按发送者查看未读信息\n3.返回上一级\n请选择：')
        if value == '1':
            read_sno()
        elif value == '2':
            read_sender()
        elif value == '3':
            check_message()


def read_sno():
    """按短信编号查看未读信息"""
    read_mes()
    sno = int(input('请输入要查看的短信编号：'))
    with con.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
        result = cursor.execute(
            'select sno as sno, sender as sender, title as title, '
            'content as content from tb_sms where sno=%s and sread=0 and uname=%s' % (sno, current_uname)
        )
        flag = False
        for row in cursor.fetchall():
            if row['sno'] == sno:
                flag = True
                print('编号', '发送者', '标题', '  内容', sep='\t')
                print(row['sno'], row['sender'], row['title'], row['content'], sep='\t\t')
            try:
                with con.cursor() as cursor1:
                    result2 = cursor1.execute(
                        'update tb_sms set sread=1 where sno=%s' % sno
                        )
                    if result2 > 0:
                        pass
                con.commit()
            except pymysql.MySQLError as err:
                print(err)
                con.rollback()
        if not flag:
            print('输入错误')


def read_sender():
    """按发送者查看未读信息"""
    read_mes()
    sender = input('请输入要查看的发送者：')
    with con.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
        result = cursor.execute(
            'select sno as sno, sender as sender, title as title, '
            'content as content from tb_sms where sender=%s and sread=0 and uname=%s and sremove=1' %
            (sender, current_uname)
        )
        flag = False
        for row in cursor.fetchall():
            if row['sender'] == sender:
                flag = True
                print(row['sno'], row['sender'], row['title'], row['content'], sep='\t\t')
            try:
                with con.cursor() as cursor1:
                    result2 = cursor1.execute(
                        'update tb_sms set sread=1 where sender=%s and sremove=1' % sender
                    )
                    if result2 > 0:
                        pass
                con.commit()
            except pymysql.MySQLError as err:
                print(err)
                con.rollback()
        if not flag:
            print('输入有误')


def sign_read():
    read_mes()
    value = input('1.按编号标记\n2.全部标记.\n3.返回上一级\n请选择：')
    if value == '1':
        sign_read_sno()
    elif value == '2':
        sign_read_all()
    elif value == '3':
        check_message()


def sign_read_sno():
    """按短信编号标记已读信息"""
    read_mes()
    sno = int(input('请输入要标记的短信编号：'))
    try:
        with con.cursor() as cursor:
            result = cursor.execute(
                'update tb_sms set sread=1 where sno=%s and uname=%s' % (sno, current_uname)
            )
            if result > 0:
                print('标记成功')
        con.commit()
    except pymysql.MySQLError as err:
        print(err)
        con.rollback()
    return


def sign_read_all():
    """标记全部已读信息"""
    read_mes()
    try:
        with con.cursor() as cursor:
            result = cursor.execute(
                'update tb_sms set sread=1 where uname=%s and sremove=1' % current_uname
            )
            if result > 0:
                print('标记成功')
        con.commit()
    except pymysql.MySQLError as err:
        print(err)
        con.rollback()
    return


def check_message():
    while True:
        value = input('1.读取消息\n2.标记已读\n3.返回上级\n请选择：')
        if value == '1':
            read_check()
        elif value == '2':
            sign_read()
        elif value == '3':
            show_mess_system()


def find_read_check_sno():
    """按短信编号查看信息"""
    find_mes()
    sno = int(input('请输入要查看的短信编号：'))
    with con.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
        result = cursor.execute(
            'select sno as sno, sender as sender, title as title, '
            'content as content from tb_sms where sno=%s and uname=%s' % (sno, current_uname)
        )
        print('编号', '发送者', '标题', '  内容', sep='\t')
        for row in cursor.fetchall():
            print(row['sno'], row['sender'], row['title'], row['content'], sep='\t\t')
        try:
            with con.cursor() as cursor1:
                result2 = cursor1.execute(
                    'update tb_sms set sread=1 where sno=%s' % sno
                )
                if result2 > 0:
                    pass
            con.commit()
        except pymysql.MySQLError as err:
            print(err)
            con.rollback()
    return


def find_read_check_sender():
    """按发送者查看信息"""
    find_mes()
    sender = input('请输入要查看的发送者：')
    with con.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
        result = cursor.execute(
            'select sno as sno, sender as sender, title as title, '
            'content as content from tb_sms where sender=%s and uname=%s and sremove=1' % (sender, current_uname)
        )
        print('编号', '发送者', '标题', '  内容', sep='\t')
        for row in cursor.fetchall():
            print(row['sno'], row['sender'], row['title'], row['content'], sep='\t\t')
        try:
            with con.cursor() as cursor1:
                result2 = cursor1.execute(
                    'update tb_sms set sread=1 where sender=%s and sremove=1' % sender
                )
                if result2 > 0:
                    pass
            con.commit()
        except pymysql.MySQLError as err:
            print(err)
            con.rollback()
    return


def find_read_check():
    while True:
        value = input('1.按短信编号查看信息\n2.按发送者查看信息\n3.返回上一级\n请选择：')
        if value == '1':
            find_read_check_sno()
        elif value == '2':
            find_read_check_sender()
        elif value == '3':
            return


def dele_mes_sno():
    """按短信编号删除信息"""
    find_mes()
    sno = int(input('请输入要删除的短信编号：'))
    with con.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
        result = cursor.execute(
            'select sno as sno, sender as sender, title as title, '
            'content as content from tb_sms where sno=%s' % sno
        )
        flag = False
        for row in cursor.fetchall():
            if row['sno'] == sno:
                flag = True
                print('编号', '发送者', '标题', '  内容', sep='\t')
                print(row['sno'], row['sender'], row['title'], row['content'], sep='\t\t')
            value = input('确认是否删除：\n1.删除\n2.取消')
            if value == '1':
                try:
                    with con.cursor() as cursor1:
                        result2 = cursor1.execute(
                            'update tb_sms set sremove=0 where sno=%s' % sno
                        )
                        if result2 > 0:
                            print('删除成功')
                    con.commit()
                except pymysql.MySQLError as err:
                    print(err)
                    con.rollback()
            elif value == '2':
                return
        if not flag:
            print('输入错误')
    return


def dele_mes_sender():
    """按发送者删除信息"""
    find_mes()
    sender = input('请输入要删除的发送者：')
    with con.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
        result = cursor.execute(
            'select sno as sno, sender as sender, title as title, '
            'content as content from tb_sms where sender=%s and uname=%s and sremove=1' % (sender, current_uname)
        )
        flag = False
        for row in cursor.fetchall():
            if row['sender'] == sender:
                flag = True
                print('编号', '发送者', '标题', '  内容', sep='\t')
                print(row['sno'], row['sender'], row['title'], row['content'], sep='\t\t')
            value = input('确认是否删除：\n1.删除\n2.取消')
            if value == '1':
                try:
                    with con.cursor() as cursor1:
                        result2 = cursor1.execute(
                            'update tb_sms set sremove=0 where sender=%s and uname=%s' % (sender, current_uname)
                        )
                        if result2 > 0:
                            print('删除成功')
                    con.commit()
                except pymysql.MySQLError as err:
                    print(err)
                    con.rollback()
            elif value == '2':
                return
        if not flag:
            print('输入有误')
    return


def dele_mes():
    value = input('1.按编号删除\n2.按发送者删除\n3.返回上级\n请选择：')
    if value == '1':
        dele_mes_sno()
    elif value == '2':
        dele_mes_sender()
    elif value == '3':
        return


def find_all():
    value = input('1.读取信息\n2.删除信息\n3.返回上级\n请选择：')
    if value == '1':
        find_read_check()
    elif value == '2':
        dele_mes()
    elif value == '3':
        return


def clean_mess():
    """清除所有信息"""
    find_mes()
    value = input('确认是否删除：\n1.删除\n2.取消')
    if value == '1':
        try:
            with con.cursor() as cursor1:
                result2 = cursor1.execute(
                    'update tb_sms set sremove=0 where uname=%s' % current_uname
                )
                if result2 > 0:
                    print('删除成功')
            con.commit()
        except pymysql.MySQLError as err:
            print(err)
            con.rollback()
    elif value == '2':
        return
    return


def show_mess_system():
    while True:
        value = input('1.发送短信息\n2.查看未读消息\n'
                      '3.查看所有信息\n4.清除所有信息\n5.注销\n请选择：')
        if value == '1':
            send_mes()
        elif value == '2':
            check_message()
        elif value == '3':
            find_all()
        elif value == '4':
            clean_mess()
        elif value == '5':
            homePage.show_home_page()


