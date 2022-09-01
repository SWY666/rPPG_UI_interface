import numpy as np
from PyQt5.QtGui import QImage
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import QtGui
import cv2
import time
from PyQt5.QtCore import Qt
from multiprocessing import Process

url = "rtsp://admin:Aa123456@192.168.0.19:554/"

class camerago(QObject):
    changePixmap = pyqtSignal(QImage)
    imagesend = pyqtSignal(np.ndarray)
    finished = pyqtSignal()

    def __init__(self, sr, queue, value):
        super().__init__()
        self.cont = True
        self.samplingrate = sr
        self.queue = queue
        self.value = value

    def run(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        count = 0
        start = time.time()
        while self.cont:
            ret, frame = self.cap.read()
            self.queue.put(frame)
            cv2.imshow("hello?", frame)
            cv2.waitKey(5)
            count += 1
            if count == 30:
                print(time.time() - start)
                count = 0
        self.cap.release()
        cv2.destroyAllWindows()
        print("camera结束")
        self.value.value = False
        self.queue.put(None)
        self.finished.emit()

    def goout(self):
        self.cont = False

class camerag(Process):
    def __init__(self, sr, queue, value1, value2, getfps, queue2, fps = 30):
        super().__init__()
        self.cont = True
        self.samplingrate = sr
        self.name = "摄像头抓取进程"
        self.queue = queue
        self.value1 = value1
        self.value2 = value2
        self.queue2 = queue2
        self.getfps = getfps
        self.samplingrate.value = fps
        self.getfps.value = True


    def run(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FPS, self.samplingrate.value)
        while self.value2.value:
            ret, frame = self.cap.read()
            self.queue2.put(frame)
            self.queue.put(frame)
            # cv2.imshow("hello?", frame)
            # cv2.waitKey(5)
        # cv2.destroyAllWindows()
        self.cap.release()
        self.value1.value = False
        self.queue.put(None)
        self.queue2.put(None)
        # print(f"camera结束{self.cap.isOpened()}")

class showcamera(QObject):
    showpic = pyqtSignal(QImage)
    finished = pyqtSignal()
    def __init__(self, queue2, value1):
        super().__init__()
        self.queue2 = queue2
        self.value1 = value1

    def run(self):
        while True:
            frame = self.queue2.get()
            if isinstance(frame, np.ndarray):
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QtGui.QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0],
                                                 QImage.Format_RGB888)
                image = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.showpic.emit(image)
            else:break
        self.finished.emit()
        # print("图片传送功能")



