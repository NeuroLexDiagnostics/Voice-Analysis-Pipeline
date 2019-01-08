# Feature_Selection_API

In order to utilize this API, please make sure you are in a Python3 Environment.

Please make sure to have the following packages installed:
- seaborn
- sklearn

Direction:
- provide a path to a csv file
- non-numeric features and incomplete columns will be removed 

## How to use:
run prompt.py 

### Obtaining data set:
```
Begin Operation... 
Notice: Non-numeric data besides the target class (can be categorical) will be ignored... 
Please provide a path to a csv file: D:\\MHA_Data\subdata.csv
```

### Encode target class:
```
Please provide the name of the target class: Severity
Your target class is not numerical. Transforming it to categorical...
Here is a list of unique values (size: 5): 
['Moderately Severe Depression', 'Severe Depression', 'Moderate Depression', 'Minimal Depression', 'Mild Depression']
Please provide an numeric encoding separated by space in the same order: 4 5 3 1 2
Here is the mapping according to the encoding you provide: 
{'Severity': {'Moderately Severe Depression': '4', 'Severe Depression': '5', 'Moderate Depression': '3', 'Minimal Depression': '1', 'Mild Depression': '2'}}
```

### Data Visualization:
```
Non-numeric columns and columns with missing values removed.
Data Normalized (z-score).
Would you like to (continue) visualize your data? (y/n) y
Here is a list of method to choose: 
1. Correlation Plot Between Two Features
2. Pair-wise Grid Plot Among 3+ Features (no more than 6)
3. Violin Plot Between Features and the Target Class
4. Heat Map of Correlation Between Every Pair of Features
Please choose a method by number 1 - 4: 4
Begin heap map plot... 
Would you like to (continue) visualize your data? (y/n) n
Data visualization is skipped. 
```
![alt_text](https://github.com/DrDongSi/Voice-Analysis-Pipeline/blob/master/DigiPsych_API/Feature_Selection_API/graphs/visualization.png)

### Principle Component Analysis:
```
Would you like to perform principle component analysis? (y/n) y
Begin PCA... 
Suggested number of components by PCA with explained variance >= 0.9 is: 3
```
![alt text](https://github.com/DrDongSi/Voice-Analysis-Pipeline/blob/master/DigiPsych_API/Feature_Selection_API/graphs/pca.png)

### Test Classifier:
```
Would you like to perform feature selection? (y/n) y
Begin to test classifiers... 
       Classifier_name     Score
0  K_Nearest_Neighbors  0.498633
1        Random_Forest  0.452812
2                  SVM  0.450304
3  Logistic_Regression  0.446089
4    Gradient_Boosting  0.417785
5             SK_learn  0.412209
6             AdaBoost  0.392986
7          Gaussian_NB  0.295931
8         DecisionTree  0.294488
Optimal classifier is K_Nearest_Neighbors with score 0.4986326109391125
Second Optimal classifier is Random_Forest with score 0.45281217750257996
```

### Get best number of features (using top 2 classifiers above)
```
Do you want to find the best number of feature using K_Nearest_Neighbors? (y/n) y
Find the best number of features using K_Nearest_Neighbors... 
current number of features: 1
current number of features: 2
current number of features: 3
current number of features: 4
current number of features: 5
current number of features: 6
current number of features: 7
current number of features: 8
Number of features: 5, accuracy score 0.5351301046734483
The selected features are: 
                                        Feature
0             F0semitoneFrom27.5Hz_sma3nz_amean
1  F0semitoneFrom27.5Hz_sma3nz_meanFallingSlope
2      F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2
3    F0semitoneFrom27.5Hz_sma3nz_percentile20.0
4    F0semitoneFrom27.5Hz_sma3nz_percentile80.0
Do you want to find the best number of feature using Random_Forest? (y/n) n
Skip for Random_Forest.
```
![alt text](https://github.com/DrDongSi/Voice-Analysis-Pipeline/blob/master/DigiPsych_API/Feature_Selection_API/graphs/classifier.png)

### Feature Selection
1. univariance feature selection (univariance)
2. recursive feature elimination (RFE)
3. lasso select from model (lasso)
4. use top 2 classifiers above to select from model (optimal_classifer)

Notice:
- method 1 doesn't use the top 2 classifiers identified above
- K_Nearest_Neighbor cannot be used for method 2-4 and return an empty dataframe if prompted


univariance
```
Please choose a feature selection method(RFE/univariance/lasso/optimal_classifier): univariance
Starting Univariance Feature Selection: 
Please choose the number of features to select: 3
Number of Features: 3
                                      Feature     Score
4  F0semitoneFrom27.5Hz_sma3nz_percentile20.0  1.912893
3    F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2  1.876267
6  F0semitoneFrom27.5Hz_sma3nz_percentile80.0  1.185713
End of Operation.
```
![alt text](https://github.com/DrDongSi/Voice-Analysis-Pipeline/blob/master/DigiPsych_API/Feature_Selection_API/graphs/uni.png)

optimal_classifier (k neareast neighbors - will be skipped, random forest)
```
Please choose a feature selection method(RFE/univariance/lasso/optimal_classifier): optimal_classifier
Using K_Nearest_Neighbors
Please choose the maximum number of features to select: 5
(<class 'ValueError'>, ValueError('The underlying estimator KNeighborsClassifier has no `coef_` or `feature_importances_` attribute. Either pass a fitted estimator to SelectFromModel or call fit before calling transform.'), <traceback object at 0x11289BC0>)
Empty DataFrame
Columns: [Empty]
Index: []
Using Random_Forest
Please choose the maximum number of features to select: 5
Number of Features: 5
                                    Feature
0         F0semitoneFrom27.5Hz_sma3nz_amean
1  F0semitoneFrom27.5Hz_sma3nz_pctlrange0-2
End of Operation.
```
![alt text](https://github.com/DrDongSi/Voice-Analysis-Pipeline/blob/master/DigiPsych_API/Feature_Selection_API/graphs/optimal.png)


