# -*- coding:utf-8 -*-

# ------------根据坐标计算题号和答案------????????????????????????


def judgey0(y):
    if (y / 5 < 1):
        return  y + 1
    elif y / 5 < 2 and y/5>=1:
        return y % 5 + 20 + 1
    else:
        return y % 5 + 40 + 1


def judgex0(x):
    if(x%5==1):
        return 'A'
    elif(x%5==2):
        return 'B'
    elif(x%5==3):
        return 'C'
    elif(x%5==4):
        return 'D'


def judge0(x,y):
    if x/5<1 :
        #print(judgey0(y))
        return (judgey0(y),judgex0(x))
    elif x/5<2 and x/5>=1:
        #print(judgey0(y)+5)
        return (judgey0(y)+5,judgex0(x))
    elif x/5<3 and x/5>=2:
       # print(judgey0(y)+10)
        return (judgey0(y)+10,judgex0(x))
    else:
        #print(judgey0(y)+15)
        return (judgey0(y)+15,judgex0(x))