#encoding=utf-8
import sys
from numpy import *
import kNN



#datingDataMat,datingLabels = kNN.file2matrix('thefile.csv','\t')
#print datingDataMat
#bayes.testingNB2(datingDataMat,datingLabels)


kNN.commonClassTest('output.csv','\t',0.2);
