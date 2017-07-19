# -*- coding:utf-8 -*-

import cv2
import matplotlib.pyplot as plt
import imutils
from imutils.perspective import four_point_transform
from count_blocks import *

# 读入图片
image = cv2.imread("1.jpg")
# 转换为灰度图像
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# 高斯滤波
blurred = cv2.GaussianBlur(gray, (3, 3), 0)
# 自适应二值化方法
blurred=cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,51,5)
# ret,threshed = cv2.threshold(blurred,125,255,cv2.THRESH_BINARY)  # 二值化

# 最外圈加几层
blurred=cv2.copyMakeBorder(blurred,5,5,5,5,cv2.BORDER_CONSTANT,value=(255,255,255))


# -------------形态学处理------------
# 结构元素
# cross = cv2.getStructuringElement(cv2.MORPH_CROSS,(5,5)) #十字形
square = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)) #方形

# morph_c = cv2.dilate(blurred,cross)
# morph_c = cv2.erode(morph_c,cross)

morph_s = cv2.dilate(blurred,square)
morph_s = cv2.erode(morph_s,square)


# -----------canny边缘检测---------------
# edged = cv2.Canny(blurred, 50, 150)
edged = cv2.Canny(morph_s, 50, 150)


# --------------------轮廓--找四个顶点-------------------
cnts = cv2.findContours(edged, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
docCnt = None
# 确保至少有一个轮廓被找到
if len(cnts) > 0:
    # 将轮廓按大小降序排序
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    # 对排序后的轮廓循环处理
    for c in cnts:
        # 获取近似的轮廓
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # 如果近似轮廓有四个顶点，那么就认为找到了答题卡
        if len(approx) == 4:
            docCnt = approx
            break

# 展示寻找四个顶点的结果
newimage=image.copy()
for i in docCnt:
    # circle函数为在图像上作图，新建了一个图像用来演示四角选取
    cv2.circle(newimage, (i[0][0],i[0][1]), 50, (255, 0, 0), -1)


# ---------------四点变换------------------
paper = four_point_transform(image, docCnt.reshape(4, 2))
warped = four_point_transform(gray, docCnt.reshape(4, 2))


# ---------------重塑图像及预处理------------------
width1=2400
height1=2800
# 对灰度图应用二值化算法
thresh=cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,53,2)
# 重塑可能用到的图像
thresh = cv2.resize(thresh, (width1, height1), cv2.INTER_LANCZOS4)
paper2 = cv2.resize(paper, (width1, height1), cv2.INTER_LANCZOS4)

# 均值滤波
# ChQImg = cv2.blur(thresh, (23, 23))

# 形态学
square2 = cv2.getStructuringElement(cv2.MORPH_RECT,(20,20)) #方形
square3 = cv2.getStructuringElement(cv2.MORPH_RECT,(30,30)) #方形
morph_s2 = cv2.dilate(thresh,square2)
morph_s2 = cv2.erode(morph_s2,square3)


# ---------------------------寻找黑块坐标----------------
# 在二值图像中查找轮廓
Answer = []
cnts = cv2.findContours(morph_s2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(len(cnts[0]),len(cnts[1]),len(cnts[2]))
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
for c in cnts:
     # 计算轮廓的边界框，然后利用边界框数据计算宽高比
      (x, y, w, h) = cv2.boundingRect(c)
      if (w > 100 & h > 20)and y>900 and y<2000:
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # 绘制中心及其轮廓
            cv2.drawContours(paper2, c, -1, (0, 0, 255), 5, lineType=0)
            cv2.circle(paper2, (cX, cY), 7, (255, 255, 255), -1)
            # 保存题目坐标信息
            Answer.append((cX, cY))
print(Answer)

# ---------------------计算题号---------------- ???????????????????????????????
# IDAnswer=[]
# for i in Answer:
#     for j in range(0,len(xt1)-1):
#         if i[0]>xt1[j] and i[0]<xt1[j+1]:
#             for k in range(0,len(yt1)-1):
#                 if i[1]>yt1[k] and i[1]<yt1[k+1]:
#                     judge0(j,k)
#                     IDAnswer.append(judge0(j,k))
IDAnswer=[]
for i in Answer:
    IDAnswer.append(judge0(i[0],i[1])) # ?????????????????????????????????????????

# ------------------对答案部分重新排序，以最好的方式输出---------------
IDAnswer.sort()
print(IDAnswer)
print(len(IDAnswer))

# --------------------中间结果展示------------------------
cv2.namedWindow("aa",0)
cv2.imshow("aa",blurred)
# cv2.namedWindow("bb",0)
# cv2.imshow("bb",morph_c)
cv2.namedWindow("cc",0)
cv2.imshow("cc",morph_s)
cv2.namedWindow("dd",0)
cv2.imshow("dd",edged)
cv2.namedWindow("ee",0)
cv2.imshow("ee",newimage)
cv2.namedWindow("ff",0)
cv2.imshow("ff",paper)
cv2.namedWindow("gg",0)
cv2.imshow("gg",warped)
cv2.namedWindow("hh",0)
cv2.imshow("hh",thresh)
cv2.namedWindow("ii",0)
cv2.imshow("ii",morph_s2)
cv2.namedWindow("jj",0)
cv2.imshow("jj",paper2)

# 按ESC销毁所有窗口
while(1):
    if(cv2.waitKey(30)==27):
        cv2.destroyAllWindows()
        break

