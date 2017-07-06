# -*- coding: UTF-8 -*-
from PIL import Image
from tools.NeuralNet import *
# 读取训练好的模型

img = Image.open('1.bmp').convert('L')

# resize的过程
if img.size[0] != 28 or img.size[1] != 28:
    img = img.resize((28, 28))

# 暂存像素值的一维数组
arr = []

for i in range(28):
    for j in range(28):
        # mnist 里的颜色是0代表白色（背景），1.0代表黑色
        pixel = 1.0 - float(img.getpixel((j, i)))/255.0
        # pixel = 255.0 - float(img.getpixel((j, i))) # 如果是0-255的颜色值
        arr.append([pixel])

        
INPUT = 28*28
OUTPUT = 10
net = NeuralNet([INPUT, 40, OUTPUT])
net.load()


predicted = net.predict(arr)
        
print predicted