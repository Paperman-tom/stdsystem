from enum import Enum, unique
from datetime import datetime

# 定义性别
@unique
class Gender(Enum):
    BOYS = 1
    GIRLS = 0


@unique
class Graduate(Enum):
    UNDERGRADUATE = 1
    MASTER = 0



# 用户信息模型
class Std(object):

    def __init__(self):
        self.__id = None
        self.__name = None
        self.__gender = Gender.BOYS.name
        self.__birthday = None
        self.__tel = None
        self.__email = None
        self.__graduate = Graduate.UNDERGRADUATE.name

    __slots__ = ("__id", "__name", "__gender", "__birthday", "__tel",
                 "__email", "__graduate", )

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, gender):
        if not isinstance(gender, Gender):
            raise ValueError("性别参数有误！")
        self.__gender = gender.name

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday):
        self.__birthday = birthday

    @property
    def tel(self):
        return self.__tel

    @tel.setter
    def tel(self, tel):
        self.__tel = tel

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def graduate(self):
        return self.__graduate

    @graduate.setter
    def graduate(self, graduate):
        if not isinstance(graduate, Graduate):
            raise ValueError("身份参数有误！")
        self.__graduate = graduate.name


    def __str__(self):
        return "Name:%s|Gender:%s|Birthday:%s|Tel:%s|Email:%s|Graduate:%s" \
               % (self.name, self.gender, self.birthday, self.tel,
                  self.email, self.graduate)

    __repr__ = __str__