# -*- coding: UTF-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)


class Config(object):
    """配置参数"""

    '''sqlalchemy的配置参数'''
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/cck"

    '''设置sqlalchemy自动跟踪数据库'''
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    '''为True时,查询时显示原始SQL语句'''
    SQLALCHEMY_ECHO = True


app.config.from_object(Config)

'''创建数据库sqlalchemy工具对象'''
db = SQLAlchemy(app)


class User(db.Model):
    """用户表"""

    '''指名数据库表名'''
    __tablename__ = "tbl_users"

    '''整形的主键会默认设置为自增主键'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("tb_roles.id"))


class Role(db.Model):
    """用户角色/身份表"""

    __tablename__ = "tb_roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)

    users = db.relationship("User", backref="role")

    def __repr__(self):
        """定义后，可以让显示对象的时候更直观"""

        return "Role object: name=%s" % self.name


if __name__ == "__main__":

    db.drop_all()
    '''创建所有的表'''
    db.create_all()

    '''创建对象'''
    role1 = Role(name="admin")
    '''session记录对象任务'''
    db.session.add(role1)
    '''提交任务到数据库中'''
    db.session.commit()
    role2 = Role(name="stuff")
    '''session记录对象任务'''
    db.session.add(role2)
    '''提交任务到数据库中'''
    db.session.commit()

    us1 = User(name="wang", email="wang@qq.com", password="123", role_id=role1.id)
    us2 = User(name="tian", email="tian@qq.com", password="123", role_id=role2.id)
    us3 = User(name="li", email="li@qq.com", password="123", role_id=role2.id)
    us4 = User(name="zhao", email="zhao@qq.com", password="123", role_id=role1.id)

    db.session.add_all([us1, us2, us3, us4])
    db.session.commit()
