#-*- encoding:UTF-8 -*-
from tools.MysqlBase import *

    
if __name__ == '__main__':   
    db = MysqlBase()
    db.insert('insert into test values(%s,%s)',(2,'fff'))
    db.multi_insert_test()
