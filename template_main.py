from DigiPsych_API.Feature_Extract_API.opensmile import OpenSmile
from DigiPsych_API.Analysis_API import *

'''
Template Main File. Enables user to leverage all the API methods provided in
the DigiPsych API

'''
# Enter Methods Here

def main():
    osmile = OpenSmile()
    data,labels = osmile.getGemaps('C:\\Users\\lazhang\\TIGER_AUDIO\\TIGER_15_T1_Speech_01.wav')
    print(data)
if __name__ == '__main__':
    main()
