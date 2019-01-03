# DigiPsych Voice Analysis Pipeline

### Features Provided and Background Information:
#####Gemaps:
Gemaps Features are explained at the following link:
https://sail.usc.edu/publications/files/eyben-preprinttaffc-2015.pdf

#####Avec:
Avec Features are explained at the following link:
https://ibug.doc.ic.ac.uk/media/uploads/documents/avec2013.pdf

#####NLTK:
NLTK Features and implementation details explained on their documentation link:
https://www.nltk.org/api/nltk.html

#####SPACY:
Spacy Features and implementation details explained on their documentation link:
https://spacy.io/api/

### Dependencies:

Please Make sure you are executing the pipeline in a Python3 Environment and have the following modules/packages installed:

pip install pandas scikit-learn


### How To Use:

#####Voice Feature Wrapper:
```
python Voice_Feature_Wrapper.py
```
- Provides AVEC2013 Features
- Provides GeMAPS Features

#####Language Feature Wrapper:
```
python Language_Feature_Wrapper.py
```
- Provides SPACY Features
- Provides NLTK Features

### Pipeline Backlog:
- Implement Librosa Spectral Features -- Ali
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
- Implement Linguistic: Complexity Features
    - 4.1 Standardized word entropy
    - 4.2 Suffix ratio
    - 4.3 Number ratio
    - 4.4 Brunet’s index
    - 4.5 Honore’s statistic
    - 4.6 Type-token ratio
- Implement Command Line Usage -- Larry
- Configure "__init__.py" to 'enable' -- Abbad
- Feature Selection Implementation -- Sherry
    - AutoML Capability
    - MRMR
