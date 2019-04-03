import pandas as pd
import numpy as np
from sklearn.ensemble import ExtraTreesClassifier
import matplotlib.pyplot as plt

# Read csv files
data = pd.read_csv("C:/Users/aadam/Documents/transcripts/Features/nltk_features_2019-03-09-14-29-35.csv")
phq = pd.read_csv("C:/Users/aadam/Documents/GitHub/Depression_Free_Speech/Screen/UW_Depression_Screen.csv")

# Copy data to dataID
dataID = data.copy(deep=True).iloc[:,data.columns != 'Unnamed: 0']

# Delete file extension on file column
dataID['Transcipt_File'] = dataID['Transcipt_File'].str.split('_t1.txt', 1, expand=True)
dataID['Transcipt_File'] = dataID['Transcipt_File'].str.split('_t2.txt', 1, expand=True)

# Separate participant ID and visit/arm
dataID['participant_id'] = dataID['Transcipt_File'].str.split('_', 1, expand=True)[0]
dataID['Transcipt_File'] = dataID['Transcipt_File'].str.split('_', 1, expand=True)[1]

# Get rid of 'p' in patient number
dataID['participant_id'] = dataID['participant_id'].str[1:4] 

# Extract needed cols
phqID = phq[['participant_id', 'redcap_event_name', 'phq9_total_score_98e14a', 'phq9_total_score_v2_6cd628']] 
dataID = dataID.rename(index=str, columns={"Transcipt_File": "redcap_event_name"})

# Change type from object to int so it can merge
dataID[['participant_id']] = dataID[['participant_id']].astype(int) 
merged = dataID.merge(phqID, on=['redcap_event_name', 'participant_id'])

# Combine the two total score columns
merged['phq9_total_score'] = merged['phq9_total_score_98e14a'].combine_first(merged['phq9_total_score_v2_6cd628'])

# Drop unnimportant columns to prepare for feature selection
merged = merged.drop(['phq9_total_score_98e14a', 'phq9_total_score_v2_6cd628', 'participant_id', 'redcap_event_name'], axis = 1)

X = merged.iloc[:, merged.columns != 'phq9_total_score']  # Independent columns
Y =  merged[['phq9_total_score']]    # Target column

model = ExtraTreesClassifier()
model.fit(X,Y)

print(model.feature_importances_) #use inbuilt class

# Plot top 10 most important features
feat_importances = pd.Series(model.feature_importances_, index=X.columns)
feat_importances.nlargest(10).plot(kind='barh')
plt.show()
