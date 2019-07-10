from flask import Flask,render_template,request,redirect,session

app = Flask(__name__)

print(app.config)
# app.config['DEBUG'] = True
app.config.from_object("setting.Pro")