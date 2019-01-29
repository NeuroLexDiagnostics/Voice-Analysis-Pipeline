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

### Pipeline Backlog:
- Implement Prosodic:Voice Activity Detection Features -- Abbad
    - 5.1 Response time
    - 5.2 Response length
    - 5.3 Silence ratio
    - 5.4 Silence to utt. ratio
    - 5.5 Long silence ratio
    - 5.6 Avg. silence count
    - 5.7 Silence rate
    - 5.8 Cont. speech rate
    - 5.9 Avg. cont. word count

- Feature Selection Implementation -- Sherry
- Implement Semantic Coherence: https://github.com/facuzeta/coherence

### Credits:
- audEERING for OpenSmile Capability: https://www.audeering.com/
- Neurolex VoiceBook: https://www.neurolex.ai/voicebook/
    - https://github.com/jim-schwoebel/voicebook
- Semantic Coherence:
    - https://www.nature.com/articles/npjschz201530.pdf
