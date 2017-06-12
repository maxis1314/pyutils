# coding: utf-8

from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask import flash
from tools.MysqlBase import *

mysql = MysqlBase('python')

class Todo():
    pass

todos_view = Blueprint('todos', __name__)

TRASHED, PLANNED, COMPLETED = -1, 0, 1


# 显示所有 Todo
@todos_view.route('')
def show():    
    status = int(request.args.get('status', PLANNED))
    if status == TRASHED:
        flash('无法查看已删除的 Todo')
        status = PLANNED
    try:
        
        todos = mysql.query_h('select * from todos where status=%s'%status)#[{'content':'11','status':'111'},{'content':'222','status':'111'}]
    except Exception as e:
        todos = []
        flash(e)
    return render_template('todos.html', todos=todos, status=status)


# 新建一个 Todo
@todos_view.route('', methods=['POST'])
def add():
    content = request.form['content']  
    try:
        mysql.insert('insert into todos(content,status) values(%s,%s)',(content,PLANNED));           
    except Exception as e:
        flash('error')
    return redirect(url_for('todos.show'))


# 删除一个 Todo
@todos_view.route('/<todo_id>', methods=['DELETE'])
def delete(todo_id):
    status = int(request.args.get('status', PLANNED))
    todo = Todo.create_without_data(todo_id)
    todo.set('status', TRASHED)
    try:
        todo.save()
    except Exception as e:
        flash(e.error)
    return redirect(url_for('todos.show', status=status))


# 将一个 Todo 的状态设置为已完成
@todos_view.route('/<todo_id>/done', methods=['POST'])
def done(todo_id):
    status = int(request.args.get('status', PLANNED))
    todo = Todo.create_without_data(todo_id)
    todo.set('status', COMPLETED)
    try:
        todo.save()
    except Exception as e:
        flash(e.error)
    return redirect(url_for('todos.show', status=status))


# 将一个 Todo 的状态设置为未完成
@todos_view.route('/<todo_id>/undone', methods=['POST'])
def undone(todo_id):
    status = int(request.args.get('status', PLANNED))
    todo = Todo.create_without_data(todo_id)
    todo.set('status', PLANNED)
    try:
        todo.save()
    except Exception as e:
        flash(e.error)
    return redirect(url_for('todos.show', status=status))
