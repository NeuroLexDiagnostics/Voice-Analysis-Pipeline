# DigiPsych Voice Analysis Pipeline

### How To Use:
In order to use the voice analysis pipeline, you can call the following two
imports:

```python
from DigiPsych_API.Feature_Extract_API import *
from DigiPsych_API.Analysis_API import *
```

From there you should be able to leverage the DigiPsych Pipeline.

Currently the best supported method is to extract audio features (./Feature_Extract_API/opensmile.py).

To use opensmile.py, complete the imports as stated above, and create an OpenSmile object.

```python
from DigiPsych_API.Feature_Extract_API import *
from DigiPsych_API.Analysis_API import *

osmile = OpenSmile()
```

To get AVEC and Gemaps Audio features, one would just need to make simple calls
to the following methods.

```python
avec_features, avec_labels = osmile.getAvec()
gemaps_features, gemaps_labels = osmile.getGemaps()
```

### To Do's:

#####Extend the Feature_Extract_API.
- Add NLP Features
- Add Linguistic Features
- Add Prosody Features
- Output dataframe with data and labels
- Avec Gemaps folder deletion
- Other Features? ... TBD

#####Document Feature_Extract_API modifications in Wiki.
- Modify Wiki to update with new API information

#####Ensure ease of use.
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
