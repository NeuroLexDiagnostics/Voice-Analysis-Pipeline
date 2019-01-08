import warnings
warnings.filterwarnings("ignore")

# basic package
import os
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler, MinMaxScaler

# separate target class column from feature column 
def separateVars(df, target_name):
    y = df[target_name]
    x= df.drop([target_name], axis=1)
    return x, y

# encode target class
def encode(df, encoding):
    df.replace(encoding, inplace = True)
    return df

# remove columns with missing values, select only numeric data
def cleanData(df):
    df = df.select_dtypes(['number']).dropna(axis=1,how='any')
    return df

# standardization
def standardization(df):
    col_name = list(df)
    df_norm = StandardScaler().fit_transform(df)
    df_norm_table = pd.DataFrame(df_norm, columns=col_name)
    return df_norm_table

# normalize data to range [0, 1]
def zeroOne_normalize(df):
    col_name = list(df)
    df_norm = MinMaxScaler(feature_range=(0,1)).fit_transform(df)
    df_norm_table = pd.DataFrame(df_norm, columns=col_name)
    return df_norm_table