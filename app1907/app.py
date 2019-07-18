from flask import Flask

app = Flask(__name__)

@app.before_request
def f():
    print('te')


if __name__ == '__main__':
    app.run()
    app.__call__