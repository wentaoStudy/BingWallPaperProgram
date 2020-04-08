'''
@Author: wentaoStudy
@Date: 2020-03-17 15:07:30
@LastEditTime: 2020-04-08 09:09:31
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
        imageFiles = os.listdir("images")
        for dir in imageFiles:
            if not os.path.isdir('images//' + dir):
                imageTime = (os.path.getmtime('images//' + dir))
                if imageTime - toDay > 0 :
                    ifDownload = False
        return ifDownload

class PicLabel(QLabel):
    def __init__(self , parent = None):
        super(PicLabel , self).__init__(parent)

    def mousePressEvent(self , e):
        super().mousePressEvent(e)
        print(str(self.objectName()))
        SetPaper.setWallPaper(str(self.objectName()))
        print("鼠标单击")

    # def mouseReleaseEvent(self , QMouseEvent):
    #     SetPaper.setWallPaper(label.objectName)
    #     print("鼠标单击")

class BingPaperDesktop(QWidget):
    def __init__(self):
        super(BingPaperDesktop , self).__init__()
        self.initUi()
        self.downloadThread = DownThread()
        self.downloadThread.start()
        self.downloadThread.end.connect(self.end)

    def picPassTime(path):
        pass

    def initUi(self):
        self.setWindowTitle("Bing壁纸")
        self.vBoxLayout = QVBoxLayout()
        imageFiles = os.listdir("images")
        self.pictureLabelList = []
        now = datetime.now()
        sevenDaysAgo = (now - timedelta(days=7)).timestamp()
        for dir in imageFiles:
            if not os.path.isdir('images//' + dir):
                labelTemp = PicLabel()
                labelTemp.setObjectName('images//' + dir)
                imageTime = (os.path.getmtime('images//' + dir))
                if imageTime < sevenDaysAgo:
                    os.remove('images//' + dir)
                else:
                    labelTemp.setPixmap(QPixmap('images//' + dir).scaled(QSize(320 , 180)))
                    self.pictureLabelList.append(labelTemp)
        for label in self.pictureLabelList:
            self.vBoxLayout.addWidget(label)

        scroll = QScrollArea()
        scroll.setWidgetResizable = True
        self.frame = QFrame(scroll)
        self.frame.setLayout(self.vBoxLayout)
        scroll.setWidget(self.frame)
        
        layout = QVBoxLayout()
        layout.addWidget(scroll)
        
        #系统右下角图标
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

        #系统图标
        self.setWindowIcon(QIcon("python.png"))

        self.setLayout(layout)
        
    def labelClicked(self):
        label = self.sender()
        SetPaper.setWallPaper(label.objectName)
        print(label.objectName)

    def end(self):

        for label in self.pictureLabelList:
            self.vBoxLayout.removeWidget(label)

        imageFiles = os.listdir("images")
        self.pictureLabelList = []
        now = datetime.now()
        sevenDaysAgo = (now - timedelta(days=7)).timestamp()
        toDay = datetime(now.year , now.month , now.day , 0 , 0 , 0 ,0).timestamp()
        for dir in imageFiles:
            if not os.path.isdir('images//' + dir):
                labelTemp = PicLabel()
                labelTemp.setObjectName('images//' + dir)
                imageTime = (os.path.getmtime('images//' + dir))
                if imageTime < sevenDaysAgo:
                    os.remove('images//' + dir)
                elif imageTime - toDay > 0 :
                    print(toDay , imageTime)
                    labelTemp.setPixmap(QPixmap('images//' + dir).scaled(QSize(320 , 180)))
                    self.pictureLabelList.append(labelTemp)
        self.vBoxLayout = QVBoxLayout()
        # self.vBoxLayout.setGeometry(QRect(self.vBoxLayout.geometry().x() ,self.vBoxLayout.geometry().y() , self.vBoxLayout.geometry().width() , self.vBoxLayout.geometry().height() + 180 ))
        for label in self.pictureLabelList:
            self.vBoxLayout.addWidget(label)
            
    def tryIconQuitClicked(self):
        sys.exit(app.exec_())

    def tryIconMainWindowHide(self):
        self.setVisible(False)
    
    def tryIconMainWindowShow(self):
        self.setVisible(True)

    #重写系统关闭窗口事件，让关闭窗口变成隐藏窗口
    def closeEvent(self, event):
        event.ignore()
        self.tryIconMainWindowHide()

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
    window.resize(400,360)
    window.show()
    sys.exit(app.exec_())


                
