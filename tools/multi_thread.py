#-*- encoding:UTF-8 -*-
import threading
import time
 
class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.name = name
 
 
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        while 1:
            print("Starting " + self.name)
            time.sleep(1)
 
# 创建新线程
thread1 = myThread(1, "this is thread1")
thread2 = myThread(2, "this is thread2")
thread3 = myThread(3, "this is thread3")
 
# 开启线程
thread1.start()
thread2.start()
thread3.start()