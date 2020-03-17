'''
@Author: wentaoStudy
@Date: 2020-03-17 15:07:30
@LastEditTime: 2020-03-17 23:05:39
@LastEditors: wentaoStudy
@Email: 2335844083@qq.com
'''
from PyQt5.QtWidgets import QWidget , QApplication , QPushButton , QLabel , QVBoxLayout , QScrollArea , QFrame
from PyQt5.QtGui import QPixmap 
from PyQt5.QtCore import *
import sys , os
import SetPaper


class picLabel(QLabel):
    def __init__(self , parent = None):
        super(picLabel , self).__init__(parent)

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

    def initUi(self):
        self.setWindowTitle("Bing壁纸")
        self.vBoxLayout = QVBoxLayout()
        imageFiles = os.listdir("images")
        self.pictureLabelList = []
        for dir in imageFiles:
            if not os.path.isdir('images//' + dir):
                labelTemp = picLabel()
                labelTemp.setObjectName('images//' + dir)
                labelTemp.setPixmap(QPixmap('images//' + dir).scaled(QSize(320 , 180)))
                self.pictureLabelList.append(labelTemp)
        for label in self.pictureLabelList:
            self.vBoxLayout.addWidget(label)

        scroll = QScrollArea()
        frame = QFrame(scroll)
        frame.setLayout(self.vBoxLayout)
        scroll.setWidget(frame)
        
        layout = QVBoxLayout()
        layout.addWidget(scroll)
        self.setLayout(layout)
        
    def labelClicked(self):
        label = self.sender()
        SetPaper.setWallPaper(label.objectName)
        print(label.objectName)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BingPaperDesktop()
    window.show()
    sys.exit(app.exec_())

                

