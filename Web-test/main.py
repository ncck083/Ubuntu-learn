# -*- coding: UTF-8 -*-
import datetime
import hashlib
import json
import os

from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from RSA_encrypt import decrypt_data

from config import app
from use_sql import db

# app = Flask(__name__)
# app.config.from_pyfile("config.py")

# 允许上传的文件类型
ALLOWED_SUFFIX = set(['png', 'jpg', 'jpeg', 'gif'])

# 判断是否是允许的文件类型
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_SUFFIX

def get_str_MD5(str_data):

    my_MD5 = hashlib.md5()
    my_MD5.update(str_data.encode("utf8"))
    return my_MD5.hexdigest()

def get_file_MD5(file_name):

    my_md5 = hashlib.md5()
    my_md5.update(file_name)
    file_MD5 = my_md5.hexdigest()
    return file_MD5

@app.route("/", methods = ["GET", "POST"])
def login_Check(): 
    """登录检查页面
    
    Returns:
        [type] -- [description]
    """

    # register_flag = json.loads(request.args.get("data"))
    # print(register_flag)
    # if 1 == register_flag:
    #     return render_template("register.html")
    up_load = url_for("upload")
    if request.method == "POST":
        user_name = request.form.get("username")
        pass_word = request.form.get('password')
        print("password is: ", pass_word)
        if None == user_name or None == pass_word:
            return "用户名或者密码不能为空"
        
        pass_word = get_str_MD5(pass_word)
        print(pass_word)

        ret = sql_select("user_login", "name", user_name)
        print(ret)
        if False != ret and ret[2] == pass_word:
            session["name"] = user_name
            return redirect(up_load)

        print(password)
    return render_template("login.html")

@app.route("/register", methods = ["GET", "POST"])
def register_new_user():
    """注册新用户
    
    Returns:
        [type] -- [description]
    """

    if request.method == 'POST':
        user_name = request.form.get('username')
        pass_word = request.form.get('password')
        pass_words = request.form.get('passwords')
        login_view = url_for("login")
        if None == user_name or None == pass_word:
            return "用户名或者密码不能为空"

        if sql_select("user_login", "name", user_name):
            return "用户已存在"

        if pass_word != pass_words:
            return "两次密码不一样"
        else:
            pass_word = get_str_MD5(pass_word)
            print(pass_word)
            db.session.execute("INSERT INTO `user_login`(name, password) VALUES('%s','%s');"
            %(user_name, pass_word))
            db.session.commit()
            return redirect(login_view)
    
    return render_template("register.html")

def sql_select(table, tag_name, data_name):
    """查询数据是否在表中
    
    Arguments:
        table {[string]} -- [description]
        tag_name {[string]} -- [description]
        data_name {[string]} -- [description]
    """

    mysql = "SELECT * FROM `%s` where %s = '%s';"%(table, tag_name, data_name)
    ret = db.session.execute(mysql)
    ret = list(ret)
    if [] == ret:
        return False
    else:
        return ret[0]

# 展示上传的文件
@app.route('/uploaded/<filename>')
def upladed(filename):
    # 安全的发送文件
    return send_from_directory(app.config['UPLOADED_FOLDER'], filename)

def save_picture(photo, new_pic_name, user_name):

    print(photo.filename)
    # 拼接文件保存的完整路径名
    pathname = os.path.join(app.config['UPLOADED_FOLDER'],
                            new_pic_name )
    print(new_pic_name)
    # 保存上传文件，参数是文件保存的路径名
    
    photo_data = photo.read()
    photo_MD5 = get_file_MD5(photo_data)

    ret = sql_select("user_picture", "pic_MD5", photo_MD5)
    if False != ret:
        return False

    sql = "INSERT INTO `user_picture`(picture, user_name, pic_MD5) VALUES('%s','%s','%s');"%(
            new_pic_name, user_name, photo_MD5)
    db.session.execute(sql)
    db.session.commit()
    photo.seek(0, 0)
    photo.save(pathname)
    img_url = url_for('upladed', filename=photo.filename)

@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    img_url = None
    user_name = session["name"]
    user_name = str(user_name)
    print(user_name)
    if None != user_name:
        print("user name is : ", user_name)
        if request.method == 'POST':
            # 获取上传对象
            photo = request.files.get('photo')
                       
            pic_name = request.form.get("pic_name")
            print(user_name, pic_name)
            now_time = datetime.datetime.now()
            now_time = now_time.strftime("%Y-%m-%d-%H-%M-%S")
            new_pic_name = user_name + "-" + pic_name + "-" + now_time + os.path.splitext(photo.filename)[1] 
            # 保存前验证文件的类型
            if photo and allowed_file(photo.filename):
                ret = save_picture(photo, new_pic_name, user_name)
            
            if False == ret:
                return "图片已存在"
            
        sql = "SELECT picture FROM `user_picture` WHERE user_name = '%s'"%user_name
        pic = db.session.execute(sql)
        pic = list(pic)
        pic_list = []
        for i in range(len(pic)):
            pic_list.append(pic[i][0])
        print(pic_list)
        return render_template('upload.html', pic=pic_list)
    return render_template("login.html")
    
if __name__ == "__main__":
    #启动flask程序
    print(app.url_map)
    app.run(host="192.168.95.130", port=5000)