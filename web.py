# -*- coding: utf-8 -*-



from datetime import datetime, timedelta
import sys
from std import *
from user import *
from userdb import *
import pymysql
import json

from flask import Flask, request, render_template, jsonify, url_for, redirect



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

webApp.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


@webApp.route("/", methods=["GET", "POST"])
def home():
    return render_template("login.html")


@webApp.route("/info", methods=["POST"])
def info():
    print(request.form)
    name = request.form["name"]
    id = request.form["id"]
    gender = request.form["gender"]
    birthday = request.form["birthday"]
    tel = request.form["tel"]
    email = request.form["email"]
    graduate = request.form["graduate"]
    for keys in request.form:
        print(keys + "=" + request.form[keys])
    try:
        s = Std()
        s.name = name
        s.id = id
        s.tel = tel
        s.email = email
        s.birthday = birthday
        s.gender = Gender[gender]
        s.graduate = Graduate[graduate]
        print(s)
        insertData(s)
        return render_template("login.html")
    except (ValueError, TypeError, RuntimeError):
        return render_template("register2.html", message="Unexpected error: %s" % sys.exc_info()[1])


@webApp.route("/register",methods=["GET"])
def registerpage():
    return render_template("register2.html")


@webApp.route("/register/", methods=["POST"])
def register():
    print(request.get_data(as_text=True))
    data = request.get_json()
    print("data=", data)
    username = data["username"]
    password = data["password"]
    email = data["email"]
    # username = request.values.get("username")
    # password = request.values.get("password")
    # email = request.values.get("email")
    print(username, password, email)
    try:
        u = User()
        u.role = Role['STUDENT']
        md5 = hashlib.md5()
        md5.update(password.encode("utf-8"))
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
            if Role[user.role] == Role.ADMIN:
                stds = queryallStd()
                # print(stds)
                # print('ok')
                return render_template("admin.html", username=user.username, role=roles[user.role], users=users, stds=stds)
            elif Role[user.role] == Role.STUDENT:
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
    print(request.get_data(as_text=True))
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
        return 'err'


@webApp.route("/admin/alterS", methods=["POST"])
def alterS():
    print(request.get_data(as_text=True))
    data = request.get_json()
    print("data=", data)
    try:
        alterStd(data)
        return "change successfully"
    except (ValueError, TypeError, RuntimeError):
        return 'err'


@webApp.route("/admin/delS", methods=["POST"])
def delS():
    print(request.get_data(as_text=True))
    data = request.get_json()
    print("data=", data)
    try:
        delStd(data)
        return "delete successfully"
    except (ValueError, TypeError, RuntimeError):
        return 'err'


@webApp.route("/admin/delU", methods=["POST"])
def delU():
    print(request.get_data(as_text=True))
    data = request.get_json()
    print("data=", data)
    try:
        delUser(data)
        return "delete successfully"
    except (ValueError, TypeError, RuntimeError):
        return 'err'


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
    print(request.get_data(as_text=True))
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
        return 'err'



if __name__ == "__main__":
    webApp.run()