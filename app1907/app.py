from flask import Flask,request

app = Flask(__name__)

@app.before_request
def f():
    print('te')

@app.route('/index',methods=['GET','POST'])
def index():

    return 'Index'


if __name__ == '__main__':
    app.run()
    app.wsgi_app