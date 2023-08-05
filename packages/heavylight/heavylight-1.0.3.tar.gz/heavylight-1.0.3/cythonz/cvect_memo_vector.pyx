# cython: language_level=3, boundscheck=False, wraparound=False
# distutils: language=c++

from libcpp.vector cimport vector
from libcpp cimport bool

cdef class Policy:
    cdef int proj_len
    cdef vector[double] _v1
    cdef vector[bool] _b1
    cdef vector[double] _v2
    cdef vector[bool] _b2

    def __init__(self, proj_len: int):
        cdef int i = 0
        self.proj_len = proj_len
        while i < proj_len:
            self._v1.push_back(0)      # there is probably a better way
            self._b1.push_back(False)
            self._v2.push_back(0)
            self._b2.push_back(False)
            i += 1

    cdef public double num_pols(self, int t) nogil:
        #_v1
        #_b1
        if self._b1[t]:
            return self._v1[t]
        else:
            if t == 0:
                value = 1
            else:
                value = self.num_pols(t - 1) - self.num_deaths(t - 1)
            self._v1[t] = value
            self._b1[t] = True
            return value
        
    cdef public double num_deaths(self, int t) nogil:
        #_v2
        #_b2
        if self._b2[t]:
            return self._v2[t]
        else:
            value = self.num_pols(t) * 0.01
            self._v2[t] = value
            self._b2[t] = True
            return value
    


def run_pol():
    p = Policy(400)
    return p.num_pols(399)


