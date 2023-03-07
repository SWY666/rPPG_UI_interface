#去趋势化函数
import numpy as np
cimport numpy as np
from scipy import signal

def Drtrending(list l0, int sr):
    cdef np.ndarray[double, ndim=1] l1 = np.array(l0)
    cdef list result = [0.0 for x in range(len(l1))]
    cdef double means
    if len(l0) <= sr:
        return l0
    else:
        for i in range(1, sr):
            means = np.mean(l0[:i])
            result[i] = (l1[i] - means) / means
        for i in range(sr, len(l1)):
            means = np.mean(l0[i-sr:i])
            result[i] = (l1[i] - means) / means
        result[0] = result[1]

    return result

def MA(list meanlist,int samplingrate):
    cdef int M = int(samplingrate/4)
    if len(meanlist) <= M:
        return meanlist
    else:
        return MAlistMaker(meanlist, M)

cdef list MAlistMaker(list meanlist,int M):
    cdef list result = [0.0 for i in range(len(meanlist))]
    for index in range(len(meanlist)):
        if index + 1 < M:
            result[index] = (sum(meanlist[0:index+1])+sum(meanlist[index-M:-1]))/M
        else:
            result[index] = sum(meanlist[index-M+1:index+1])/M
    return result


def IPPG_process(list listin, int samplingrate, double f1=0.65, double f2=4):
    cdef list result = Drtrending(listin, samplingrate)
    result = MA(result, samplingrate)
    b, a = signal.butter(8, [2 * f1 / samplingrate, 2 * f2 / samplingrate], 'bandpass')
    cdef np.ndarray[double, ndim=1] meanslist_after_BP = signal.filtfilt(b, a, result)
    return meanslist_after_BP


def peakcheckez(list a, int samplingrate):
    cdef list result = []
    cdef int hr
    for i in range(len(a)):
        if i == 0 or i == len(a)-1:
            pass
        else:
            if a[i]>a[i-1] and a[i]> a[i+1]:
                result.append(i)

    if len(result) <= 2:
        hr = 0
    else:
        hr = int((len(result)*60)/((result[-1]-result[1])/samplingrate))

    return hr, result
