#cython: boundscheck=False, wraparound=False, nonecheck=False
import numpy as np

def goertzel(long[:] chunk, double[:] coeff):
        cdef int N, M, ii, jj
        N = chunk.shape[0]
        M = 8 #coeff.shape[0]
        cdef double[:] s_prev, prev_part, s_prev2, s
        s_prev=np.zeros(M)
        prev_part=np.zeros(M)
        s_prev2=np.zeros(M)
        s=np.zeros(M)

        for ii in range(N):
          for jj in range(M):
            s[jj] = chunk[ii] + prev_part[jj]
            s_prev2[jj] = s_prev[jj]
            s_prev[jj] = s[jj]
            prev_part[jj] = (coeff[jj] * s_prev[jj]) - s_prev2[jj]

        for jj in range(M):
           s_prev[jj]=s_prev[jj] * s_prev[jj] - s_prev2[jj] * prev_part[jj]

        return s_prev