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

# feature selection package
from sklearn.model_selection import train_test_split
from sklearn.model_selection import learning_curve
from sklearn.model_selection import validation_curve
from sklearn.model_selection import cross_val_score
from sklearn import linear_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import PolynomialFeatures
from scipy.stats import boxcox
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection.from_model import SelectFromModel
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFECV
from sklearn.feature_selection import VarianceThreshold
from mlxtend.feature_selection import ExhaustiveFeatureSelector as EFS
from sklearn.decomposition import PCA

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression, LassoCV
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.svm import SVC

# plot cumulative explained variance vs. number of components
def pcaPlot(df):
    df_pca = PCA().fit(df);
    explained_var = np.cumsum(df_pca.explained_variance_ratio_)
    plt.plot(explained_var)
    plt.grid(True)
    plt.title('(PCA) Num. of Components vs. Cumulative explained variance')
    plt.xlabel('number of components')
    plt.ylabel('cumulative explained variance')
    plt.show()
    
#     print(explained_var)
    # return number of components with explained variance >= 90%
    return bisect.bisect_left(explained_var, 0.9)

# find best classifier by score
def optimalClassifier(x_train, x_test, y_train, y_test):
    classifiers = [DecisionTreeClassifier(random_state=0),
                   GaussianNB(),
                   SVC(),
                   AdaBoostClassifier(n_estimators=100),
                   GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0),
                   LogisticRegression(random_state=1),
                   KNeighborsClassifier(n_neighbors=7),
                   RandomForestClassifier(n_estimators=10, max_depth=None, min_samples_split=2, random_state=0),
                   svm.SVC(kernel='linear', C = 1.0)]
    names = ['DecisionTree','Gaussian_NB','SK_learn','AdaBoost','Gradient_Boosting','Logistic_Regression','K_Nearest_Neighbors','Random_Forest','SVM']
    means = []
    
    for classifier in classifiers:
        try:
            classifier.fit(x_train, y_train)
            scores = cross_val_score(classifier, x_test, y_test, cv=5)
            means.append(scores.mean())
        except:
            means.append(0)
    
    df = pd.DataFrame({'Classifier_reference':classifiers,
                          'Classifier_name':names,
                          'Score':means})
    
    df.sort_values(by='Score', ascending=False, inplace=True)
    df = df.reset_index(drop=True)
    print(df[['Classifier_name','Score']])
    print("Optimal classifier is " + str(df['Classifier_name'][0]) + " with score " + str(df['Score'][0]))
    print("Second Optimal classifier is " + str(df['Classifier_name'][1]) + " with score " + str(df['Score'][1]))
    
    name1 = str(df['Classifier_name'][0])
    name2 = str(df['Classifier_name'][1])
    classifier1 = None
    classifier2 = None
    
    for classifier,name in zip(classifiers,names):
        if name == str(df['Classifier_name'][0]):
            classifier1 = classifier
        elif name == str(df['Classifier_name'][1]):
            classifier2 = classifier
    
    return classifier1, name1, classifier2, name2
   
# get the best number of features
def getBestK(x_train, x_test, y_train, y_test, classifier, name):
    classifier.fit(x_train, y_train)
    scores = cross_val_score(classifier, x_test, y_test, cv=5)  
    highest_score = np.mean(scores)
    std = np.std(scores)
    k_value = len(x_train.columns)# total number of features
    selected_features = list(x_train.head())
    
    means = []
    stds = []
    
    # get feature subset of all size
    # update best number of features 
    for i in range(1, len(x_train.columns)+1):
        print("current number of features: " + str(i))
        select = SelectKBest(k=i)
        select.fit(x_train, y_train)
        x_train_selected = select.transform(x_train)
                   
        cols = list(x_train.columns[select.get_support(indices=True)])
        x_test_selected = x_test[cols]
        
        classifier.fit(x_train_selected, y_train)
        scores = cross_val_score(classifier, x_test_selected, y_test, cv=5)
   
        if np.mean(scores) > highest_score or (np.mean(scores) == highest_score and np.std(scores) < std):
            highest_score = np.mean(scores)
            std = np.std(scores)
            k_value = i
            selected_features = cols
        
        means.append(np.mean(scores))
        stds.append(np.std(scores))
    
    print("Number of features: " + str(k_value) + ", accuracy score " + str(highest_score))
    print("The selected features are: \n" + str(pd.DataFrame({'Feature':selected_features})))
    
    x_axis = np.array(range(1, len(x_train.columns)+1))
    means = np.array(means)
    stds = np.array(stds)
    
    # plot number of features vs. cross validation score with standard deviation shading 
    plt.figure()
    plt.title("Number of features vs. Cross Val Score (" + name + ")")
    plt.xlabel("Number of features selected")
    plt.ylabel("Cross validation score of number of selected features")
    plt.plot(x_axis, means, 'o-', color='g')
    plt.fill_between(x_axis, means + stds, means - stds, alpha=0.15, color='g')
    plt.show()

    return selected_features

# univariance feature selection
def univariance(x, y, k_value):
    if k_value > len(x.columns):
        print("There are only " + str(len(x.columns)) + " features, change k to " + str(len(x.columns)) + "...")
        k_value = len(x.columns)

    selector = SelectKBest(k=k_value)
    fit = selector.fit(x, y)
    
    scores = pd.DataFrame(fit.scores_)
    features = pd.DataFrame(x.columns)

    table = pd.concat([features,scores],axis=1)
    table.columns = ['Feature','Score']
    
    print("Number of Features: " + str(k_value)) 
    return table.nlargest(k_value,'Score')        

# Recursive Feature Elimination
def RFEFeatSelect(x, y, classifier):
    try:
        step_value = 1
        if len(x.columns) > 500:
            step_value = int(round(len(x.columns)/100))
        
        rfe = RFECV(estimator=classifier, step=step_value, scoring='accuracy')
        fit = rfe.fit(x, y)
        
        feature_selected = []
        for bool, feature in zip(fit.support_, list(x)):
            if bool:
                feature_selected.append(feature)    
        
        print("Number of Features: " + str(fit.n_features_))
        
        # plot number of features vs. cross validation score
        plt.figure()
        plt.title("(RFE) Number of feature vs. Cross Validation Score")
        plt.xlabel("Number of features selected")
        plt.ylabel("Cross validation score of number of selected features")
        plt.plot(range(1, len(rfe.grid_scores_) + 1), rfe.grid_scores_)
        plt.show()
        
        return pd.DataFrame({"Feature": feature_selected})
    except RuntimeError:
        print(sys.exc_info())
        return pd.DataFrame(columns=['Empty'])

# select from model using classifier
def modelFeatSelect(x, y, classifier, k_value):
    try:
        sfm = SelectFromModel(classifier, threshold=0.1)
        sfm.fit(x, y)
        n_features = sfm.transform(x).shape[1]
        
        while n_features > k_value:
            sfm.threshold += 0.05
            x_transform = sfm.transform(x)
            n_features = x_transform.shape[1]
        
        index = sfm.get_support()
        features = pd.DataFrame({"Feature": x.columns[index]})
        
        print("Number of Features: " + str(k_value)) 
        return features
    except ValueError:
        print(sys.exc_info())
        return pd.DataFrame(columns=['Empty'])