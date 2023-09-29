from dateutil.parser import parse
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from itertools import product
import numpy as np
import pandas as pd
import torch

def plot_df(df, x, y, title="", xlabel='Date', ylabel='Frequency', dpi=50):
    plt.figure(figsize=(10,5), dpi=dpi)
    plt.plot(x, y, color='tab:red')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()


def freq(dp):
    new = {"seq":[], "Time": [], "frequency": [], 'channel': []}
    # #print(data.info)
    i=0
    for index in dp.index:
        if dp.loc[index]['sub_category'] == "uplink_unconfirmed":
            i+=1
            new["seq"].append(i)
            new["frequency"].append(dp.loc[index]["data"]["hotspot"]["frequency"])
            new["channel"].append(dp.loc[index]["data"]["hotspot"]["channel"])
            new["Time"].append(dp.loc[index]['reported_at'])
    return new

data = pd.read_json("event-debug (7).json", orient='columns')

Freqtime = freq(data)

pd =pd.DataFrame(data=Freqtime)
print(pd)

torch.
#data.index=data['reported_at']

#plot_df(data, x=Freqtime['seq'], y=Freqtime['frequency'], title='Frequency analysis.')
# allfreq = Freqtime['frequency'].copy()
# arr = np.array(allfreq)
# freq = np.unique(arr)
# colors = cm.rainbow(np.linspace(0, 1, len(arr)))
# #mycolors = np.random.choice(list(mpl.colors.XKCD_COLORS.keys()), len(freq), replace=False)
# mycolors=['olive','blue','orange','cyan','green','gray','pink','red']
# temp=[]
# for y in freq:
#     temp.append(y)
#
# plt.figure()
# #plt.boxplot(Freqtime['seq'], Freqtime['frequency'], c=allfreq, cmap='plasma', alpha=0.7)
#
# #plt.show()
# channel=len(freq)
# count={}
# prem = product(freq, repeat=8)
# for i in prem:
#     count[i]=0
#     for j in range(0,len(arr),len(freq)):
#
#         if ((j+channel) < len(arr)) and (list(i)== allfreq[j:j+channel]):
#             count[i]+=1
#
# for key in count.keys():
#     if count[key]>0:
#         print(key, count[key])
# #print(count)
# # m=len(freq)
# # k = len(new["frequency"])//m
# # l = list(np.arange(0,k))
# # for i in range(0,k):
# #     while len(s1) > 0:
# #         l[i] = s1[:m]
# #         s1 = s1[m:]
# #         break
# # n = l
# print(n,len(n))
#
# new1 =pd.DataFrame(new,columns=["frequency","Time"])
#
# new1["frequency"].plot(kind="hist")
# plt.show()
