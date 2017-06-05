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

@app.route('/blogDetail')
def blogDetail():
    _id = request.args.get('id')
    blog = mysql.query('select * from blog where id=%s',(_id))
    return render_template('blog_detail.html',blog=blog[0],id=int(_id))

@app.route('/blogHome')
def blogHome():
    _from = request.args.get('from')
    if _from is None or _from.strip()== '':
        _from=0
    else:
        _from=int(float(_from))
    list = mysql.query(u'select * from blog order by id limit '+str(_from)+u',20')
    return render_template('blog_index.html',list=list,_from=_from)

@app.route('/blogSearch')
def blogSearch():
    _from = request.args.get('from')
    _key = request.args.get('key')
    if _from is None or _from.strip()== '':
        _from=0
    else:
        _from=int(float(_from))
    list = mysql.query(u'select * from blog where title like "%'+_key+u'%" order by id limit '+str(_from)+u',100')
    return render_template('blog_index.html',list=list,_from=_from)
    
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
