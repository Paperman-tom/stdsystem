from enum import Enum, unique
import hashlib
# 定义角色
@unique
class Role(Enum):
    # 学生
    STUDENT = 1
    # 管理员
    ADMIN = 2


# 用户信息模型
class User(object):

    def __init__(self):
        self.__role = Role.STUDENT.name
        self.__email = None
        # 缺省设置用户名和密码一样
        self.__username = "admin"
        md5 = hashlib.md5()
        md5.update(self.__username.encode("utf-8"))
        self.__password = md5.hexdigest()

    __slots__ = ("__role", "__email", "__username", "__password")

    @property
    def role(self):
        return self.__role

    @role.setter
    def role(self, role):
        if not isinstance(role, Role):
            raise ValueError("角色参数有误！")
        self.__role = role.name

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        if len(password) < 6:
            raise ValueError("密码长度不得小于6位")
        self.__password = password

    def __str__(self):
        return "Role:%s|Email:%s|Username:%s|Password:%s" \
               % (self.role, self.email, self.username, self.password)

    __repr__ = __str__