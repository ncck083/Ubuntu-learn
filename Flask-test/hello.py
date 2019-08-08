# -*- coding: UTF-8 -*-
import json
from flask import Flask, render_template, request,jsonify, url_for, redirect, session

#创建flask应用对象
#__name__当前模块名字
#          模块名，flask以这个模块所在目录为总目录，默认则个目录中的static为静态陌路，templates为模板目录
app = Flask(__name__)
app.debug = True

'''flask的session需要用到的密钥字符串'''
app.config["SECRET_KEY"] = "asfcadfcqaw"

@app.route("/login")
def index():
    """定义的视图函数"""
 
    return render_template("test.html")
    
@app.route("/login_check1", methods = ["GET", "POST"])
def login_Check():
    print("request.data is: ", request.form.get("username"))
    print("request.data is: ", request.form.get("password"))

    login_suc = url_for("login_success", username = request.form.get("username"), data = 7)
    login = url_for("index")
    
    if "cck" == request.form.get("username") and "123456" == request.form.get("password"):
        session["name"] = request.form.get("username")
        return redirect(login_suc)
    
    else:
        return redirect(login)
    return "login success"

@app.route("/login_success/?<string:username><int:data>", methods = ["GET", "POST"])
def login_success(username, data):
    data = {
        "name": username,
        "data": data
    }
    #return render_template("main.html", name = username, data = data)
    return render_template("main.html", **data)
if __name__ == "__main__":
    #启动flask程序
    print(app.url_map)
    app.run(host="192.168.95.130", port=5000)