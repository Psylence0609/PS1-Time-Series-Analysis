# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 09:22:33 2021

@author: prane
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pymannkendall as mk
import math
from pyper import *

r=R(use_numpy=True)

W = 48
K = 3
stride = 48 # stride

df = pd.read_csv(r'C:\Users\prane\Desktop\PS-1\json_to_csv\91314.csv').iloc[:]
# df = pd.read_csv('/home/ansh/Documents/GREENDECK_cliff/data/json_to_csv/155.csv').iloc[:]
df['trend'] = df.value.ewm(com=10).mean().values




strings = []
T = []
H = []
P = []
Z = []
M = []
C = []
I = []
S = []
V_S = []
trend_change_index = []

for ix in range(W, len(df), stride):
    vals = df.value.values[ix-W:ix+W+1]
    # title = str(mk.original_test(vals))

    # t, h, p, z, Tau, s, var_s, slope, intercept = mk.original_test(vals, alpha=0.01)
    t, h, p, z, Tau, s, var_s, slope, intercept = mk.regional_test(vals, alpha=0.01)
    
    T.append(t)
    H.append(h)
    P.append(p)
    Z.append(z)
    S.append(s)
    V_S.append(var_s)
    M.append(slope)
    C.append(intercept)
    I.append(ix)

M = np.array(M).reshape(-1,1)
C = np.array(C).reshape(-1,1)

window = np.array(range(0, 2*W+1))
windows = np.array([np.array(range(i-W, i+W+1)) for i in I])
tan_lines = window*M + C



def digitize_trend_string(T):
    '''
    takes a list/array of trend strings
    converts them according to the mapping:
        -1 : decreasing
         0 : no trend
         1 : increasing
    '''
    T = np.array(T)
    T_ = np.zeros(T.shape)
    T_[np.where(T=='increasing')[0]] = 1
    T_[np.where(T=='decreasing')[0]] = -1
    T_[np.where(T=='no trend')[0]] = 0
    return T_


T_ = digitize_trend_string(T)
R = []
ongoing = None
trend_cp = []
trend_cp_string = []
alert_pt = []
for ix in range(len(T_)):
    if ix < K-1: continue;
    
    elif np.all(T_[ix-K+1:ix+1] == 0):
        if ongoing == 0:
            print(I[ix], "0.")
        elif ongoing == 1:
            ongoing = 0
            trend_cp.append(I[ix-K+1])
            alert_pt.append(min(I[ix] + W, len(df)-1))
            trend_cp_string.append('increasing => no_trend')
            print(I[ix], "**alert:: trend change increasing to no_trend.**")
        elif ongoing == -1:
            ongoing = 0
            trend_cp.append(I[ix-K+1])
            alert_pt.append(min(I[ix] + W, len(df)-1))
            trend_cp_string.append('decreasing => no_trend')
            print(I[ix], "**alert:: trend change decreasing to no_trend.**")
        elif ongoing == None:
            ongoing = 0
            print(I[ix], "info:: set ongoing trend to no_trend.")
            
    elif np.all(T_[ix-K+1:ix+1] == 1):
        if ongoing == 1:
            print(I[ix], "1.")
        elif ongoing == 0:
            ongoing = 1
            trend_cp.append(I[ix-K+1])
            alert_pt.append(min(I[ix] + W, len(df)-1))
            trend_cp_string.append('no_trend => increasing')
            print(I[ix], "**alert:: trend change no_trend to increasing.**")
        elif ongoing == -1:
            ongoing = 1
            trend_cp.append(I[ix-K+1])
            alert_pt.append(min(I[ix] + W, len(df)-1))
            trend_cp_string.append('decreasing => increasing')
            print(I[ix], "**alert:: trend change decreasing to increasing.**")
        elif ongoing == None:
            ongoing = 1
            print(I[ix], "info:: set ongoing trend to increasing.")
            
    elif np.all(T_[ix-K+1:ix+1] == -1):
        if ongoing == -1:
            print(I[ix], "-1.")
        elif ongoing == 0:
            ongoing = -1
            trend_cp.append(I[ix-K+1])
            alert_pt.append(min(I[ix] + W, len(df)-1))
            trend_cp_string.append('no_trend => decreasing')
            print(I[ix], "**alert:: trend change no_trend to decreasing.**")
        elif ongoing == 1:
            ongoing = -1
            trend_cp.append(I[ix-K+1])
            alert_pt.append(min(I[ix] + W, len(df)-1))
            trend_cp_string.append('increasing => decreasing')
            print(I[ix], "**alert:: trend change increasing to decreasing.**")
        elif ongoing == None:
            ongoing = -1
            print(I[ix], "info:: set ongoing trend to decreasing.")
        
        

plt.figure(figsize=(20,8))
plt.plot(df.value.values)
plt.plot(df.trend.values, c='violet')


for cp, s in zip(trend_cp, trend_cp_string):
    plt.axvline(cp)
    plt.text(cp-10, df.value.values[cp], s, rotation=90)
plt.scatter(alert_pt, df.value.values[alert_pt], marker='x', c='r', s=100)


for x,y,t in zip(windows, tan_lines, T):
    if t == 'increasing':
        plt.plot(x,y, c='g', linewidth=10, alpha=0.15)
    elif t == 'decreasing':
        plt.plot(x,y, c='r', linewidth=10, alpha=0.15)
    elif t == 'no trend':
        plt.plot(x,y, c='b', linewidth=10, alpha=0.15)
'''
plt.plot(672,df.value.values[672],'r*',markersize=10) 

plt.plot(480,df.value.values[480],'r*',markersize=10)

plt.plot(1872,df.value.values[1872],'r*',markersize=10)       
plt.plot(1920,df.value.values[1920],'r*',markersize=10)
plt.plot(2208,df.value.values[2208],'r*',markersize=10)        
plt.plot(2544,df.value.values[2544],'r*',markersize=10)     
plt.plot(3312,df.value.values[3312],'r*',markersize=10)


N=len(P)
d=3

set=np.zeros((N,d))

for j in range(0,N):
    if T_[j]==1:
        set[j,0]=M[j,0]
    elif T_[j]==-1:
        set[j,1]=M[j,0]
    else:
        set[j,2]=M[j,0]
        

index=pd.Series(range(0,N))
dataset=pd.DataFrame(set,index=index,columns=['Incresing','Decreasing','No trend']) 

arm_selected=[]
number_of_selections = [0]*d
sums_of_reward=[0]*d;
total_reward=0

for n in range(0,N):
    arm=0
    max_upper_bound=0
    for i in range(0,d):
        if(number_of_selections[i] >0 ):
            average_reward = sums_of_reward[i]/number_of_selections[i]
            delta_i=math.sqrt(2*math.log(n+1)/number_of_selections[i])
            upper_bound=average_reward+delta_i
        else:
            upper_bound = 1e400
        if upper_bound>max_upper_bound:
            max_upper_bound = upper_bound
            arm=i
    arm_selected.append(arm)
    number_of_selections[arm]+=1
    reward=abs(dataset.values[n,arm])
    sums_of_reward[arm]+=reward
    total_reward+=reward

S=pd.Series(arm_selected).value_counts(normalize=True)
'''
def locate_change(df,i,incre,pvalue_thr=0.01):
    l=len(df.index)
    x0=df[0:i,1]
    y0=df[0:i,0]
    point=[]
    while(i<l):
        x1=df[i:min(i+incre,l),1]
        y1=df[i:min(i+incre,l),0]
        
        slope0=M[int(i/W)-1,0]
        slope=M[int(i/W),0]
        c0=C[int(i/W)-1,0]
        c=C[int(i/W),0]
        tscore=linear_test(slope0,slope,c0,c,x1)
        
        if(tscore<pvalue_thr):
            point.append(i/2)
        i+=incre
        
    return point
            
            
        
    
    
def linear_test(m0,m,c0,c,X,Y):
    l=len(X.index)
    predicted = m*X[,0]+c
    residuals=Y-predicted
    r_square=residuals[,0]**2
    SSR=r_square.sum(axis=0,skipna=True)
    SSRx=
    
    