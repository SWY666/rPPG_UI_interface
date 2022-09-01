from PyQt5.QtCore import pyqtSignal, QObject
from scipy import signal
import time
from cwtbag import cwt_filtering
import numpy as np
import tttt
import wave_process as wp
#  测试版1.0  ############################################################################################################################
####以下这些函数的用处会在下面的类里面提到。

#融合函数
#去趋势化函数
def Drtrending(meanlist,samplingrate):
    if len(meanlist) <=samplingrate:
        return meanlist
    else:
        result = [0 for i in range(len(meanlist))]
        for index in range(len(meanlist)):
            if index+1 < samplingrate:
                M = (sum(meanlist[0:index+1])+sum(meanlist[index-samplingrate:-1]))/samplingrate
            else:
                M = sum(meanlist[index-samplingrate+1:index+1])/samplingrate
            result[index] = (meanlist[index]-M)/M
        return result

def DeTrendc(l0, sr):
    if len(l0) <= sr:
        return l0
    else:
        l1 = np.array(l0)
        result = [0 for x in range(len(l1))]

        for i in range(1, sr):
            means = np.mean(l0[:i])
            result[i] = (l1[i] - means) / means
        for i in range(sr, len(l1)):
            means = np.mean(l0[i-sr:i])
            result[i] = (l1[i] - means) / means
        result[0] = result[1]

    return result

#MA高频滤波函数
def MA(meanlist,samplingrate):
    M = int(samplingrate/4)
    if len(meanlist) <= M:
        return meanlist
    else:
        result = [0 for i in range(len(meanlist))]
        for index in range(len(meanlist)):
            if index + 1 < M:
                result[index] = (sum(meanlist[0:index+1])+sum(meanlist[index-M:-1]))/M
            else:
                result[index] = sum(meanlist[index-M+1:index+1])/M
    return result
#预处理（包含去趋势化，MA高阶滤波以及带通滤波）
def preprocess(listin, samplingrate, f1=0.65, f2=4):
    listin = DeTrendc(listin,samplingrate)
    listin= MA(listin, samplingrate)
    #这边不知道为啥是黄的但是可以正常跑。
    b, a = signal.butter(8, [2 * f1 / samplingrate, 2 * f2 / samplingrate], 'bandpass')
    meanslist_after_BP = signal.filtfilt(b, a, listin)
    # meanslist_after_BP = MA(meanslist_after_BP, samplingrate)
    # b, a = signal.butter(8, [2 * f1 / samplingrate, 2 * 2 / samplingrate], 'bandpass')
    # meanslist_after_BP = signal.filtfilt(b, a, meanslist_after_BP)
    return meanslist_after_BP
#预处理＋融合方案(上方代码的整合)，之后放到主函数vedioprocess里面让主函数看起来干净一点。
def IPPG_process(g, samplingrate, f1=0.5, f2=3):
    g = preprocess(g, samplingrate, f1, f2)
    return g

def peakcheckez(a, samplingrate):
    result = []
    for i in range(len(a)):
        if i == 0 or i == len(a)-1:
            pass
        else:
            if a[i]>a[i-1] and a[i]> a[i+1]:
                result.append(i)
    if len(result) <= 4:
        hr = 0
    else:
        # hr = (len(result)*60)/((result[-1]-result[1])/samplingrate)
        hr = 60 / ((result[-1] - result[-4]) / (3 * samplingrate))

    return int(hr), result

def bgrselect(frame):
    return frame[:,:,1]



##################################################################################################

#单做成函数比较复杂，所以做成了一个类。
#python的多线程无法利用CPU多核特性，但先前的人脸检测又太耗时，所以只能用多进程做，多进程的话不能传递普通变量，我选择了queue进行数据传递。
#其实我还是觉得视频版本和摄像头版本分开来做好一点，视频版本如果传入多个视频，感觉可以此外多做一点速度和内存上的优化。
#如果之后的实验只做绿通道的话，那么这个函数可以稍微简化（三通道改为单绿通道）一下节省空间加快速度。


class face_managemengt(QObject):
    useless = pyqtSignal()
    go = pyqtSignal(list)
    finished = pyqtSignal()
    message = pyqtSignal(list)
    overed = pyqtSignal()
    fpssignal = pyqtSignal(int)
    def __init__(self, samplingrate, queue_ROI, time11, Allthingsdown, getfps, threshold = 3, maxinum = 8, f1 = 0.7, f2 = 4, video = False):
        super().__init__()
        self.reservoir = []
        self.samplingratev, self.queue_ROI = samplingrate, queue_ROI
        self.getfps = getfps
        self.handle = True
        self.time = 0
        self.threshold = threshold
        self.maxinum = maxinum
        self.ALL_THINGS_DOWN = Allthingsdown
        self.f1 = f1
        self.f2 = f2
        self.video = video
        self.time11 = time11
        self.name = "图像中转进程"
        self.data1 = []
        self.count = []

    def run(self):
        # print("face_management_go")
        while not self.getfps.value:
            time.sleep(0.01)
            pass
        self.samplingrate = self.samplingratev.value
        self.fpssignal.emit(self.samplingrate)
        # print(self.samplingrate, "心率计算模块开始执行")
        while True:
            #从前面的队列里面拿人脸框数据（里面的一个元素是【时间戳（int），【一秒内帧数数量的人脸框】】）
            data = self.queue_ROI.get()
            #检测到时间戳是-1就退出
            if data[0] == -1:
                break
            #时间戳正常就开始解构数据
            self.decode(data)
            time.sleep(0.02)
        self.overed.emit()
        self.finished.emit()
        self.ALL_THINGS_DOWN = True
        # print("face_management已经退出")

    #解构数据正常则类内的时间戳加一，然后对数据进行心率计算。
    def decode(self, data):
        self.time += 1
        self.heartratecal(data)

    def heartratecal(self, data):
        try:
            #对一秒内的（30帧）人脸框列表里面的每一个元素都进行人脸皮肤提取，提取的结果是一个浮点型数据。
            self.face_sliceg(data[1])
        except:
            print("别晃了兄弟")
            #出现问题就直接类内的累计数据归零。
            self.data1 = []
        if len(self.data1) >= self.threshold * self.samplingrate:
            #如果序列长度超过缓冲（默认3秒），就开始心率计算
            self.IPPG_processg()
        while len(self.data1) >= (self.maxinum + 1) * self.samplingrate:
            #计算完成后，当序列长度超过最大长度的时候，对序列进行裁剪，控制在8秒（默认）以内。
            del self.data1[0:self.samplingrate]

    def face_sliceg(self, data_in):
        count = 0
        add = []
        deletenot = False
        for data in data_in:
            if data is None:
                add.append(0)
                count += 1
                #如果超过一半没有检测到人脸那么就判定为是人脸缺失你，然后把类内的数据清零。
                if count >= int(len(data_in)/2):
                    deletenot = True

            else:
                #这个tttt.RGBskinnum就是高速的人脸皮肤提取函数
                trove = tttt.RGBskinnum(data)
                add.append(trove[0])
                self.count.append(trove[1])
                if len(self.count) >= 8*self.samplingrate:
                    del self.count[:self.samplingrate]

        if deletenot:
            #发射无效
            self.useless.emit()
            #数据清零。
            self.data1 = []
            pass
        else: self.data1 = self.data1 + add

    def IPPG_processg(self):
        raw = self.data1[:]
        new = self.data1[:]
        background = 0
        #这一步是差分法防止出现阶跃的信号。
        for i in range(1,len(new),1):
            if abs(raw[i]-raw[i-1]) > 1:
                background = raw[i] - new[i-1]
                new[i] = new[i-1]
            else:
                new[i] = raw[i] - background
        #这个wp.IPPG_process就是高速的滤波函数
        wave1 = wp.IPPG_process(new, self.samplingrate)
        if len(self.data1) >= (self.maxinum + 1) * self.samplingrate:
            wave1 = wave1[self.samplingrate:]
            del self.data1[0:self.samplingrate]
        #小波滤波
        wave, cwtwave, cwt = cwt_filtering(wave1, self.samplingrate)
        # result = get_heartrate((wave, self.samplingrate))
        #零点检测
        result, resultp = peakcheckez(wave, self.samplingrate)
        # 然后根据置信值选择最优的波形（所以有的时候输出的心率波形不连续）
        #发射信号给主界面以及展示细节窗口
        self.go.emit([wave1, wave, cwtwave, resultp, self.time, self.samplingrate, cwt, result, new, self.count])
        self.message.emit([result, wave, float(self.time), self.time - len(self.data1) / self.samplingrate, resultp])




