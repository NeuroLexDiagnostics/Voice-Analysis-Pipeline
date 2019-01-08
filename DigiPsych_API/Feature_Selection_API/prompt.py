import warnings
warnings.filterwarnings("ignore")

# basic package
import os
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.model_selection import ShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LassoCV

# import other files in the same folder
import preprocessing
import visualization
import feature_selection
import evaluate_model

# prompt for encoding target class
def encodePrompt(y, target_name):
    while True:
        try:
            pd.to_numeric(y)
            break
        except ValueError:
            print("Your target class is not numerical. Transforming it to categorical...")
            y = y.astype('category').str.replace('\r\n','')
            
            print("Here is a list of unique values (size: " + str(len(y.unique())) + "): ")
            print(y.unique().tolist())
            
            while True:
                encoding = input("Please provide an numeric encoding separated by space in the same order: ")
                encoding = encoding.split()
                if len(y.unique()) != len(encoding):
                    print("The length of encoding doesn't match the number of unique values. Please try again.")
                else:
                    try:
                        pd.to_numeric(encoding)
                        break
                    except ValueError:
                        print("The encoding is not numeric. Please try again.")
                    
            print("Here is the mapping according to the encoding you provide: ")
            mapping = {target_name : {k:v for k,v in zip(y.unique(), encoding)}}
            print(mapping)
            
            # encode y
            df_encode = pd.DataFrame({target_name: y})
            df_encode[target_name] = df_encode[target_name].astype('category')
            df_encode.replace(mapping, inplace=True, regex=True)
            
            return df_encode[target_name]

# prompt for data visualization
def visualPrompt(x_standard, y):
     while True:
        answer = input("Would you like to (continue) visualize your data? (y/n) ")
        if answer == 'y':
            print("Here is a list of method to choose: ")
            print("1. Correlation Plot Between Two Features")
            print("2. Pair-wise Grid Plot Among 3+ Features (no more than 6)")
            print("3. Violin Plot Between Features and the Target Class")
            print("4. Heat Map of Correlation Between Every Pair of Features")
            
            method = input("Please choose a method by number 1 - 4: ")
            
            if method == '1':
                while True:
                    features = input("Please provide 2 features(separated by space): ")
                    features = features.split()
                    if len(features) != 2:
                        print("You provided " + str(len(features)) + " feature(s). Please provide 2 features: ")
                    else:
                        print("Begin correlation plot... ")
                        visualization.corrPlot(x_standard, features[0], features[1])
                        break
            elif method == '2':
                while True:
                    features = input("Please provide 3-6 features(separated by space): ")
                    features = features.split()
                    if len(features) < 3 or len(features) > 6:
                        print("You provided " + str(len(features)) + " feature(s). Please provide 3-6 features: ")
                    else:
                        print("Begin pair-wise grid plot... ")
                        visualization.pairGrid(x_standard, features)
                        break
            elif method == '3':
                while True:
                     if len(x_standard.columns) > 20:
                         print("There are too many features in your data")
                         features = input("Please provide a list of features you wish to plot(recommend number: 5 - 15): ")
                         features = features.split()
                         
                         selected = pd.DataFrame()
                         for feature in features:
                            if feature not in x_standard.head():
                                print(str(feature) + " doesn't exist in your data and is skipped.")
                            else:
                                selected[feature] = x_standard[feature]
    
                         print("Begin violin plot... ")
                         visualization.violinPlot(selected, y)
                         break
                     else:
                         print("Begin violin plot... ")
                         visualization.violinPlot(x_standard, y)
                         break
            elif method == '4':
                while True:
                    if len(x_standard.columns) > 20:
                         print("There are too many features in your data, plot the first 20...")
                         visualization.heapMap(x_standard.iloc[:, : 20])
                         break
                    else:     
                        print("Begin heap map plot... ")
                        visualization.heapMap(x_standard)
                        break
            else:
                print("Please provide a number 1, 2, 3, or 4 to visualize your data.")
        else:
            print("Data visualization is skipped. ")
            break

# prompt for model evaluation
def evalModelPrompt(x_train, x_test, y_train, y_test, x_standard, y, classifier, name):
    print("Find the best number of features using " + name + "... ")
    selected_features = feature_selection.getBestK(x_train, x_test, y_train, y_test, classifier, name)
        
    title = "Learning Curves with " + name + " (use selected features)"
    x_selected = x_standard[list(selected_features)]
    x_train_selected = x_train[list(selected_features)]
        
    classifier.fit(x_train_selected, y_train)
    evaluate_model.plot_learning_curve(classifier, title, x_selected, y, cv=5)

# prompt for univariance feature selection
def uniPrompt(x_train, y_train, x_standard, y):
    print("Starting Univariance Feature Selection: ")
    while True:
        value = input("Please choose the number of features to select: ")
        try:
            k_value = int(value)
        except ValueError:
            print("The input you entered is not an integer. Please try again.")
        else:
            if k_value > 0:
                result = feature_selection.univariance(x_train, y_train, k_value)
                print(result)
                
                features = list(result['Feature'])
                title = "Learning Curves (univariance, log regression model)"
                x_selected = x_standard[features]
                x_train_selected = x_train[features]
        
                logreg = LogisticRegression(C=1)
                logreg.fit(x_train_selected, y_train)    
                evaluate_model.plot_learning_curve(logreg, title, x_selected, y, cv=5) 
                
                break
            else:
                print("The integer you entered is not positive. Please try again.")
                
# prompt for RFE feature selection
def RFEPrompt(x_train, y_train, x_standard, y, classifier, name):
    print("Starting RFE: ")
    
    result = feature_selection.RFEFeatSelect(x_train, y_train, classifier)
    if result != None:
        print(pd.DataFrame({'Feature':result}))
        
        title = "Learning Curves with " + name + " (use current feature subset)"
        x_selected = x_standard[list(result)]
        x_train_selected = x_train[list(result)]
        
        classifier.fit(x_train_selected, y_train)    
        evaluate_model.plot_learning_curve(classifier, title, x_selected, y, cv=5)       

# prompt for select from model feature selection
def modelPrompt(x_train, y_train, x_standard, y, classifier, name):
    while True:
        value = input("Please choose the maximum number of features to select: ")
        try:
            k_value = int(value)
        except ValueError:
            print("The input you entered is not an integer. Please try again.")
        else:
            if k_value > 0:
                result = feature_selection.modelFeatSelect(x_train, y_train, classifier, k_value)
                print(result)
                if not result.empty:
                    features = list(result['Feature'])
                    title = "Learning Curves (" + name + ", log regression model)"
                    x_selected = x_standard[features]
                    x_train_selected = x_train[features]
            
                    logreg = LogisticRegression(C=1)
                    logreg.fit(x_train_selected, y_train)    
                    evaluate_model.plot_learning_curve(logreg, title, x_selected, y, cv=5) 
                
                break
            else:
                print("The integer you entered is not positive. Please try again.")
def main():
    print("Begin Operation... ")
    print("Notice: Non-numeric data besides the target class (can be categorical) will be ignored... ")
    
    # get path to csv file
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
    df = pd.read_csv(csv_path, index_col=0)
    
    # get target class
    while True:
        target_name = input("Please provide the name of the target class: ")
        if target_name in df.head():
            x, y = preprocessing.separateVars(df, target_name)
            break
        else: 
            print("The name that you provided doesn't exist in this csv file. Please try again.")
            
    # get target class encoding
    y = encodePrompt(y, target_name)
    
    # remove non numeric data from feature columns
    x = preprocessing.cleanData(x)
    print("Non-numeric columns and columns with missing values removed.")
    # normalize data
    x_standard = preprocessing.standardization(x)
    print("Data Normalized (z-score).")
    
    # visualize data
    visualPrompt(x_standard, y)
    
    answer = input("Would you like to perform principle component analysis? (y/n) ")
    if answer == 'y':
        print("Begin PCA... ")
        num_comp = feature_selection.pcaPlot(x_standard)
        print("Suggested number of components by PCA with explained variance >= 0.9 is: " + str(num_comp))    
    else:
        print("PCA is skipped. ")
    
    answer = input("Would you like to perform feature selection? (y/n) ")
    if answer == 'y':
        # split train and test datasets
        x_train, x_test, y_train, y_test = train_test_split(x_standard, y, test_size=0.3, random_state=0)
        # find optimal classifier
        print("Begin to test classifiers... ")
        classifier1, name1, classifier2, name2 = feature_selection.optimalClassifier(x_train, x_test, y_train, y_test)
        
        # plot learning curve of current classifier
        title = "Learning Curves (" + name1 + ")"
        evaluate_model.plot_learning_curve(classifier1, title, x_standard, y, cv=5)    
        
        title = "Learning Curves (" + name2 + ")"
        evaluate_model.plot_learning_curve(classifier2, title, x_standard, y, cv=5)    
        
        answer = input("Do you want to find the best number of feature using " + name1 + "? (y/n) ")
        if answer == 'y':
            evalModelPrompt(x_train, x_test, y_train, y_test, x_standard, y, classifier1, name1)
        else:
            print("Skip for " + name1 + ".") 
                
        answer = input("Do you want to find the best number of feature using " + name2 + "? (y/n) ")
        if answer == 'y':
            evalModelPrompt(x_train, x_test, y_train, y_test, x_standard, y, classifier2, name2)
        else:
            print("Skip for " + name2 + ".")
         
        # feature selection
        while True:
            method = input("Please choose a feature selection method(RFE/univariance/lasso/optimal_classifier): ")
            if method == 'RFE':
                print("Using " + name1)
                RFEPrompt(x_train, y_train, x_standard, y, classifier1, name1)
                print("Using " + name2)
                RFEPrompt(x_train, y_train, x_standard, y, classifier2, name2)
                break
            elif method == 'univariance':
                uniPrompt(x_train, y_train, x_standard, y)
                break
            elif method == 'lasso':
                print("Using lasso")
                modelPrompt(x_train, y_train, x_standard, y, LassoCV(cv=5), 'Lasso')
                break
            elif method == 'optimal_classifier':
                print("Using " + name1)
                modelPrompt(x_train, y_train, x_standard, y, classifier1, name1)
                print("Using " + name2)
                modelPrompt(x_train, y_train, x_standard, y, classifier2, name2)
                break
            else:
                print("The method you provide is not an option. Please choose among RFE, and univariance. ")
    else:
        print("Feature Selection is skipped. ")
        
    print("End of Operation.")
    
if __name__ == '__main__':
    main() 
