import pandas as pd
from DigiPsych_API.ML_API import Model_Selector

'''
This Program is to demonstrate the ML_API currently in progress

This takes an existing set of feature(s), with their respective PHQ-9 Scores.

ML_API is specifically targeted for depression severity and symptom severity
investigations.

However, it can be adapted to regression and classification cases if 'score' or 'severity' is specified

'score' corresponds to regression cases. If you specify score parameter, you are performing regression
'severity' corresponds to classification cases. If you specify severity parameter, you are performing Classification

You cannot specify both at the same time.
'''

def main():

    ms = Model_Selector(data=,score=)
if __name__ == '__main__':
    main()
