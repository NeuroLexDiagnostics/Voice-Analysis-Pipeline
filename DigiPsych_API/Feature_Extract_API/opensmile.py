import pandas as pd
import os
import sys
import csv
import shutil
import tempfile

'''
OpenSmile API. Enables users to leverage capabilities provided by opensmile toolkit.
Given
- Extracts AVEC2013 Features
- Extracts GeMaps Features

---
To Do:
- Do I want to enable get_gemaps(folder_path)/get_avec(folder_path)
'''

class OpenSmile():
    def __init__(self):
        '''
        Initialize temp folders to enable saving of Gemaps and Avec Data
        '''
        self.exportFolder = tempfile.gettempdir()
        #Stores GEMAPS ARFF Files
        self.exportGemaps = os.path.join(self.exportFolder, 'Gemaps')
        os.makedirs(self.exportGemaps)
        #Stores AVEC ARFF Files
        self.exportAvec = os.path.join(self.exportFolder, 'Avec')
        os.makedirs(self.exportAvec)

    def __del__(self):
        '''
        Destructor removes Temp Folders for GeMaps + Avec
        '''
        shutil.rmtree(self.exportGemaps)
        shutil.rmtree(self.exportAvec)

    def getAvec(self,audioFile):
        '''
        Gets Avec Features for provided audio file
        '''

        if '/' in audioFile:
            fi = audioFile.split('/')
            outFile = self.exportAvec + '/' + fi[-1][:-4] + '.arff'
        elif '\\' in audioFile:
            fi = audioFile.split('\\')
            outFile = self.exportAvec + '/' + fi[-1][:-4] + '.arff'
        else:
            outFile = self.exportAvec + '/' + audioFile[:-4] + '.arff'
        self.openSmileAvec(audioFile,outFile)
        print(audioFile)
        print(outFile)
        data,labels = self.parseArff(outFile)
        return data,labels

    def getGemaps(self,audioFile):
        '''
        Gets Gemaps Features for provided audio file
        '''
        if '/' in audioFile:
            fi = audioFile.split('/')
            outFile = self.exportGemaps + '/' + fi[-1][:-4] + '.arff'
        elif '\\' in audioFile:
            fi = audioFile.split('\\')
            outFile = self.exportGemaps + '/' + fi[-1][:-4] + '.arff'
        else:
            outFile = self.exportGemaps + '/' + audioFile[:-4] + '.arff'
        self.openSmileGemaps(audioFile,outFile)
        data,labels = self.parseArff(outFile)
        return data,labels

    def openSmileGemaps(self,wavFile,outFile):
        '''
        Enables usage of Opensmile Gemaps Capability
        '''
        OpenSmile =  os.getcwd() + '\\openSMILE-2.3.0\\bin\Win32\\SMILExtract_Release.exe' #Enter the location of your openSMILE download
        configAddr = os.getcwd() + '\\opensmile-2.3.0\\config\\gemaps\\eGeMAPSv01a.conf'
        os.system(OpenSmile+ ' -C ' + configAddr+ ' ' + ' -I' + ' ' + wavFile + ' -O' + ' ' + outFile)

    def openSmileAvec(self,wavFile,outFile):
        '''
        Enables usage of Opensmile Avec Capability
        '''
        OpenSmile = os.getcwd() + '\\openSMILE-2.3.0\\bin\Win32\\SMILExtract_Release.exe' #Enter the location of your openSMILE download
        configAddr = os.getcwd() + '\\openSMILE-2.3.0\\scripts\\avec2013\\avec2013_functionals.conf'
        os.system(OpenSmile + ' -C ' + configAddr + ' ' + ' -I' + ' ' + wavFile + ' -O' + ' ' + outFile)

    def parseArff(self,arff_file):
        '''
        Parses Arff File created by OpenSmile Feature Extraction
        '''
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
        temp = temp[-1]
        data[0] = temp[:-5] + '.wav'
        return data,labels

#
# def main():
#     oSmile = OpenSmile()
#     data,label = oSmile.getAvec("C:\\Users\\lazhang\\SNAP_LAB\\TIGER\\TIGER_DATA\\TIGER_AUDIO\\TIGER_15_T1_Speech_01.wav")
#     data,label = oSmile.getGemaps("C:\\Users\\lazhang\\SNAP_LAB\\TIGER\\TIGER_DATA\\TIGER_AUDIO\\TIGER_15_T1_Speech_01.wav")
#
#
# if __name__ == '__main__':
#     main()
