# cython: language_level=3str
import numpy as np

ctypedef fused idf:
    int
    double
    long long

ctypedef fused fd:
    double
    long long

def spkCount(idf[:] S,fd[:] time, fd dt, idf window):
    assert tuple(S.shape) == tuple(time.shape)
    cdef Py_ssize_t size = time.shape[0]
    cdef int count
    yest = np.zeros(size, dtype= np.double)
    cdef double[:] yest_view = yest
    cdef double w
    w = window/dt
    cdef Py_ssize_t j, i
    for j in range(size - int(w)):
        count = 0
        for i in range(j, int(w)+j):
            if S[i] > 0:
                count = count + 1
        yest_view[j] = count/(w*dt*1e-3)
    return yest