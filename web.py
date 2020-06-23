# -*- coding: utf-8 -*-



from datetime import datetime, timedelta
import sys
from std import *
from user import *
from userdb import *
import pymysql
import json

from flask import Flask, request, render_template, jsonify, abort
from flask.json import JSONEncoder

class MyJSONEncoder(JSONEncoder):
    """
    方便对象序列化
    """
    def default(self, obj):
        if isinstance(obj, User):
            return {
                'username': obj.username,
                'email': obj.email,
                'role': obj.role,
            }
        if isinstance(obj, Std):
            return {
                'id': obj.id,
                'name': obj.name,
                'gender': obj.gender,
                'birthday': obj.birthday,
                'tel': obj.tel,
                'email': obj.email,
                'graduate': obj.graduate,
            }
        return super(MyJSONEncoder, self).default(obj)


# 如果已经存在user表，则先删除掉
executeSql(r"DROP TABLE IF EXISTS std")
executeSql(r"DROP TABLE IF EXISTS user")

executeSql("SET NAMES UTF8MB4;")
executeSql("SET CHARACTER SET UTF8MB4;")
executeSql("SET character_set_connection=UTF8MB4;")
# 创建数据表，如果不存在的情况下
executeSql(r"CREATE TABLE user (username VARCHAR(30) PRIMARY KEY, password VARCHAR(100),email VARCHAR(20) NOT NULL UNIQUE ,"
           r"role VARCHAR(10) NOT NULL);")
# 创建数据表，如果不存在的情况下
executeSql(r"CREATE TABLE std (id VARCHAR(20) PRIMARY KEY, name VARCHAR(30),"
           r"gender VARCHAR(10), birthday DATE, tel VARCHAR(20), email VARCHAR(20) NOT NULL, graduate VARCHAR(20),"
           r"FOREIGN KEY (email) REFERENCES user(email) ON UPDATE CASCADE);")



ADMINU = User()
ADMINU.role = Role['ADMIN']
md5 = hashlib.md5()
md5.update("admin".encode("utf-8"))
ADMINU.password = md5.hexdigest()
ADMINU.username = "admin"
ADMINU.email = "admin@admin.com"
insertData(ADMINU)





webApp = Flask(__name__)
webApp.json_encoder = MyJSONEncoder

webApp.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


@webApp.route("/", methods=["GET", "POST"])
def home():
    return render_template("login.html")


@webApp.route("/info", methods=["POST"])
def info():
    # print(request.form)
    name = request.form["name"]
    id = request.form["id"]
    gender = request.form["gender"]
    birthday = request.form["birthday"]
    tel = request.form["tel"]
    email = request.form["email"]
    graduate = request.form["graduate"]
    # for keys in request.form:
    #     print(keys + "=" + request.form[keys])
    try:
        s = Std()
        s.name = name
        s.id = id
        s.tel = tel
        s.email = email
        s.birthday = birthday
        s.gender = Gender[gender]
        s.graduate = Graduate[graduate]
        # print(s)
        insertData(s)
        return render_template("login.html")
    except (ValueError, TypeError, RuntimeError):
        return render_template("register2.html", message="Unexpected error: %s" % sys.exc_info()[1])


@webApp.route("/register",methods=["GET"])
def registerpage():
    return render_template("register2.html")


@webApp.route("/register/", methods=["POST"])
def register():
    # print(request.get_data(as_text=True))
    data = request.get_json()
    print("data=", data)
    username = data["username"]
    password = data["password"]
    email = data["email"]
    # print(username, password, email)
    try:
        u = User()
        u.role = Role['STUDENT']
        md5 = hashlib.md5()
        md5.update(password.encode("utf-8")) #使用md5加密算法加密密码
        u.password = md5.hexdigest()
        u.username = username
        u.email = email
        insertData(u)
        return jsonify({"name": username, "email": email})
    except (ValueError, TypeError, RuntimeError):
        return render_template("register2.html", message="Unexpected error: %s" % sys.exc_info()[1], username=username)


@webApp.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = queryUserByname(username)
    if user is None:
        return render_template("login.html", message="用户%s不存在，请检查用户名" % username)
    else:
        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
        if user.password == md5.hexdigest():
            roles = {Role.ADMIN.name: "管理员", Role.STUDENT.name: "学生"}
            users = []
            stds=[]
            if Role[user.role] == Role.ADMIN: #如果身份是管理员，则展示管理员界面
                stds = queryallStd()
                # print(stds)
                # print('ok')
                return render_template("admin.html", username=user.username, role=roles[user.role], users=users, stds=stds)
            elif Role[user.role] == Role.STUDENT: #如果身份是学生，则展示学生界面
                users.append(user)
                std = queryStdByemail(user.email)
                return render_template("index.html", username=user.username, role=roles[user.role], users=users, std=std)
        else:
            return render_template("login.html", message="密码错了", username=user.username)


@webApp.route("/login", methods=["GET"])
def loginpage():
    return render_template("login.html")


@webApp.route("/update", methods=["POST"])
def update():
    # print(request.get_data(as_text=True))
    data = request.get_json()
    print("data=", data)
    id = data["id"]
    birthday = data["birthday"]
    tel = data["tel"]
    try:
        newstd={'id': id, 'birthday': birthday, 'tel': tel}
        updateStd(newstd)
        return "change successfully"
    except (ValueError, TypeError, RuntimeError):
        return abort(400)


@webApp.route("/admin/alterS", methods=["POST"])
def alterS():
    # print(request.get_data(as_text=True))
    data = request.get_json()
    print("data=", data)
    try:
        alterStd(data)
        return "change successfully"
    except (ValueError, TypeError, RuntimeError):
        return abort(400)


@webApp.route("/admin/delS", methods=["POST"])
def delS():
    # print(request.get_data(as_text=True))
    data = request.get_json()
    print("data=", data)
    try:
        delStd(data)
        return "delete successfully"
    except (ValueError, TypeError, RuntimeError):
        return abort(400)



@webApp.route("/admin/delU", methods=["POST"])
def delU():
    # print(request.get_data(as_text=True))
    data = request.get_json()
    print("data=", data)
    try:
        delUser(data)
        return "delete successfully"
    except (ValueError, TypeError, RuntimeError):
        return abort(400)


@webApp.route("/admin/stds", methods=["GET", "POST"])
def allstds():
    stds = queryallStd()
    return render_template("admin.html",  stds=stds)


@webApp.route("/admin/users", methods=["GET", "POST"])
def allusers():
    userStds = queryStudents()
    userAdms = queryAdmins()
    return render_template("adusers.html",  stds=userStds, adms=userAdms)


@webApp.route("/admin/addADM", methods=["POST"])
def addADM():
    # print(request.get_data(as_text=True))
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    email = data["email"]
    print(username, password, email)
    try:
        u = User()
        u.role = Role['ADMIN']
        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
        u.password = md5.hexdigest()
        u.username = username
        u.email = email
        insertData(u)
        return jsonify({"name": username, "email": email})
    except (ValueError, TypeError, RuntimeError):
        return abort(400)


@webApp.route("/admin/searchU", methods=["POST"])
def searchU():
    # print(request.get_data(as_text=True))
    data = request.get_json()
    username = data["username"]
    print(username)
    try:
        results = queryUsersBysname(username)
        print(results)
        # print(jsonify(results))
        return jsonify(results)
    except (ValueError, TypeError, RuntimeError):
        return abort(400)


@webApp.route("/admin/searchS", methods=["POST"])
def searchS():
    # print(request.get_data(as_text=True))
    data = request.get_json()
    key = data["key"]
    kw = data["kw"]
    print(key, kw)
    try:
        results = queryStdByKey(key,kw)
        print(results)
        # print(jsonify(results))
        return jsonify(results)
    except (ValueError, TypeError, RuntimeError):
        return abort(400)



if __name__ == "__main__":
    webApp.run()