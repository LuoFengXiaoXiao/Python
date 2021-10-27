
# _*_coding:utf-8 _*_
# @Time    : 2021/10/18 10:05
# @Author  : 风逝*落枫萧萧
# @FileName: TencentCourse.py
# @Software: vscode

import sqlite3 as db
import re
import os
import json
from tkinter import *
from Crypto.Cipher import AES


json_dic = {}


class Application(Frame):
    def __init__(self, master=None):
        self.master = master
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text='Hello, world!')
        self.helloLabel.pack()
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.pack()
        

    def hello(self):
        name = self.nameInput.get() or 'world'
        messagebox.showinfo('Message', 'Hello, %s' % name)

def OperateByDir(path: str=''):
    if path=='':
        cwd=os.getcwd()
        res=os.listdir(cwd)
        for i in res: 
            if ".sqlite" in i: 
                #l1 = i.rsplit(".")[0]+"."+i.rsplit(".")[1]
                #os.rename(os.path.join(cwd,i),os.path.join(cwd,l1))
                #os.rename(os.path.join(cwd,i),os.path.join(cwd,i+".sqlite"))
                db_fetcher(filename = i)
                mergeTS(filename = i)
                #print('什么鬼？')
        #修改合成之后视频的名字
        for i in res: 
            if ".sqlite" in i: 
                db_changeFileName(i)
        

def json_getFileName(filename:str):
    #修改文件名字
    #根据获得的Json文件修改
    '''
    读取Json文件(将其命名为Index,json)：
        1. "result"中的数组"terms"
        2. "terms"中的数组"chapter_info"
        3. "chapter_info"中的数组"sub_info"
        4. "sub_info"中的数组"task_info"
        5. "task_info"中的各个Object中的"name"是视频名字，"resid_list"是视频的识别码
    '''
    json_dic.clear()
    if not os.path.exists(filename):
        return
    with open(filename,encoding="utf-8") as f:
        data = json.load(f)
        #data1 = json.dumps(f)
        subdata = data['result']
        subdata1 = subdata['terms']
        #print('subdata type is {}'.format(type(subdata)))
        #print('subdata1 type is {}'.format(type(subdata1)))
        subdata2 = (subdata1[0])['chapter_info']
        #print('subdata2 type is {}'.format(type(subdata2)))
        #此时取到了json的文件夹目录，即
        '''
            "csid": 9196584,
            "sub_id": 0,
            "introduce": "",
            "name": "xxxx",
            "endtime": 0,
            "term_id": 100356835,
            "task_info": [],
            "bgtime": 0,
            "cid": 301049
        '''
        #其中name就是分段的地址，可用来判断文件夹
        subdata3 = (subdata2[0])['sub_info']
        #print('subdata3 type is {}'.format(type(subdata3)))
        for i in range(0,len(subdata3)):
            subdata4 = (subdata3[i])['task_info']
            max = len(subdata4)
            for j in range(0,max):
                json_dic[(subdata4[j])['resid_list']] = (subdata4[j])['name']
        #print(len(json_dic))

def db_changeFileName(filename: str):
    '''
    处理.sqlite文件的入口
    :param filename: .sqlite文件名
    :return:
    '''
    caches_table_name = 'caches'
    #连接到数据库
    con = db.connect(filename)
    #创建一个cursor，连接到数据库之后，需要打开游标，称之为Cursor，通过Cursor执行SQL语句，然后获得执行结果
    cu = con.cursor()
    result = cu.execute('SELECT * FROM {}'.format(caches_table_name))

    data = result.fetchall()
    Namekey = data[2][0]
    for key in json_dic:
        if Namekey.find(key)>0:
            videoFile = filename.split('.')[0]+'.mp4'
            if not os.path.exists(videoFile):
                return
            os.rename(filename.split('.')[0]+'.mp4',json_dic[key]+'.mp4')
            print(videoFile+' is change name to '+ json_dic[key]+'.mp4' + ' !!!')
            con.close()
            return
    con.close()
    
    



def db_getDumpNum(filename: str):
    '''
    处理.sqlite文件的入口
    :param filename: .sqlite文件名
    :return:
    '''
    caches_table_name = 'caches'
    #连接到数据库
    con = db.connect(filename)
    #创建一个cursor，连接到数据库之后，需要打开游标，称之为Cursor，通过Cursor执行SQL语句，然后获得执行结果
    cu = con.cursor()
    result = cu.execute('SELECT * FROM {}'.format(caches_table_name))

    data = result.fetchall()
    datalen = len(data)-2
    print('共有数据-{}'.format(datalen))
    con.close()

    return datalen
    
def db_getUiqueName(filename: str):
        cwd=os.getcwd()
        res=os.listdir(cwd)
        for i in res: 
            if ".sqlite" in i: 
                #l1 = i.rsplit(".")[0]+"."+i.rsplit(".")[1]
                #os.rename(os.path.join(cwd,i),os.path.join(cwd,l1))
                #os.rename(os.path.join(cwd,i),os.path.join(cwd,i+".sqlite"))
                db_fetcher(filename = i)
                mergeTS(filename = i)


def db_fetcher(filename: str):
    '''
    处理.sqlite文件的入口
    :param filename: .sqlite文件名
    :return:
    生成各个文件的片段
    '''

    caches_table_name = 'caches'
    #连接到数据库
    print('{} is working!!!'.format(filename))
    con = db.connect(filename)
    #创建一个cursor，连接到数据库之后，需要打开游标，称之为Cursor，通过Cursor执行SQL语句，然后获得执行结果
    cu = con.cursor()
    result = cu.execute('SELECT * FROM {}'.format(caches_table_name))

    data = result.fetchall()
    #获取解码符号,防止AES乱序
    for i in range(0, len(data)):
        if 'ke.qq.com' in data[i][0]:
            AES_KEY = data[i][1]
            print('AES is {}'.format(data[i][0]))
            break

    newName = filename.split('.')[0]
    

    #解码乱序问题
    #根据时间来解码
    #提取所有的start时间
    ls = []
    for i in range(0, len(data)):
        a = ''
        #ls.append(int(str(re.findall(r"start=(.+)&end=",data[i][0]))))
        for j in re.findall(r"start=(.+)&end=",data[i][0]):
            print('j is {}'.format(j)+'  i =  {}'.format(i) )
            a += str(j)
            #print('a = {}'.format(a))
            #print(a)
        #防止有一些没有start的数据
        if not a=='':
            ls.append(int(float(a)))
    
    #print(type(ls[0]))
    ls.sort()
    #print(ls)

    for i in range(2, len(data)):
        videoIndex = 0
        if 'start' in data[i][0]:
            a = ''
            for j in re.findall(r"start=(.+)&end=",data[i][0]):
                a += str(j)
            videoIndex = ls.index(int(a))
            raw = data[i][1]
            dump_name = newName + '-{}.ts'.format(videoIndex)
        plain = aes128_decrypt(raw=raw, key=AES_KEY, dump_file=dump_name)
        if plain:
            print('{} of {} dumped succeed'.format(i - 1, len(data)-2))
        else:
            print('{} of {} dumped failed'.format(i - 1, len(data)))

    con.close()


def aes128_decrypt(raw: bytes, key: bytes, iv: bytes = b'0000000000000000', dump_file: str = ''):
    '''
    二进制文件的AES-128解密
    :param raw: 原始二进制内容
    :param key: AES-128文件二进制内容（16bytes）
    :param iv: AES_IV
    :param dump_file: 保存文件名
    :return: 正常True，异常False
    '''
    data = raw
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plain = cipher.decrypt(data)
    try:
        open(dump_file, 'wb').write(plain)
        return True
    except Exception as e:
        print(e)
        return False

def mergeTS(filename: str):
    '''
    合并生成的TS文件
    可直接通过cmd合并'copy /b *.ts new.mp4'，但是默认按照名称的顺序，可自行尝试
    转换为mp4文件
    '''
    newName = filename.split('.')[0]+'.mp4'
    if os.path.exists(newName):
        #print('{} is exists !!!'.format(newName))
        os.remove(newName)


    num = db_getDumpNum(filename)
    #print(num)
    for i in range(0,num):
        print('当前视频编号-{}'.format(i))
        plain = filename.split('.')[0]+'-{}.ts'.format(i)
        if os.path.exists(plain):
            file = open(plain,'rb')
            try:
                with open(newName, 'ab+') as fs:
                    fs.write(file.read())
                    file.close()
                    os.remove(plain)
                
            except Exception as e:
                print('{} {} write error: {}'.format(newName,plain,e))

    fs.close()
    print(newName + ' merge done!!!')

    

def main():
    #print('main is run !!!')

    json_getFileName("Index.json")
    OperateByDir()
    
    #本来打算写个界面，目前没空，先不写了
    # app = Application()
    # # 设置窗口标题:
    # app.master.title('腾讯课堂转换器')
    # # 设置窗口大小和位置
    # screenWidth = app.winfo_screenwidth()  # 获取显示区域的宽度
    # screenHeight = app.winfo_screenheight()  # 获取显示区域的高度
    # width = 300  # 设定窗口宽度
    # height = 160  # 设定窗口高度
    # left = (screenWidth - width) / 2
    # top = (screenHeight - height) / 2

    # # 宽度x高度+x偏移+y偏移
    # # 在设定宽度和高度的基础上指定窗口相对于屏幕左上角的偏移位置
    # app.master.geometry("%dx%d+%d+%d" % (width, height, left, top))

    # # 主消息循环:
    # app.mainloop()

        
   

if __name__ == '__main__':
    main()









        