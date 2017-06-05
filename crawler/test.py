#-*- encoding:UTF-8 -*-
from tools.MysqlBase import *

    
if __name__ == '__main__':   
    db = MysqlBase('python')
    #db.insert('insert into test values(%s,%s)',(2,'fff'))
    #db.multi_insert_test()
    db.execute('create table blog(link varchar(20),dt varchar(20),title varchar(200),body text)');
