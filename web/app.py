from flask import Flask, render_template, json, request
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from tools.MysqlBase import *

mysql = MysqlBase('python')
app = Flask(__name__)

@app.route('/')
@app.route('/showHome')
def main():
    userlist = mysql.query('select * from tbl_user')
    return render_template('index.html',list=userlist)

@app.route('/blogHome')
def blogHome():
    list = mysql.query('select * from blog')
    return render_template('blog_index.html',list=list)

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            _hashed_password = generate_password_hash(_password)
            mysql.insert('insert into tbl_user(user_name,user_username,user_password) values(%s,%s,%s)',(_name,_email,_hashed_password));           
            if True:               
                return json.dumps({'message':'User created successfully !','list':mysql.query('select * from tbl_user')})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})

if __name__ == "__main__":
    app.run(port=5000,debug=True)
