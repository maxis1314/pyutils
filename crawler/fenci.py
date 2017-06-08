#encoding=utf-8
import sys
from numpy import *
from tools.MysqlBase import *
import jieba

reload(sys) 
sys.setdefaultencoding( "utf-8" )

db = MysqlBase('python')


def f(x): 
    if x=='\n' or x=='\t' or x==' ' or x=='，' or len(x)<=1 or len(x)>=8:
        return False       
    
    match = re.search('^[0-9a-zA-Z\.\-_#]+$', x)    
    if match:
        return False
    return True


list_of_all_the_lines = db.query('select * from blog where tags<>"" limit 100')
linenum = 0

wfile_object = open('output.csv', 'w')

all_words=[]
part_words=[]
class_article=[]
count_words={}
for record in list_of_all_the_lines:
    line = record[3]+' '+record[4]
    line = line.strip()       
    seg_list = jieba.cut(line, cut_all=False)
    list1 =list(seg_list)
    list1 = filter(f, list1) 
    
    tags = record[5].split(',')
    if tags is None or tags[0]=='':
        continue
    linenum=linenum+1
    class_article.append(tags[0])#.replace(' ','_'))
    part_words.append(list1)   
    
    
    for word in list1:
        if count_words.has_key(word):
            count_words[word]=count_words[word]+1
        else:
            count_words[word]=1
    

for i in sorted(count_words.items(), key=lambda d: d[1],reverse=True):
    #print i[0],'\t',i[1],len(i[0])
    all_words.append(i[0])
#cut 10%
wordnum=len(all_words)
print 'all word num = ',wordnum
p10 = int(wordnum*0.1)

all_words=all_words[p10:]
wordnum=len(all_words)

trainingMat = zeros((linenum,wordnum))


for i in range(0,len(part_words)):
    for j in range(0,len(all_words)):
        trainingMat[i][j]=int(part_words[i].count(all_words[j]))

print trainingMat





wfile_object.write('#'+"\t".join(all_words))
print len(class_article)
print trainingMat.shape[0]
for i in range(0,trainingMat.shape[0]):
    print i,class_article[i]
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

 