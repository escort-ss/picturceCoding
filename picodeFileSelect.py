import picodeWindows
from os import getcwd
from  PySide2.QtWidgets import QMainWindow,QMessageBox,QFileDialog
from random import randint
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
    if big_w/step!=big_w/step or big_w%step!=0:
        return "fault"
    dst_im = small_img.copy()
    initial=(step/2)
    initial=int(initial)
    for i in range(initial, big_w,step):
        for j in range(initial, big_h,step):
            map_x = int( i/step-0.5 )
            map_y = int( j/step-0.5 )
            dst_im.putpixel( (map_x, map_y), big_img.getpixel( (i, j) ) )
    return dst_im
class Window(picodeWindows.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.uncode = False #未加密的小文件
        self.ampTimes = 2
        self.backPic = False #将嵌入小文件的背景
        self.coded =False #加密完成的文件
        self.filePathC= '' #已加密的图片的地址
        self.filePathD = '' #未加密的图片的地址
        self.filePathB=''#底片的地址
        self.fileToBackPic.clicked.connect(self.selectBackPic)
        self.defaultColor.clicked.connect(self.clearBackPic)
        self.fileToCode.clicked.connect(self.picToCode)
        self.fileToDecode.clicked.connect(self.picToDecode)
        self.toCode.clicked.connect(self.codePic)
        self.toDecode.clicked.connect(self.decodePic)
        self.codeTimes2.clicked.connect(lambda :self.selectTimes(2))
        self.codeTimes4.clicked.connect(lambda :self.selectTimes(4))
        self.codeTimes6.clicked.connect(lambda :self.selectTimes(6))
        self.codeTimes8.clicked.connect(lambda :self.selectTimes(8))
        self.toSaveC.clicked.connect(lambda: self.savePic(self.filePathC,"coded"))
        self.toSaveD.clicked.connect(lambda: self.savePic(self.filePathD,"uncoded"))#打开需要加密的图片
    def clearBackPic(self):
        self.backPic = False
        self.filePathB = ''
    def random_colour(self):
        color = randint(0, 255), randint(0, 255), randint(0, 255)
        (x, y) = self.uncode.size
        xb = x * self.ampTimes
        yb = y * self.ampTimes
        self.backPic = Image.new('RGB', (xb, yb), color)
    def selectTimes(self,time):
        self.ampTimes = time
        str1="已选择缩放倍率为"+str(self.ampTimes)
        QMessageBox.information(self, "提示", self.tr(str1))
    def picToCode(self):
        self.filePathC, filetype = QFileDialog.getOpenFileName(self, "open a pic", "", "*.png;;")#打开选择文件的对话框
        self.toCodeAddress.append(self.filePathC)#将地址输入到文本框
#打开需要解密的文件
    def picToDecode(self):
        self.filePathD, filetype = QFileDialog.getOpenFileName(self, "open a pic", "", "*.png;;")
        self.toDecodedAddress.setText(self.filePathD)#将地址输入到文本框

    def codePic(self):
        if self.filePathC == ''  :
            QMessageBox.information(self, "提示", self.tr("没有选择需加密的图片文件！"))
            return 0
        elif self.filePathB == '' :
            QMessageBox.information(self, "提示", self.tr("没有选择底片文件！,默认将使用随机纯色图片"))
            self.uncode = Image.open(self.filePathC)
            self.random_colour()
            self.coded = code(self.backPic, self.uncode, self.ampTimes)
            self.coded.show()
            return 0
        else:
            self.backPic= Image.open(self.filePathB)
        self.uncode = Image.open(self.filePathC)
        (x,y)=self.uncode.size
        (xb,yb)=self.backPic.size
        if xb/x <= yb/y:
            self.backPic=self.backPic.resize((x,int(yb*x/xb)+1))
        else:
            self.backPic=self.backPic.resize((int(xb*y/yb)+1,y))
        self.backPic=self.backPic.crop((0, 0, x, y))
        xb=x*self.ampTimes
        yb=y*self.ampTimes
        self.backPic=self.backPic.resize((xb,yb))
        self.coded=code(self.backPic,self.uncode,self.ampTimes)
        self.coded.show()
        return 0
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
        if  self.uncode=="fault":
            str1="图片分辨率有误"
            QMessageBox.information(self, "提示", self.tr(str1))
            self.uncode=None
            self.coded=None
            return 0
        self.uncode.show()
        return 0
    def savePic(self,filePath,name):

        if filePath == '':
            QMessageBox.information(self, "提示", self.tr("没有图片文件！"))
            return 0
        if name == 'coded':
            name=str(self.ampTimes)+'×'+str(self.ampTimes)+'Times'+name+".png"
            self.coded.save(name)
        else:
            name=name+".png"
            self.uncode.save(name)
        self.filePath="已保存到"+getcwd()+'\\'+name
        QMessageBox.information(self, "提示", self.tr(self.filePath))
        self.coded=None
        self.uncode=None
        return 0
    def selectBackPic(self):
        self.filePathB, filetype = QFileDialog.getOpenFileName(self, "open a pic", "", "*.png;;")#打开选择文件的对话框
        self.toBackPicAddress.append(self.filePathB)
