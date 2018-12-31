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
To use the DigiPsych Voice Analysis Pipeline, execute Voice_Feature_Wrapper.py

```
python Voice_Feature_Wrapper.py
```

Provide a full path to the audio files. Once Pipeline finishes executing, check 'Output_Folder' and it's subdirectories for outputted CSV Files corresponding to sets of features that correspond to an audio files.


### To Do's:

Extend the Feature_Extract_API.
- Add NLP Features
- Add Linguistic Features
- Add Prosody Features
- Output dataframe with data and labels
- Avec Gemaps folder deletion
- Other Features? ... TBD

Document Feature_Extract_API modifications in Wiki.
- Modify Wiki to update with new API information

Ensure ease of use.
- The level of usage should be something along the lines of the code below.
- The methods should export dataframes/dictionaries/sets that we can then combine or export

```python
osmile = OpenSmile()
ling = Linguistic()
pros = Prosody()
for fi in os.listdir(audioPath):
  osmile.method1(fi)
  osmile.method2(fi)
  ling.method1(fi)
  ling.method2(fi)
  ling.method3(fi)
  pros.method1(fi)
```
