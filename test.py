'''
@Author: wentaoStudy
@Date: 2020-06-15 21:00:31
@LastEditTime: 2020-06-15 21:04:34
@LastEditors: wentaoStudy
@Email: 2335844083@qq.com
'''

from datetime import datetime , timedelta


#返回图片是多少天前获取的，例如今天获取的返回0昨天获取的返回1
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

print(getImageOverNowTime("images/aliRiceHarvest_ZH-CN9267319542_2020_5_14.jpg"))