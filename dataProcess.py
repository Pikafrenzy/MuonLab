#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 13:03:10 2025

@author: ambroselo
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spOp
import statistics

testFile = open("test.txt","r")

dataFile = open("log.txt","r")

def fileToData(file):
    dataString = file.read()
    values = []
    for (i,string) in enumerate(dataString):
        if i%3 == 0:
            values.append(int(dataString[i:i+3],16))
    return values

def bins():
    return np.linspace(0,255,256)

data = fileToData(dataFile)

fig, ax = plt.subplots()
ax.hist(data,bins = bins())
print(statistics.median(data))

lifetimeNumber = []
lifetimeCount = []
for i in range(0,256):
    if(not data.count(i) == 0):
        lifetimeNumber.append(i*80+25)
        lifetimeCount.append(data.count(i))

fig2, ax2 = plt.subplots()
ax2.scatter(np.array(lifetimeNumber),lifetimeCount,2,label = "Raw Data")

def exponential(t,a,i,n):
    return a*np.exp(-i*t)+n

def doubleExponential(t,a,i,b,j,n):
    return a*np.exp(-i*t)+b*np.exp(-j*t)+n

def captureExponential(t,a,b,i,n):
    return a*np.exp(-i*t)+b*np.exp(-1.5*i*t)+n

singleExpParam, singleExpCoVar = spOp.curve_fit(exponential, lifetimeNumber, lifetimeCount,[80,0.01,1])

doubleExpParam, doubleExpCoVar = spOp.curve_fit(doubleExponential, lifetimeNumber, lifetimeCount,[80,0.01,80,0.01,1])

captureExpParam, captureExpCoVar = spOp.curve_fit(captureExponential, lifetimeNumber, lifetimeCount,[80,80,0.01,1])

lifetimeNumberSingleExpFit = []
lifetimeNumberDoubleExpFit = []
lifetimeNumberCaptureExpFit = []
for i, num in enumerate(lifetimeNumber):
    lifetimeNumberSingleExpFit.append(exponential(lifetimeNumber[i],singleExpParam[0],singleExpParam[1],singleExpParam[2]))
    lifetimeNumberDoubleExpFit.append(doubleExponential(lifetimeNumber[i],doubleExpParam[0],doubleExpParam[1],doubleExpParam[2],doubleExpParam[3],doubleExpParam[4]))
    lifetimeNumberCaptureExpFit.append(captureExponential(lifetimeNumber[i],captureExpParam[0],captureExpParam[1],captureExpParam[2],captureExpParam[3]))


singleExpFitLabel = "$y = {:.3f}e^{{-{:.3G}t}}+{:.3f}$".format(*singleExpParam)
doubleExpFitLabel = "$y = {:.3f}e^{{-{:.3G}t}}+{:.3f}e^{{-{:.3G}t}}+{:.3f}$".format(*doubleExpParam)
captureExpFitLabel = "$y = {:.3f}e^{{-{:.3G}t}}+{:.3f}e^{{-{:.3G}t}}+{:.3f}$".format(captureExpParam[0],captureExpParam[2],captureExpParam[1],1.5*captureExpParam[2],captureExpParam[3])

ax2.plot(np.array(lifetimeNumber),lifetimeNumberSingleExpFit,'tab:orange',linestyle = '--',label = singleExpFitLabel)
ax2.plot(np.array(lifetimeNumber),lifetimeNumberDoubleExpFit,'tab:green',linestyle = '--', label = doubleExpFitLabel)
ax2.plot(np.array(lifetimeNumber),lifetimeNumberCaptureExpFit,'tab:red',linestyle = '--', label = captureExpFitLabel)
ax2.legend()
ax2.set_title("Time between Start and Stop Signals")
ax2.set_xlabel("Lifetime (ns)")
ax2.set_ylabel("Count")

print(doubleExpParam)