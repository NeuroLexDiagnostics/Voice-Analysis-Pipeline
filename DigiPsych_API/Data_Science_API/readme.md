# Data_Science_API

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
1. Correlation Plot
2. Pair-wise Grid Plot
3. Violin Plot
4. Heat Map of Correlation

Heat map (limitation: with large dataset, only plot first 20 features)
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
```
![alt_text](https://github.com/DrDongSi/Voice-Analysis-Pipeline/blob/master/DigiPsych_API/Data_Science_API/graphs/visualization.png)

Correlation plot
```
Would you like to (continue) visualize your data? (y/n) y
Here is a list of method to choose: 
1. Correlation Plot Between Two Features
2. Pair-wise Grid Plot Among 3+ Features (no more than 6)
3. Violin Plot Between Features and the Target Class
4. Heat Map of Correlation Between Every Pair of Features
Please choose a method by number 1 - 4: 1
Please provide 2 features(separated by space): F0semitoneFrom27.5Hz_sma3nz_amean F0semitoneFrom27.5Hz_sma3nz_meanFallingSlope 
Begin correlation plot... 
Would you like to (continue) visualize your data? (y/n) n
Data visualization is skipped. 
```
![alt text](https://github.com/DrDongSi/Voice-Analysis-Pipeline/blob/master/Data_Science_API/Feature_Selection_API/graphs/corr.png)

### Feature Transformation:
1. Principle Component Analysis
2. Independent Component Analysis
3. Factor Analysis

```
Would you like to perform feature transformation? (y/n) y
Do you want to remove features with no variance? (y/n) y
1 features have been removed. 
Do you want to remove highly correlated features? (y/n) y
The default threshold is 0.8. Do you want to use a different value? (y/n): y
Please provide a threshold for correlation (0-1): 0.95
36 features have been removed. 
```

Principle Component Analysis (PCA):
- Exhausively find the best n_component by R-square score: (part of output is omitted)
```
Would you like to (continue) transform your data? (y/n) y
Here is a list of method to choose: 
1. Principle Component Analysis 
2. Independent Component Analysis 
3. Factor Analysis 
Please choose a method by number 1 - 3: 1
Do you want to exhaustively test the best n_component? (y/n): y
 N_components  R^2_score
0              1  -0.822875
1              4  -0.945766
2              7  -0.720466
3             10  -0.706812
4             13  -0.645367
5             16  -0.672676
6             19  -0.508822
7             22  -0.699985
```
![alt_text](https://github.com/DrDongSi/Voice-Analysis-Pipeline/blob/master/DigiPsych_API/Data_Science_API/graphs/pca_plot.png)

Independent Component Analysis (ICA):
- Similar with PCA, ICA has the option to exhausively find the best n_component. 
```
Would you like to (continue) transform your data? (y/n) y
Here is a list of method to choose: 
1. Principle Component Analysis 
2. Independent Component Analysis 
3. Factor Analysis 
Please choose a method by number 1 - 3: 2
Do you want to exhaustively test the best n_component? (y/n): n
Please provide a component value: 5
```
![alt_text](https://github.com/DrDongSi/Voice-Analysis-Pipeline/blob/master/DigiPsych_API/Data_Science_API/graphs/ica_plot.png)

Factor Analysis:
```
Would you like to (continue) transform your data? (y/n) y
Here is a list of method to choose: 
1. Principle Component Analysis 
2. Independent Component Analysis 
3. Factor Analysis 
Please choose a method by number 1 - 3: 3
The n_component is 3. Do you want to use a different value? (y/n): n
```
![alt_text](https://github.com/DrDongSi/Voice-Analysis-Pipeline/blob/master/DigiPsych_API/Data_Science_API/graphs/fa_plot.png)

Resulted dataset: (part of output is omitted)
```
Would you like to (continue) transform your data? (y/n) n
Current number of features: 3
Do you want to see the dataset? (y/n) y
Remaining features: 
        col_0     col_1     col_2
0    0.151453 -0.082298  0.460190
1    0.205265 -0.236694 -1.009321
2    0.065721 -0.286916  1.120802
3   -0.103863 -0.759068 -0.997405
4    0.423430 -0.066747  0.207043
5    0.354218 -0.288809 -1.168685
6   -0.136175 -0.495896  0.602562
7    0.813616  0.209811 -0.992529
[296 rows x 3 columns]
Feature transformation is terminated.
```

### Test Classifier:
Low variance filter and high correlation filter:
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
![alt text](https://github.com/DrDongSi/Voice-Analysis-Pipeline/blob/master/DigiPsych_API/Data_Science_API/graphs/classifier.png)

### Feature Selection
1. univariance feature selection (univariance)
2. recursive feature elimination (RFE)
3. lasso select from model (lasso)
4. use top 2 classifiers above to select from model (optimal_classifer)

Notice:
- method 1 doesn't use the top 2 classifiers identified above
- K_Nearest_Neighbor cannot be used for method 2-4 and return an empty dataframe if prompted


Univariance:
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
![alt text](https://github.com/DrDongSi/Voice-Analysis-Pipeline/blob/master/DigiPsych_API/Data_Science_API/graphs/uni.png)

Optimal_classifier (k neareast neighbors - will be skipped, random forest):
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
![alt text](https://github.com/DrDongSi/Voice-Analysis-Pipeline/blob/master/DigiPsych_API/Data_Science_API/graphs/optimal.png)


