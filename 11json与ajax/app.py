from flask import Flask, render_template
from flask import request, redirect, url_for
from libs import db
from views.users import user_app
from views.articles import article_app
from flask_migrate import Migrate
from models import Category, User
from flask import session
import json
from sqlalchemy import MetaData

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///my.db"
app.secret_key = "123456"

db.init_app(app)

app.register_blueprint(user_app, url_prefix="/user")
app.register_blueprint(article_app, url_prefix="/article")

@app.route('/')
def index():
    return render_template("index.html" )

#
@app.route('/login', methods=['get', 'post'])
def login():
    message = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.validate_password(password):
            session['user'] = user.username
        # 登录成功返回首页
            return redirect(url_for("index"))
        else:
            message = "用户名与密码不匹配"
    #登录失败，给出提示
    return render_template("login.html", message=message)

@app.route("/logout")
def logout():
    if session.get('user'):
        session.pop("user")

    return redirect(url_for("index"))


@app.route("/image/upload", methods=['get','post'])
def upload():
    file = {
        "uploaded": 1,
        "fileName": "foo.jpg",
        "url": "/files/foo.jpg"
    }
    return json.dumps(file)

@app.route("/image/browser")
def browser():
    pass
# @app.route("/test")
# def test():
#     try:
#         number += 1
#     except Exception:
#         number = 0
#     return "number="+str(number)
#
# from flask import  make_response
# @app.route("/test_cookie")
# def test_cookie():
#     # 获取cookie
#
#     username = request.cookies.get("username")
#     response = make_response("<b>"+str(username)+"</b>")
#     response.set_cookie("number", "10")
#     return response
#
#
# @app.route("/test_cookie2")
# def test_cookie2():
#     number = request.cookies.get("number", "0")
#     number = int(number)+1
#     username = request.cookies.get("username")
#     response = make_response( "<b>number=" + str(number) + "</b>")
#     response.set_cookie("number", str(number))
#     return response

@app.route("/test_session")
def test_session():
    try:
        session['number'] += 1
    except:
        session['number'] = 0
    return "number="+str(session['number'])


@app.context_processor
def account():
    username = session.get('user')
    return {"username":username}

@app.context_processor
def getCateList():
    cates = Category.query.all()
    return {"cates":cates}

# 添加render_as_batch=True
# SQLite支持批处理修改
# 但是这种如果修改多个字段，可能在发生错误时，发生修改不一致

migrate = Migrate(app,db,render_as_batch=True)