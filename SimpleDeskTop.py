'''
@Author: wentaoStudy
@Date: 2020-03-17 15:07:30
@LastEditTime: 2020-06-17 07:17:48
@LastEditors: wentaoStudy
@Email: 2335844083@qq.com
'''
from PyQt5.QtWidgets import *
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import sys , os ,time
import SetPaper , GetPaper
from datetime import datetime , timedelta
from multiprocessing import Process
import chardet
import re


#这里定义存放图片的文件夹名称，
#如果需要修改的话baseImageDir中的文件夹名称
#需要和baseImageDirName中的一致
baseImageDir = 'images//'
baseImageDirName = 'images'

#这里定义的是用来判断是否需要下载今天的Bing图片的线程
class DownThread(QThread):
    end = pyqtSignal()
    def __init__(self):
        super(DownThread , self).__init__()

    def run(self):
        while True:
            ifDown = self.detectedIfDownload()
            print(ifDown)
            if ifDown:
                GetPaper.getPaper()
                self.end.emit()
            time.sleep(1800)
    
    #判断是否需要下载图片
    def detectedIfDownload(self):
        ifDownload = True
        now = datetime.now()
        toDay = datetime(now.year , now.month , now.day , 0 , 0 , 0 ,0).timestamp()
        imageFiles = os.listdir(baseImageDirName)
        for dir in imageFiles:
            if not os.path.isdir(baseImageDir + dir):
                time_list = dir.split("_")
                try:
                    print(time_list)
                    imageTime = datetime(int(time_list[2]) , int(time_list[3]) , int((time_list[4]).split(".")[0]), 0 , 0 , 0 ,0).timestamp()
                    print(imageTime)
                except:
                    imageTime = toDay
                # imageTime = (os.path.getmtime(baseImageDir + dir))
                if imageTime - toDay >= 0 :
                    ifDownload = False
        return ifDownload

class ChangeImage(QThread):
    trigger = pyqtSignal()      #创建信号
    def __init__(self):
        super(ChangeImage , self).__init__()
        self.flag = 1   #自定义变量
        
    def run(self):
        imageFiles = os.listdir(baseImageDirName)
        count = 0
        # if self.flag == 1:
        while self.flag == 1:
            SetPaper.setWallPaper(baseImageDir + imageFiles[count%len(imageFiles)])
            count += 1
            time.sleep(900)

    def stop(self):     #重写stop方法
        self.flag = 0														# 2.
        print('线程退出了')

#返回图片是多少天前获取的，例如今天获取的返回0昨天获取的返回1 , 输入值为地址串
def getImageOverNowTime(string_path):
    #依据文件时间进行判断的方法 ：os.path.getmtime(path)
    #依据文件名进行判断的方式，如果依据文件时间进行判断会出现问题
    time_list = string_path.split("_")
    now = datetime.now()
    try:
        timeDelta = datetime(now.year , now.month , now.day , 0 , 0 , 0 ,0) - datetime(int(time_list[2]) , int(time_list[3]) , int((time_list[4]).split(".")[0]), 0 , 0 , 0 ,0)
        return timeDelta.days
    except:
        return -1
        
#重写QLabel，使其具有点击设置壁纸的功能
class PicLabel(QLabel):
    def __init__(self , parent = None):
        super(PicLabel , self).__init__(parent)

    def mousePressEvent(self , e):
        super().mousePressEvent(e)
        print(str(self.objectName()))
        SetPaper.setWallPaper(str(self.objectName()))
        print("鼠标单击")

class ListView(QListView):

    def __init__(self, *args, **kwargs):
        super(ListView, self).__init__(*args, **kwargs)
        # 模型
        self._model = QStandardItemModel(self)
        self.setModel(self._model)
        self.setContentsMargins(QMargins(0 ,0,0,0))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.initUi()

    def initUi(self):
        imageFiles = os.listdir(baseImageDirName)
        self.pictureLabelList = []
        for dir in imageFiles:
            if not os.path.isdir(baseImageDir + dir):
                if getImageOverNowTime(dir) > 7:
                    os.remove(baseImageDir + dir)
                else:
                    labelTemp = PicLabel()
                    labelTemp.setObjectName(baseImageDir + dir)
                    labelTemp.setPixmap(QPixmap(baseImageDir + dir).scaled(QSize(320 , 180)))
                    self.pictureLabelList.append(labelTemp)
        for label in self.pictureLabelList:
            item = QStandardItem()
            self._model.appendRow(item)  # 添加item

            # 得到索引
            index = self._model.indexFromItem(item)
            widget = label
            item.setSizeHint(QSize(320,180))  # 主要是调整item的高度
            # 设置自定义的widget
            self.setIndexWidget(index, widget)

class BingPaperDesktop(QWidget):
    def __init__(self):
        super(BingPaperDesktop , self).__init__()
        self.listPictureView = ListView()
        self.initUi()
        self.tryIcon()
        self.createDownLoadThread()
        self.createChangeImageThread()

    def initUi(self):
        self.setWindowTitle("Bing壁纸")
        #系统图标
        self.setWindowIcon(QIcon("python.png"))
        layout = QVBoxLayout()
        layout.addWidget(self.listPictureView)
        self.checkbox_change_image = QCheckBox("循环播放壁纸")
        self.checkbox_change_image.stateChanged.connect(self.change_image_checkbox_sate_change)
        layout.addWidget(self.checkbox_change_image)
        layout.addWidget(QCheckBox("允许其他来源图片"))
        self.setScrollBarStyle(self.listPictureView)
        #为layout设置margins
        layout.setContentsMargins(QMargins(0 ,0,0,0))
        self.setLayout(layout)

    #系统右下角图标
    def tryIcon(self):
        tryIcon = QSystemTrayIcon(self)
        tryIcon.setIcon(QIcon("python.png"))
        menu = QMenu()
        tryIconQuit = QAction("退出",self)
        tryIconQuit.triggered.connect(self.tryIconQuitClicked)
        menu.addAction(tryIconQuit)
        tryIconHide = QAction("隐藏" ,self)
        tryIconHide.triggered.connect(self.tryIconMainWindowHide)
        menu.addAction(tryIconHide)
        tryIconShow = QAction("显示" ,self)
        tryIconShow.triggered.connect(self.tryIconMainWindowShow)
        menu.addAction(tryIconShow)
        tryIcon.setContextMenu(menu)
        # tryIcon.activated.connect(self.tryIconMainWindowShow)
        tryIcon.show()

    #创建用于下载图片的线程
    def createDownLoadThread(self):
        self.downloadThread = DownThread()
        self.downloadThread.start()
        self.downloadThread.end.connect(self.downloadEnd)

    def createChangeImageThread(self):
        self.changeImageThread = ChangeImage()
        # self.changeImageThread.start()
        
    #为控件设置ScrollBar属性
    def setScrollBarStyle(self , widget):
        with open("Data/ScrollBar.qss", "rb") as fp:
            content = fp.read()
            encoding = chardet.detect(content) or {}
            content = content.decode(encoding.get("encoding") or "utf-8")
        widget.setStyleSheet(content)

    #当图片下载完毕会发生的事情
    def downloadEnd(self):
        imageFiles = os.listdir(baseImageDirName)
        self.pictureLabelList = []
        for dir in imageFiles:
            if not os.path.isdir(baseImageDir + dir):
                if getImageOverNowTime(dir) > 7:
                    os.remove(baseImageDir + dir)
                else:
                    labelTemp = PicLabel()
                    labelTemp.setObjectName(baseImageDir + dir)
                    labelTemp.setPixmap(QPixmap(baseImageDir + dir).scaled(QSize(320 , 180)))
                    self.pictureLabelList.append(labelTemp)
        for label in self.pictureLabelList:
            item = QStandardItem()
            self.listPictureView._model.appendRow(item)  # 添加item

            # 得到索引
            index = self.listPictureView._model.indexFromItem(item)
            widget = label
            item.setSizeHint(QSize(330,180))  # 主要是调整item的高度
            # 设置自定义的widget
            self.listPictureView.setIndexWidget(index, widget)
    
    def tryIconQuitClicked(self):
        sys.exit(app.exec_())

    def tryIconMainWindowHide(self):
        self.setVisible(False)
    
    def tryIconMainWindowShow(self):
        self.setVisible(True)

    # #重写系统关闭窗口事件，让关闭窗口变成隐藏窗口
    def closeEvent(self, event):
        event.ignore()
        self.tryIconMainWindowHide()

    def change_image_checkbox_sate_change(self):
        if self.checkbox_change_image.isChecked():
            self.changeImageThread = ChangeImage()
            self.changeImageThread.start()
        else:
            self.changeImageThread.stop()

def judgeAndCreateDir():
    baseDir = os.getcwd()
    ifDirExist = os.path.exists(baseImageDirName)
    if not ifDirExist:
        os.mkdir(baseImageDirName)

#对整个系统进行初始化
def systemInit():
    judgeAndCreateDir()
    
if __name__ == "__main__":
    systemInit()
    app = QApplication(sys.argv)
    window = BingPaperDesktop()
    # window.resize(320 , 180)
    # size = QSize(320 , )
    # window.setFixedSize(size)
    # window.setWindowFlags(Qt.FramelessWindowHint)
    window.show()
    sys.exit(app.exec_())


                
