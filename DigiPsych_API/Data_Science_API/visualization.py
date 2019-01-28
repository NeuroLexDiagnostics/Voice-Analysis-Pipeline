import warnings
from matplotlib.streamplot import InvalidIndexError
warnings.filterwarnings("ignore")

# basic package
import os
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# get correlation plot between two variables
def corrPlot(df, first, second):
    if first in df.head() and second in df.head():
        sns.jointplot(df.loc[:,first], df.loc[:,second], kind="regg", color="#ce1414")   
        plt.show()
    else:
        print("At least one of the features doesn't exist in the table. ")

# get pair-wise plot along 3+ variables
def pairGrid(df, features):
    for feature in features:
        if feature not in df.head():
            print("At least one of the features doesn't exist in the table. ")
            return     
    sns.set(style="white")
    partial = df.loc[:,features]
    g = sns.PairGrid(partial, diag_sharey=False)
    g.map_lower(sns.kdeplot, cmap="Blues_d")
    g.map_upper(plt.scatter)
    g.map_diag(sns.kdeplot, lw=len(features))
    plt.show()

# plot every feature vs. target class 
# color-code every class/label in target class
def violinPlot(x, y):
    try:
        name = list(y)[0]
        size = len(x.columns)
        sns.set(style="whitegrid")
        data = pd.concat([y,x],axis=1)
        data = pd.melt(data,id_vars=name,
                        var_name="features",
                        value_name="value")
        plt.figure(figsize=(size,size))
        sns.swarmplot(x="features", y="value", hue=name, data=data)
    
        plt.xticks(rotation=90)
        plt.show()
    except InvalidIndexError:
        print("There are repeat features. Please try again. ")

# heapMap color-code correlation between every pair of features
def heapMap(df):
    size = len(df.columns)
    f,ax = plt.subplots(figsize=(size, size))
    sns.heatmap(df.corr(), annot=True, linewidths=.5, fmt= '.1f',ax=ax)
    plt.show()