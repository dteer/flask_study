from flask import Flask,request

app = Flask(__name__)



def index():
    print(request.method)
    return 'Index'



if __name__ == '__main__':
    app.run()
