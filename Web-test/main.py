# -*- coding: UTF-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from RSA_encrypt import decrypt_data
app = Flask(__name__)
app.config.from_pyfile("config.py")

@app.route("/")
def login():
    """[summary]
    
    Returns:
        [type] -- [description]
    """
    return render_template("login.html")

@app.route("/login_check1", methods = ["GET", "POST"])
def login_Check():    
    password = request.values.get('passwords')
    #password = decrypt_data(password)
    print("aaaaaaaaaaaa")
    print(password)
    return password
    
if __name__ == "__main__":
    #启动flask程序
    print(app.url_map)
    app.run(host="192.168.95.130", port=5000)