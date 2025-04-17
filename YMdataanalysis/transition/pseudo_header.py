import numpy as np
import pandas as pd
import json
import os
import random
import sys
import csv
from tqdm import tqdm
from calendar import c
import fileinput
from scipy.special import kn
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

# binning functions

def get_blocks(sample, binsize):
    blocks = []

    n = len(sample)

    if n%binsize != 0:
        sample = sample[0:n-n%binsize:1]

    for j in range(n//binsize):
        blocks.append(sample[j*binsize:(j+1)*binsize:1])

    return blocks

# bootstrap of a sample

def bootstrap(sample, bootstrap_size):
    bootstrap_samples = []
    
    n = len(sample)

    for j in range(bootstrap_size):
        bootstrap_sample = []

        for i in range(n):
            r = random.randint(0, n-1)

            bootstrap_sample.append(sample[r])

        bootstrap_samples.append(bootstrap_sample)

    return bootstrap_samples

# bootstrap of a two samples

def bootstrap2(sample1, sample2, bootstrap_size):
    bootstrap_samples1 = []
    bootstrap_samples2 = []
    
    n = len(sample1)

    for j in range(bootstrap_size):
        bootstrap_sample1 = []
        bootstrap_sample2 = []

        for i in range(n):
            r = random.randint(0, n-1)

            bootstrap_sample1.append(sample1[r])
            bootstrap_sample2.append(sample2[r])

        bootstrap_samples1.append(bootstrap_sample1)
        bootstrap_samples2.append(bootstrap_sample2)

    return bootstrap_samples1, bootstrap_samples2

# file writing

def scrivi_su_file(vettore1, vettore2, vettore3, nome_file):
    with open(nome_file, 'w') as file_output:
        for valore1, valore2, valore3 in zip(vettore1, vettore2, vettore3):
            riga = f"{valore1}\t{valore2}\t{valore3}\n"  
            file_output.write(riga)

# general matplotlib params

plt.rcParams["figure.figsize"] = [16, 9]
plt.rcParams["figure.autolayout"] = True

plt.rc('font', size = 40)          # controls default text sizes
plt.rc('axes', titlesize = 40)     # fontsize of the axes title
plt.rc('axes', labelsize = 40)    # fontsize of the x and y labels
plt.rc('xtick', labelsize = 30)    # fontsize of the tick labels
plt.rc('ytick', labelsize = 30)    # fontsize of the tick labels
plt.rc('legend', fontsize = 30)    # legend fontsize
plt.rc('figure', titlesize = 40)  # fontsize of the figure title


# perform finite size scaling

def FSS(L, Y, SY, S_DIM1, S_DIM2, H_C, MIN, MAX, STEP):
    nov = int((MAX-MIN)/STEP)

    x = (np.linspace(MIN-H_C, MAX-H_C, nov+1)*L**(1/S_DIM2)).tolist()
    
    y = (Y*L**(-S_DIM1/S_DIM2)).tolist()
    sy = (SY*L**(-S_DIM1/S_DIM2)).tolist()
    
    return x, y, sy

# y = a + b*x

def binder1(x, a, b):
     return a + b*x

def binder2(x,a,b,c):
     return a + b*x + c*x**3

# y = a + b*x + c*x^3

# y = a + b*(x-c)^2

def quadratic(x, a, b, c):
     return a + b*(x-c)**2

# y = a + b*x^c

def f_scaling(x, a, b, c):
	return a + b*x**c

def gammanu(x,a,b):
     return a+b*x**float(7/4)

def nu(x,a,b):
     return a+b*x

# reduced chi squared

def rchisq(model, data, err, n):
     return np.sum(((model-data)/err)**2)/n

# V T=0

def V_0(x, a, b, c):
	return a + b*x + c*1/x

# V T=finite

def V_finite(x, a, b, c, d):
	return a + b*x + c*1/x + d*np.log(x)

# V T=finite log only

def V_finite_log(x, a, b, c):
	return a + b*x + 0.5*c*np.log(x)

# modified bessel function of the second kind of order zero

def K0(x, a, b):
      return a*kn(0, b*x)

# modified bessel function of the second kind of order one

def K1(x, a, b):
      return a*kn(1, b*x)

# E0=(Nt, h = const)

def NGNt(x, a, b):
     return a*x*np.sqrt(1-b/x**2)

# test func
def test(x, a, b, c):
     return 1/x*(a+b*np.sqrt(x**2-c))**2*np.sqrt(1-1/(1+b/a*np.sqrt(x**2-c)))




