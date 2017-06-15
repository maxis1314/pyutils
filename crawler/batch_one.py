#-*- encoding:UTF-8 -*-
from tools.MysqlBase import *
import subprocess
import time
import random
import sys 
if __name__ == '__main__':    
    db = MysqlBase('python')    
    id = sys.argv[1]
    while True:
        print "================new round ============================="       
        list = db.query('select * from bloglist where id=%s'%id)
        if len(list)>0:
            randInx = int(len(list)*random.random())
            list=[list[randInx]]
            for i in list:
                if i[1] == 'cnblog':
                    subprocess.Popen(u'python cnblog.py '+i[2],shell=True).wait()            
                elif i[1] == 'csdnblog':
                    subprocess.Popen(u'python csdnblog.py '+i[2],shell=True).wait()    
            db.execute('update  bloglist set flag = 1 where id =%d' % (list[0][0]))
            print 'update  bloglist set flag = 1 where id =%d' % (list[0][0])            
