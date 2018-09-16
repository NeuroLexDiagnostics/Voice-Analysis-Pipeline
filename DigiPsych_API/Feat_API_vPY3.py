import pandas as pd
import os
import sys
import csv

'''
Feat_Extract API has been developed with the purpose of extracting a whole
panel/array of featuresets from audio files.

Given an audio file, the API should be able to grab a whole list of feature(s)
from the data.

Feat_API_vPY3 API will include:
- GEMAPS
- AVEC

Other Feature(s) in progress:
-
'''
class Feat_Extract(object):
    def __init__(self,audioPath,out_folder):
        '''
        - Audio File: Only the audio file name, no path name
        - Audio Path: Audio Path to folder.
        - out_folder: Where all the data will be outputted.
            - Out folder will follow this consistent structure:
                <Out-Folder>:
                    | FeatureSets
                    | ExportAvec
                    | ExportGemaps
        '''
        self.audioPath = audioPath
        self.output = out_folder
        if self.output not in os.listdir():
            os.mkdir(self.output)
            os.mkdir(self.output + '\\FeatureSets/')
            os.mkdir(self.output + '\\ExportAvec/')
            os.mkdir(self.output + '\\ExportGemaps/')
    def get_all_gemaps(self):
        for a in os.listdir(audioPath):
            if '.wav' in a:
                self.get_gemaps(a)
    def get_all_avec(self):
        for a in os.listdir(audioPath):
            if '.wav' in a:
                self.get_avec(a)
    def get_gemaps(self,audioFile):
        '''
        '''
        wavFile = self.audioPath + audioFile
        exportfile = self.output + '/' + 'ExportGemaps/' + audioFile[:-4] + '.arff'
        self.openSmileGemaps(wavFile,exportfile)
        data,labels = self.parseArff(exportfile)
        return data,labels
    def get_avec(self):
        '''
        '''
        wavFile = self.audioPath + audioFile
        exportfile = self.output + '/' +'ExportAvec/' + audioFile[:-4] + '.arff'
        self.openSmileAvec(wavFile,exportfile)
        data,labels = self.parseArff(exportfile)
        return data,labels

    def arff_to_csv(self,fdir,csvfile):
        '''
        Convert directory of arff files to "CSV"
        '''
        #Check if directory has files
        if len(os.listdir(fdir)) == 0:
            print("You have not executed gemaps or avec yet to get features.")
            sys.exit(1)

        with open(csvfile,'w',newline='') as outfile:
            writer = csv.writer(outfile)
            arff_files = os.listdir(fdir)
            c = 0
            for arff_f in arff_files:
                path = fdir + arff_f
                print(path)
                f = open(path,'r')
                data = []
                labels = []

                for line in f:
                    #print(line.strip('\n'))
                    if '@attribute' in line:
                        temp = line.split(" ")
                        feature = temp[1]
                        #print(feature)
                        labels.append(feature)

                    if ',' in line:
                        temp = line.split(",")
                        for item in temp:
                            data.append(item)

                if len(data) != 0:
                    if c == 0:
                        writer.writerow(labels)
                        c += 1
                    data[0] = arff_f[:-5] + '.wav'
                    writer.writerow(data)
                f.close()
            outfile.close()

    def parseArff(self,arff_file):
        f = open(arff_file,'r')
        data = []
        labels = []
        for line in f:
            if '@attribute' in line:
                temp = line.split(" ")
                feature = temp[1]
                labels.append(feature)
            if ',' in line:
                temp = line.split(",")
                for item in temp:
                    data.append(item)
        temp = arff_file.split('/')

        temp = temp[2:]
        arff_file ="/".join(temp)


        data[0] = arff_file[:-5] + '.wav'

        return data,labels

    def openSmileGemaps(self,wavFile,outFile):
        OpenSmile =  os.getcwd() + '\\openSMILE-2.3.0\\bin\Win32\\SMILExtract_Release.exe' #Enter the location of your openSMILE download
        configAddr = os.getcwd() + '\\opensmile-2.3.0\\config\\gemaps\\eGeMAPSv01a.conf'
        os.system(OpenSmile+ ' -C ' + configAddr+ ' ' + ' -I' + ' ' + wavFile + ' -O' + ' ' + outFile)

    def openSmileAvec(self,wavFile,outFile):
        OpenSmile = os.getcwd() + '\\openSMILE-2.3.0\\bin\Win32\\SMILExtract_Release.exe' #Enter the location of your openSMILE download
        configAddr = os.getcwd() + '\\openSMILE-2.3.0\\scripts\\avec2013\\avec2013_functionals.conf'
        os.system(OpenSmile + ' -C ' + configAddr + ' ' + ' -I' + ' ' + wavFile + ' -O' + ' ' + outFile)
