from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    r'C:\Users\prane\Desktop\PS-1\Trend\json_to_csv\91314.csv').iloc[:]

ts = df['ds']
for i in range(0, ts.shape[0]):
    ts[i] = datetime.utcfromtimestamp(
        ts[i]).strftime('%Y-%m-%d %H:%M:%S')


df['ds'] = ts[0]
df.to_csv(r'C:\Users\prane\Desktop\PS-1\Trend\json_to_csv\91314.csv')
