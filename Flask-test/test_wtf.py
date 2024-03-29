# -*- coding: UTF-8 -*-
from flask import Flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask_wtf import FlaskForm
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import EqualTo

app = Flask(__name__)

app.config["SECRET_KEY"] = "fsjnkfvwesnfovkez"

'''定义表单的模型类'''
class RegisterForm(FlaskForm):
    """自定义的注册表单模型类"""

#                             名字              验证器/检验器  
#DataRequired 保证数据必须填写，并且不能为空
    user_name = StringField(label=u"用户名", validators=[DataRequired(u"用户名不能为空")])
    password = PasswordField(label=u"密码", validators=[DataRequired(u"密码不能为空")])
    password2 = PasswordField(label=u"密码", validators=[DataRequired(u"验证密码不能为空"), 
                                                        EqualTo("password", u"密码不一致")])

    submit = SubmitField(label=u"提交")

@app.route("/register", methods = ["GET", "POST"])
def register():
    
    '''创建表单对象,如果是post请求，前端发送了数据，flask会把数据在构造form对象的时候存放在对象中'''
    form = RegisterForm()

    '''判断form中的数据是否合理
    如果form中的数据完全满足所有的验证器，则返回真，否则返回假'''
    print("aaaaaaaaaa", form.user_name)
    print("aaaaaaaaaa", form.password)
    print("aaaaaaaaaa", form.password2)
    ret = form.validate_on_submit()
    print(ret)
    if ret:
        user_name = form.user_name.data
        pwd = form.password.data
        pwd2 = form.password2.data
        print(user_name, pwd)
        return redirect(url_for("index"))

    return render_template("register.html", form = form)

@app.route("/index")
def index():

    return "success"

if __name__ == "__main__":
    app.run(host="192.168.95.130", port=5001, debug = True)