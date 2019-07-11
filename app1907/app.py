from flask import Flask,request,session

app = Flask(__name__)
app.config.from_object('settings.Dev')




if __name__ == '__main__':
    app.run()