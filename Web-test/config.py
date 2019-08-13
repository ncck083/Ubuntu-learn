# -*- coding: UTF-8 -*-
from flask import Flask
import os


class Config(object):
    """配置参数"""

    '''sqlalchemy的配置参数'''
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/cck"

    '''设置sqlalchemy自动跟踪数据库'''
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    '''为True时,查询时显示原始SQL语句'''
    SQLALCHEMY_ECHO = False

    DEBUG = True

    '''sqlalchemy的配置参数'''
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/cck"

    '''设置sqlalchemy自动跟踪数据库'''
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    '''为True时,查询时显示原始SQL语句'''
    SQLALCHEMY_ECHO = True

    '''上传文件保存位置'''
    UPLOADED_FOLDER = os.path.join(os.getcwd(), "static/upload")

    '''请求大小， 文件大小限制'''
    MAX_CONTENT_LENGTH = 1024 *1024 * 8

    '''flask的session需要用到的密钥字符串'''
    SECRET_KEY = "1d2wawssdf"


app = Flask(__name__)
app.config.from_object(Config)