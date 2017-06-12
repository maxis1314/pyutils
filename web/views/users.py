# coding: utf-8

from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import flash,session
from tools.MysqlBase import *
import hashlib

mysql = MysqlBase('python')

users_view = Blueprint('users', __name__)


@users_view.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('users/register.html')
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        email = request.form.get('email', '').strip()
        if not username or not password:
            flash('用户名和密码不能为空。')
            return redirect(url_for('users.register'))
        #user.set_username(username)
        #user.set_password(password)
        try:
            _hashed_password = hashlib.md5(password).hexdigest()
            mysql.insert('insert into tbl_user(user_name,user_username,user_password) values(%s,%s,%s)',(username,email,_hashed_password));   
        except Exception as e:
            str(e)
            return redirect(url_for('users.register'))
        return redirect(url_for('todos.show'))

@users_view.route('/password', methods=['GET', 'POST'])
def password():
    if request.method == 'GET':
        return render_template('users/password.html')
    if request.method == 'POST':       
        password = request.form.get('password', '').strip()        
        if not password:
            flash('密码不能为空。')
            return redirect(url_for('users.password'))
        #user.set_username(username)
        #user.set_password(password)
        try:
            _hashed_password = hashlib.md5(password).hexdigest()
            mysql.insert('update tbl_user set user_password=%s where user_id=%s',(_hashed_password,session['id']));   
        except Exception as e:
            flash(str(e))
            return redirect(url_for('users.password'))
        return redirect(url_for('todos.show'))

@users_view.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('users/login.html')
    if request.method == 'POST':
        #user = User()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            flash('用户名和密码不能为空。')
            return redirect(url_for('users.login'))
        try:
            #user.login(username, password)
            user = mysql.query_h("""select * from tbl_user where user_name='%s'"""%(username))   
            _hashed_password = hashlib.md5(password).hexdigest()
            print user
            if len(user)>0 and user[0]['user_password'] == _hashed_password:
                session['login'] = True
                session['name'] = username
                session['id'] = user[0]['user_id']
            else:
                flash('username or password error!')
                return redirect(url_for('users.login'))
        except Exception as e:
            str(e)
            return redirect(url_for('users.login'))
        return redirect(url_for('todos.show'))


@users_view.route('/logout')
def logout():
    session['login'] = False
    session['name'] = None
    session['id'] = None
    return redirect(url_for('users.login'))
