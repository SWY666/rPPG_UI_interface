#pydd.txt
import numpy as np
cimport numpy as np
cimport cython
import cv2
import dlib

DTYPE = np.int
ctypedef np.int_t DTYPE_t
detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')
predictor = dlib.shape_predictor('shape_predictor_5_face_landmarks.dat')


def RGBskin(np.ndarray[unsigned char, ndim=3] frame):
    cdef int x = frame.shape[0]
    cdef int y = frame.shape[1]
    cdef np.ndarray[unsigned char, ndim=2] newpic = np.zeros((x, y), dtype=np.uint8)
    cdef np.ndarray[unsigned char, ndim=2] allb = frame[:, :, 0]
    cdef np.ndarray[unsigned char, ndim=2] allg = frame[:, :, 1]
    cdef np.ndarray[unsigned char, ndim=2] allr = frame[:, :, 2]
    cdef int r
    cdef int g
    cdef int b
    for i in range(x):
        for j in range(y):
            r = allr[i, j]
            g = allg[i, j]
            b = allb[i, j]
            if r>50 and g>20 and b>20 and max(b,g,r)-min(b,g,r)>15 and abs(r-g)>15 and r>g and r>b: # g>40
                if r>220 and g>210 and b>170 and g>b:
                    pass
                else:
                    newpic[i,j] = 1
    return newpic

def RGBskinerode(np.ndarray[unsigned char, ndim=3] frame):
    cdef np.ndarray[unsigned char, ndim=2] kernel = np.ones((5, 5), np.uint8)
    cdef int x = frame.shape[0]
    cdef int y = frame.shape[1]
    cdef np.ndarray[unsigned char, ndim=2] newpic = np.zeros((x, y), dtype=np.uint8)
    cdef np.ndarray[unsigned char, ndim=2] allb = frame[:, :, 0]
    cdef np.ndarray[unsigned char, ndim=2] allg = frame[:, :, 1]
    cdef np.ndarray[unsigned char, ndim=2] allr = frame[:, :, 2]
    cdef int r
    cdef int g
    cdef int b
    cdef double sum = 0
    cdef int count = 0
    for i in range(x):
        for j in range(y):
            r = allr[i, j]
            g = allg[i, j]
            b = allb[i, j]
            if r>95 and g>40 and b>20 and max(b,g,r)-min(b,g,r)>15 and abs(r-g)>15 and r>g and r>b:
                if r>220 and g>210 and b>170 and g>b:
                    pass
                else:
                    newpic[i,j] = 255
    cdef np.ndarray[unsigned char, ndim=2] after_erode = cv2.erode(newpic, kernel)
    for i in range(x):
        for j in range(y):
            if after_erode[i, j] == 255:
                sum = sum + allg[i, j]
                count = count + 1
    cdef double result
    result = sum / count
    return result

def RGBskinerodepic(np.ndarray[unsigned char, ndim=3] frame):
    cdef np.ndarray[unsigned char, ndim=2] kernel = np.ones((5, 5), np.uint8)
    cdef int x = frame.shape[0]
    cdef int y = frame.shape[1]
    cdef np.ndarray[unsigned char, ndim=2] newpic = np.zeros((x, y), dtype=np.uint8)
    cdef np.ndarray[unsigned char, ndim=2] allb = frame[:, :, 0]
    cdef np.ndarray[unsigned char, ndim=2] allg = frame[:, :, 1]
    cdef np.ndarray[unsigned char, ndim=2] allr = frame[:, :, 2]
    cdef int r
    cdef int g
    cdef int b
    cdef double sum = 0
    cdef int count = 0
    for i in range(x):
        for j in range(y):
            r = allr[i, j]
            g = allg[i, j]
            b = allb[i, j]
            if r>95 and g>40 and b>20 and max(b,g,r)-min(b,g,r)>15 and abs(r-g)>15 and r>g and r>b:
                if r>220 and g>210 and b>170 and g>b:
                    pass
                else:
                    newpic[i,j] = 255
    cdef np.ndarray[unsigned char, ndim=2] after_erode = cv2.erode(newpic, kernel)
    return after_erode



def hello():
    print("hello")

#专用皮肤提取算法
def RGBskinnum(np.ndarray[unsigned char, ndim=3] frame):
    cdef int x = frame.shape[0]
    cdef int y = frame.shape[1]
    cdef np.ndarray[unsigned char, ndim=2] allb = frame[:,:,0]
    cdef np.ndarray[unsigned char, ndim=2] allg = frame[:,:,1]
    cdef np.ndarray[unsigned char, ndim=2] allr = frame[:,:,2]
    cdef double sum = 0
    cdef int count = 0
    cdef int r
    cdef int g
    cdef int b
    for i in range(x):
        for j in range(y):
            r = allr[i, j]
            g = allg[i, j]
            b = allb[i, j]
            if r>95 and g>40 and b>20 and max(b,g,r)-min(b,g,r)>15 and abs(r-g)>15 and r>g and r>b:
                if r>220 and g>210 and b>170 and g>b:
                    pass
                else:
                    sum = sum + g
                    count = count + 1
    cdef double result
    if count == 0:
        result = 1.0
    else:
        result = sum / count
    return result, sum, count


#检验算法
def RGBskincheck(np.ndarray[unsigned char, ndim=3] frame):
    cdef int x = frame.shape[0]
    cdef int y = frame.shape[1]
    cdef np.ndarray[unsigned char, ndim=3] newpic = np.zeros((x, y, 3), dtype=np.uint8)
    cdef np.ndarray[unsigned char, ndim=2] allb = frame[:,:,0]
    cdef np.ndarray[unsigned char, ndim=2] allg = frame[:,:,1]
    cdef np.ndarray[unsigned char, ndim=2] allr = frame[:,:,2]
    cdef double sum = 0
    cdef int count = 0
    cdef int r
    cdef int g
    cdef int b
    for i in range(x):
        for j in range(y):
            r = allr[i, j]
            g = allg[i, j]
            b = allb[i, j]
            if r>95 and g>40 and b>20 and max(b,g,r)-min(b,g,r)>15 and abs(r-g)>15 and r>g and r>b:
                if r>220 and g>210 and b>170 and g>b:
                    pass
                else:
                    #if g < 150 and g > 145:
                        newpic[i,j, 0] = b
                        newpic[i,j, 1] = g
                        newpic[i,j, 2] = r
                        sum = sum + g
                        count = count + 1
    cdef double result
    if count == 0:
        result = 1.0
    else:
        result = sum / count
    return result, sum, count, newpic
#改进的检验算法（三角形）
def RGBskincheckg(np.ndarray[unsigned char, ndim=3] frame):
    rects = detector(frame, 0)
    shape = predictor(frame, rects[0].rect)
    cdef int distancex = rects[0].rect.left()
    cdef int distancey = rects[0].rect.top()
    cdef float x0 = shape.part(0).x-distancex
    cdef float x2 = shape.part(2).x-distancex
    cdef float x4 = shape.part(4).x-distancex
    cdef float y0 = shape.part(0).y-distancey
    cdef float y2 = shape.part(2).y-distancey
    cdef float y4 = shape.part(4).y-distancey
    ################################
    #算斜率
    cdef float k02 = (y2-y0)/(x2-x0)
    cdef float k04 = (y4-y0)/(x4-x0)
    cdef float k24 = (y2-y4)/(x2-x4)
    cdef float b02 = (x2*y0-x0*y2)/(x2-x0)
    cdef float b04 = (x4*y0-x0*y4)/(x4-x0)
    cdef float b24 = (x2*y4-x4*y2)/(x2-x4)
    ################################
    cdef np.ndarray[unsigned char, ndim=3] face = frame[rects[0].rect.top():rects[0].rect.bottom(),rects[0].rect.left():rects[0].rect.right()]
    cdef int x = face.shape[0]
    cdef int y = face.shape[1]
    cdef np.ndarray[unsigned char, ndim=3] newpic = np.zeros((x, y, 3), dtype=np.uint8)
    cdef np.ndarray[unsigned char, ndim=2] allb = face[:,:,0]
    cdef np.ndarray[unsigned char, ndim=2] allg = face[:,:,1]
    cdef np.ndarray[unsigned char, ndim=2] allr = face[:,:,2]
    cdef double sum = 0
    cdef int count = 0
    cdef int r
    cdef int g
    cdef int b
    for i in range(x):
        for j in range(y):
            if i > k02*j + b02 and i < k04*j + b04 and i < k24*j + b24:
                r = allr[i, j]
                g = allg[i, j]
                b = allb[i, j]
                if r>95 and g>40 and b>20 and max(b,g,r)-min(b,g,r)>15 and abs(r-g)>15 and r>g and r>b:
                    if r>220 and g>210 and b>170 and g>b:
                        pass
                    else:
                        if g < 180 and g > 130:
                            newpic[i,j, 0] = b
                            newpic[i,j, 1] = g
                            newpic[i,j, 2] = r
                            sum = sum + g
                            count = count + 1
    cdef double result
    if count == 0:
        result = 1.0
    else:
        result = sum / count
    return result, sum, count, newpic
#改进的检验算法（正方形）
def RGBskincheckzf(np.ndarray[unsigned char, ndim=3] frame):
    rects = detector(frame, 0)
    shape = predictor(frame, rects[0].rect)
    cdef int distancex = rects[0].rect.left()
    cdef int distancey = rects[0].rect.top()
    cdef float x0 = shape.part(0).x-distancex
    cdef float x2 = shape.part(2).x-distancex
    cdef float x4 = shape.part(4).x-distancex
    cdef float y0 = shape.part(0).y-distancey
    cdef float y2 = shape.part(2).y-distancey
    cdef float y4 = shape.part(4).y-distancey
    ################################
    #算斜率
    cdef float k02 = (y2-y0)/(x2-x0)
    #cdef float k04 = (y4-y0)/(x4-x0)
    #cdef float k24 = (y2-y4)/(x2-x4)
    cdef float b02 = y2 - k02*x2
    #cdef float b04 = (x4*y0-x0*y4)/(x4-x0)
    cdef float b4 = y4-k02*x4
    cdef float b021 = -1.2 * b4 + 2.2 * b02
    cdef float b44 = 1.8 * b4 - 0.8 *b02
    cdef float b022 = -0.5 * b4 + 1.5 * b02
    cdef float b023 = 0.3 * b4 + 0.7 * b02
    ################################
    cdef np.ndarray[unsigned char, ndim=3] face = frame[rects[0].rect.top():rects[0].rect.bottom(),rects[0].rect.left():rects[0].rect.right()]
    cdef int x = face.shape[0]
    cdef int y = face.shape[1]
    cdef np.ndarray[unsigned char, ndim=3] newpic = np.zeros((x, y, 3), dtype=np.uint8)
    cdef np.ndarray[unsigned char, ndim=2] allb = face[:,:,0]
    cdef np.ndarray[unsigned char, ndim=2] allg = face[:,:,1]
    cdef np.ndarray[unsigned char, ndim=2] allr = face[:,:,2]
    cdef double sum = 0
    cdef double count = 0
    cdef int r
    cdef int g
    cdef int b
    for i in range(x):
        for j in range(y):
            if (i > k02*j + b021 and i < k02*j + b44):
                r = allr[i, j]
                g = allg[i, j]
                b = allb[i, j]
                if r>95 and g>40 and b>20 and max(b,g,r)-min(b,g,r)>15 and abs(r-g)>15 and r>g and r>b:
                    if r>220 and g>210 and b>170 and g>b:
                        pass
                    else:
                        #if g < 180 and g > 120:
                            newpic[i,j, 0] = b
                            newpic[i,j, 1] = g
                            newpic[i,j, 2] = r
                            sum = sum + g
                            count = count + 1
    cdef double result
    if count == 0:
        result = 1.0
    else:
        result = sum / count
    return result, sum, count, newpic
#
def RGBskinnumpro(np.ndarray[unsigned char, ndim=3] frame):
    cdef list ROIlist = []
    cdef int x = frame.shape[0]
    cdef int y = frame.shape[1]
    cdef np.ndarray[unsigned char, ndim=2] allb = frame[:,:,0]
    cdef np.ndarray[unsigned char, ndim=2] allg = frame[:,:,1]
    cdef np.ndarray[unsigned char, ndim=2] allr = frame[:,:,2]
    cdef double sum = 0
    cdef int count = 0
    cdef int r
    cdef int g
    cdef int b
    for i in range(x):
        for j in range(y):
            r = allr[i, j]
            g = allg[i, j]
            b = allb[i, j]
            if r>95 and g>40 and b>20 and max(b,g,r)-min(b,g,r)>15 and abs(r-g)>15 and r>g and r>b:
                if r>220 and g>210 and b>170 and g>b:
                    pass
                else:
                    ROIlist.append(g)

    cdef np.ndarray[long, ndim=1] ROIarray = np.array(ROIlist)
    cdef double m = np.mean(ROIarray)
    cdef double mstd = np.std(ROIarray)
    cdef double bottom_threshold = m - mstd*1.5
    cdef double top_threshold = m + mstd*1.5

    for item in ROIarray:
        if item > bottom_threshold and item < top_threshold:
            sum = sum + item
            count = count + 1



    cdef double result
    result = sum / count
    return result


def histo(np.ndarray[unsigned char, ndim=3] frame):
    cdef int x = frame.shape[0]
    cdef int y = frame.shape[1]
    cdef np.ndarray[unsigned char, ndim=2] newpic = np.zeros((x, y), dtype=np.uint8)
    cdef np.ndarray[unsigned char, ndim=2] allg = frame[:,:,1]
    cdef np.ndarray[unsigned char, ndim=3] frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cdef np.ndarray[unsigned char, ndim=2] H = frameHSV[:,:,0]
    cdef double sum = 0
    cdef int count = 0
    cdef int g

    for i in range(x):
        for j in range(y):
            if 0<H[i,j]<=20:
                newpic[i,j] = 255
                g = allg[i, j]
                sum = sum + g
                count = count + 1
    cdef double result
    result = sum / count
    return newpic


def histonumez(np.ndarray[unsigned char, ndim=3] frame):
    cdef int x = frame.shape[0]
    cdef int y = frame.shape[1]
    cdef np.ndarray[unsigned char, ndim=2] allg = frame[:,:,1]
    cdef np.ndarray[unsigned char, ndim=3] frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cdef np.ndarray[unsigned char, ndim=2] H = frameHSV[:,:,0]
    cdef double sum = 0
    cdef int count = 0
    cdef int g

    for i in range(x):
        for j in range(y):
            if 0<H[i,j]<=20:
                g = allg[i, j]
                sum = sum + g
                count = count + 1
    cdef double result
    result = sum / count
    return result


def otsu(np.ndarray[unsigned char, ndim=3] frame):
    cdef int x = frame.shape[0]
    cdef int y = frame.shape[1]
    cdef double sum = 0
    cdef int count = 0
    cdef int g
    cdef np.ndarray[unsigned char, ndim=2] newpic = np.zeros((x, y), dtype=np.uint8)
    cdef np.ndarray[unsigned char, ndim=3] frameYCC = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    cdef np.ndarray[unsigned char, ndim=2] Y = frameYCC[:,:,0]
    cdef np.ndarray[unsigned char, ndim=2] Cr = frameYCC[:,:,1]
    cdef np.ndarray[unsigned char, ndim=2] Cb = frameYCC[:,:,2]
    cdef double ret2
    cdef np.ndarray[unsigned char, ndim=2] th2
    ret2, th2 = cv2.threshold(Y, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    for i in range(frame.shape[0]):
        for j in range(frame.shape[1]):
            if th2[i, j] > 0 and Y[i, j]< 195:
                newpic[i,j] = 255
    return newpic


def otsunum(np.ndarray[unsigned char, ndim=3] frame):
    cdef int x = frame.shape[0]
    cdef int y = frame.shape[1]
    cdef double sum = 0
    cdef int count = 0
    cdef int g
    cdef np.ndarray[unsigned char, ndim=3] frameYCC = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    cdef np.ndarray[unsigned char, ndim=2] Y = frameYCC[:,:,0]
    cdef np.ndarray[unsigned char, ndim=2] Cr = frameYCC[:,:,1]
    cdef np.ndarray[unsigned char, ndim=2] Cb = frameYCC[:,:,2]
    cdef np.ndarray[unsigned char, ndim=2] allg = frame[:,:,1]
    cdef double ret2
    cdef np.ndarray[unsigned char, ndim=2] th2
    ret2, th2 = cv2.threshold(Y, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    for i in range(x):
        for j in range(y):
            if th2[i, j] > 0 and Y[i, j]< 195:
                g = allg[i, j]
                sum = sum + g
                count = count + 1
    cdef double result
    result = sum / count
    return result





