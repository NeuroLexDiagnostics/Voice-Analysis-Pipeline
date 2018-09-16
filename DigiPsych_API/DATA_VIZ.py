import matplotlib.pyplot as plt
import seaborn
import pandas as pd
import sys
import os
from Data_API import Data_API
import scipy
from scipy import stats
class Data_Viz(object):
    def __init__(self):
        self.d_api = Data_API('./Screens/June_Screens.xlsx','./FeatureSets/JuneAvec.p','./FeatureSets/Junegemaps.p','./SubmissionIDs/JuneBatchSubmissionID.csv')
        self.data = self.d_api.join_avec_gemaps()
        self.param_list = self.data.columns.tolist()
    def plot_dist(self,param):
        if param not in self.param_list:
            st = param + " is not in the data you provided."
            print(st)
            print("Please check the following parameter list for valid parameters",param_list)
            return
        n,bins,patches = plt.hist(self.data[param],density=True, facecolor='g')
        plt.title(param)
        plt.show()

    def plot_param_vs_severity(self,param):
        severity = self.d_api.severity
        y = severity.astype('category').cat.codes
        if param not in self.param_list:
            st = param + " is not in the data you provided."
            print(st)
            print("Please check the following parameter list for valid parameters",param_list)
            return
        X= self.data[param]
        plt.scatter(X,y)
        plt.show()
        '''
        Plots and highlights severity level with legend, to analyze the spread of each type of data
        '''

    def plot_param_vs_phq(self,param):
        y = self.d_api.score.fillna(0)
        print(y.dtypes)
        if param not in self.param_list:
            st = param + " is not in the data you provided."
            print(st)
            print("Please check the following parameter list for valid parameters",param_list)
            return
        print(self.data[param])
        X= pd.to_numeric(self.data[param])
        print(X.dtypes)
        print(X)
        plt.scatter(X,y)
        slope, intercept, r_value, p_value, std_err = stats.linregress(X,y)
        r_sq = r_value ** 2
        print("R-Squared Value: ", r_sq)
        plt.show()
        '''
        TODO: Get Index with NaN, Remove value
        Regression Plot (Scatter + Trend Line). Give r value too of feature_value vs. phq-9 score
        '''
        
def main():
    dv = Data_Viz()
    cols = dv.d_api.gemaps.columns.tolist()
    #print(cols)
    dv.plot_param_vs_phq(cols[80])
if __name__ == '__main__':
    main()
