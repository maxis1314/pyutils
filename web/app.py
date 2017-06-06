from flask import Flask, render_template, json, request,session,redirect,url_for
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from tools.MysqlBase import *
import hashlib



mysql = MysqlBase('python')
app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

@app.route('/')
@app.route('/showHome')
def main():
    userlist = mysql.query('select * from tbl_user')
    return render_template('index.html',list=userlist)

@app.route('/blogDetail')
def blogDetail():
    if not session.has_key('login') or not session['login']:    
        return redirect(url_for('showSignIn'))
    _id = request.args.get('id')
    blog = mysql.query('select * from blog where id=%s',(_id))
    return render_template('blog_detail.html',blog=blog[0],id=int(_id))

@app.route('/blogHome')
def blogHome():
    if not session.has_key('login') or not session['login']:    
        return redirect(url_for('showSignIn'))
    _from = request.args.get('from')
    if _from is None or _from.strip()== '':
        _from=0
    else:
        _from=int(float(_from))
    list = mysql.query(u'select * from blog order by id limit '+str(_from)+u',20')
    return render_template('blog_index.html',list=list,_from=_from)

@app.route('/blogSearch')
def blogSearch():
    if not session.has_key('login') or not session['login']:    
        return redirect(url_for('showSignIn'))
    _from = request.args.get('from')
    _key = request.args.get('key')
    if _from is None or _from.strip()== '':
        _from=0
    else:
        _from=int(float(_from))
    list = mysql.query(u'select * from blog where title like \'%'+_key+u'%\' order by id desc')
    return render_template('blog_index.html',list=list,_from=_from,_key=_key,is_search=True)
    
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

@app.route('/signIn',methods=['POST','GET'])
def signIn():
    _name = request.form['inputName']    
    _password = request.form['inputPassword']
    _hashed_password = hashlib.md5(_password).hexdigest()
    user = mysql.query('select * from tbl_user where user_name=%s',(_name))   
    if len(user)>0 and user[0][3] == _hashed_password:
        session['login'] = True
        return json.dumps({'error':0})
    else:
        return json.dumps({'error':1})

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            _hashed_password = hashlib.md5(_password).hexdigest()
            mysql.insert('insert into tbl_user(user_name,user_username,user_password) values(%s,%s,%s)',(_name,_email,_hashed_password));           
            if True:               
                return json.dumps({'message':'User created successfully !','error':0})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})

if __name__ == "__main__":
    app.run(port=5000,debug=True)
