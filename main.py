import os
import sys
from cwtbag import frequencies
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QGridLayout, QFileDialog, QDialog
import heartrate
from multiprocessing import freeze_support
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import time
import numpy as np
from datawindow import *
from process_management import Manage_unit
from videoProcess import VideoManager
import pyqtgraph as pg

pg.setConfigOptions(leftButtonPan=False)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

#创建文件夹以便在里面存放txt
def makdir(filename, count=0, trait = False):
    try:
        timenow = time.localtime()
        if trait == False:
            if count == 0:
                os.makedirs(r"{}/心率文件{}年{}月{}日{}时{}分".format(filename,timenow.tm_year,timenow.tm_mon,timenow.tm_mday,timenow.tm_hour,timenow.tm_min))
                return r"{}/心率文件{}年{}月{}日{}时{}分".format(filename,timenow.tm_year,timenow.tm_mon,timenow.tm_mday,timenow.tm_hour,timenow.tm_min)
            else:
                os.makedirs(r"{}/心率文件{}年{}月{}日{}时{}分({})".format(filename, timenow.tm_year,timenow.tm_mon,timenow.tm_mday,timenow.tm_hour,timenow.tm_min, count))
                return r"{}/心率文件{}年{}月{}日{}时{}分({})".format(filename, timenow.tm_year,timenow.tm_mon,timenow.tm_mday,timenow.tm_hour,timenow.tm_min, count)
        else:
            if count == 0:
                os.makedirs(r"{}/心率视频文件{}年{}月{}日{}时{}分".format(filename,timenow.tm_year,timenow.tm_mon,timenow.tm_mday,timenow.tm_hour,timenow.tm_min))
                return r"{}/心率视频文件{}年{}月{}日{}时{}分".format(filename,timenow.tm_year,timenow.tm_mon,timenow.tm_mday,timenow.tm_hour,timenow.tm_min)
            else:
                os.makedirs(r"{}/心率视频文件{}年{}月{}日{}时{}分({})".format(filename, timenow.tm_year,timenow.tm_mon,timenow.tm_mday,timenow.tm_hour,timenow.tm_min, count))
                return r"{}/心率视频文件{}年{}月{}日{}时{}分({})".format(filename, timenow.tm_year,timenow.tm_mon,timenow.tm_mday,timenow.tm_hour,timenow.tm_min, count)
    except:
        count += 1
        return makdir(filename, count)

#展示细节的窗口，里面就是一些表格控件
class datawin(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.child = Ui_Dialog()
        self.child.setupUi(self)
        self.pw2 = pg.PlotWidget(title="历史（8秒内）心率变动")
        # self.F = MyFigure(width=3, height=1, dpi=100)
        # self.gridlayout = QGridLayout(self.child.groupBox_2)
        # self.gridlayout.addWidget(self.F)
        # self.F1 = MyFigure(width=3, height=1, dpi=100)
        # self.gridlayout = QGridLayout(self.child.groupBox)
        # self.gridlayout.addWidget(self.F1)
        # self.F2 = MyFigure(width=3, height=1, dpi=100, config="cout")
        # self.gridlayout = QGridLayout(self.child.groupBox_3)
        # self.gridlayout.addWidget(self.F2)
        # self.F = MyFigure(width=3, height=1, dpi=100)
        # self.gridlayout = QGridLayout(self.child.groupBox_2)
        # self.gridlayout.addWidget(self.F)
        self.F3 = pg.PlotWidget(title="原始波形")
        # self.F3 = MyFigure(width=3, height=1, dpi=100, config="cout")
        self.gridlayout = QGridLayout(self.child.groupBox_4)
        self.gridlayout.addWidget(self.F3)
        self.F4 = pg.PlotWidget(title="count")
        self.gridlayout = QGridLayout(self.child.groupBox_5)
        self.gridlayout.addWidget(self.F4)

    def drawall(self, datain):
        begin = datain[4] - int(len(datain[1]) / datain[5])
        end = datain[4]
        # self.F1.updatecanvas1(datain[1],datain[3], begin, end, datain[5])
        # self.F2.updatecont(datain[2], begin, end, datain[5])
        # self.F4.updatecanvas(datain[9])
        # self.F.updatecanvas(datain[0])
        self.F3.plotItem.clear()
        self.F3.plotItem.plot([x for x in range(len(datain[8]))], datain[8], pen="b")
        # self.F4.plotItem.clear()
        # self.F4.plotItem.plot([x for x in range(len(datain[9]))], datain[9], pen="b")
        # self.F3.updatecanvas(datain[8])

#同时继承两个类！
class myapp(QMainWindow, heartrate.Ui_MainWindow):
    message = pyqtSignal(list)

    def todatabox(self, list):
        self.message.emit(list)

    def __init__(self):
        QMainWindow.__init__(self)
        heartrate.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # 下面是一些状态量，来判断·一些进程是否应该退出
        self.hr_part_visible = 0
        self.readstart = False
        self.wrt = False
        self.isclosing = False
        self.pstart = False
        self.camera_should_be_delete = False
        self.vstart = False
        self.deleting_camera = False
        self.deleting_video = False
        self.heartratesheetexist = False
        ####################################
        self.comboboxset()
        self.layoutset()#pyqtgraph画布设置
        self.actionset()#菜单栏按键设置
        self.canvasset()#画布设置用于画波形
        self.visibleset()#一些控件的显示设置
        ####################################
        self.dirnow = ""
        # self.samplingrate_input.setRange(30, 30)
        self.Admission = True
        self.heartrate_output.setText("")
        self.threshold = 3 #3秒起算
        self.time11 = 0#基本没用
        self.hrlist = []#储存心率模块
        self.multi = 10#基本没用
        self.count = 0
        self.time1 = 0

    #菜单栏设置
    def actionset(self):
        self.video_cancel.setEnabled(False)
        self.exit.setEnabled(False)
        self.start.triggered.connect(self.operation_start)
        self.exit.triggered.connect(self.just_cancel)
        self.video_option.triggered.connect(self.video_process1)
        self.video_cancel.triggered.connect(self.just_cancel)
    #画布设置用于绘制波形
    def canvasset(self):
        pass
        # self.F = MyFigure(width=3, height=1, dpi=100)
        # self.gridlayout = QGridLayout(self.wave_panel)
        # self.gridlayout.addWidget(self.F)
        # self.F1 = MyFigure(width=3, height=1, dpi=100)
        # self.gridlayout = QGridLayout(self.heartrate_fluctuate)
        # self.gridlayout.addWidget(self.F1)

    def visibleset(self):
        self.videoshow.setVisible(False)
        self.heartrate_modulevisible_set(False)
        self.video_state.setVisible(False)
        self.jindu.setVisible(False)
        self.jindu2.setVisible(False)
    #心率模块的显示与隐藏
    def heartrate_modulevisible_set(self, boolin):
        if boolin:
            self.hr_part_visible += 1
        if self.hr_part_visible == 2:
            self.hr_part_visible -= 1
        else:
            self.hrsheet.setVisible(boolin)
            self.heartrate_time.setVisible(boolin)
            self.on_time_hr_shower.setVisible(boolin)
            self.heartrate_output.setVisible(boolin)
            if boolin:
                # self.pw1 = pg.PlotWidget(title="模拟心率波形")
                self.pw2 = pg.PlotWidget(title="历史（8秒内）心率变动")
                # self.Graphs.addWidget(self.pw1)
                self.Graphs.addWidget(self.pw2)
            else:
                self.videoshow.setText(" ")
                try:
                    # self.Graphs.removeWidget(self.pw1)
                    self.Graphs.removeWidget(self.pw2)
                    # self.pw1.deleteLater()
                    self.pw2.deleteLater()
                except:
                    pass
            self.heartratesheetexist = boolin
            if not boolin:
                self.hr_part_visible = 0

    def layoutset(self):
        pass
        # self.pw1 = pg.PlotWidget(title="模拟心率波形")
        # self.pw2 = pg.PlotWidget(title="历史（8秒内）心率变动")
        # self.plot1 = self.pw1.plot([x for x in range(100)], pen = "r")
        # self.pw1 = pg.PlotWidget(title="绘制多条线")
        # self.pw2 = pg.PlotWidget(title="绘制条状图")
        # self.curve1 = self.pw1.plot(pen="y")

    def show_wave(self, datain):
        if self.heartratesheetexist:
            pass
            # self.pw1.plotItem.clear()
            # self.pw1.plotItem.plot([x for x in range(len(datain[0]))], datain[0], pen="r")
        # self.plot1.setData([50 for x in range(100)])
        # self.pw1.setData(datain)

    def show_hr(self, hr):
        if self.heartratesheetexist:
            self.heartrate_output.setText(str(int(hr)))
            self.pw2.plotItem.clear()
            self.pw2.plotItem.plot([x for x in range(len(self.hrlist))], self.hrlist, pen="g")
        # self.F1.updatecanvas(self.hrlist)
        # self.pw2.plot(self.hrlist)

    def pyqtgraphset(self):
        pass

    def comboboxset(self):
        self.comboBox.activated.connect(self.on_combobox1_Activate)

    def on_combobox1_Activate(self, index):
        if self.comboBox.currentText() == "心率波形查看":
            self.heartrate_modulevisible_set(True)
            print("心率波形查看")
        elif self.comboBox.currentText() == "疲劳度查看":
            self.heartrate_modulevisible_set(False)
            print("疲劳度查看")




##################视频处理进程#####################
    def video_process1(self):
        self.vstart = True
        self.video_option.setEnabled(False)
        file_name, ok = QFileDialog.getOpenFileNames(self.centralwidget, caption="选择视频文件", filter="视频文件(*.mp4)")
        if len(file_name) == 0:
            pass
        else:
            box = []
            for file in file_name:
                tail = file.split(r".")[-1]
                # print(tail)
                if tail != "mp4" and tail != "avi":
                    pass
                else:
                    box.append(file)
            directory1 = QFileDialog.getExistingDirectory(self.centralwidget,
                                                          "选择保存文件地址",
                                                          "./")  # 起始路径
            if len(directory1) == 0:
                pass
            else:
                directory1 = makdir(directory1, trait=True)
                self.Videomanager = VideoManager(box, directory1)
                self.Videomanager.spy.current_progress.connect(self.change_progress)
                self.Videomanager.spy.finished.connect(self.video_exit2)
                self.Videomanager.mystart()
                self.video_cancel.setEnabled(True)
                self.jindu2.setText("处理已完成！")
    #强制退出
    def video_exit(self):
        self.deleting_video = True
        self.Videomanager.spy.current_progress.disconnect(self.change_progress)
        self.Videomanager.myexit()
        self.video_option.setEnabled(True)
        self.video_cancel.setEnabled(False)
        self.deleting_video = False
        self.vstart = False
        self.jindu2.setText("处理已完成！")
    #普通退出
    def video_exit2(self):
        self.vstart = False
        self.video_option.setEnabled(True)
        self.video_cancel.setEnabled(False)
        self.jindu2.setText("处理已完成！")
    #显示进度
    def change_progress(self, tuple):
        self.jindu2.setText(f"当前进度{tuple[0]}/{tuple[1]}个视频")
    #返回视频处理模式是否在工作
    def isvideoworking(self):
        return self.vstart

######################################################

    # 判断是否有摄像处理心率进行
    def iscameraworking(self):
        return self.pstart
    #创建摄像头处理心率进程+线程类并且启动
    def cameralaunch(self):
        if not self.iscameraworking():
            self.manager = Manage_unit(self.time11)
            # 连接子类的QObject和主界面的函数方法
            self.manager.facemgo.useless.connect(self.useless)
            self.manager.facemgo.message.connect(self.write)
            self.manager.facemgo.go.connect(self.todatabox)
            self.manager.facemgo.fpssignal.connect(self.set_current_fps)
            self.manager.showcam.showpic.connect(self.showcamera)
            self.manager.boost.connect(self.exit_button_open)
            # 启动子类的线程和进程
            self.manager.mystart()
            ####################################################################################
            self.pstart = True
        else:
            self.warning()
    #收到信号槽之后开启exit按钮的控制
    def exit_button_open(self):
        self.exit.setEnabled(True)
    #重复进程警告
    def warning(self):
        pass
        # print("当前已有操作进行!")
    #销毁摄像头进程和线程和队列
    def delete_cameraworking(self):
        self.deleting_camera = True
        if self.iscameraworking():
            try:
                self.manager.finished.connect(self.camera_delete_admission)
                self.manager.facemgo.useless.disconnect(self.useless)
                self.manager.facemgo.message.disconnect(self.write)
                self.manager.facemgo.go.disconnect(self.todatabox)
                self.manager.facemgo.fpssignal.disconnect(self.set_current_fps)
                self.manager.showcam.showpic.disconnect(self.showcamera)
                self.manager.boost.disconnect(self.exit_button_open)
            except:
                pass

            self.manager.myexit()
            while not self.camera_should_be_delete:
                time.sleep(0.01)
            self.camera_should_be_delete = False
            # self.manager.finished.disconnect(self.camera_delete_admission)
            self.pstart = False
            # self.F.updatecanvas([0 for x in range(20)])
            # self.F1.updatecanvas([0 for x in range(20)])
            self.heartrate_output.setText("0")
            # del self.manager
        else:
            pass
            # print("还没有开始！")
        self.deleting_camera = False
    #和上函数绑定，防止类析构到一半就del掉类
    def camera_delete_admission(self):
        self.camera_should_be_delete = True
    #删除当前正在运行的摄像头线程与进程
    def just_cancel(self):
        self.exit.setEnabled(False)
        self.videoshow.setVisible(False)
        self.heartrate_modulevisible_set(False)
        self.delete_cameraworking()
        del self.hrlist[:]
        self.start.setEnabled(True)
    #调整当前的摄像头帧率
    def set_current_fps(self, fps):
        self.samplingrate_input = fps


#####槽函数########################################################################
    #显示心率
############################################################################################################################
    #显示心率波形
#############################################################################################################################
        # self.F.updatecanvas1(datain[0], datain[1], datain[2], datain[3],self.samplingrate_input)
    #显示时间戳
    def show_time(self,time_now):
        self.heartrate_time.setText(str(time_now))
    #如果没有人脸则直接刷新
    def useless(self):
        # self.F.updatecanvas([0 for x in range(20)])
        # self.F1.updatecanvas([0 for x in range(20)])
        self.heartrate_output.setText("人脸缺失")
    #包装好的显示心率函数
    def display(self, listin):
        self.show_hr(str(listin[7]))

    def showcamera(self, image):
        self.videoshow.setPixmap(QPixmap.fromImage(image))
#################################################################################
    #点击开始按钮触发时间，先选择文件储藏的位置然后启动一个进程管理类（在process_management里）
    def operation_start(self):
        directory1 = QFileDialog.getExistingDirectory(self.centralwidget,
                                                      "选取文件夹",
                                                      "./")  # 起始路径
        if len(directory1) == 0:
            pass
        else:
            self.dir_now = makdir(directory1)
            self.time11 += 1
            self.opstart()

    #开始操作
    def opstart(self):
        self.start.setEnabled(False)
        self.videoshow.setVisible(True)
        self.heartrate_modulevisible_set(True)
        self.cameralaunch()
        self.exit.setEnabled(True)

    #退出程序之前大清理
    def targetdown(self):
        self.exit.setEnabled(False)
        self.start.setEnabled(False)
        self.video_option.setEnabled(False)
        self.detail.setEnabled(False)
        if self.isvideoworking():
            self.video_exit()
        if self.iscameraworking():
            self.delete_cameraworking()
        else:
            pass
        # print("结束")
    #写数据到指定位置的txt里
    def write(self, data):
        if self.isclosing:
            pass
        else:
            if self.count % self.multi == 0:
                if self.count != 0:
                    self.time1 += 1
                    self.f.close()
                self.f = open(
                    self.dir_now + rf"/心率文件{self.time1 * self.multi + 1}个到第{(self.time1 + 1) * self.multi}.txt", 'w',
                    encoding="utf-8")
                self.readstart = True
            hr, list_to_show, time_now, time_begin, peaks = data[0], data[1], data[2], data[3], data[4]
            #############################
            self.hrlist.append(hr)
            if len(self.hrlist) >= 8:
                myhrlist = self.hrlist[:]
                mymean = np.mean(np.array(myhrlist[3:]))
                mystd = np.std(np.array(myhrlist[3:]))
                newhrlist = []
                for i in range(len(myhrlist)):
                    current = self.hrlist[i]
                    if (50 < current < 180) and (abs(current - mymean) < 0.15 * mystd):
                        newhrlist.append(current)
                if len(newhrlist) == 0:
                    hr = mymean
                else:
                    hr = np.mean(np.array(newhrlist))
                self.hrlist.pop(0)
            #############################
            self.wrt = True
            self.f.write(f"第{time_begin}秒到第{time_now}秒\n")
            self.f.write(f"心率是{hr}\n波形{self.samplingrate_input}帧是\n{list(list_to_show)}")
            self.wrt = False
            self.show_hr(hr)
            self.show_wave((list_to_show, peaks, time_begin, time_now))
            self.show_time("第" + str(time_begin) + "秒到" + str(time_now) + "秒")
            self.count += 1
    #返回是否有进程正在退出，防止点退出的时候进程没有退干净。
    def isdeleting(self):
        return self.deleting_camera or self.deleting_video
    #主界面退出事件
    def closeEvent(self, event):
        if self.isdeleting():
            while self.isdeleting():
                # print("请等待进程终止")
                time.sleep(0.1)
        else:
            self.targetdown()
        event.accept()

#画布类
class MyFigure(FigureCanvas):
    #画板类
    def __init__(self, width=5, height=2, dpi=100, config="wave"):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MyFigure,self).__init__(self.fig)
        self.model = config
        self.axes0 = self.fig.add_subplot(111)
        self.axes0.plot([x for x in range(10)], [0 for x in range(10)])
        self.draw()

    def updatecanvas(self, listin):
        self.axes0.cla()
        self.axes0.plot([x for x in range(len(listin))], listin)
        self.draw()

    def updatecanvas1(self, listin, peaks, begin, end, sr, means=False):
        if not means:
            wave = list(np.arange(begin*sr, end*sr, 1)/sr)
            self.axes0.cla()
            self.axes0.plot(wave, listin)
            self.axes0.scatter([wave[x] for x in peaks], [listin[x] for x in peaks], s=25, c='r')
            # self.axes0.plot([x for x in range(len(listin))], [means for x in range(len(listin))], 'orange')
            self.draw()

    def updatecont(self, matrixin, begin, end, samplingrate):
        self.axes0.cla()
        self.axes0.contourf(np.arange(begin*samplingrate, end*samplingrate, 1)/samplingrate, frequencies, abs(matrixin))
        self.draw()

if __name__ == '__main__':
    freeze_support()
    app = QApplication(sys.argv)
    window = myapp()
    datapanel = datawin()

    btn = window.detail
    btn.triggered.connect(datapanel.show)
    window.message.connect(datapanel.drawall)


    window.show()
    sys.exit(app.exec_())