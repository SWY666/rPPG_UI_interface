import os
import cv2
from PyQt5.QtCore import QThread
from multiprocessing import Value
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
import time
from ctypes import c_bool
from PyQt5.QtCore import pyqtSignal, QObject
from multiprocessing import Process
import dlib
from math import sqrt
import tttt
import wave_process
from cwtbag import cwt_filtering

detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')
predictor = dlib.shape_predictor('shape_predictor_5_face_landmarks.dat')

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

def generate_dir(dirname):
    currentdir = dirname
    success = trymkdir(currentdir)
    count = 0
    while not success:
        time.sleep(0.2)
        count += 1
        currentdir = dirname + str(count)
        success = trymkdir(currentdir)
    return currentdir

def trymkdir(dirname):
    success = True
    try:
        os.mkdir(dirname)
    except:
        success = False
    return success

def getmean(frame_list, func):
    plg = []
    sumlist = []
    countlist = []
    count1 = 0
    for index in range(len(frame_list)):
        # print(f"第{count1}次")
        count1 += 1
        result, sum, count = func(frame_list[index])
        plg.append(result)
        sumlist.append(sum)
        countlist.append(count)

    return plg, sumlist, countlist

def the_only_face(frame_in):
    rects = detector(frame_in, 0)
    lens = len(rects)
    if lens == 0:
        the_only_rect = (False, None)
    elif lens == 1:
        the_only_rect = (True, rects[0].rect)
    else:
        axis_x = int(frame_in.shape[0] / 2)
        axis_y = int(frame_in.shape[1] / 2)
        distances = [0.0 for x in range(lens)]
        for i in range(lens):
            rects_axis_x = int((rects[i].rect.right() - rects[i].rect.left()) / 2)
            rects_axis_y = int((rects[i].rect.right() - rects[i].rect.left()) / 2)
            distances[i] = (rects_axis_x-axis_x)**2 + (rects_axis_y-axis_y)**2

        min_distance_index = distances.index(min(distances))
        the_only_rect = (True, rects[min_distance_index].rect)

    return the_only_rect
#配合the_only_face的人脸提取
def rect_catch(frame, sr, STOP, maxlenth=20, multiple=8):
    lens = len(frame)
    count = 0
    axis1 = []
    ################################
    get_face = True
    for i in range(lens):
        if STOP.value:
            break
        rects = detector(frame[i], 0)
        if len(rects) > 0:
            break
        count += 1
        if count == sr or STOP.value:
            get_face = False
    #################################
    if get_face:
        the_just_face = frame[count]
        rectuple = the_only_face(the_just_face)
        the_just_face_rect = rectuple[1]
        t0, b0, l0, r0 = the_just_face_rect.top(), the_just_face_rect.bottom(),the_just_face_rect.left(),the_just_face_rect.right()
        centerx = (t0 + b0) / 2
        centery = (l0 + r0) / 2
        myaxis = (centerx, centery)
        maxh = (b0 - t0) / multiple
        maxw = (r0 - l0) / multiple
        finaladdh = max(maxh, maxlenth)
        finaladdw = max(maxw, maxlenth)
        for i in range(lens):
            if STOP.value:
                break
            else:
                if i != count:
                    try:
                        # rects = detector(frame[i], 0)
                        current_face = the_only_face(frame[i])
                        face_rect = current_face[1]
                        centerx = (face_rect.top() + face_rect.bottom()) / 2
                        centery = (face_rect.top() + face_rect.bottom()) / 2
                        temp = sqrt((centerx - myaxis[0]) ** 2 + (centery - myaxis[1]) ** 2)
                        if temp <= (face_rect.bottom() - face_rect.top() / multiple):
                            pass
                        else:
                            myaxis = (centerx, centery)
                            t0, b0, l0, r0 = face_rect.top(), face_rect.bottom(), face_rect.top(), face_rect.bottom()
                    except:
                        pass
                t, b, l, r = t0, b0, l0, r0

                tf, bf, lf, rf = max(0, t - int(finaladdh / 2)), min(frame[0].shape[0], b + int(finaladdh / 2)), \
                                 max(0, l - int(finaladdw / 2)), min(frame[0].shape[0], r + int(finaladdh / 2))
                thisface = frame[i][tf: bf, lf: rf]
                axis1.append(thisface)
    else:
        axis1 = ([None for x in range(lens)])

    return axis1

class Video_Message_box(QObject):
    current_progress = pyqtSignal(tuple)
    def __init__(self):
        super().__init__()

    def progress_send(self, progress, total):
        self.current_progress.emit((progress, total))

class videoP(Process):
    def __init__(self, filenames, value, STOP, targetdir):
        super().__init__()
        self.filenames = filenames
        self.total = len(filenames)
        self.value = value
        self.STOP = STOP
        self.targetdir = targetdir
        # self.video_message_box = Video_Message_box()
        # self.targetdir = targetdir

    def run(self):
        for index in range(len(self.filenames)):
            if self.STOP.value:
                break
            # print(self.filenames[index])
            cap = cv2.VideoCapture(self.filenames[index])
            samplingrate = int(cap.get(cv2.CAP_PROP_FPS))
            # print("帧数是{}".format(samplingrate))
            success = True
            image = []
            while (success):
                success, frame = cap.read()
                # frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                if frame is not None:
                    image.append(frame)
            cap.release()
            image.pop(-1)
            image = image[:]
            # print("片段总时长{}".format(len(image) / samplingrate))
            pfg = rect_catch(image, samplingrate, self.STOP)
            if self.STOP.value:
                break
            pfg, countlist, sumlist = getmean(pfg, tttt.RGBskinnum)
            plf = wave_process.IPPG_process(pfg, samplingrate)
            hr, result = wave_process.peakcheckez(cwt_filtering(plf, 30)[0].tolist(), samplingrate)
            ######################
            targetfile = self.targetdir + r"/" + self.filenames[index].split(r"/")[-1].split(r".")[0]
            real_target_file = generate_dir(targetfile)
            # print(real_target_file)
            with open(real_target_file + r"/result.txt", "w") as f:
                f.write("心率是" + str(hr) + "\n")
                f.write("波形数据:" + "\n")
                f.write(str(plf.tolist()))
            #########################
            self.value.value += 1
        # print("完成")
        self.STOP.value = False

    # def progress_send(self, progress):
    #     self.video_message_box.progress_send(progress, self.total)
#########我是老大###########
class VideoManager(QObject):
    current_progress = pyqtSignal(tuple)

    def __init__(self, filenames, targetdir):
        super().__init__()
        self.targetdir = targetdir
        self.value = Value("I", 0)
        self.STOP = Value(c_bool, False)
        self.total = len(filenames)
        self.videoprocess = videoP(filenames, self.value, self.STOP, targetdir)
        self.spy = spy_progress(self.value, self.total, self.STOP)
        self.spy_thread = QThread(self)
        self.spy.finished.connect(self.spy_thread.quit)
        self.spy.finished.connect(self.stop_process)
        self.spy_thread.finished.connect(self.spy.deleteLater)
        self.spy_thread.finished.connect(self.spy_thread.deleteLater)
        self.spy.moveToThread(self.spy_thread)
        self.spy_thread.started.connect(self.spy.run)
        self.process_over = False
        self.willclose = False

    def mystart(self):
        self.spy_thread.start()
        self.videoprocess.start()

    def myexit1(self):
        if not self.process_over:
            self.videoprocess.terminate()
            self.willclose = True
            if self.value.value != self.total:
                self.value.value = self.total

    def stop_process(self):
        if self.videoprocess.is_alive():
            self.videoprocess.join()
        self.videoprocess.close()

    def myexit(self):
        self.STOP.value = True
        while self.STOP.value:
            time.sleep(0.1)
            # print("视频进程处理中")
        self.videoprocess.join()
        self.value.value = self.total
        while not self.STOP.value:
            time.sleep(0.05)
        # print("视频处理进程结束")

###########################
class spy_progress(QObject):
    current_progress = pyqtSignal(tuple)
    finished = pyqtSignal()

    def __init__(self, value, total, STOP):
        super().__init__()
        self.value = value
        self.total = total
        self.current = -1
        self.STOP = STOP

    def run(self):
        while self.value.value < self.total:
            time.sleep(0.01)
            if self.value.value > self.current:
                self.current += 1
                self.current_progress.emit((self.current, self.total))
        # print("视频进程处理监测结束")
        self.finished.emit()
        self.STOP.value = True







