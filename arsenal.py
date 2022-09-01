import dlib
from multiprocessing import Process
from math import sqrt
import numpy as np
import time

detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')
# predictor = dlib.shape_predictor('shape_predictor_5_face_landmarks.dat')


# def cutframe

def rect_catch_group(order, frame, queue_ROI, queue2):
    axis1 = []
    maxlenth = 20
    multiple = 8
    rects = detector(frame[0], 0)
    centerx = (rects[0].rect.top() + rects[0].rect.bottom()) / 2
    centery = (rects[0].rect.left() + rects[0].rect.right()) / 2
    myaxis = (centerx, centery)
    t0, b0, l0, r0 = rects[0].rect.top() , rects[0].rect.bottom(), rects[0].rect.left() , rects[0].rect.right()
    maxh = (b0-t0)/multiple
    maxw = (r0-l0)/multiple
    finaladdh = max(maxh, maxlenth)
    finaladdw = max(maxw, maxlenth)
    tf = max(0, t0 - int(finaladdh/2))#上边沿的y值
    lf = max(0, l0 - int(finaladdw / 2))#左边沿x值
    bf0 = min(frame[0].shape[0], b0 + int(finaladdh / 2))#下边沿y值
    rf0 = min(frame[0].shape[1], r0 + int(finaladdw / 2))#右边缘的x值
    for image in frame:
        try:
            rects = detector(image, 0)
            centerx = (rects[0].rect.top() + rects[0].rect.bottom()) / 2
            centery = (rects[0].rect.left() + rects[0].rect.right()) / 2
            temp = sqrt((centerx - myaxis[0])**2+(centery - myaxis[1])**2)
            if temp <= (rects[0].rect.bottom() - rects[0].rect.top()/8):
                t, b, l, r = tf, bf0, lf, rf0
            else:
                t, b, l, r = max(0, rects[0].rect.top() - int(finaladdh/2)), min(frame[0].shape[0], rects[0].rect.bottom() + int(finaladdh / 2)),\
                             max(0, rects[0].rect.left() - int(finaladdw / 2)), min(frame[0].shape[0], rects[0].rect.right() + int(finaladdh / 2))

            axis1.append(image[t: b, l: r])
            # queue2.put((t, b, l, r))
        except:
            axis1.append(None)
    queue_ROI.put([order, axis1])

def rect_catch_group0(order, frame, queue_ROI):
    maxlenth = 20
    axis1 = []
    rects = detector(frame[0], 0)
    t,b,l,r = rects[0].rect.top() ,rects[0].rect.bottom(),rects[0].rect.left() ,rects[0].rect.right()
    maxh = (b-t)/8
    maxw = (r-l)/8
    finaladdh = max(maxh, maxlenth)
    finaladdw = max(maxw, maxlenth)
    tf = min(0, t - int(finaladdh/2))
    lf = min(0, l - int(finaladdw / 2))
    for image in frame:
        try:
            # rects = detector(image, 0)
            bf = max(image.shape[0], b + int(finaladdh / 2))
            rf = max(image.shape[1], r + int(finaladdw / 2))
            print(t, b, l, r)
            axis1.append(image[t:b,l:r])

            # queue2.put((rects[0].rect.top(), rects[0].rect.bottom(),rects[0].rect.left(), rects[0].rect.right()))
        except:
            axis1.append(None)
    queue_ROI.put([order, axis1])

class image_process(Process):
    def __init__(self, queue, queue_ROI, samplingrate, value, getfps):
        super().__init__()
        self.queue = queue
        self.queue_ROI = queue_ROI
        self.samplingratev = samplingrate
        self.order = 0
        self.name = "图像处理进程"
        self.mylist = []
        self.value = value
        self.rectaxislist = []
        self.getfps = getfps

    def run(self):
        while not self.getfps.value:
            time.sleep(0.01)
            pass
        self.samplingrate = self.samplingratev.value
        # print(self.samplingrate, "人脸识别模块开始执行")
        while self.value.value:
            frame = self.queue.get()
            if isinstance(frame, np.ndarray):
                self.mylist.append(frame)
                if len(self.mylist) == self.samplingrate:
                    self.order += 1
                    mylist = self.mylist[:]
                    del self.mylist[:]
                    rect_catch(self.order, mylist, self.queue_ROI, self.samplingrate)
        self.queue_ROI.put([-1, None])
        # print("image_process结束")

def image_recognize(queue, queue_ROI, samplingrate, value):
    order = 0
    mylist = []
    detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')
    while value.value:
        print("image_process")
        frame = queue.get()
        mylist.append(frame)
        if len(mylist) == samplingrate:
            order += 1
            axis1 = []
            for image in mylist:
                try:
                    rects = detector(image, 0)
                    axis1.append(
                        image[rects[0].rect.top():rects[0].rect.bottom(), rects[0].rect.left():rects[0].rect.right()])
                except:
                    axis1.append(None)
            queue_ROI.put([order, axis1])
            del mylist[:]
    queue_ROI.put([-1, None])
    print("进程结束")
#这个函数在一张原图中筛选唯一人脸
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
def rect_catch(order, frame, queue_ROI, sr, maxlenth=20, multiple=8):
    lens = len(frame)
    count = 0
    axis1 = []
    ################################
    get_face = True
    for i in range(lens):
        rects = detector(frame[i], 0)
        if len(rects) > 0:
            break
        count += 1
        if count == sr:
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

            tf, bf, lf, rf = max(0, t - int(finaladdh / 2)), min(frame[0].shape[0],b + int(finaladdh / 2)), \
                             max(0, l - int(finaladdw / 2)), min(frame[0].shape[0],r + int(finaladdh / 2))
            thisface = frame[i][tf: bf, lf: rf]
            axis1.append(thisface)
    else:
        axis1 = ([None for x in range(lens)])
    queue_ROI.put([order, axis1])

def ctx_image_process(queue, queue_ROI, samplingrate, value, getfps):
    order = 0
    mylist = []
    while not getfps.value:
        time.sleep(0.01)
        pass
    samplingrate = samplingrate.value
    # print(self.samplingrate, "人脸识别模块开始执行")
    while value.value:
        frame = queue.get()
        if isinstance(frame, np.ndarray):
            mylist.append(frame)
            if len(mylist) == samplingrate:
                order += 1
                cur_mylist = mylist[:]
                del mylist[:]
                rect_catch(order, cur_mylist, queue_ROI, samplingrate)
    queue_ROI.put([-1, None])
    # print("image_process结束")

















