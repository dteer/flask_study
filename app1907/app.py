from flask import Flask, render_template, request, url_for

app = Flask(__name__)
app.config.from_object("settings.Dev")


#1、endpoint为地址的名称，不写，默认为函数名
#2、传参 int: <int:nid> str: <nid>
@app.route('/index/<int:nid>',methods=['GET','POST'],endpoint='n1')
def index(nid):
    print(url_for('n1'))                    #url_for获取名称n1的地址
    return 'Index'