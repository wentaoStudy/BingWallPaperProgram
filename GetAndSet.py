'''
@Description: 
@Author: wentaoStudy
@Date: 2020-02-28 13:30:59
@LastEditTime: 2020-02-28 15:46:14
@LastEditors: wentaoStudy
@Email: 2335844083@qq.com
'''

import os
import re 
import requests 
import time
from PIL import Image
from lxml import etree
import win32gui ,win32con, win32api

def spiderPic(html):
    print('正在查找壁纸，请稍后......')
    html = etree.HTML(html)
    html_data = html.xpath('/html/head/link[@id="bgLink"]/@href')   #查找URL
    for addr in html_data:
        actaddr="https://cn.bing.com"+addr
        print('正在下载壁纸：'+addr[11:42]+'...')  #爬取的地址长度超过30时，用'...'代替后面的内容
 
        try:
            pics = requests.get(actaddr,timeout=10)  #请求URL时间（最大10秒）
        except requests.exceptions.ConnectionError:
            print('您当前请求的URL地址出现错误')
            continue

        localtime = time.localtime(time.time())
        filename=re.findall(r'([a-zA-Z0-9_-]*)_1920x1080.jpg',addr)
        fq = open('D:\\BingWallPaper\\' + (str(filename[0])+"_"+str(localtime.tm_year)+'_'+str(localtime.tm_mon)+'_'+str(localtime.tm_mday)+'.jpg'),'wb')     #下载图片，并保存和命名
        fq.write(pics.content)
        fq.close()
        # im = Image.open('D:\\BingWallPaper\\' + (str(filename[0])+"_"+str(localtime.tm_year)+'_'+str(localtime.tm_mon)+'_'+str(localtime.tm_mday)+'.jpg'))
        # im.show()
        setWallPaper('D:\\BingWallPaper\\' + (str(filename[0])+"_"+str(localtime.tm_year)+'_'+str(localtime.tm_mon)+'_'+str(localtime.tm_mday)+'.jpg'))

 
 
# 设置壁纸
def setWallPaper(filePath):
    baseFolder = os.path.dirname(filePath)
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

if __name__ == '__main__':
    print("现在时间："+time.asctime(time.localtime(time.time())) + ",为您下载今日Bing壁纸")
    result = requests.get('https://cn.bing.com/')
    # result = requests.get('https://cn.bing.com/?FORM=BEHPTB&ensearch=1')   #英文版网站的壁纸
    spiderPic(result.text)
    # setWallPaper(path)

