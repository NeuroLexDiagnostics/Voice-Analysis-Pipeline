# DigiPsych Voice Analysis Pipeline

In order to utilize the Voice Analysis Pipeline, please make sure you are in a
Python3 Environment.

Please make sure to have the following dependencies installed:
- nltk
- spacy
- numpy
- pandas
- textblob
- mlxtend
- sklearn
- seaborn
- matplotlib

### Features Provided and Background Information:
For additional information, please refer to the wiki (https://github.com/larryzhang95/Voice-Analysis-Pipeline/wiki)

##### Gemaps:
Gemaps Features are explained at the following link:
https://sail.usc.edu/publications/files/eyben-preprinttaffc-2015.pdf

##### Avec:
Avec Features are explained at the following link:
https://ibug.doc.ic.ac.uk/media/uploads/documents/avec2013.pdf

##### NLTK:
NLTK Features and implementation details explained on their documentation link:
https://www.nltk.org/api/nltk.html

##### SPACY:
Spacy Features and implementation details explained on their documentation link:
https://spacy.io/api/

### Dependencies:

Please Make sure you are executing the pipeline in a Python3 Environment and have the following modules/packages installed:

pip install pandas scikit-learn textblob librosa nltk spacy librosa seaborn matplotlib speech_recognition


### How To Use:

##### New Command Line Featurizing: 
```
python featurize.py -a <Enter Audio Folder> -l <gemaps> <avec> <librosa> <all>  #Extracting audio 
python featurize.py -t <Enter Transcript Folder> -l <nltk> <spacy> <all> #Extracting transcript
```
##### Voice Feature Wrapper:
```
python Voice_Feature_Wrapper.py
```
- Provides AVEC2013 Features
- Provides GeMAPS Features
- Provides Librosa Features

##### Language Feature Wrapper:
```
python Language_Feature_Wrapper.py
```
- Provides SPACY Features
- Provides NLTK Features
- Provides Linguistic Features of Complexity
- Provides Semantic Coherence Features

### Credits:
- audEERING for OpenSmile Capability: https://www.audeering.com/
- Neurolex VoiceBook: https://www.neurolex.ai/voicebook/
    - https://github.com/jim-schwoebel/voicebook
- Semantic Coherence:
    - https://www.nature.com/articles/npjschz201530.pdf

#### Acknowledgements:
We would like to thank Neurolex Diagnostics for assisting in developing the basis for this work. 

We also have an associated paper with this pipeline submitted to Interspeech 2019, and plan to continue adding features. If you would like to request a feature to be added, please file an issue, and corresponding papers/sources which our collaborators and students may be able to implement
