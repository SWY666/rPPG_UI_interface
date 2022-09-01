from PyQt5.QtCore import QThread
import multiprocessing as mp
from camera import camerag, showcamera
from arsenal import image_process
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from image_process_final import face_managemengt
import time
from ctypes import c_bool
from PyQt5.QtCore import pyqtSignal, QObject
from arsenal import ctx_image_process

class Manage_unit(QObject):
    finished = pyqtSignal()
    boost = pyqtSignal()
    def __init__(self, time11):
        super().__init__()
        ctx = mp.get_context('spawn')
        self.queue = ctx.Queue(200)
        self.queue_ROI = ctx.Queue(200)
        self.samplingrate = ctx.Value("I", 30)
        self.getfps = ctx.Value(c_bool, False)
        self.processstart = ctx.Value(c_bool, True)
        self.processstop = ctx.Value(c_bool, True)
        self.ALL_THINGS_DOWN = ctx.Value(c_bool, False)
        self.queue2 = ctx.Queue(200)
        self.OVER = False
        # self.image_process = image_process(self.queue, self.queue_ROI, self.samplingrate,
        #                                    self.processstart, self.getfps)
        self.image_process = ctx.Process(target=ctx_image_process, args=(self.queue, self.queue_ROI, self.samplingrate, self.processstart, self.getfps,))
        self.camera = camerag(self.samplingrate, self.queue, self.processstart, self.processstop, self.getfps, self.queue2)
        # 线程部署1
        self.facemgo = face_managemengt(self.samplingrate, self.queue_ROI, time11, self.ALL_THINGS_DOWN, self.getfps)
        self.showcam = showcamera(self.queue2, self.processstart)
        self.facem = QThread(self)
        self.showcamgo = QThread(self)
        #####连接#####
        self.showcam.finished.connect(self.showcamgo.quit)
        self.showcamgo.finished.connect(self.showcam.deleteLater)
        self.showcamgo.finished.connect(self.showcamgo.deleteLater)
        self.facemgo.finished.connect(self.facem.quit)
        self.facem.finished.connect(self.facemgo.deleteLater)
        self.facem.finished.connect(self.facem.deleteLater)

    def mystart(self):
        self.camera.start()
        self.image_process.start()
        self.showcam.moveToThread(self.showcamgo)
        self.showcamgo.started.connect(self.showcam.run)
        self.facemgo.moveToThread(self.facem)
        self.facem.started.connect(self.facemgo.run)
        self.showcamgo.start()
        self.facem.start()
        self.boost.emit()

    def myexit(self):
        if self.camera.is_alive():
            self.processstop.value = False
            while not self.ALL_THINGS_DOWN:
                # print("等待停止运行")
                time.sleep(0.05)
            self.letsjoin()
        self.finished.emit()

    def letsjoin(self):
        # print("到此为止都结束了！")
        clear_pipe(self.queue_ROI)
        clear_pipe(self.queue)
        # clear_pipe(self.queue_rect)
        # self.queue.cancel_join_thread()
        # self.queue_ROI.cancel_join_thread()
        # self.queue_rect.cancel_join_thread()
        # print("卡在这里了？")
        self.image_process.join()
        # print(f"图像处理进程处理完毕{self.image_process.is_alive()}")
        self.queue.close()
        # print("已经关闭管道")
        self.camera.join(timeout=1)
        if self.camera.is_alive():
            # print("出事")
            self.camera.terminate()
            self.camera.join()
        # print("摄像头进程处理完毕")
        # print(self.camera.is_alive())
        # print(self.image_process.is_alive())
        self.camera.close()
        self.image_process.close()
        self.OVER = True


def clear_pipe(queue_in):
    while not queue_in.empty():  # _q is a multiprocess.Queue object used to communicate inter-process
        try:
            queue_in.get(timeout=0.001)
        except:
            pass