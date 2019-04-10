from DigiPsych_API.Feature_Extract_API.opensmile import OpenSmile
import os
import pandas as pd
import sys
from datetime import datetime
from DigiPsych_API.Feature_Extract_API.librosa_features import librosa_featurize

output_folder = './Output_Folder/'

def osmile(path, optionsPassed):
    osm = OpenSmile()
    if 'avec' in optionsPassed:
        avecDF = pd.DataFrame()
        if 'Avec' not in os.listdir(output_folder):
            os.mkdir(output_folder + 'Avec')
        for audioFile in os.listdir(path):
            if audioFile == '.DS_Store':
                continue
            avec_features, avec_labels = osm.getAvec(os.path.join(path,audioFile))
            avec_dict = dict(zip(avec_labels,avec_features))
            avecDF = avecDF.append(avec_dict,ignore_index=True)
        a_name = avecDF['name']
        avecDF.drop(['name'],axis=1)
        avecDF.insert(0,'AudioFile',a_name)
        avec_name = 'avec_features_' + date + '.csv'
        avecDF.to_csv(os.path.join(output_folder + 'Avec',avec_name))
    if 'gemaps' in optionsPassed:
        gemapsDF = pd.DataFrame()
        if 'Gemaps' not in os.listdir(output_folder):
            os.mkdir(output_folder + 'Gemaps')
        for audioFile in os.listdir(path):
            if audioFile == '.DS_Store':
                continue
            gemaps_features, gemaps_labels = osm.getGemaps(os.path.join(path,audioFile))
            gemaps_dict = dict(zip(gemaps_labels,gemaps_features))
            gemapsDF = gemapsDF.append(gemaps_dict,ignore_index=True)
        g_name = gemapsDF['name']
        gemapsDF.drop(['name'],axis=1)
        gemapsDF.insert(0,'AudioFile',g_name)
        date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        gemaps_name = 'gemaps_features_' + date + '.csv'
        gemapsDF.drop(['class'],axis=1)
        gemapsDF.to_csv(os.path.join(output_folder + 'Gemaps',gemaps_name))
    print("OpenSmile Features Successfully Extracted.")

def librosa(path):
    librosaDF = pd.DataFrame()
    if 'Librosa' not in os.listdir(output_folder):
        os.mkdir(output_folder + 'Librosa')
    for audioFile in os.listdir(path):
        if audioFile == '.DS_Store':
            continue
        librosa_features, librosa_labels = librosa_featurize(os.path.join(path, audioFile))
        librosa_dict = dict(zip(librosa_labels, librosa_features))
        librosa_dict['AudioFile'] = audioFile
        librosaDF = librosaDF.append(librosa_dict, ignore_index=True)
    aFile = librosaDF['AudioFile']
    librosaDF.drop(['AudioFile'],axis=1,inplace=True)
    librosaDF.insert(0, 'AudioFile', aFile)
    date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    librosa_name = 'librosa_features_' + date + '.csv'
    librosaDF.to_csv(os.path.join(output_folder + 'Librosa', librosa_name))
    print("Librosa Features Successfully Extracted.")

def checkpath(path):
    files = os.listdir(path)
    for fi in files:
        #Checks if file is of wav
        if fi == '.DS_Store':
            continue
        if '.wav' not in fi:
            return False
    return True

def feature_suite(path, optionsSelected):
    if optionsSelected == 'all':
        osmile(path,['avec','gemaps'])
        librosa(path)
    else:
        osmile(path, optionsSelected)
        if 'librosa' in optionsSelected:
            librosa(path)

def main():
    if os.path.exists(output_folder) == False:
        os.mkdir(output_folder)
    audio_path = None
    while True:
        audio_path = input("Please provide a path to a folder of audio files: ")
        if os.path.exists(audio_path) == False:
            print("The Path that you provided is incorrect. Please try again.")
        elif checkpath(audio_path) == False:
            print("Please provide a file of 16-bit PCM Wav Files as inputs.")
        else:
            break
    feature_suite(audio_path)
if __name__ == '__main__':
    main()
