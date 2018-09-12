from DigiPsych_API.Feat_API_vPY3 import Feat_Extract
import os
import sys

def get_gemaps_avec(audioDir):
    if audioDir[:-1] != '/':
        audioDir = audioDir + '/'
    export = 'AudioFeatures'
    fe = None
    for fi in os.listdir(audioDir):
        if '.wav' in fi:
            fe = Feat_Extract(audioDir,fi,export)
            fe.get_gemaps()
            fe.get_avec()
    fe.arff_to_csv('./' + export + '/ExportAvec/','./AudioFeatures/FeatureSets/AVEC_FEATS.csv')
    fe.arff_to_csv('./' + export + '/ExportGemaps/','./AudioFeatures/FeatureSets/GEMAPS_FEATS.csv')
    os.remove('./AudioFeatures/ExportAvec/')
    os.remove('./AudioFeatures/ExportGemaps/')
    print("Your GEMAPS and AVEC Feature Data should be in folder /AudioFeatures/FeatureSets/")
'''
This Program is responsible for interacting with the Feature Extraction APIs
'''
def main():
    audioDir = input("What is the directory path to your audio?")
    if os.path.exists(audioDir) == False:
        print("The audio directory you provided does not exist. Please try again")
        sys.exit(1)
    get_gemaps_avec(audioDir)

if __name__ == '__main__':
    main()
