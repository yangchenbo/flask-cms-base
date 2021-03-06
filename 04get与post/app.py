from flask import Flask, render_template
from flask import request
app = Flask(__name__)


@app.route('/')
def index():
    # 假设有这么一些新闻
    lists = [
        {"title": "头条新闻", "intro": "习近平发表了新年演说"},
        {"title": "新年新闻", "intro": "ETC收费据说费用更高了"},
        {"title": "过大年了", "intro": "全国互联网公司都在发红包"},
    ]


    return render_template("index.html" , newsLists=lists)


@app.route('/login', methods=['get', 'post'])
def login():
    # username = request.args.get("username")
    # password = request.args.get("password")
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        print(username, password)
    return render_template("login.html")



@app.route("/register")
def register():
    return render_template("register.html")


@app.context_processor
def account():
    username = "luxp"
    return {"username":username}