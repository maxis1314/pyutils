# coding: utf-8
from flask import Flask, render_template, json, request,session,redirect,url_for,send_from_directory
#from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from tools.MysqlBase import *
import hashlib
from tools.Predict import *
import subprocess

from views.todos import todos_view
from views.users import users_view
from views.rss import rss_view

mysql = MysqlBase('python')
app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'



app.register_blueprint(todos_view, url_prefix='/todos')
app.register_blueprint(users_view, url_prefix='/users')
app.register_blueprint(rss_view, url_prefix='/rss')

@app.route('/index')
def index():
    return render_template('info.html',title='index')

@app.route('/')
@app.route('/showHome')
def main():
    userlist = mysql.query('select * from tbl_user')
    return render_template('index.html',list=userlist)

    
@app.before_request
def before_request():
    print 'start procee request'
    
@app.route('/blogDetail')
def blogDetail():
    if not session.has_key('login') or not session['login']:    
        return redirect(url_for('showSignIn'))
    _id = request.args.get('id')
    blog = mysql.query('select * from blog where id=%s'%(_id))
    
    before = mysql.query('select * from blog where id<%s order by id desc limit 1'%(_id))
    after = mysql.query('select * from blog where id>%s order by id limit 1'%(_id))
    if len(before)<1:
        before=[[_id]]
    if len(after)<1:
        after=[[_id]]
    
    if len(blog)<1:
        return render_template('info.html',title='blog not exits')
    return render_template('blog_detail.html',blog=blog[0],id=int(_id),beforeid=before[0][0],afterid=after[0][0])

@app.route('/blogCatPredict')
def blogCatPredict():
    _id = request.args.get('id')
    predict = Predict()
    blog = mysql.query('select * from blog where id=%s'%(_id))
    result = predict.classify(blog[0][3] +' ' + blog[0][4])
    #return json.dumps({'predict_cat':result})
    return render_template('info.html',title=result)

@app.route('/blogModel')
def blogModel():   
    predict = Predict()    
    list = []
    for i in sorted(predict.cateWordsProb.items(), key=lambda d: d[1],reverse=True): 
        ra = i[0].split('_')
        list.append((predict.md5_cat[ra[0]],ra[1],i[1]))

    return render_template('info.html',title='Model Detail',list=list)
    
@app.route('/ajaxBlogCatPredict')
def ajaxBlogCatPredict():
    _id = request.args.get('id')
    predict = Predict()
    blog = mysql.query('select * from blog where id=%s'%(_id))
    result = predict.maybe(blog[0][3] +' ' + blog[0][4],3)
    return json.dumps({'predict_cat':','.join(result)})
    
    
@app.route('/blogHome')
def blogHome():
    if not session.has_key('login') or not session['login']:    
        return redirect(url_for('showSignIn'))
    _from = request.args.get('from')
    if _from is None or _from.strip()== '':
        _from=0
    else:
        _from=int(float(_from))
    list = mysql.query(u'select * from blog order by id desc limit '+str(_from)+u',20')
    numblog = mysql.query(u'select count(*) from blog')
    return render_template('blog_index.html',list=list,_from=_from,numblog=numblog[0][0])

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
    sql = u'select * from blog where title like \'%'+_key+u'%\' order by dt desc'
    print sql
    list = mysql.query(sql)
    return render_template('blog_index.html',list=list,_from=_from,_key=_key,is_search=True)

@app.route('/tagSearch')
def tagSearch():
    if not session.has_key('login') or not session['login']:    
        return redirect(url_for('showSignIn'))
    _from = request.args.get('from')
    _key = request.args.get('key')
    if _from is None or _from.strip()== '':
        _from=0
    else:
        _from=int(float(_from))
    sql = u'select * from blog where tags like \'%'+_key+u'%\' or categories like \'%'+_key+u'%\' order by dt desc'
    print sql
    list = mysql.query(sql)
    return render_template('blog_index.html',list=list,_from=_from,_key=_key,is_search=True)

    
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showAddBlog')
def showAddBlog():
    list = mysql.query('select * from bloglist order by id desc')
    return render_template('add_blog.html',list=list)
    
@app.route('/logout')
def logout():
    session['login'] = False
    session['name'] = None
    session['id'] = None
    return redirect(url_for('showSignIn'))

@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

@app.route('/signIn',methods=['POST','GET'])
def signIn():
    _name = request.form['inputName']    
    _password = request.form['inputPassword']
    _hashed_password = hashlib.md5(_password).hexdigest()
    user = mysql.query("""select * from tbl_user where user_name='%s'"""%(_name))   
    print user,_name
    if len(user)>0 and user[0][3] == _hashed_password:
        session['login'] = True
        session['name'] = _name
        session['id'] = user[0][0]
        return json.dumps({'error':0})
    else:
        return json.dumps({'error':1})

        
@app.route('/addBlog',methods=['POST','GET'])
def addBlog():
    _name = request.form['inputName']
    _type = request.form['type']
    mysql.insert('insert into bloglist(type,name) values(%s,%s)',(_type,_name));   
    return json.dumps({'error':0})   
    
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

@app.route('/robots.txt')
@app.route('/favicon.svg')
@app.route('/favicon.ico')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])



@app.route('/crawler/<todo_id>')
def crawler(todo_id):
    list = mysql.query('select * from bloglist where id=%s'%todo_id)
    if len(list)>0:
        randInx = int(len(list)*random.random())
        list=[list[randInx]]
        for i in list:
            if i[1] == 'cnblog':
                subprocess.Popen(u'python F:/git/pyutils/crawler/cnblog.py '+i[2],shell=True)         
            elif i[1] == 'csdnblog':
                subprocess.Popen(u'python F:/git/pyutils/crawler/csdnblog.py '+i[2],shell=True)
        mysql.execute('update  bloglist set flag = 1 where id =%d' % (list[0][0]))
        print 'update  bloglist set flag = 1 where id =%d' % (list[0][0])            

    return json.dumps({'error':todo_id})

    
if __name__ == "__main__":
    app.run(port=5000,debug=True)
