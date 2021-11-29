# Author: LJR
import sys
import os
import numpy as np
from pylab import plot, legend, xlabel, ylabel, savefig

def fit_linear(x, y):
    W = np.polyfit(x, y, 1)
    return np.poly1d(W), W

def fit_exp(x, y):
    W = np.polyfit(x, np.log(y), 1)
    W[0] = np.exp(W[0])
    return lambda a: W[0]*np.exp(W[0]*a), W

def fit_log(x, y):
    W = np.polyfit(np.log(x), y, 1)
    return lambda a: W[0] + W[1]*np.log(a), W

def fit_poly(x, y):
    W = np.polyfit(x, y, 5)
    return np.poly1d(W), W

def plotFile(filename, method):
    data = np.genfromtxt(filename, delimiter=','); x=data[:,0]; y=data[:,1]
    if method=='linear':
        fun_fit = fit_linear
    elif method=='exp':
        fun_fit = fit_exp
    elif method=='log':
        fun_fit = fit_log
    elif method=='poly':
        fun_fit = fit_poly
    else:
        raise Exception("Invalid Method!")
    # Expand fit range
    xmax = np.amax(x);  xmin = np.amin(x)
    xlen = xmax - xmin; xex  = xlen/5
    xfit = np.arange(xmin-xex, xmax+xex, 0.05)
    fitline, W = fun_fit(x, y); W = np.around(W, 2)
    plot(xfit, fitline(xfit), 'r-', label=f'Fit parameters = {W[0]}, {W[1]}\nMethod={method}')
    plot(x, y, 'o')
    legend()
    savefig(filename[:-4]+f'_{method}.pdf', format="pdf")

if __name__=='__main__':
    plotFile('data_10ohm.csv', 'poly')
