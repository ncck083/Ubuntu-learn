# -*- coding: UTF-8 -*-


"""配置参数"""

'''sqlalchemy的配置参数'''
SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1:3306/cck"

'''设置sqlalchemy自动跟踪数据库'''
SQLALCHEMY_TRACK_MODIFICATIONS = True

'''为True时,查询时显示原始SQL语句'''
SQLALCHEMY_ECHO = False

DEBUG = True
