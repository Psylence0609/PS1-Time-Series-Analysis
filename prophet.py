# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 09:34:05 2021

@author: prane
"""

from fbprophet import Prophet
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet.plot import plot_plotly, plot_components_plotly
from fbprophet.plot import add_changepoints_to_plot
import os


directory_in_str=r"C:\Users\prane\Desktop\PS-1\Trend\json_to_csv"
directory=os.fsencode(directory_in_str)

for file in os.listdir(directory):
    '''
    Read file
    '''
    filename=os.fsdecode(file)
    f=directory_in_str+"\\" + filename
    df = pd.read_csv(f).iloc[:]
    
    '''
    Initialize variables
    '''
    x=1
    num=0
    diff=df.iloc[1,1]-df.iloc[0,1]
    if(diff==900):
        x=48
        num=288
    else:
        x=96
        num=120
    
    df=df.iloc[df.shape[0]-num:df.shape[0]-1,:]
    
    n=int(0.05*df.shape[0])
    period=df.iloc[df.shape[0]-1,1]-df.iloc[0,1]
    days=int(period/172800)
    
    '''
    rename
    '''
    dict={'timestamp':'ds','value':'y'}

    df.rename(columns=dict,inplace=True)

    ts=pd.to_datetime(df.ds, unit='s')
    df['ds']=ts

    '''
    Convolve
    '''
    '''
    k=np.ones(x)/x
    values_convolved=np.convolve(df['y'],k,mode='same')
    df['y']=values_convolved
    df.drop(df.tail(n).index,
        inplace = True)
    df=df.iloc[n:,:]
    '''
    '''
    Prophet
    '''
    m=Prophet(changepoint_prior_scale=0.0015)
    m.fit(df)
    future=m.make_future_dataframe(periods=days)
    forecast=m.predict(future)
    fig=m.plot(forecast)
    a = add_changepoints_to_plot(fig.gca(), m, forecast)
    save=filename.split('.')[0]
    fig.savefig(r"C:\Users\prane\Desktop\PS-1\Trend\fbprophet_graphs\Online_0.0015_noconvolve\\"+save+".jpeg")
    
    
    
