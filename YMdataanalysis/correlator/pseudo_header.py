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
plt.rc('legend', fontsize = 20)    # legend fontsize
plt.rc('figure', titlesize = 40)  # fontsize of the figure title

# plot w/ error bars

def plotting(X, Y, SY, COLOR, LATTICEDIM, XLABEL, YLABEL, TITLE, SAVEPATH):
    plt.grid()
    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    plt.title(TITLE)
    plt.plot(X, Y, marker = "^", color = COLOR, markersize = 8, linewidth = 1, label = LATTICEDIM)
    plt.errorbar(X, Y, SY, color = COLOR, capsize = 8)
    plt.legend()
    plt.savefig(SAVEPATH, facecolor = 'w')

# perform finite size scaling

def FSS(L, Y, SY, S_DIM1, S_DIM2, H_C, MIN, MAX, STEP):
    nov = int((MAX-MIN)/STEP)

    x = (np.linspace(MIN-H_C, MAX-H_C, nov+1)*L**(1/S_DIM2)).tolist()
    
    y = (Y*L**(-S_DIM1/S_DIM2)).tolist()
    sy = (SY*L**(-S_DIM1/S_DIM2)).tolist()
    
    return x, y, sy

# y = a + b*x

def linear(x, a, b):
     return a + b*x

# y = a + b*(x-c)^2

def quadratic(x, a, b, c):
     return a + b*(x-c)**2

# y = a + b*x^c

def f_scaling(x, a, b, c):
	return a + b*x**c

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

# modified bessel function of the second kind of order zero symmetric version for a L=96 lattice

def K0sym(x, a, b):
     return a*(kn(0,b*x)+kn(0,b*(96-x)))

# modified bessel function of the second kind of order one

def K1(x, a, b):
      return a*kn(1, b*x)

# symmetrized K1

def K1sym(x, a, b):
      return a*(kn(1, b*x)+kn(1,b*(96-x)))

# E0=(Nt, h = const)

def NGNt(x, a):
     return a*x*np.sqrt(1-np.pi/(3*a*x**2))

# E_0 Makeenko
def E0Makeenko(x, a, b):
     sqrtlambda11 = 9*a/8*1/x+np.sqrt(81/16*a**2/x**2+b-np.pi/x**2)
     omega = np.sqrt(x**2-3*x*a/2*1/sqrtlambda11)
     return omega*sqrtlambda11**2

# E0NG mod

def NGNtmod(x,a,b,c):
     return a*x*np.sqrt(1+b/x**2)+c/x**7



