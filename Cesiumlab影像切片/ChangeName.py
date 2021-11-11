# WangXi 2021/09/08
# 修改切图名字

import os
import sys
import math

# 遍历文件夹
def InitFileName(file):
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            if os.path.splitext(f)[1] == '.png':
                os.rename(os.path.join(root, f),os.path.join(root,f+"_1"))

        # 遍历所有的文件夹
        #for d in dirs:
            #print("InitFileName")

def ChangeFileName(file):
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            if os.path.splitext(f)[1] == '.png_1':
                num = os.path.join(root, f).split("\\")
                length = len(num)
                newname = math.pow(2,int(num[length-1-2]))-1-int(os.path.splitext(f)[0])
                newname1 =  str(newname).split('.')[0]
                os.rename(os.path.join(root, f),os.path.join(root,newname1+".png"))
                print(os.path.join(root,newname1+".png"))

        # 遍历所有的文件夹
        #for d in dirs:
            #print("ChangeFileName")

def IsChangeName(file):
    #isChange = False
    for root, dirs, files in os.walk(file):
        for f in files:
            if f == '-1.png':
                print("数据已处理过，请勿重复处理！！！")
                #isChange = True
                sys.exit()
    #return isChange


def printContent():
    print(str(sys.argv[0]))


def main():
    IsChangeName(os.getcwd())
    InitFileName(os.getcwd())
    ChangeFileName(os.getcwd())
    print("数据处理成功！！！")
        

   


if __name__ == '__main__':
    main()
