import warnings
warnings.filterwarnings("ignore")

# basic package
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# feature selection package
from sklearn.model_selection import train_test_split
from sklearn.model_selection import learning_curve
from sklearn.model_selection import validation_curve
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn import linear_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import PolynomialFeatures
from scipy.stats import boxcox
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFECV

# normalize data to range [0, 1]
def zeroOne_normalize(df):
    col_name = list(df)
    df_norm = MinMaxScaler().fit_transform(df)
    df_norm_table = pd.DataFrame(df_norm, columns=col_name)
    return df_norm_table

# compute feature relevance(correlation) to target class 
# and redundancy with other features
# return a table with all features ranked by correlation from high to low
# and redundancy from low to high 

# relevance formula: correlation with target class
# redundancy formula: sum of absolute value of correlation with other features / (number of features - 1)
def mrmr(x, y):
    corr_matrix_abs = abs(x.corr())
    lst = []
    features = x.head()
    corr = x.apply(lambda x: x.corr(y))
    depend = (corr_matrix_abs.sum(axis=1) - 1)/ (len(features) - 1)
    lst = zip(features, corr, depend)
    
    lst = sorted(lst, key=lambda x: (x[1], -1 * abs(x[2])), reverse=True)
    output = pd.DataFrame(lst, columns=['Feature', 'Correlation (absolute value high to low)', 'Dependency (low to high)'])
    return output

# convert categorical features to numeric
def convertToNumeric(string):
    arr = string.split()
    if arr[0]=='Minimal':
        return 1
    elif arr[0]=='Mild':
        return 2
    elif arr[0]=='Moderately':
        return 3
    elif arr[0]=='Severe':
        return 4
    else: # na
        return 0

# get csv file in path, encode 'Severity' to numeric, select only numeric data
# move target class to the last column
def cleanData(path):
    df = pd.read_csv(path, index_col=0)
    df['Severity_score'] = df['Severity'].apply(convertToNumeric)
    df = df.select_dtypes(['number']).dropna(axis=1,how='any')
    return df

# separate target class column from feature column 
def separateVars(df):
    y = df['Severity_score']
    x= df.drop(['Severity_score'], axis=1)
    return x, y

def main():
    csv_path = None
    while True:
        csv_path = input("Please provide a path to a csv file: ")
        if os.path.exists(csv_path) == False:
            print("The path that you provided is incorrect. Please try again.")
        elif os.path.isfile(csv_path) == False:
            print("The path that you provided is not a file. Please try again.")
        elif csv_path.endswith('.csv') == False:
            print("The path that you provided is not a csv file. Please try again.")
        else:
            break  
    df = cleanData(csv_path)
    x, y = separateVars(df) 
    x_norm = zeroOne_normalize(x)
    result = mrmr(x_norm, y)
    print(result)

if __name__ == '__main__':
    main() 
