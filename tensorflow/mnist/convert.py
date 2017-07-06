# -*- coding: UTF-8 -*-
from PIL import Image
from tools.NeuralNet import *
# ��ȡѵ���õ�ģ��

img = Image.open('1.bmp').convert('L')

# resize�Ĺ���
if img.size[0] != 28 or img.size[1] != 28:
    img = img.resize((28, 28))

# �ݴ�����ֵ��һά����
arr = []

for i in range(28):
    for j in range(28):
        # mnist �����ɫ��0�����ɫ����������1.0�����ɫ
        pixel = 1.0 - float(img.getpixel((j, i)))/255.0
        # pixel = 255.0 - float(img.getpixel((j, i))) # �����0-255����ɫֵ
        arr.append([pixel])

        
INPUT = 28*28
OUTPUT = 10
net = NeuralNet([INPUT, 40, OUTPUT])
net.load()


predicted = net.predict(arr)
        
print predicted