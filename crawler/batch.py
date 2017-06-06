#-*- encoding:UTF-8 -*-
from tools.MysqlBase import *
import subprocess
    
if __name__ == '__main__':   
    db = MysqlBase('python')
    list = db.query('select * from bloglist')
    
    for i in list:
        subprocess.Popen(u'python cnblog.py '+i[2],shell=True)
    
    #db.multi_insert_test()
    #db.execute('create table blog(link varchar(20),dt varchar(20),title varchar(200),body text)');
