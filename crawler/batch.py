#-*- encoding:UTF-8 -*-
from tools.MysqlBase import *
import subprocess
    
if __name__ == '__main__':   
    db = MysqlBase('python')
    list = db.query('select * from bloglist where flag=0')
    
    for i in list:
        if i[1] == 'cnblog':
            subprocess.Popen(u'python cnblog.py '+i[2],shell=True).wait()            
            
        db.execute('update  bloglist set flag = 1 where id =%d' % (i[0]));
        
    #print 22222222222
    #db.multi_insert_test()
    #db.execute('create table blog(link varchar(20),dt varchar(20),title varchar(200),body text)');