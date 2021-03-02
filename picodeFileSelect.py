import picodeWindows
import os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
import random

from PIL import Image
def code(big_img, small_img):

    big_w, big_h = big_img.size
    small_w, small_h = small_img.size

    dst_im = big_img.copy()

    stepx = big_w/small_w
    stepy = big_h/small_h
    for i in range(0, small_w):
        for j in range(0, small_h):
            map_x = int( i*stepx + stepx*0.5 )
            map_y = int( j*stepy + stepy*0.5 )

            if map_x < big_w and map_y < big_h :
                dst_im.putpixel( (map_x, map_y), small_img.getpixel( (i, j) ) )

    return dst_im
def decode(big_img, small_img):

    big_w, big_h = big_img.size
    small_w, small_h = small_img.size

    dst_im = small_img.copy()

    stepx = big_w / small_w
    stepy = big_h / small_h
    for i in range(3, big_w,6):
        for j in range(3, big_h,6):
            map_x = int( i/stepx-0.5 )
            map_y = int( j/stepy-0.5 )

            dst_im.putpixel( (map_x, map_y), big_img.getpixel( (i, j) ) )

    return dst_im
def random_colour():
    return random.randint(0,255),random.randint(0,255),random.randint(0,255)
class Window(picodeWindows.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.uncode = False #未加密的小文件
        self.backPic = False #将嵌入小文件的背景
        self.coded =False #加密完成的文件
        self.filePathC= '' #已加密的图片的地址
        self.filePathD = '' #未加密的图片的地址
        self.fileToCode.clicked.connect(self.picToCode)#一个按钮的点击事件，响应函数为 def msg(self):
        self.fileToDecode.clicked.connect(self.picToDecode)  # 一个按钮的点击事件，响应函数为 def msg(self):
        self.toCode.clicked.connect(self.codePic)
        self.toDecode.clicked.connect(self.decodePic)
#打开需要加密的图片
    def picToCode(self):
        self.filePathC, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "open a pic", "", "*.png;;")#打开选择文件的对话框
        self.toCodeAddress.append(self.filePathC)#将地址输入到文本框
        jpg = QtGui.QPixmap( self.filePathC).scaled(self.toCodePic.width(), self.toCodePic.height())
        self.toCodePic.setPixmap(jpg)
#打开需要解密的文件
    def picToDecode(self):
        self.filePathD, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "open a pic", "", "*.png;;")
        self.toDecodedAddress.append(self.filePathD)#将地址输入到文本框
        jpg = QtGui.QPixmap(self.filePathD).scaled(self.toDecodePic.width(), self.toDecodePic.height())
        self.toDecodePic.setPixmap(jpg)
    def codePic(self):
        if self.filePathC == ''  :
            QMessageBox.information(self, "提示", self.tr("没有选择图片文件！"))
            return 0
        self.uncode = Image.open(self.filePathC)
        (x,y)=self.uncode.size
        xb=x*6
        yb=y*6
        self.backPic= Image.new('RGB', (xb, yb), random_colour())#制作背景图，被加密图片的6*6倍大小
        self.coded=code(self.backPic,self.uncode)
        self.coded.save('coded.png')
        self.filePathD=os.getcwd()+'\\coded.png'
        self.toDecodedAddress.append(self.filePathD)  # 将地址输入到文本框
        jpg = QtGui.QPixmap(self.filePathD)
        self.toDecodePic.setPixmap(jpg)
    def decodePic(self):
        if self.filePathD == '':
            QMessageBox.information(self, "提示", self.tr("没有选择图片文件！"))
            return 0
        self.coded=Image.open(self.filePathD)
        (x,y) = self.coded.size
        xb = x / 6
        yb = y / 6
        self.uncode=self.coded.resize((int(xb),int(yb)))#制作解密后图片，加密图片的1/36大小
        self.uncode = decode(self.coded, self.uncode)
        self.uncode.save('uncode.png')
        self.filePathC = os.getcwd() + '\\uncode.png'
        self.toCodeAddress.append(self.filePathC)  # 将地址输入到文本框
        jpg = QtGui.QPixmap(self.filePathC).scaled(self.toCodePic.width(), self.toCodePic.height())
        self.toCodePic.setPixmap(jpg)
