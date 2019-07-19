from flask import Flask, request, render_template
from wtforms import Form
from wtforms.fields import simple, html5, core
from wtforms import widgets
from wtforms import validators

app = Flask(__name__)


#FormMeta(type)
    #cls._unbound_fields = None
    #cls._wtforms_meta = None

#用户登录---------------------
class LoginForm(Form):
    name = simple.StringField(
        validators=[  # 验证
            validators.DataRequired(message='用户名不能为空'),
            validators.length(min=6, max=18, message='用户名长度必须大于6小于18')
        ],
        widget=widgets.TextArea(),  # 插件
        render_kw={'placeholder': '请输入用户名'},
    )
    # pwd = simple.PasswordField(
    #     validators=[
    #         validators.Regexp(regex="^[a-z]+", message='密码全为小写字母')
    #     ],  # 验证
    #     render_kw={'placeholder': '请输入密码'}
    # )
"""

UnboundField类：
    字段进行排序
    
创建LoginForm类时存在属性：
    LoginForm._unbound_fields = None
    LoginForm._wtforms_meta = None
     不等于：LoginForm.name = simple.StringField()  
    LoginForm.name = UnboundField(creation_counter=1,simple.StringField) 
            =====>simple.StringField()中继承的父类__new__方法改变了return对象
    LoginForm.pwd = UnboundField(creation_counter=2, simple.PasswordField)
"""


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        print(form.name, type(form.name))  # <input />       form.name是StringField()对象，StringField().__str__
        print(form.pwd, type(form.pwd))  # <input />       form.pwd是PasswordField()对象,PasswordField().__str__
        return render_template('login.html', form=form)

    form = LoginForm(formdata=request.form)
    if form.validate():
        print('验证成功')
        print(form.data)
        return '验证成功'
    else:
        print('验证失败')
        print(form.errors)
        return render_template('login.html', form=form)

form = LoginForm()


# if __name__ == '__main__':
    # app.run()


""" 
第三方组件：wtforms
    作用：
        - 生成html标签
        - form表单验证
        
"""
