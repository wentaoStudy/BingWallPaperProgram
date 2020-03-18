'''
@Author: wentaoStudy
@Date: 2020-03-17 22:07:49
@LastEditTime: 2020-03-18 13:34:07
@LastEditors: wentaoStudy
@Email: 2335844083@qq.com
'''

import os
from PIL import Image
import win32gui ,win32con, win32api

def setWallPaper(filePath):
    baseFolder = os.getcwd() + "\\" + os.path.dirname(filePath)
    fileName = os.path.basename(filePath).split('.')[0] + '.bmp'
    bmpFile = os.path.join(baseFolder, fileName)
    if (not os.path.exists(fileName)):
        img = Image.open(filePath)
        img.save(bmpFile,'BMP')
        
    print(u'正在设置图片:%s为桌面壁纸...' % fileName)
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2") #2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, bmpFile, 1+2)
    print(u'成功应用图片:%s为桌面壁纸'  % fileName)
    os.remove('images\\' + fileName)