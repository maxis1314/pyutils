# -*- coding: utf-8 -*-
from numpy import *
from os import listdir,mkdir,path,makedirs 
import re
import jieba
import operator
import sys
import pickle
reload(sys) 
sys.setdefaultencoding( "utf-8" )

def f(x): 
    if x=='\n' or x=='\t' or x==' ' or x=='，' or len(x)<=1 or len(x)>=8:
        return False       
    
    match = re.search('^[0-9a-zA-Z\.\-_#]+$', x)    
    if match:
        return False
    return True
    
##############################################################
## 1. 创建新文件夹，存放预处理后的文本数据
##############################################################
def createFiles():
    srcFilesList = listdir('temp/originSample')
    print srcFilesList
    for i in range(len(srcFilesList)):
        #if i==0: continue
        dataFilesDir = 'temp/originSample/' + srcFilesList[i] # 20个文件夹每个的路径
        dataFilesList = listdir(dataFilesDir)
        targetDir = 'temp/processedSample_includeNotSpecial/' + srcFilesList[i] # 20个新文件夹每个的路径
        if path.exists(targetDir)==False:
            makedirs(targetDir)
        else:
            print '%s exists' % targetDir
        for j in range(len(dataFilesList)):
            createProcessFile(srcFilesList[i],dataFilesList[j]) # 调用createProcessFile()在新文档中处理文本
            print 'processed %s %s' % (srcFilesList[i],dataFilesList[j])

##############################################################
## 2. 建立目标文件夹，生成目标文件
## @param srcFilesName 某组新闻文件夹的文件名，比如alt.atheism
## @param dataFilesName 文件夹下某个数据文件的文件名
## @param dataList 数据文件按行读取后的字符串列表
##############################################################
def createProcessFile(srcFilesName,dataFilesName):
    srcFile = 'temp/originSample/' + srcFilesName + '/' + dataFilesName
    targetFile= 'temp/processedSample_includeNotSpecial/' + srcFilesName\
                + '/' + dataFilesName
    fw = open(targetFile,'w')
    dataList = open(srcFile).readlines()
    for line in dataList:
        resLine = lineProcess(line) # 调用lineProcess()处理每行文本
        for word in resLine:
            fw.write('%s\n' % word) #一行一个单词
    fw.close()
##############################################################
##3. 对每行字符串进行处理，主要是去除非字母字符，转换大写为小写，去除停用词
## @param line 待处理的一行字符串
## @return words 按非字母分隔后的单词所组成的列表
##############################################################
def lineProcess(line):
    list1 = list(jieba.cut(line, cut_all=False))
    list1 = filter(f, list1)
    return list1
    
    
########################################################
## 统计每个词的总的出现次数
## @param strDir
## @param wordMap
## return newWordMap 返回字典，<key, value>结构，按key排序，value都大于4，即都是出现次数大于4的词
#########################################################
def countWords():
    wordMap = {}
    newWordMap = {}
    fileDir = 'temp/processedSample_includeNotSpecial'
    sampleFilesList = listdir(fileDir)
    for i in range(len(sampleFilesList)):
        sampleFilesDir = fileDir + '/' + sampleFilesList[i]
        sampleList = listdir(sampleFilesDir)
        for j in range(len(sampleList)):
            sampleDir = sampleFilesDir + '/' + sampleList[j]
            for line in open(sampleDir).readlines():
                word = line.strip('\n')
                wordMap[word] = wordMap.get(word,0.0) + 1.0
    #只返回出现次数大于4的单词
    for key, value in wordMap.items():
        if value > 4:
            newWordMap[key] = value
    sortedNewWordMap = sorted(newWordMap.iteritems())
    print 'wordMap size : %d' % len(wordMap)
    print 'newWordMap size : %d' % len(sortedNewWordMap)
    return sortedNewWordMap
############################################################
##打印属性字典
###########################################################
def printWordMap():
    print 'Print Word Map'
    countLine=0
    fr = open('temp/allDicWordCountMap.txt','w')
    sortedWordMap = countWords()
    for item in sortedWordMap:
        fr.write('%s %.1f\n' % (item[0],item[1]))
        countLine += 1
    print 'sortedWordMap size : %d' % countLine
    
#####################################################
##特征词选取,去除无相关词
####################################################
def filterSpecialWords():
    fileDir = 'temp/processedSample_includeNotSpecial'
    wordMapDict = {}
    sortedWordMap = countWords()
    for i in range(len(sortedWordMap)):
        wordMapDict[sortedWordMap[i][0]]=sortedWordMap[i][0]    
    sampleDir = listdir(fileDir)
    savetofile('model/wordset.txt',wordMapDict)
    for i in range(len(sampleDir)):
        targetDir = 'temp/processedSampleOnlySpecial' + '/' + sampleDir[i]
        srcDir = 'temp/processedSample_includeNotSpecial' + '/' + sampleDir[i]
        if path.exists(targetDir) == False:
            makedirs(targetDir)
        sample = listdir(srcDir)
        for j in range(len(sample)):
            targetSampleFile = targetDir + '/' + sample[j]
            fr=open(targetSampleFile,'w')
            srcSampleFile = srcDir + '/' + sample[j]
            for line in open(srcSampleFile).readlines():
                word = line.strip('\n')
                if word in wordMapDict.keys():
                    fr.write('%s\n' % word)
            fr.close()

def filterWords(words):    
    wordMapDict = loadtovar('model/wordset.txt')
    newwords=[]
    for word in words:        
        if word in wordMapDict.keys():
            newwords.append(word)
    return newwords

##########################################################
## 创建训练样例集合和测试样例集合
## @param indexOfSample 第k次实验
## @param classifyRightCate 第k次实验的测试集中，<doc rightCategory>数据
## @param trainSamplePercent 训练集与测试集的分割比例
############################################################
def createTestSample(indexOfSample,classifyRightCate,trainSamplePercent=0.9):
    fr = open(classifyRightCate,'w')
    fileDir = 'temp/processedSampleOnlySpecial'
    sampleFilesList=listdir(fileDir)
    for i in range(len(sampleFilesList)):
        sampleFilesDir = fileDir + '/' + sampleFilesList[i]
        sampleList = listdir(sampleFilesDir)
        m = len(sampleList)
        testBeginIndex = indexOfSample * ( m * (1-trainSamplePercent) ) 
        testEndIndex = (indexOfSample + 1) * ( m * (1-trainSamplePercent) )
        for j in range(m):
            # 序号在规定区间内的作为测试样本，需要为测试样本生成类别-序号文件，最后加入分类的结果，
            # 一行对应一个文件，方便统计准确率  
            if (j > testBeginIndex) and (j < testEndIndex): 
                fr.write('%s %s\n' % (sampleList[j],sampleFilesList[i])) # 写入内容：每篇文档序号 它所在的文档名称即分类
                targetDir = 'temp/TestSample'+str(indexOfSample)+\
                            '/'+sampleFilesList[i]
            else:
                targetDir = 'temp/TrainSample'+str(indexOfSample)+\
                            '/'+sampleFilesList[i]
            if path.exists(targetDir) == False:
                makedirs(targetDir)
            sampleDir = sampleFilesDir + '/' + sampleList[j]
            sample = open(sampleDir).readlines()
            sampleWriter = open(targetDir+'/'+sampleList[j],'w')
            for line in sample:
                sampleWriter.write('%s\n' % line.strip('\n'))
            sampleWriter.close()
    fr.close()
    
# 调用以上函数生成标注集，训练和测试集合
def test():
    for i in range(10):
        classifyRightCate = 'temp/classifyRightCate' + str(i) + '.txt'
        createTestSample(i,classifyRightCate)
        
        
########################################################################
## 统计训练样本中，每个目录下每个单词的出现次数, 及每个目录下的单词总数
## @param 训练样本集目录
## @return cateWordsProb <类目_单词 ,某单词出现次数>
## @return cateWordsNum <类目，单词总数>
#########################################################################
def getCateWordsProb(strDir):
    #strDir = TrainSample0 
    cateWordsNum = {}
    cateWordsProb = {}
    cateDir = listdir(strDir)
    for i in range(len(cateDir)):
        count = 0 # 记录每个目录下（即每个类下）单词总数
        sampleDir = strDir + '/' + cateDir[i]
        sample = listdir(sampleDir)
        for j in range(len(sample)):
            sampleFile = sampleDir + '/' + sample[j]
            words = open(sampleFile).readlines()
            for line in words:
                count = count + 1
                word = line.strip('\n')                
                keyName = cateDir[i] + '_' + word
                cateWordsProb[keyName] = cateWordsProb.get(keyName,0)+1 # 记录每个目录下（即每个类下）每个单词的出现次数
        cateWordsNum[cateDir[i]] = count
        print 'cate %d contains %d' % (i,cateWordsNum[cateDir[i]])
    print 'cate-word unique num: %d' % len(cateWordsProb)
    #print cateWordsProb
    #print cateWordsNum
    return cateWordsProb, cateWordsNum
    
    
    
##########################################
## 用贝叶斯对测试文档分类
## @param traindir 训练集目录
## @param testdir  测试集目录
## @param classifyResultFileNew  分类结果文件
## @return 返回该测试样本在该类别的概率
##########################################
def NBprocess(index,traindir,testdir,classifyResultFileNew):
    crWriter = open(classifyResultFileNew,'w')
    # traindir = 'TrainSample0'
    # testdir = 'TestSample0'
    #返回类k下词C的出现次数，类k总词数
    cateWordsProb, cateWordsNum = getCateWordsProb(traindir)
    trainDirFiles = listdir(traindir)#all categories
    
    #训练集的总词数
    trainTotalNum = sum(cateWordsNum.values())
    print 'trainTotalNum: %d' % trainTotalNum
    
    wordMapDict = loadtovar('model/wordset.txt')
    
    savetofile(u'model/'+str(index)+'.model',(trainDirFiles,cateWordsProb, cateWordsNum,wordMapDict))

    #开始对测试样例做分类
    testDirFiles = listdir(testdir)
    for i in range(len(testDirFiles)):
        testSampleDir = testdir + '/' + testDirFiles[i]
        testSample = listdir(testSampleDir)
        for j in range(len(testSample)):
            testFilesWords = []
            sampleDir = testSampleDir + '/' + testSample[j]
            lines = open(sampleDir).readlines()
            for line in lines:
                word = line.strip('\n')
                testFilesWords.append(word)

            maxP = 0.0
            #trainDirFiles = listdir(traindir)#all categories
            for k in range(len(trainDirFiles)):
                p = computeCateProb(trainDirFiles[k], testFilesWords,\
                                    cateWordsNum, trainTotalNum, cateWordsProb)
                #print j,'=',trainDirFiles[k],'~',p
                if k==0:
                    maxP = p
                    bestCate = trainDirFiles[k]
                    continue
                if p > maxP:
                    maxP = p
                    bestCate = trainDirFiles[k]
                #print bestCate
            crWriter.write('%s %s\n' % (testSample[j],bestCate))
    crWriter.close()
    
def classify_file(modelname,sampleDir):
    lines = open(sampleDir).readlines()
    testFilesWords=[]
    for line in lines:
        word = line.strip('\n')
        testFilesWords.append(word)
        #print word
    
    trainDirFiles,cateWordsProb, cateWordsNum,wordDict = loadtovar(modelname)
    trainTotalNum = sum(cateWordsNum.values())
    maxP = 0.0
    #trainDirFiles = listdir(traindir)#all categories
    for k in range(len(trainDirFiles)):
        p = computeCateProb(trainDirFiles[k], testFilesWords,\
                            cateWordsNum, trainTotalNum, cateWordsProb)
        #print j,'=',trainDirFiles[k],'~',p
        if k==0:
            maxP = p
            bestCate = trainDirFiles[k]
            continue
        if p > maxP:
            maxP = p
            bestCate = trainDirFiles[k]
    print bestCate    
    return bestCate
    
def classify(modelname,str):
    testFilesWords=list(lineProcess(str))
    testFilesWords = filterWords(testFilesWords)
    testFilesWords = [ww.encode('utf-8') for ww in testFilesWords]  
    #for ww in testFilesWords:
    #    print ww
    
    #print testFilesWords
    trainDirFiles,cateWordsProb, cateWordsNum,wordsDict = loadtovar(modelname)
    #for i in sorted(cateWordsProb.items(), key=lambda d: d[1],reverse=True):
    #    print i[0],'\t',i[1]
    trainTotalNum = sum(cateWordsNum.values())
    for k in range(len(trainDirFiles)):
        p = computeCateProb(trainDirFiles[k], testFilesWords,\
                            cateWordsNum, trainTotalNum, cateWordsProb)
        #print trainDirFiles[k],'~',p
        if k==0:
            maxP = p
            bestCate = trainDirFiles[k]
            continue
        if p > maxP:
            maxP = p
            bestCate = trainDirFiles[k]
    return bestCate
def inspectmodel(modelname):
    trainDirFiles,cateWordsProb, cateWordsNum = loadtovar(modelname)
    for i in sorted(cateWordsProb.items(), key=lambda d: d[1],reverse=True):
        print i[0],'\t',i[1]

    
#################################################
## @param traindir       类k
## @param testFilesWords 某个测试文档
## @param cateWordsNum   训练集类k下单词总数 <类目，单词总数>
## @param totalWordsNum  训练集单词总数
## @param cateWordsProb  训练集类k下词c出现的次数 <类目_单词 ,某单词出现次数>
## 计算 条件概率 =（类k中单词i的数目+0.0001）/（类k中单词总数+训练样本中所有类单词总数）
## 计算 先验概率 =（类k中单词总数）/（训练样本中所有类单词总数）
#################################################
def computeCateProb(traindir,testFilesWords,cateWordsNum,\
                    totalWordsNum,cateWordsProb):
    prob = 0
    wordNumInCate = cateWordsNum[traindir]  # 类k下单词总数 <类目，单词总数>
    for i in range(len(testFilesWords)):
        keyName = traindir + '_' + testFilesWords[i]
        if cateWordsProb.has_key(keyName):
            testFileWordNumInCate = cateWordsProb[keyName] # 类k下词c出现的次数
            #print "hit"
        else: testFileWordNumInCate = 0.0
        xcProb = log((testFileWordNumInCate + 0.0001) / (wordNumInCate + totalWordsNum))  # 求对数避免很多很小的数相乘下溢出
                 
        prob = prob + xcProb
    res = prob + log(wordNumInCate) - log(totalWordsNum)
    return res
    
    
def computeAccuracy(rightCate,resultCate,k):
    rightCateDict = {}
    resultCateDict = {}
    rightCount = 0.0

    for line in open(rightCate).readlines():
        (sampleFile,cate) = line.strip('\n').split(' ')
        rightCateDict[sampleFile] = cate
        
    for line in open(resultCate).readlines():
        (sampleFile,cate) = line.strip('\n').split(' ')
        resultCateDict[sampleFile] = cate
        
    for sampleFile in rightCateDict.keys():
        #print 'rightCate: %s  resultCate: %s' % \
         #     (rightCateDict[sampleFile],resultCateDict[sampleFile])
        #print 'equal or not: %s' % (rightCateDict[sampleFile]==resultCateDict[sampleFile])

        if (rightCateDict[sampleFile]==resultCateDict[sampleFile]):
            rightCount += 1.0
            print sampleFile,rightCateDict[sampleFile]
    print 'rightCount : %d  rightCate: %d' % (rightCount,len(rightCateDict))
    accuracy = rightCount/len(rightCateDict)
    print 'accuracy %d : %f' % (k,accuracy)
    return accuracy
    
    
#############################################################################
## 生成每次迭代的测试用例、标注集
def step1():
    createFiles()
    filterSpecialWords()
    for i in range(10):
        classifyRightCate = 'temp/classifyRightCate' + str(i) + '.txt'
        createTestSample(i,classifyRightCate)
##############################################################################
## bayes对测试文档做分类
def step2():
    for i in range(10):       
        print i
        traindir = 'temp/TrainSample' + str(i)
        testdir = 'temp/TestSample' + str(i)
        classifyResultFileNew = 'temp/classifyResultFileNew' + str(i) + '.txt'
        NBprocess(i,traindir,testdir,classifyResultFileNew)
##############################################################################
## 计算准确率
def step3():
    accuracyOfEveryExp = []
    for i in range(10):
        rightCate = 'temp/classifyRightCate'+str(i)+'.txt'
        resultCate = 'temp/classifyResultFileNew'+str(i)+'.txt'
        accuracyOfEveryExp.append(computeAccuracy(rightCate,resultCate,i))
    return accuracyOfEveryExp

def savetofile(filename,summer):
    with open(filename, 'w') as f:                     # open file with write-mode
        picklestring = pickle.dump(summer, f)   # serialize and save object
def loadtovar(filename):
    with open(filename, 'r') as f:
        summer = pickle.load(f)   # read file and build object
    return summer


computeAccuracy('temp/classifyRightCate0.txt','temp/classifyResultFileNew0.txt',1);  
file = '674df412a56185e63631413d4a99d4db/1618.txt'
lines = open(u'temp/originSample/'+file).readlines()
testFilesWords=[]
for line in lines:
    testFilesWords.append(line)
print classify('model/0.model',' '.join(testFilesWords));
print "\n======================\n"
#classify_file('model/0.model',u'temp/processedSampleOnlySpecial/'+file);
sys.exit()
#computeAccuracy('temp/classifyRightCate0.txt','temp/classifyResultFileNew0.txt',1);sys.exit()
#inspectmodel('model/0.model')
#sys.exit() 
step1()
step2()
step3()

for i in range(10):
    predict_word = '100 pills'
    result = classify('model/'+str(i)+'.model',predict_word)
    print predict_word,' => ',result
#inspectmodel('model/0.model')