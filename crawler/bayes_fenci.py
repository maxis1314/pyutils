#encoding=utf-8
import sys
from numpy import *
from tools.MysqlBase import *
import jieba
from os import listdir,mkdir,path,makedirs 
import hashlib
import base64
import pickle

reload(sys) 
sys.setdefaultencoding( "utf-8" )

db = MysqlBase('python')


list_of_all_the_lines = db.query('select * from blog where categories<>"" limit 1000')
linenum = 0

wfile_object = open('../ml/knn/input.csv', 'w')

all_words=[]
part_words=[]
class_article=[]
mapfile={}
for record in list_of_all_the_lines:
    line = record[3]+' '+record[4]
    
    tags = record[6].split(',')
    if tags is None or tags[0]=='':
        continue
    #dirname = base64.b64encode(tags[0])
    dirname = hashlib.md5(tags[0]).hexdigest()
    mapfile[dirname]=tags[0]
    if not path.exists(u'originSample/'+dirname):
        makedirs(u'originSample/'+dirname)
    wfile_object = open('originSample/'+dirname+'/'+str(record[0])+'.txt', 'w')
    wfile_object.write(line)
    wfile_object.close()

with open('md5_catname', 'w') as f:                     # open file with write-mode
        picklestring = pickle.dump(mapfile, f)   # serialize and save object
 