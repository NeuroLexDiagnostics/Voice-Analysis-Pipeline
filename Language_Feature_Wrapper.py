from DigiPsych_API.Feature_Extract_API.nltk_featurize import nltk_featurize
from DigiPsych_API.Feature_Extract_API.spacy_features import spacy_featurize
from DigiPsych_API.Feature_Extract_API import ling_complexity
import os
import pandas as pd
import numpy as np
from datetime import datetime

'''
If Csv: must have column named 'transcript', must have ID identifier
Otherwise, if text files, then must be in a folder of text files.

## TODO:Implement CSV Method for NLTK + SPACY
'''

output_folder = './Output_Folder/'

def nltk_feats(path,bit):
    nltk_df = pd.DataFrame()
    if 'Language' not in os.listdir(output_folder):
        os.mkdir(output_folder + 'Language')
    if bit == 1:
        #Provides path to a csv file containing transcripts
        df = pd.read_csv(path)
        id = df['ID']
        transcripts = df['transcript']
    else:
        #Provides path to a folder of text files
        transcript_files = os.listdir(path)
        for fi in transcript_files:
            print("Parsing File: " , fi)
            file_path = os.path.join(path,fi)
            with open(file_path,'r') as f:
                content = f.read()
                features,labels = nltk_featurize(content)
                nltk_dict = dict(zip(labels,features))
                nltk_dict['Transcipt_File'] = fi
                nltk_df = nltk_df.append(nltk_dict,ignore_index=True)
    date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    file_name = output_folder + 'Language/' + 'nltk_features_' + date + '.csv'
    print("Data Outputed to following path:",file_name)
    nltk_df.to_csv(file_name)
    print("NLTK Features Successfully Extracted")

def spacy_features(path,bit):
    spacy_df = pd.DataFrame()
    if 'Language' not in os.listdir(output_folder):
        os.mkdir(output_folder + 'Language')
    if bit == 1:
        #Provides path to a csv file containing transcripts
        df = pd.read_csv(path)
        id = df['ID']
        transcripts = df['transcript']
    else:
        #Provides path to a folder of text files
        transcript_files = os.listdir(path)
        for fi in transcript_files:
            print("Parsing File: " , fi)
            file_path = os.path.join(path,fi)
            with open(file_path,'r') as f:
                content = f.read()
                features,labels = spacy_featurize(content)
                spacy_dict = dict(zip(labels,features))
                spacy_dict['Transcipt_File'] = fi
                spacy_df = spacy_df.append(spacy_dict,ignore_index=True)

    date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    file_name = output_folder + 'Language/' + 'spacy_features_' + date + '.csv'
    print("Data Outputed to following path:",file_name)
    spacy_df.to_csv(file_name)
    print("Spacy Features Successfully Extracted")

def ling_complex(path, bit):
    if 'Language' not in os.listdir(output_folder):
        os.mkdir(output_folder + 'Language')
    if bit == 1:
        #Provides path to a csv file containing transcripts
        df = pd.read_csv(path)
        id = df['ID']
        transcripts = df['transcript']
    else:
        transcript_files = os.listdir(path)
        indexes = []
        allData = []
        for fi in transcript_files:
            print("Parsing File: " , fi)
            file_path = os.path.join(path,fi)
            currRow = ling_complexity.lingComplexResult(file_path)
            allData.append(currRow)
            indexes.append(fi)
    lingComplex_df = pd.DataFrame(data = allData, columns = ['Transcript', 'Unintelligble', 'Number Ratio', 'Brunet Index', 'Honore Stat', 'Suffix Ratio', 'Type Token Ratio'])
    date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    file_name = output_folder + 'Language/' + 'lingComplex_features_' + date + '.csv'
    print("Data Outputed to following path:",file_name)
    lingComplex_df.to_csv(file_name)
    print("Linguistic Complexity Features Successfully Extracted")

def checkpath(path):
    files = os.listdir(path)
    for fi in files:
        #Checks if file is of wav
        if fi == '.DS_Store':
            continue
        if '.txt' not in fi:
            return False
    return True

def feature_suite(path,bit):
    nltk_feats(path,bit)
    spacy_features(path,bit)
    ling_complex(path, bit)


def main():
    if os.path.exists(output_folder) == False:
        os.mkdir(output_folder)
    transcript_path = None
    bit = None
    while True:
        print("If passing a csv of transcripts, please label the transcript column 'transcript'")
        transcript_path = input("Please provide a path to a folder of transcript text files or a csv of transcripts:")
        print (transcript_path)
        if '.csv' in transcript_path:
            if os.path.isfile(transcript_path) == False:
                print("The CSV path you provided is incorrect, Please try again")
                return
            bit = 1
        elif os.path.exists(transcript_path) == False:
            print("The Path that you provided is incorrect. Please try again.")
        elif checkpath(transcript_path) == False:
            print("Please provide a Folder of only text document Files as inputs.")
        else:
            bit = 0
            break
    feature_suite(transcript_path,bit)

if __name__ == '__main__':
    main()
