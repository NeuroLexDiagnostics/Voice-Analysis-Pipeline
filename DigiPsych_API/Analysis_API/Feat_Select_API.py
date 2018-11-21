import os
import sys
import pandas as pd
import numpy as np
from sklearn.linear_model import LassoCV,RidgeCV
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.feature_selection import SelectKBest,f_regression #ANOVA
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale,LabelEncoder,StandardScaler
from Data_API import MHA_Data_API
class Audio_Feat_Selector:
    '''
    Audio Feature Selector which enable(s) different feature selection algorithms
    to be applied to any data we input to the object.
    '''
    def __init__(self,feat_data,combined_data):
        self.combined_data = combined_data
        #self.feat_data = self.feat_clean(feat_data)

        self.score = combined_data['Score']
        self.audio_files = feat_data['AudioFile']
        self.feat_data = self.feat_clean(feat_data)
    def feat_clean(self,df):
        #droplist = ['name']
        dropList = ['AudioFile']#,'unused_target_label','class']
        return df.drop(dropList,axis=1)

    def Lasso(self):
        #Issues: Sift through some details of lasso Results
        #See if there's 0 value coefficients, drop said coefficients.
        #identify if coefficients have mapability
        print("Lasso Feature Selection is in Progress...")
        X = self.feat_data
        Y = self.score
        names = list(self.feat_data.columns.values)
        lasso = LassoCV()
        lasso.fit(X,Y)
        print(lasso.coef_)
        feat_dict = {'Lasso':{lasso.coef_}}
        # Issue: This algorithm require(s) final value? - We want to take in the PHQ-9's maybe
        print("Lasso Completed.")
        return feat_dict

    def RidgeRegression(self):
        print("Ridge Regression Feature Selection is in Progress...")
        X = self.feat_data
        Y = self.score
        names = list(self.feat_data.columns.values)
        ridge = LassoCV()
        ridge.fit(X,Y)
        feat_dict = {'Ridge':{ridge.coef_}}
        print("Ridge Regression Completed.")
        return feat_dict

    def RFRegression(self):
        print("RF Regression Feature Selection is in Progress...")
        X = self.feat_data
        Y = self.score
        rf = RandomForestRegressor()
        rf.fit(X,Y)
        feat_dict ={'Random_Forest':{rf.feature_importances_}}
        print("RF Regression Completed.")
        return feat_dict

    def MRMR(self):
        print("MRMR Feature Selection is in Progress...")
        print("MRMR Completed.")

    def LDA(self):
        print("LDA Feature Selection is in Progress...")
        X = self.feat_data
        Y = self.score
        lda = LinearDiscriminantAnalysis()
        lda.fit(X,Y)
        feat_dict ={'LDA':{lda.coef_}}
        print("LDA Completed.")
        return feat_dict

    def PCA(self):
        #http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
        # What paramaters will the number of principal components: Scree Plot Methodology
        # Scale Features(s)
        print("PCA Feature Selection is in Progress...")
        X = self.feat_data
        ss = StandardScaler()
        X = ss.fit_transform(X)
        print(X)
        Y = self.score
        X = scale(X)
        tot_comp = 88
        pca = PCA(n_components=tot_comp)
        pca.fit(X)
        var = np.cumsum(np.round(pca.explained_variance_ratio_,decimals=4)*100)
        num_comps = None
        for i in range(len(var)):
            print(var[i])
            if var[i] >= 100:
                num_comps = i
                break
        if num_comps == None:
            num_comps = tot_comp

        pca = PCA(n_components=num_comps)
        X_train = pca.fit_transform(X)
        feat_dict = {'PCA':X_train}
        print(feat_dict)
        print("PCA Completed.")
        return feat_dict

    def generateReport(self):
        '''
        Comprehensive Feature Selector

        - Creates Report for Different Featureset(s) extracted
        - Similarity/Differences across Feature(s) selected per each algorithm
        - Output a pickle of feature(s) based off a dataset.

        Format:
        - Dictionary:
        - []'Algorithm':{'Features'},
        'Algorithm':{'Features'},
        'Algorithm':{'Features'},
        'Algorithm':{'Features'},
        ......]

        When user unpickles data, they should be able to use the feature's sets per algorithm to grab column(s) from
        dataframe

        Results will have file_name format: <Date>_FeatSelect_Report.log
        '''
        report_dict = {}
        lasso_feat_dict = self.Lasso()
        report_dict['LASSO'] = lasso_feat_dict
        rr_feat_dict = self.RidgeRegression()
        report_dict['RIDGE_REG'] = rr_feat_dict
        rfr_feat_dict = self.RFRegression()
        report_dict['RF_REG'] = rfr_feat_dict
        mrmr_feat_dict = self.MRMR()
        report_dict['MRMR'] = mrmr_feat_dict
        lda_feat_dict = self.LDA()
        report_dict['LDA'] = lda_feat_dict
        pca_feat_dict = self.PCA()
        report_dict['PCA'] = pca_feat_dict
        return report_dict

# def main():
#     gemaps = './FeatureSets/Julygemaps.p'
#     avec = './FeatureSets/Julyavec.p'
#     screen = './Screens/July_screens.xlsx'
#     mapping = './SubmissionIDs/JulyBatchSubmissionID.csv'
#     d = MHA_Data_API(screen,avec,gemaps,mapping)
#     af = Audio_Feat_Selector(d.join_avec_gemaps(),d.join_data_by_audio())
#     af.PCA()
# if __name__ == '__main__':
#     main()
