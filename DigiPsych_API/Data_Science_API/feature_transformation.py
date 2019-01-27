import warnings
warnings.filterwarnings("ignore")

# basic package
import os
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import bisect

# advanced package
from sklearn.metrics import r2_score
from sklearn.decomposition import PCA
from sklearn.decomposition import FastICA 
from sklearn.decomposition import FactorAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import VarianceThreshold

# drop columns with no variance
def low_var_filter(df):
    df_low = df.loc[:, df.var() != 0.0]
    removed = len(df.columns) - len(df_low.columns)
    print(str(removed) + " features have been removed. ")
    return df_low

# remove high correlated columns where the correlation is above threshold
def high_corr_filter(df, threshold=0.8):
    # check threshold value
    if threshold <= 0 or threshold >= 1:
        print("The correlation threshold has to be between 0 and 1. "
              "Change to use the default threshold 0.8.");
        threshold = 0.8
    
    # get highly correlated features
    df_corr = df.corr(method='pearson', min_periods=1)
    df_not_correlated = ~(df_corr.mask(np.tril(np.ones([len(df_corr)]*2, dtype=bool))).abs() > threshold).any()
    
    # remove features
    un_corr_idx = df_not_correlated.loc[df_not_correlated[df_not_correlated.index] == True].index
    df_out = df[un_corr_idx]
    
    removed = len(df.columns) - len(df_out.columns)
    print(str(removed) + " features have been removed. ")
    return df_out

# factor analysis, combine features in group of group_value
def factor_analysis(df, group_value=3):
    # check group_value range
    if group_value <= 1 or group_value > len(df.columns):
        print("Group value has to be between 1 and number of columns. "
              "Change to use default group value 3. ")
        group_value = 3
    
    try:
        # round group_value in case the parameter is float
        group_value = int(round(group_value))
    
        # transform df using factor analysis
        fa = FactorAnalysis(n_components = group_value, random_state=0)
        df_fa = fa.fit_transform(df)
        
        plt.figure()
        plt.title('Factor Analysis Components')
        
        for i in range(group_value):
            for j in range(i+1, group_value):
                plt.scatter(df_fa[:,i], df_fa[:,j])
        
        plt.show()
        
        return df_fa
    except ValueError:
        print("Skipped n_component = " + str(group_value) + " since i > min(n_samples, n_features).")

# plot cumulative explained variance vs. number of components
def pca_plot(df):
    df_pca = PCA().fit(df);
    explained_var = np.cumsum(df_pca.explained_variance_ratio_)
    plt.plot(explained_var)
    plt.grid(True)
    plt.title('(PCA) Num. of Components vs. Cumulative explained variance')
    plt.xlabel('number of components')
    plt.ylabel('cumulative explained variance')
    plt.show()  

# plot ica components by comp_value
def ica_plot(df, comp_value):
    try:
        ica = FastICA(n_components=comp_value)
        df_ica = ica.fit_transform(df)
        
        plt.figure()
        plt.title('ICA Components')
        
        for i in range(comp_value):
            for j in range(i+1, comp_value):
                plt.scatter(df_ica[:,i], df_ica[:,j])
                
        plt.show()
        
        return df_ica
    except ValueError:
        print("Skipped n_component = " + str(comp_value) + " since i > min(n_samples, n_features).")

# choose between pca and ica 
# exhaustively test all n_components in steps to transform data
# get the best n_components by r-square score
def get_best_N(x_standard, y, method):
    x_train, x_test, y_train, y_test = train_test_split(x_standard, y, test_size=0.3, random_state=0)
    # get upper bound for n_components
    size = min(x_train.shape[0], x_train.shape[1])
    
    # with large size, increase step 
    step = 1
    if size > 100:
        step = int(round(size/50))
    
    result = []   
    for i in range(1, size, step):
        try:
            print(i)
            
            if method == 'PCA':
                analysis = PCA(n_components=i)
            elif method == 'ICA':
                analysis = FastICA(n_components=i)
            else:
                print("Method name not recognized. Please choose between PCA and ICA. ")
                break
            
            analysis.fit(x_train)
            
            # transform train and test dataset
            x_train_analysis = analysis.transform(x_train)
            x_test_analysis = analysis.fit_transform(x_test)
            
            # train model over transformed features
            model = LogisticRegression()
            model.fit(x_train_analysis, y_train)  
            
            # predict model using transformed test dataset
            y_pred = model.predict(x_test_analysis)
            
            # compare true result and predicted result to get r-square score
            score = r2_score(y_test, y_pred)
            result.append((i, score))
        except ValueError:
            print("Skipped n_component = " + str(i) + " since i > min(n_samples, n_features).")
            break
    
    df = pd.DataFrame(result, columns = ['N_components', 'R^2_score'])
    df.sort_values(['R^2_score'], ascending=False)
    
    print(df)
