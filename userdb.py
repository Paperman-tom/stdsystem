import pymysql
from datetime import datetime
from user import *
from std import *
def executeSql(sql, params=None, isQuery=False):
    """
    负责打开和关闭数据库的操作，这也包括游标。
    负责执行SQL语句
    \n
    :param sql: 符合MySQL标准的SQL语句
    :param params: SQL语句中的参数值
    :param isQuery: 声明当前这条被执行的SQL语句是否为查询
    :return: 只有当isQuery为True时，返回查询后的结果列表，否则返回空列表
    """
    results = []
    # 打开一个数据库连接
    db_conn = pymysql.connect(host="127.0.0.1", user="root", password="wzr001017", db="std")
    db_conn.set_charset("utf8")
    with db_conn.cursor() as cursor:
        cursor.execute(sql, params)
        if isQuery:
            results = cursor.fetchall()
        db_conn.commit()
    # 关闭数据库连接
    db_conn.close()
    return results





# 新增一个注册用户
def insertData(data):
    if isinstance(data, User):
        sql = "INSERT INTO user VALUES(%s, %s, %s, %s)"
        params = (data.username, data.password, data.email, data.role)
        # 目前这种SQL语句总感觉有点勉强，因为有很多个占位符，参数必须要严格按照先后顺序插入
        executeSql(sql, params)
        print("execute insert success. -> %s" % str(data))
    elif isinstance(data, Std):
        sql = "INSERT INTO std VALUES(%s, %s, %s, %s, %s, %s, %s)"
        params = (data.id, data.name, data.gender, data.birthday, data.tel, data.email,data.graduate)
        # 目前这种SQL语句总感觉有点勉强，因为有很多个占位符，参数必须要严格按照先后顺序插入
        executeSql(sql, params)
        print("execute insert success. -> %s" % str(data))
    else:
        raise TypeError("存入用户失败了，当前参数对象并非一个合法的用户对象：%s" % type(data))


def updateStd(data):
        sql = "UPDATE std SET birthday=%s, tel=%s WHERE id=%s"
        params = (data['birthday'], data['tel'], data['id'])
        # 目前这种SQL语句总感觉有点勉强，因为有很多个占位符，参数必须要严格按照先后顺序插入
        executeSql(sql, params)
        print("execute update success. -> %s" % str(data))


def alterEmail(data):
    sql = "UPDATE user SET email=%s WHERE email=%s"
    params = (data['nemail'], data['pemail'])
    # 目前这种SQL语句总感觉有点勉强，因为有很多个占位符，参数必须要严格按照先后顺序插入
    executeSql(sql, params)
    print("execute update success. -> %s" % str(data))


def alterStd(data):
    alterEmail(data)
    sql = "UPDATE std SET name=%s, gender=%s, birthday=%s, tel=%s, graduate=%s WHERE id=%s"
    params = (data['nname'], data['ngender'], data['nbirthday'], data['ntel'], data['ngra'], data['id'])
    # 目前这种SQL语句总感觉有点勉强，因为有很多个占位符，参数必须要严格按照先后顺序插入
    executeSql(sql, params)
    print("execute update success. -> %s" % str(data))




def delUser(data):
    sql = "DELETE FROM user WHERE email=%s"
    params = (data['pemail'])
    executeSql(sql, params)


def delStd(data):
    sql = "DELETE FROM std WHERE id=%s"
    params = (data['id'])
    executeSql(sql, params)
    delUser(data)



def pack(type,values):
    """
    将数据源组装成为目标对象
    \n
    :param values: 被组装的数据源，必须是一个元组
    :return: 返回被组装后的数据对象
    """
    if type == 'user':
        u = User()
        u.username = values[0]
        u.password = values[1]
        u.email = values[2]
        u.role = Role[values[3]]
        return u
    elif type == "std":
        s = Std()
        s.id = values[0]
        s.name = values[1]
        s.gender = Gender[values[2]]
        s.birthday = values[3]
        s.tel = values[4]
        s.email = values[5]
        s.graduate = Graduate[values[6]]
        return s


def queryallStd():
    """
    查询表中的所有数据
    :return: 返回所有的用户数据
    """

    sql = "SELECT * FROM std;"
    values = executeSql(sql=sql, isQuery=True)
    datas = []
    for value in values:
        datas.append(pack('std', value))
    return datas


def querydatasByRole(role):
    """
    根据用户角色查询对应的所有用户信息
    :param role: 要查询的用户角色
    :return: 返回查询到的用户集合，若角色不存在则返回空的集合
    """

    datas = []
    if role in Role:
        sql = "SELECT * FROM user WHERE role = %s"
        params = (role.name,)
        values = executeSql(sql, params, True)
        for value in values:
            datas.append(pack('user',value))
    return datas


def queryStudents():
    """
    查询表中所有的学生信息
    :return: 返回查到的所有学生信息
    """
    return querydatasByRole(Role.STUDENT)



def queryAdmins():
    """
    查询表中所有的管理员信息
    :return: 返回查到的所有管理员信息
    """
    return querydatasByRole(Role.ADMIN)


def queryUserByname(name):
    """
    根据用户名查询对应的用户在本地数据表中是否存在
    \n
    :param name: 被查询的用户名
    :return: 若存在对应的用户则返回该用户的对象，否则返回None
    """

    if not name is None:
        sql = "SELECT * FROM user WHERE username = %s"
        params = (name,)
        values = executeSql(sql, params, True)
        if len(values) > 0:
            return pack("user", values[0])
        return None


def queryStdByemail(email):
    """
    根据email查询对应的学生在本地数据表中是否存在
    \n
    :param email: 被查询的email
    :return: 若存在对应的学生则返回该学生的对象，否则返回None
    """

    if not email is None:
        sql = "SELECT * FROM std WHERE email = %s"
        params = (email,)
        values = executeSql(sql, params, True)
        if len(values) > 0:
            return pack("std", values[0])
        return None

def queryStdByKey(key,kw):
    """
    根据email查询对应的学生在本地数据表中是否存在
    \n
    :param key: 被查询的关键字名
    :param kw: 关键字
    :return: 若存在对应的学生则返回该学生的对象，否则返回None
    """
    keys=['name', 'tel', 'graduate']
    if key in keys:
        if not kw is None:
            sql = "SELECT * FROM std WHERE %s = %s"
            params = (key, kw,)
            values = executeSql(sql, params, True)
            if len(values) > 0:
                return pack("std", values[0])
            return None



def querydataBysname(sname):
    """
    根据用户名查询对应的用户在本地数据表中是否存在
    \n
    :param sname: 被查询的学生姓名
    :return: 若存在对应的用户则返回该用户的对象，否则返回None
    """
    datas = []
    if not sname is None:
        sql = "SELECT * FROM std WHERE name = %s"
        params = (sname,)
        values = executeSql(sql, params, True)
        for value in values:
            datas.append(pack('std', value))
    return datas