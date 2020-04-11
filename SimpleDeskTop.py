'''
@Author: wentaoStudy
@Date: 2020-03-17 15:07:30
@LastEditTime: 2020-04-11 14:36:49
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
        
    def detectedIfDownload(self):
        ifDownload = True
        now = datetime.now()
        toDay = datetime(now.year , now.month , now.day , 0 , 0 , 0 ,0).timestamp()
        imageFiles = os.listdir(baseImageDirName)
        for dir in imageFiles:
            if not os.path.isdir(baseImageDir + dir):
                imageTime = (os.path.getmtime(baseImageDir + dir))
                if imageTime - toDay > 0 :
                    ifDownload = False
        return ifDownload

#重写QLabel，使其具有点击设置壁纸的功能
class PicLabel(QLabel):
    def __init__(self , parent = None):
        super(PicLabel , self).__init__(parent)

    def mousePressEvent(self , e):
        super().mousePressEvent(e)
        print(str(self.objectName()))
        SetPaper.setWallPaper(str(self.objectName()))
        print("鼠标单击")

class BingPaperDesktop(QWidget):
    def __init__(self):
        super(BingPaperDesktop , self).__init__()
        self.initUi()
        self.tryIcon()
        self.createDownLoadThread()

    def initUi(self):
        self.setWindowTitle("Bing壁纸")
        #系统图标
        self.setWindowIcon(QIcon("python.png"))

        self.vBoxLayout = QVBoxLayout()
        imageFiles = os.listdir(baseImageDirName)
        self.pictureLabelList = []
        now = datetime.now()
        sevenDaysAgo = (now - timedelta(days=7)).timestamp()
        for dir in imageFiles:
            if not os.path.isdir(baseImageDir + dir):
                labelTemp = PicLabel()
                labelTemp.setObjectName(baseImageDir + dir)
                imageTime = (os.path.getmtime(baseImageDir + dir))
                if imageTime < sevenDaysAgo:
                    os.remove(baseImageDir + dir)
                else:
                    labelTemp.setPixmap(QPixmap(baseImageDir + dir).scaled(QSize(320 , 180)))
                    self.pictureLabelList.append(labelTemp)
        for label in self.pictureLabelList:
            self.vBoxLayout.addWidget(label)
        scroll = QScrollArea()
        self.frame = QFrame(scroll)
        self.frame.setLayout(self.vBoxLayout)
        scroll.setWidget(self.frame)
        #将scroll设置成没有边框
        scroll.setFrameShape(QFrame.NoFrame)
        #将scroll设置成横向没有scrollbar
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #为scrollbar设置style属性
        self.setScrollBarStyle(scroll)
        layout = QVBoxLayout()
        layout.addWidget(scroll)
        #为layout设置margins
        layout.setContentsMargins(QMargins(0 ,0,0,0))
        self.vBoxLayout.setContentsMargins(QMargins(0 ,0,0,0))
        self.frame.setContentsMargins(QMargins(5,5,5,5))
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

    #为控件设置ScrollBar属性
    def setScrollBarStyle(self , widget):
        with open("Data/ScrollBar.qss", "rb") as fp:
            content = fp.read()
            encoding = chardet.detect(content) or {}
            content = content.decode(encoding.get("encoding") or "utf-8")
        widget.setStyleSheet(content)

    #当图片下载完毕会发生的事情
    def downloadEnd(self):

        for label in self.pictureLabelList:
            self.vBoxLayout.removeWidget(label)

        imageFiles = os.listdir("images")
        self.pictureLabelList = []
        now = datetime.now()
        sevenDaysAgo = (now - timedelta(days=7)).timestamp()
        toDay = datetime(now.year , now.month , now.day , 0 , 0 , 0 ,0).timestamp()
        for dir in imageFiles:
            if not os.path.isdir(baseImageDir + dir):
                labelTemp = PicLabel()
                labelTemp.setObjectName(baseImageDir + dir)
                imageTime = (os.path.getmtime(baseImageDir + dir))
                if imageTime < sevenDaysAgo:
                    os.remove(baseImageDir + dir)
                elif imageTime - toDay > 0 :
                    print(toDay , imageTime)
                    labelTemp.setPixmap(QPixmap(baseImageDir + dir).scaled(QSize(320 , 180)))
                    self.pictureLabelList.append(labelTemp)
        # self.vBoxLayout.setGeometry(QRect(self.vBoxLayout.geometry().x() ,self.vBoxLayout.geometry().y() , self.vBoxLayout.geometry().width() , self.vBoxLayout.geometry().height() + 180 ))
        for label in self.pictureLabelList:
            self.vBoxLayout.addWidget(label)
            
    def tryIconQuitClicked(self):
        sys.exit(app.exec_())

    def tryIconMainWindowHide(self):
        self.setVisible(False)
    
    def tryIconMainWindowShow(self):
        self.setVisible(True)

    # #重写系统关闭窗口事件，让关闭窗口变成隐藏窗口
    # def closeEvent(self, event):
    #     event.ignore()
    #     self.tryIconMainWindowHide()

def judgeAndCreateDir():
    baseDir = os.getcwd()
    ifDirExist = os.path.exists("images")
    if not ifDirExist:
        os.mkdir("images")

#对整个系统进行初始化
def systemInit():
    judgeAndCreateDir()
    
if __name__ == "__main__":
    systemInit()
    app = QApplication(sys.argv)
    window = BingPaperDesktop()
    window.show()
    sys.exit(app.exec_())


                
