import pandas as pd
import os
import sys
import csv
import pyAudioAnalysis
import speech_recognition as sr
'''
Feat_API_vPY2 contains all feature extractions that can only be executed in Python 2.7

This includes the following:
Coherence Algorithm Feature(s)
pyAudioAnalysis Features(s)
'''

class Feat_Extract_Py2:
    def __init__(self,audioPath,out_folder,transcript=None):
        '''
        Automatically assume that any time we run the pipeline we are getting ALL voice data from the path.
        '''
        if sys.version_info[0] != 2:
            print("You are not in a Python2 environment. Please only use this API in Py2 environment")
        self.audioPath = audioPath
        self.output = out_folder
        self.trans = self.get_transcript(tr=transcript)

    def get_transcript(self,tr=None):
        '''
        Usage:
        tr is one of the following:
        - List
        - dataframe
        - None-- Speech Recog on audio
        '''
        transcripts = None
        if isinstance(tr,lists):
            transcripts = tr
        elif isinstance(tr,pd.DataFrame):
            tr_field = input("What is the transcript column name in the data frame?")
            if tr_field not in tr.columns.tolist():
                print("Incorrect Field, please check the entered column name")
                sys.exit(1)
            transcripts = tr[tr_field]
        elif tr == None:
            r = sr.Recognizer()
            audio = self.AudioPath
            if audio[:-1] != '/':
                audio += '/'
            transcripts = []
            for a in os.listdir(audioPath):
                tr_script = r.recognize_google(audio + a)
                transcripts.append(tr_script)
        return transcripts
            #Speech Recognition

    def get_pyAudioAnalysis(self):

    def coherence_algorithm(self):
