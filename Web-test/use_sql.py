# -*- coding: UTF-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

from config import app

pymysql.install_as_MySQLdb()

db = SQLAlchemy(app)

class User_login(db.Model):

    __tablename__ = "user_login"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False, index=True)
    password = db.Column(db.String(128))
    

    def __repr__(self):
        """定义后，可以让显示对象的时候更直观"""

        return "User_login object: name=%s" % self.name


class UserPicture(db.Model):

    __tablename__ = "user_picture"

    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(128))
    pic_MD5 = db.Column(db.String(128), index=True)
    user_name = db.Column(db.String(128), db.ForeignKey("user_login.name"))


if __name__ == "__main__":
    db.drop_all()
    '''创建所有的表'''
    db.create_all()
    pass