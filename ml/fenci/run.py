#encoding=utf-8
import sys
from numpy import *

reload(sys) 
sys.setdefaultencoding( "utf-8" )

import jieba

rfile_object = open('input.tsv', 'r')
list_of_all_the_lines = rfile_object.readlines()
linenum = len(list_of_all_the_lines)

wfile_object = open('output.csv', 'w')

all_words=[]
part_words=[]
class_article=[]
for line in list_of_all_the_lines:
    line = line.strip()
    listFromLine = line.split('\t')
    class_article.append(listFromLine[1])
    seg_list = jieba.cut(listFromLine[0], cut_all=False)
    list1 =list(seg_list)
    part_words.append(list1)
    all_words.extend(list1)   

all_words=list(set(all_words))
wordnum=len(all_words);
trainingMat = zeros((linenum,wordnum))


for i in range(0,len(part_words)):
    for j in range(0,len(all_words)):
        trainingMat[i][j]=int(part_words[i].count(all_words[j]))

print trainingMat

def f(x): return x!='\n' and x!='\t' and x!=' ' and x!='，'
all_words = filter(f, all_words) 


wfile_object.write('#'+"\t".join(all_words))
for i in range(0,trainingMat.shape[0]):
    wfile_object.write("\n"+"\t".join(map(str,trainingMat[i,:]))+'\t'+class_article[i])

wfile_object.close( )


#seg_list = jieba.cut('KNN算法之所以在分类阶段需要耗费大量的时间是因为KNN算法并没有实际的分类器。要使得KNN算法拥有较好的分类性能，需要在训练阶段建立起分 类器，将大量的计算放到学习阶段，从而减少分类阶段的时间开销。考虑到类中心向量法拥有非常好的分类速度，因此将类中心向量和KNN算法相结合，以达到分 类精度趋近于KNN算法，分类速度趋近于类中心向量法的效果。结合后的算法可简单描述入下：（1）对样本集中的所有文本进行处理将计算后得到的文本向量保存下来。（2）采用类中心向量法，计算个各类的中心向量。（3）分类时，首先将待分类文本与各个类中向量进行相似度计算并排序。然后确定一个阀值m，取排名前m个类中的文本作为使用KNN算法的样本集。（4）在新的样本集上使用KNN算法进行分类计算，将D归类。', cut_all=False)
#list1 =list(seg_list)
#target = zeros((1,wordnum))
#for j in range(0,len(all_words)):
#    target[0][j]=int(list1.count(all_words[j]))
#print target

#datingDataMat,datingLabels = kNN.file2matrix('thefile.csv')
#print 'target=',target
#print 'labels=',datingLabels
#labelme= kNN.classify0(target,datingDataMat,datingLabels,3);
#print labelme#.decode('utf8').encode('gb2312')

#import json
#jsonfile = open('wp_posts.json', 'r')
#ecodejson = json.loads(jsonfile.readline())
#
#datafile = open('data2.txt', 'w')
#for k in  ecodejson:
#    datafile.write(k['post_content'].replace('\n', '').replace('\t', '').replace('\r', '')+'\t'+k['name']+'\n')
#    

 