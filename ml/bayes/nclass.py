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
    if x=='\n' or x=='\t' or x==' ' or x=='��' or len(x)<=1 or len(x)>=8:
        return False       
    
    match = re.search('^[0-9a-zA-Z\.\-_#]+$', x)    
    if match:
        return False
    return True
    
##############################################################
## 1. �������ļ��У����Ԥ�������ı�����
##############################################################
def createFiles():
    srcFilesList = listdir('temp/originSample')
    print srcFilesList
    for i in range(len(srcFilesList)):
        #if i==0: continue
        dataFilesDir = 'temp/originSample/' + srcFilesList[i] # 20���ļ���ÿ����·��
        dataFilesList = listdir(dataFilesDir)
        targetDir = 'temp/processedSample_includeNotSpecial/' + srcFilesList[i] # 20�����ļ���ÿ����·��
        if path.exists(targetDir)==False:
            makedirs(targetDir)
        else:
            print '%s exists' % targetDir
        for j in range(len(dataFilesList)):
            createProcessFile(srcFilesList[i],dataFilesList[j]) # ����createProcessFile()�����ĵ��д����ı�
            print '%s %s' % (srcFilesList[i],dataFilesList[j])

##############################################################
## 2. ����Ŀ���ļ��У�����Ŀ���ļ�
## @param srcFilesName ĳ�������ļ��е��ļ���������alt.atheism
## @param dataFilesName �ļ�����ĳ�������ļ����ļ���
## @param dataList �����ļ����ж�ȡ����ַ����б�
##############################################################
def createProcessFile(srcFilesName,dataFilesName):
    srcFile = 'temp/originSample/' + srcFilesName + '/' + dataFilesName
    targetFile= 'temp/processedSample_includeNotSpecial/' + srcFilesName\
                + '/' + dataFilesName
    fw = open(targetFile,'w')
    dataList = open(srcFile).readlines()
    for line in dataList:
        resLine = lineProcess(line) # ����lineProcess()����ÿ���ı�
        for word in resLine:
            fw.write('%s\n' % word) #һ��һ������
    fw.close()
##############################################################
##3. ��ÿ���ַ������д�����Ҫ��ȥ������ĸ�ַ���ת����дΪСд��ȥ��ͣ�ô�
## @param line �������һ���ַ���
## @return words ������ĸ�ָ���ĵ�������ɵ��б�
##############################################################
def lineProcess(line):
    list1 = list(jieba.cut(line, cut_all=False))
    list1 = filter(f, list1)
    return list1
    
    
########################################################
## ͳ��ÿ���ʵ��ܵĳ��ִ���
## @param strDir
## @param wordMap
## return newWordMap �����ֵ䣬<key, value>�ṹ����key����value������4�������ǳ��ִ�������4�Ĵ�
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
    #ֻ���س��ִ�������4�ĵ���
    for key, value in wordMap.items():
        if value > 4:
            newWordMap[key] = value
    sortedNewWordMap = sorted(newWordMap.iteritems())
    print 'wordMap size : %d' % len(wordMap)
    print 'newWordMap size : %d' % len(sortedNewWordMap)
    return sortedNewWordMap
############################################################
##��ӡ�����ֵ�
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
##������ѡȡ,ȥ������ش�
####################################################
def filterSpecialWords():
    fileDir = 'temp/processedSample_includeNotSpecial'
    wordMapDict = {}
    sortedWordMap = countWords()
    for i in range(len(sortedWordMap)):
        wordMapDict[sortedWordMap[i][0]]=sortedWordMap[i][0]    
    sampleDir = listdir(fileDir)
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
            
##########################################################
## ����ѵ���������ϺͲ�����������
## @param indexOfSample ��k��ʵ��
## @param classifyRightCate ��k��ʵ��Ĳ��Լ��У�<doc rightCategory>����
## @param trainSamplePercent ѵ��������Լ��ķָ����
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
            # ����ڹ涨�����ڵ���Ϊ������������ҪΪ���������������-����ļ������������Ľ����
            # һ�ж�Ӧһ���ļ�������ͳ��׼ȷ��  
            if (j > testBeginIndex) and (j < testEndIndex): 
                fr.write('%s %s\n' % (sampleList[j],sampleFilesList[i])) # д�����ݣ�ÿƪ�ĵ���� �����ڵ��ĵ����Ƽ�����
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
    
# �������Ϻ������ɱ�ע����ѵ���Ͳ��Լ���
def test():
    for i in range(10):
        classifyRightCate = 'temp/classifyRightCate' + str(i) + '.txt'
        createTestSample(i,classifyRightCate)
        
        
########################################################################
## ͳ��ѵ�������У�ÿ��Ŀ¼��ÿ�����ʵĳ��ִ���, ��ÿ��Ŀ¼�µĵ�������
## @param ѵ��������Ŀ¼
## @return cateWordsProb <��Ŀ_���� ,ĳ���ʳ��ִ���>
## @return cateWordsNum <��Ŀ����������>
#########################################################################
def getCateWordsProb(strDir):
    #strDir = TrainSample0 
    cateWordsNum = {}
    cateWordsProb = {}
    cateDir = listdir(strDir)
    for i in range(len(cateDir)):
        count = 0 # ��¼ÿ��Ŀ¼�£���ÿ�����£���������
        sampleDir = strDir + '/' + cateDir[i]
        sample = listdir(sampleDir)
        for j in range(len(sample)):
            sampleFile = sampleDir + '/' + sample[j]
            words = open(sampleFile).readlines()
            for line in words:
                count = count + 1
                word = line.strip('\n')                
                keyName = cateDir[i] + '_' + word
                cateWordsProb[keyName] = cateWordsProb.get(keyName,0)+1 # ��¼ÿ��Ŀ¼�£���ÿ�����£�ÿ�����ʵĳ��ִ���
        cateWordsNum[cateDir[i]] = count
        print 'cate %d contains %d' % (i,cateWordsNum[cateDir[i]])
    print 'cate-word unique num: %d' % len(cateWordsProb)
    #print cateWordsProb
    #print cateWordsNum
    return cateWordsProb, cateWordsNum
    
    
    
##########################################
## �ñ�Ҷ˹�Բ����ĵ�����
## @param traindir ѵ����Ŀ¼
## @param testdir  ���Լ�Ŀ¼
## @param classifyResultFileNew  �������ļ�
## @return ���ظò��������ڸ����ĸ���
##########################################
def NBprocess(index,traindir,testdir,classifyResultFileNew):
    crWriter = open(classifyResultFileNew,'w')
    # traindir = 'TrainSample0'
    # testdir = 'TestSample0'
    #������k�´�C�ĳ��ִ�������k�ܴ���
    cateWordsProb, cateWordsNum = getCateWordsProb(traindir)
    trainDirFiles = listdir(traindir)#all categories
    
    #ѵ�������ܴ���
    trainTotalNum = sum(cateWordsNum.values())
    print 'trainTotalNum: %d' % trainTotalNum
    
    
    savetofile(u'model/'+str(index)+'.model',(trainDirFiles,cateWordsProb, cateWordsNum))

    #��ʼ�Բ�������������
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
                print bestCate
            crWriter.write('%s %s\n' % (testSample[j],bestCate))
    crWriter.close()

def classify(modelname,str):
    testFilesWords=list(lineProcess(str))
    #print testFilesWords
    trainDirFiles,cateWordsProb, cateWordsNum = loadtovar(modelname)
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
## @param traindir       ��k
## @param testFilesWords ĳ�������ĵ�
## @param cateWordsNum   ѵ������k�µ������� <��Ŀ����������>
## @param totalWordsNum  ѵ������������
## @param cateWordsProb  ѵ������k�´�c���ֵĴ��� <��Ŀ_���� ,ĳ���ʳ��ִ���>
## ���� �������� =����k�е���i����Ŀ+0.0001��/����k�е�������+ѵ�������������൥��������
## ���� ������� =����k�е���������/��ѵ�������������൥��������
#################################################
def computeCateProb(traindir,testFilesWords,cateWordsNum,\
                    totalWordsNum,cateWordsProb):
    prob = 0
    wordNumInCate = cateWordsNum[traindir]  # ��k�µ������� <��Ŀ����������>
    for i in range(len(testFilesWords)):
        keyName = traindir + '_' + testFilesWords[i]
        if cateWordsProb.has_key(keyName):
            testFileWordNumInCate = cateWordsProb[keyName] # ��k�´�c���ֵĴ���
        else: testFileWordNumInCate = 0.0
        xcProb = log((testFileWordNumInCate + 0.0001) / (wordNumInCate + totalWordsNum))  # ���������ܶ��С������������
                 
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
    print 'rightCount : %d  rightCate: %d' % (rightCount,len(rightCateDict))
    accuracy = rightCount/len(rightCateDict)
    print 'accuracy %d : %f' % (k,accuracy)
    return accuracy
    
    
#############################################################################
## ����ÿ�ε����Ĳ�����������ע��
def step1():
    createFiles()
    filterSpecialWords()
    for i in range(10):
        classifyRightCate = 'temp/classifyRightCate' + str(i) + '.txt'
        createTestSample(i,classifyRightCate)
##############################################################################
## bayes�Բ����ĵ�������
def step2():
    for i in range(10):       
        print i
        traindir = 'temp/TrainSample' + str(i)
        testdir = 'temp/TestSample' + str(i)
        classifyResultFileNew = 'temp/classifyResultFileNew' + str(i) + '.txt'
        NBprocess(i,traindir,testdir,classifyResultFileNew)
##############################################################################
## ����׼ȷ��
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