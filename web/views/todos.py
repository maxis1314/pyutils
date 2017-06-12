# coding: utf-8

from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import flash,session
from tools.MysqlBase import *

mysql = MysqlBase('python')

class Todo():
    pass

todos_view = Blueprint('todos', __name__)

TRASHED, PLANNED, COMPLETED = -1, 0, 1


# 显示所有 Todo
@todos_view.route('')
def show(): 
    uid  = session['id'] if session.get('id',None) is not None else 0
    status = int(request.args.get('status', PLANNED))
    if status == TRASHED:
        flash('无法查看已删除的 Todo')
        status = PLANNED
    try:
        print 'select * from todos where status=%s and uid=%s'%(status,uid)
        todos = mysql.query_h('select * from todos where status=%s and uid=%s order by last_update desc'%(status,uid))#[{'content':'11','status':'111'},{'content':'222','status':'111'}]
    except Exception as e:
        todos = []
        flash(e)
    return render_template('todos.html', todos=todos, status=status)


# 新建一个 Todo
@todos_view.route('', methods=['POST'])
def add():
    uid  = session['id'] if session.get('id',None) is not None else 0
    content = request.form['content']  
    try:
        mysql.insert('insert into todos(content,status,uid) values(%s,%s,%s)',(content,PLANNED,uid));           
    except Exception as e:
        flash('add error')
    return redirect(url_for('todos.show'))


# 删除一个 Todo
@todos_view.route('/<todo_id>', methods=['GET'])
def delete(todo_id):    
    status = int(request.args.get('status', PLANNED))
    #todo = Todo.create_without_data(todo_id)
    #todo.set('status', TRASHED)
    try:
        mysql.execute('update todos set status=%s where id=%s'%(TRASHED,todo_id));
        print 'update todos set status=%s where id=%s'%(TRASHED,todo_id)
    except Exception as e:
        flash('delete error')
    return redirect(url_for('todos.show', status=status))


# 将一个 Todo 的状态设置为已完成
@todos_view.route('/<todo_id>/done', methods=['POST'])
def done(todo_id):
    status = int(request.args.get('status', PLANNED))    
    try:
        mysql.execute('update todos set status=%s where  id=%s'%(COMPLETED,todo_id));
    except Exception as e:
        flash('done error')
    return redirect(url_for('todos.show', status=status))


# 将一个 Todo 的状态设置为未完成
@todos_view.route('/<todo_id>/undone', methods=['POST'])
def undone(todo_id):
    status = int(request.args.get('status', PLANNED))
    try:
        mysql.execute('update todos set status=%s where  id=%s'%(PLANNED,todo_id));
    except Exception as e:
        flash('undone error')
    return redirect(url_for('todos.show', status=status))
