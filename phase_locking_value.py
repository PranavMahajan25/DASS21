import numpy as np
import scipy.signal as sig

def plv(y1,y2):
    sig1_phase=np.angle(sig.hilbert(y1))
    sig2_phase=np.angle(sig.hilbert(y2))
    complex_phase_diff = np.exp(np.complex(0,1)*(sig1_phase - sig2_phase))
    plv = np.abs(np.sum(complex_phase_diff))/len(sig1_phase)
    return plv

def plv_arr(C):
    """
    Returns the sample linear phase locking values between pairs of variables in C.
    Parameters
    ----------
    C : array-like, shape (n, p)
        Array with the different variables. Each column of C is taken as a variable
        n is the length of each timeseries and p is the number of timeseries.
    Returns
    -------
    PLV_arr : array-like, shape (p, p)
        P[i, j] contains the absolute PLV of C[:, i] and C[:, j].
    """

    C = np.asarray(C)
    p = C.shape[1]
    PLV_arr = np.zeros((p, p), dtype=np.float)
    for i in range(p):
        PLV_arr[i, i] = 0 #to avoid self-loops
        for j in range(i+1, p):
            PLV_arr[i, j] = plv(C[:,i], C[:,j])
            PLV_arr[j, i] = PLV_arr[i, j]
    return PLV_arr

def test_plv():
    a = np.random.rand(100)
    b = np.random.rand(100)
    print(plv(a,b))

def test_plv_arr():
    inp = np.random.rand(100,5)
    print(plv_arr(inp))
