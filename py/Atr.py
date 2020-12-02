#!/usr/bin/python
# -*- coding:utf8 -*-
import tushare as ts
import datetime
import time as ptime
from tkinter import *


ts.set_token('7d47faf869317c68fa8d52bc1a70aa9ca70815ac4fdd93b899f81ba8')
pro = ts.pro_api()

tsCode = '002044.SZ'
dayCnt = 40


init_window = Tk()



class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name


    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("Monkey Stock v1.0")           #窗口名
        #self.init_window_name.geometry('320x160+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1068x681+10+10')
        #self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.init_data_label = Label(self.init_window_name, text="输入神秘代码")
        self.init_data_label.grid(row=0, column=0)


        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)


        #文本框
        self.init_data_Text = Text(self.init_window_name, width=67, height=10)  #原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=70, height=49)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)

        #按钮
        self.genAtrBtn = Button(self.init_window_name, text="生成ATR", 
        bg="lightblue", width=10,command = self.genAtrFunc)  # 调用内部方法  加()为直接调用
        self.genAtrBtn.grid(row=6, column=11)

    #功能函数
    def genAtrFunc(self):
    	self.excuteProgram()

    #获取当前时间
    def get_current_time(self):
	    current_time = ptime.strftime('%Y-%m-%d %H:%M:%S',ptime.localtime(ptime.time()))
	    return current_time


    def getdate(self,time,beforeOfDay):
        today = time
        offset = datetime.timedelta(days = -beforeOfDay)
        re_date = (today + offset).strftime('%Y%m%d')
        return re_date

    def excuteProgram(self):
       
        tsCode = self.init_data_Text.get('1.0','end')
        tsCode.replace("\r", "")
        tsCode.replace("\n", "")
        tsCode = tsCode[0:len(tsCode)-1]
        print("excuteProgram === " + tsCode , len(tsCode))
        sDate = self.getdate(datetime.datetime.now(),80)
        eDate = self.getdate(datetime.datetime.now(),0)
        # 自定义时间,跨度超过四个月建议
        # sDate = "20200614"
        # eDate = "20201001"
        # tsCode = 
        self.result_data_Text.delete(0.0,END)
        df = pro.daily(ts_code = tsCode , start_date = sDate, end_date = eDate)
        arr = []

        for x in range(1,dayCnt+1):
            indexxx = dayCnt - x 
            curDate = df.trade_date[indexxx]
            ci = df.close[indexxx]
            hi = df.high[indexxx]
            li = df.low[indexxx]
            cim = df.close[indexxx + 1]
            tri = max(hi,cim) - min(li,cim)
            tempDic = {'tri':tri , 'curDate':curDate }
            arr.append(tempDic)


        # print(arr)
        #计算最近20天的 平均atr
        for x in range(0,20):
            ind = x + 20  #从数组的第20开始
            if ind < len(arr): 
                totalTri = 0
                for x1 in range(0,20):
                    ind2 = ind - x1 
                    totalTri += arr[ind2]['tri']
                curDayTri = arr[ind]['tri']
                atr = (totalTri/20 * 19 + curDayTri)/20
                finalStr = ("date" , arr[ind]['curDate'] ,"tri", round(arr[ind]['tri'],3) ,"atr",round(atr,3))
                print("finalStr",finalStr)
                self.write_log_to_Text(finalStr)


    #日志动态打印
    def write_log_to_Text(self,logmsg):
        current_time = self.get_current_time()
        logmsg_in =  str(logmsg) + "\n"      #换行
        self.result_data_Text.insert(END, logmsg_in)
        # LOG_LINE_NUM = LOG_LINE_NUM + 1
        # else:
            # self.log_data_Text.delete(1.0,2.0)
            # self.log_data_Text.insert(END, logmsg_in)


ZMJ_PORTAL = MY_GUI(init_window)
ZMJ_PORTAL.set_init_window()

init_window.mainloop()





# t——当日；
# n——时间长度；
# Ci——第i日的收盘价；
# Hi——第i日的最高价；
# Li——第i日的最低价。
# 计算公式：
# 均幅指标
# 均幅指标
# 其中：
# TRi = max(Hi,Ci-1)-min(Li,Ci-1)
# 注：一般取n=14
# ，m=6


# def GetTri(curDayData,lastDayData):
	# Hi = curDayData.
	# pro.daily(ts_code = tsCode , start_date = sDate, end_date = eDate)


#近20个工作日

# for x in df:
	# print(x)
	# print(y)

# print(df)