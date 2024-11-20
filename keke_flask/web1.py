from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话加密

# 模拟的用户数据
users = {
    "admin": "password123"
}


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        # 登录成功，重定向到卡密列表页面
        return redirect(url_for('card_list'))
    else:
        # 登录失败，显示错误信息
        flash('用户名或密码错误，请重试！11111')
        return redirect(url_for('index'))


@app.route('/你干嘛~')
def card_list():
    return render_template('card_list.html')


if __name__ == '__main__':
    app.run(debug=True)
