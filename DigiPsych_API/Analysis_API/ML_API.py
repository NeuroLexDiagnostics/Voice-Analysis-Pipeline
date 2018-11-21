import os
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import scale,LabelEncoder,StandardScaler
from sklearn.model_selection import GridSearchCV,train_test_split,StratifiedKFold
import datetime
import pickle
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import xgboost as xgb #(XGBRegressor,XGBClassifier)
from sklearn.svm import SVR,SVC
#import keras #(DNNregressor/classifier)

class Model_Selector:
    '''
    TODO: Rewrite Model Structure to enable the singular build of algorithm, but fitting of
    multiple X_train, y_train

    Model Selector is a object that take(s) in data to apply any variety of model(s) upon
    given data, and regresses/evaluates against the PHQ-9 Scores associated with
    such feature(s)

    Each Algorithm will return a dictionary of result(s)
    '''
    def __init__(self,data=pd.DataFrame(),feat_sel_data=pd.DataFrame(),score=pd.Series(),severity=pd.Series(),cross_val = 0):
        self.data = None
        self.alg_bit = None
        self.target = None
        ### Create a check for if data and feat_sel_data are dataframes
        if isinstance(data,pd.DataFrame) == False:
            print("Provided Data is not a Dataframe. Please provide a dataframe")
            print("Exiting with Status 1")
            sys.exit(1)
        if isinstance(feat_sel_data,pd.DataFrame) == False:
            print("Provided Feat Data is not a Dataframe. Please provide a dataframe")
            print("Exiting with Status 1")
            sys.exit(1)
        if isinstance(score,pd.Series) == False:
            print("Provided Score Data is not a Series. Please provide a dataframe")
            print("Exiting with Status 1")
            sys.exit(1)
        if isinstance(severity,pd.Series) == False:
            print("Provided Severity Data is not a Series. Please provide a dataframe")
            print("Exiting with Status 1")
            sys.exit(1)

        if data.empty and feat_sel_data.empty:
            print("Please provide a set of data to implement models on.")
            print("Exiting with Status 1")
            sys.exit(1)
        elif data.empty == False and feat_sel_data.empty == False:
            print("Please provide only one set of data to model on.")
            print("Exiting with Status 1")
        elif data.empty == False:
            self.data = data
            if score.empty and severity.empty:
                print("Please provide either a score to regress to or severity to classify to")
                print("Exiting with Status 1")
                sys.exit(1)
            elif score.empty == False and severity.empty == False:
                print("Please only provide score or only provide severity")
                print("Exiting with Status 1")
                sys.exit(1)
            elif score.empty == False:
                self.alg_bit = 1
                self.target = score
            else:
                self.alg_bit = 0
                self.target = severity
        else:
            self.data = feat_sel_data
            if score.empty and severity.empty:
                print("Please provide either a score to regress to or severity to classify to")
                print("Exiting with Status 1")
                sys.exit(1)
            elif score.empty == False and severity.empty == False:
                print("Please only provide score or only provide severity")
                print("Exiting with Status 1")
                sys.exit(1)
            elif score.empty == False:
                self.alg_bit = 1
                self.target = score
            else:
                self.alg_bit = 0
                self.target = severity
        self.target = self.target.fillna(self.target.mean())
        self.X_Train = None
        self.X_Test = None
        self.Y_Train = None
        self.Y_Test = None
        self.cross_val = cross_val
        if self.cross_val != 0 and self.cross_val != 1:
            print("Cross Validation Bit is not 0 or 1, please choose 0/1")
            print("Exiting with Status 1")
            sys.exit(1)
        elif self.cross_val == 1:
            #KFOLD
            self.X_Train = []
            self.X_Test = []
            self.Y_Train = []
            self.Y_Test = []
            skf = StratifiedKFold(n_folds=5)
            X = self.data
            y = self.target
            for train_index, test_index in skf(X,y):
                X_train, X_test = X.iloc[train_index], X.iloc[test_index]
                y_train, y_test = y.iloc[train_index], y.iloc[test_index]
                self.X_Train.append(X_train)
                self.Y_Train.append(Y_train)
                self.X_Test.append(X_test)
                self.Y_Test.append(Y_train)
        else:
            #Train_test_split
            self.X_Train, self.X_Test,self.Y_Train,self.Y_Test = train_test_split(self.data,self.target,test_size = 0.25)
            print(self.X_Train)
            print(self.Y_Train)

    def temp_model_feed(self,model_bit):
        '''
        Must Create a new way to execute models(Execute Model^ )
        0 = RF
        1 = svm
        2 = GBT
        3 = NN

        TODO: FINISH KFOLD FEED.
        '''

        if model_bit == 0:
            print("Random Forest Model in Progress...")
            clf = self.temp_Random_Forest()
        elif model_bit == 1:
            print("Support Vector Model in Progress...")
            clf = self.temp_SVM()
        elif model_bit == 2:
            print("Gradient Boosted Tree Model in Progress...")
            clf = self.temp_GB_Tree()

        elif model_bit == 3:
            print("Neural Network Model in Progress...")
            clf = self.temp_NN()
        else:
            print("Incorrect model bit entry")
            print("Exiting with status 1")
            sys.exit(1)
        if isinstance(x_Train,pd.DataFrame()):
            print("Proceed with just 1 train_test set")
            clf.fit(self.X_train,self.Y_train)
            Y_PRED = clf.predict(self.X_Test)
            if self.alg_bit == 1:
                result_dict = {'Random_Forest':{'best_params':clf.best_params_,'rmse':mean_squared_error(self.Y_Test,Y_PRED,multioutput='uniform_average'),'pred_y':Y_PRED,'real_y':self.Y_Test}}
            else:
                result_dict = {'Random_Forest':{'best_params':clf.best_params_,'accuracy':np.mean(Y_PRED == self.Y_Test),'pred_y':Y_PRED,'real_y':self.Y_Test}}
        else:
            print("Proceed with multiple train test tests from kfold")
            best_result = None
            best_result_test_set = None
            best_result_pred_set = None
            for i in range(len(self.X_train)):
                X_train = self.X_train[i]
                y_train = self.y_train[i]
                X_test = self.X_test[i]
                y_test = self.y_test[i]
                clf.fit(X_train,y_train)
                y_pred = clf.predict(self.X_test)

        print("Model Completed")
        return result_dict
    def temp_Random_Forest(self):
        tuned_parameters=[{'n_estimators':[10,100,1000],'max_features':['auto','sqrt'],'max_depth':[2,5,20],'min_samples_split':[2,10],'min_samples_leaf':[1,2,4]}]
        if self.alg_bit == 1:
            clf = GridSearchCV(RandomForestRegressor(),tuned_parameters)

        else:
            clf = GridSearchCV(RandomForestClassifier(),tuned_parameters)
        return clf
    def temp_SVM(self):
        if self.alg_bit == 1:
            clf = GridSearchCV(SVR(),tuned_parameters)

        else:
            clf = GridSearchCV(SVC(),tuned_parameters)
        return clf
    def temp_GB_Tree(self):
        if self.alg_bit == 1:
            clf = GridSearchCV(xgb.XGBRegressor(),tuned_parameters)

        else:
            clf = GridSearchCV(xgb.XGBClassifier(),tuned_parameters)
        return clf
    # def temp_NN(self):
    #     if self.alg_bit == 1:
    #         clf = GridSearchCV(RandomForestRegressor(),tuned_parameters)
    #     else:
    #         clf = GridSearchCV(RandomForestClassifier(),tuned_parameters)
    #     return clf

    def RandomForest(self):
        #tuned_parameters =[{'n_estimators':[100],'max_features':['auto'],'max_depth':[5],'min_samples_leaf':[2],'min_samples_split':[10]}]
        tuned_parameters=[{'n_estimators':[10,100,1000],'max_features':['auto','sqrt'],'max_depth':[2,5,20],'min_samples_split':[2,10],'min_samples_leaf':[1,2,4]}]
        if self.alg_bit == 1:
            print("Random Forest Regression in Progress...")

            #Add Grid GridSearchCV
            clf = GridSearchCV(RandomForestRegressor(),tuned_parameters)
            clf.fit(self.X_Train,self.Y_Train)
            Y_PRED = clf.predict(self.X_Test)
            print("Random Forest Regression Completed.")
            #Regression
            result_dict = {'Random_Forest':{'best_params':clf.best_params_,'rmse':mean_squared_error(self.Y_Test,Y_PRED,multioutput='uniform_average'),'pred_y':Y_PRED,'real_y':self.Y_Test}}
            return result_dict
        else:
            print("Random Forest Classification in Progress...")
            #Add Grid GridSearchCV
            clf = GridSearchCV(RandomForestClassifier(),tuned_parameters)
            clf.fit(self.X_Train,self.Y_Train)
            Y_PRED = clf.predict(self.X_Test)
            print("Random Forest Classification Completed.")
            #Classification
            result_dict = {'Random_Forest':{'best_params':clf.best_params_,'accuracy':np.mean(Y_PRED == self.Y_Test),'pred_y':Y_PRED,'real_y':self.Y_Test}}
            return result_dict
    def GradientBoostedTree(self):
        tuned_parameters=[{'learning_rate':[0.001,0.01,0.1,0.99,0.9],'max_depth':[2,4,6,8,10],'n_estimators':[50,100,200,500,1000]}]
        if self.alg_bit == 1:
            print("Gradient Boosted Tree Regression in Progress...")

            #Add Grid GridSearchCV

            clf = GridSearchCV(xgb.XGBRegressor(),tuned_parameters)
            clf.fit(self.X_Train,self.Y_Train)
            Y_PRED = clf.predict(self.X_Test)
            print("Gradient Boosted Tree Regression Completed.")
            #Regression
            result_dict = {'Gradient_Boosted_Tree':{'best_params':clf.best_params_,'rmse':mean_squared_error(self.Y_Test,Y_PRED,multioutput='uniform_average'),'pred_y':Y_PRED,'real_y':self.Y_Test}}
            return result_dict
        else:
            print("Gradient Boosted Tree Classification in Progress...")


            #Add Grid GridSearchCV
            clf = GridSearchCV(xgb.XGBClassifier(),tuned_parameters)
            clf.fit(self.X_Train,self.Y_Train)
            Y_PRED = clf.predict(self.X_Test)
            print("Gradient Boosted Tree Classification Completed.")
            #Classification
            result_dict = {'Random_Forest':{'best_params':clf.best_params_,'accuracy':np.mean(Y_PRED == self.Y_Test),'pred_y':Y_PRED,'real_y':Y-TEST}}
            return result_dict
    def SVM(self):
        tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4,1],
             'C': [0.1, 10, 1000]}]
            #]
        if self.alg_bit == 1:
            print("SVM Regression in Progress...")
            #Add Grid GridSearchCV
            clf = GridSearchCV(SVR(), tuned_parameters)
            print("FITTING DATA")
            clf.fit(self.X_Train,self.Y_Train)
            print("PREDICTING DATA")
            print(self.X_Test)
            Y_PRED = clf.predict(self.X_Test)
            print(Y_PRED)
            print("SVM Regression Completed.")
            #Regression
            result_dict = {'Support_Vector_Machine':{'best_params':clf.best_params_,'rmse':mean_squared_error(self.Y_Test,Y_PRED),'pred_y':Y_PRED,'real_y':self.Y_Test}}
            return result_dict
        else:
            print("SVM Classification in Progress...")

            #Add Grid GridSearchCV
            clf = GridSearchCV(SVC(), tuned_parameters)
            clf.fit(self.X_Train,self.Y_Train)
            Y_PRED = clf.predict(self.X_Test)
            print("SVM Classification Completed.")
            #Classification
            result_dict = {'Support_Vector_Machine':{'best_params':clf.best_params_,'accuracy':np.mean(Y_PRED == self.Y_Test),'pred_y':Y_PRED,'real_y':self.Y_Test}}
            return result_dict
    # def DNN(self):
    #     if self.alg_bit == 1:
    #         print("Neural Network Regression in Progress...")
    #
    #         #Add Grid GridSearchCV
    #         clf = GridSearchCV( '<INSERT NEURAL NETWORK>', tuned_parameters)
    #         clf.fit(self.X_Train,self.Y_Train)
    #         Y_PRED = clf.predict(self.X_Test)
    #         print("Neural Network Regression Completed.")
    #         result_dict = {'Deep Neural Network':{'best_params':clf.best_params_,'rmse':mean_squared_error(self.Y_Test,Y_PRED,multioutput='uniform_average'),'pred_y':Y_PRED,'real_y':self.Y_Test}}
    #         return result_dict
    #         #Regression
    #     else:
    #         print("Neural Network Classification in Progress...")
    #
    #         #Add Grid GridSearchCV
    #         clf = GridSearchCV('<INSERT NEURAL NETWORK>', tuned_parameters)
    #         clf.fit(self.X_Train,self.Y_Train)
    #         Y_PRED = clf.predict(self.X_Test)
    #         print("Neural Network Classification Completed.")
    #         result_dict = {'Deep Neural Network':{'best_params':clf.best_params_,'accuracy':np.mean(Y_PRED == self.Y_Test),'pred_y':Y_PRED,'real_y':self.Y_Test}}
    #         return result_dict

def setup_data():
    months = ['June','July']
    feats = './FeatureSets/'
    screens = './Screens/'
    maps = './SubmissionIDs/'
    gemaps_list = []
    avec_list = []
    data_list = []
    score_list = []
    severity_list = []
    for month in months:
        ft_sets = os.listdir(feats)
        for ft in ft_sets:
            if month in ft and 'avec' in ft:
                avec = feats + ft
            if month in ft and 'gemaps' in ft:
                gemaps = feats + ft
        for s in os.listdir(screens):
            if month in s:
                screen = screens + s
        for m in os.listdir(maps):
            if month in m:
                mapping = maps + m
        d = MHA_Data_API(screen,avec,gemaps,mapping)
        gemaps_list.append(d.gemaps)
        avec_list.append(d.avec)
        data_list.append(d.join_avec_gemaps())
        score_list.append(d.score)
        severity_list.append(d.severity)
    gemaps_df = pd.concat(gemaps_list,ignore_index=True)
    avec_df = pd.concat(avec_list,ignore_index=True)
    data_df = pd.concat(data_list,ignore_index=True)
    score_df = pd.concat(score_list,ignore_index=True)
    severity_df = pd.concat(severity_list,ignore_index=True)
    return gemaps_df,avec_df,data_df,score_df,severity_df

def main():
    gemaps_df,avec_df,data_df,score_df,severity_df = setup_data()
    #sys.exit(1)
    MS = Model_Selector(data=data_df.drop(columns=['AudioFile']),score=score_df)
    result = MS.RandomForest()
    print(result)
if __name__ == '__main__':
    main()
