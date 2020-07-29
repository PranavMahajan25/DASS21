import numpy as np
from scipy import stats, linalg

def cross_corr(C):
    """
    Returns the sample linear partial correlation coefficients between pairs of variables in C, controlling 
    for the remaining variables in C.
    Parameters
    ----------
    C : array-like, shape (n, p)
        Array with the different variables. Each column of C is taken as a variable.
        n is the length of each timeseries and p is the number of timeseries.
    Returns
    -------
    C_corr : array-like, shape (p, p)
        P[i, j] contains the absolute values of partial correlation of C[:, i] and C[:, j] controlling
        for the remaining variables in C.
    """

    C = np.asarray(C)
    p = C.shape[1]
    C_corr = np.zeros((p, p), dtype=np.float)
    for i in range(p):
        C_corr[i, i] = 0
        for j in range(i+1, p):
            corr = stats.pearsonr(C[:, i], C[:, j])[0]
            C_corr[i, j] = abs(corr)
            C_corr[j, i] = abs(corr)

    return C_corr


def partial_corr(C):
    """
    Returns the sample linear partial correlation coefficients between pairs of variables in C, controlling 
    for the remaining variables in C.
    Parameters
    ----------
    C : array-like, shape (n, p)
        Array with the different variables. Each column of C is taken as a variable
        n is the length of each timeseries and p is the number of timeseries.
    Returns
    -------
    P_corr : array-like, shape (p, p)
        P[i, j] contains the absolute values of partial correlation of C[:, i] and C[:, j] controlling
        for the remaining variables in C.
    """

    C = np.asarray(C)
    p = C.shape[1]
    P_corr = np.zeros((p, p), dtype=np.float)
    for i in range(p):
        P_corr[i, i] = 0
        for j in range(i+1, p):
            idx = np.ones(p, dtype=np.bool)
            idx[i] = False
            idx[j] = False
            beta_i = linalg.lstsq(C[:, idx], C[:, j])[0]
            beta_j = linalg.lstsq(C[:, idx], C[:, i])[0]

            res_j = C[:, j] - C[:, idx].dot( beta_i)
            res_i = C[:, i] - C[:, idx].dot(beta_j)

            corr = stats.pearsonr(res_i, res_j)[0]
            P_corr[i, j] = abs(corr)
            P_corr[j, i] = abs(corr)

    return P_corr

def test_corr():
    inp = np.random.rand(100,5)
    print(cross_corr(inp))
    print(partial_corr(inp))


