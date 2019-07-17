from flask import Flask, request, render_template
from wtforms import Form
from wtforms.fields import simple, html5, core
from wtforms import widgets
from wtforms import validators

app = Flask(__name__)



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
    pwd = simple.PasswordField(
        validators=[
            validators.Regexp(regex="^[a-z]+", message='密码全为小写字母')
        ],  # 验证
        render_kw={'placeholder': '请输入密码'}
    )


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


#用户注册---------------------
class RegisterForm(Form):
    name = simple.StringField(
        label='用户名',
        validators=[
            validators.DataRequired()
        ],
        widget=widgets.TextInput(),
        render_kw={'class': 'form-control'},
        default='alex'
    )

    pwd = simple.PasswordField(
        label='密码',
        validators=[
            validators.DataRequired(message='密码不能为空')
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )

    pwd_confirm = simple.PasswordField(
        label='重复密码',
        validators=[
            validators.DataRequired(message='重复密码不能为空'),
            validators.EqualTo('pwd', message='两次密码输入不一致'),
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )

    email = html5.EmailField(
        label='邮箱',
        validators=[
            validators.DataRequired(message='邮箱不能为空'),
            validators.Email(message='邮箱格式错误')
        ],
        widget=widgets.TextInput(input_type='email'),
        render_kw={'class': 'from-control'},
    )

    gender = core.RadioField(
        label='性别',
        choices=(
            (1, '男'),
            (2, '女'),
        ),

        coerce=int,
        default=[1, ],
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegisterForm()
        return render_template('register.html', form=form)

    form = RegisterForm(formdata=request.form)
    if form.validate():
        print(form.data)
        return '注册成功'
    return render_template('register.html', form=form)


#从数据库取数据---------------------

class UserForm(Form):
    # 静态字段，实例化只执行一次
    city = core.StringField(
        label='城市',
        choices = (),   #从数据库取数据
    )
    name = simple.StringField(label='姓名')

    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)

        self.city.choices = '从数据库取数据'

@app.route('/user',methods=['GET','POST'])
def user():
    if request.method == 'GET':
        form = UserForm()
        return render_template('user.html',form=form)




if __name__ == '__main__':
    app.run()

""" 
第三方组件：wtforms
    作用：
        - 生成html标签
        - form表单验证
        
"""
