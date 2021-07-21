
import os,sys
from matplotlib.pyplot import ylabel

pathFiles = os.listdir('2016TopologyZooUCL_inverseCapacity')

smallG = {}
mediumG = {}
bigG = {}

for i in range(len(pathFiles)):
    p = pathFiles[i].split('.')

    if(len(p) == 2):
        with open('.\\2016TopologyZooUCL_inverseCapacity'+ '\\' + pathFiles[i])as f:
            line = f.readline()
            line = line.split()
            nNodes = int(line[1])
            if nNodes <= 20:
                smallG[p[0]] = 1
            else:
                if nNodes <= 40:
                    mediumG[p[0]] = 1
                else :
                    bigG[p[0]] = 1

import plotly.graph_objects as go

data = []
with open('output1.txt')as f:
    lines = f.readlines()
    for line in lines:
        if line.split()[0] in smallG.keys():
            data.append(float(line.split()[-1]))
data = sorted(data)
data1 = []
with open('SRLS-mlu-1.csv')as f:
    lines = f.readlines()
    for line in lines:
        if line.split(',')[0] in smallG.keys():
            data1.append(float(line.split(',')[-1]))
data1 = sorted(data1)

import pandas as pd
import numpy as np
import plotly.express as px

ar = np.array([data, data1])
df = pd.DataFrame(ar.T, columns=['myLS  (nNodes <= 20  time out = 1s)', 'LS ( nNodes <=20 time out = 1s)'])

fig = px.box(df, log_y= True, points=False )
fig.show()


