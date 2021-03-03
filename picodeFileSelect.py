import picodeWindows
import os
from PyQt5 import QtWidgets
import random
from PIL import Image
def code(big_img, small_img,step):

    big_w, big_h = big_img.size
    small_w, small_h = small_img.size

    dst_im = big_img.copy()

    for i in range(0, small_w):
        for j in range(0, small_h):
            map_x = int( i*step + step*0.5 )
            map_y = int( j*step + step*0.5 )

            if map_x < big_w and map_y < big_h :
                dst_im.putpixel( (map_x, map_y), small_img.getpixel( (i, j) ) )

    return dst_im
def decode(big_img, small_img,step):
    big_w, big_h = big_img.size
    small_w, small_h = small_img.size
    dst_im = small_img.copy()
    initial=(step/2)
    initial=int(initial)
    for i in range(initial, big_w,step):

        for j in range(initial, big_h,step):
            map_x = int( i/step-0.5 )
            map_y = int( j/step-0.5 )
            dst_im.putpixel( (map_x, map_y), big_img.getpixel( (i, j) ) )

    return dst_im
def random_colour():
    return random.randint(0,255),random.randint(0,255),random.randint(0,255)
class Window(picodeWindows.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.uncode = False #未加密的小文件
        self.ampTimes = 2
        self.backPic = False #将嵌入小文件的背景
        self.coded =False #加密完成的文件
        self.filePathC= '' #已加密的图片的地址
        self.filePathD = '' #未加密的图片的地址
        self.fileToCode.clicked.connect(self.picToCode)

        self.fileToDecode.clicked.connect(self.picToDecode)
        self.toCode.clicked.connect(self.codePic)
        self.toDecode.clicked.connect(self.decodePic)
        self.codeTimes2.clicked.connect(lambda :self.selectTimes(2))
        self.codeTimes4.clicked.connect(lambda :self.selectTimes(4))
        self.codeTimes6.clicked.connect(lambda :self.selectTimes(6))
        self.codeTimes8.clicked.connect(lambda :self.selectTimes(8))
        self.toSaveC.clicked.connect(lambda: self.savePic(self.filePathC,"coded"))
        self.toSaveD.clicked.connect(lambda: self.savePic(self.filePathD,"uncoded"))
#打开需要加密的图片
    def selectTimes(self,time):
        self.ampTimes = time
        str1="已选择缩放倍率为"+str(self.ampTimes)
        QMessageBox.information(self, "提示", self.tr(str1))
    def picToCode(self):
        self.filePathC, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "open a pic", "", "*.png;;")#打开选择文件的对话框
        self.toCodeAddress.append(self.filePathC)#将地址输入到文本框
#打开需要解密的文件
    def picToDecode(self):
        self.filePathD, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "open a pic", "", "*.png;;")
        self.toDecodedAddress.setText(self.filePathD)#将地址输入到文本框
    def codePic(self):
        if self.filePathC == ''  :
            QMessageBox.information(self, "提示", self.tr("没有选择图片文件！"))
            return 0
        self.uncode = Image.open(self.filePathC)
        (x,y)=self.uncode.size
        xb=x*self.ampTimes
        yb=y*self.ampTimes
        self.backPic= Image.new('RGB', (xb, yb), random_colour())#制作背景图，被加密图片的6*6倍大小
        self.coded=code(self.backPic,self.uncode,self.ampTimes)
        self.coded.show()
    def decodePic(self):
        if self.filePathD == '':
            QMessageBox.information(self, "提示", self.tr("没有选择图片文件！"))
            return 0
        self.coded=Image.open(self.filePathD)
        (x,y) = self.coded.size
        xb = x / self.ampTimes
        yb = y / self.ampTimes
        self.uncode=self.coded.resize((int(xb),int(yb)))#制作解密后图片，加密图片的1/times^2大小
        self.uncode = decode(self.coded, self.uncode,self.ampTimes)
        if  self.uncode==2 and 4 and 6 and 8:
            str1="正确放大倍率为"+self.uncode
            QMessageBox.information(self, "提示", self.tr(str1))
            self.uncode=None
            return 0
        self.uncode.show()
    def savePic(self,filePath,name):
        if filePath == '':
            QMessageBox.information(self, "提示", self.tr("没有图片文件！"))
            return 0
        name=name+".png"
        self.coded.save(name)
        self.filePath="已保存到"+os.getcwd()+'\\coded.png'
        QMessageBox.information(self, "提示", self.tr(self.filePath))
        self.coded=None
        self.uncode=None
        return 0
