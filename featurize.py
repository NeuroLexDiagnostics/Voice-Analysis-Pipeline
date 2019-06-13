import argparse
import os
import sys
import Voice_Feature_Wrapper
import Language_Feature_Wrapper

output_folder = './Output_Folder/'

def main(audio,transcripts, options):
    if audio == None and transcripts == None:
        print("Please Provide a path to Audio Files or Transcript")
        sys.exit()
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    bit = None
    if audio:
        audio_path = audio
        print(audio_path)
        if not os.path.exists(audio_path):
            print("The Path that you provided is incorrect. Please try again.")
        elif not Voice_Feature_Wrapper.checkpath(audio_path):
            print("Please provide a file of 16-bit PCM Wav Files as inputs.")
        optionPass = []
        if 'all' in options:
            optionPass.append('all')
            Voice_Feature_Wrapper.feature_suite(audio_path, optionPass)
        else:
            if 'avec' in options:
                optionPass.append('avec')
            elif 'gemaps' in options:
                optionPass.append('gemaps')
            elif 'librosa' in options:
                optionPass.append('librosa')
            Voice_Feature_Wrapper.feature_suite(audio_path,optionPass)
    elif transcripts:
        print('If passing a csv of transcripts, please label the transcript column \'transcript\'')
        transcript_path = transcripts
        print(transcript_path)
        if '.csv' in transcript_path:
            if not os.path.isfile(transcript_path):
                print('The CSV path you provided is incorrect, Please try again')
                return
            bit = 1
        elif not os.path.exists(transcript_path):
            print('The Path that you provided is incorrect. Please try again.')
        elif not Language_Feature_Wrapper.checkpath(transcript_path):
            print('Please provide a Folder of only text document Files as inputs.')
        else:
            bit = 0
        if 'all' in options:
            Language_Feature_Wrapper.feature_suite(transcript_path, bit)
        else:
            langOptions = []
            if 'nltk' in options:
                langOptions.append('nltk')
            if 'spacy' in options:
                langOptions.append('spacy')
            if 'ling' in options:
                langOptions.append('ling')
            if 'coh' in options:
                langOptions.append('coh')
            Language_Feature_Wrapper.feature_suite_selected(transcript_path, bit, langOptions)
    else:
        print('Please enter path of the files. Use help for more details')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=' command line processing..')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a", "--audio", action='store', help='<Path to a folder of audio files')
    group.add_argument("-t", "--transcripts", action='store',
                       help='Path to a folder of transcript text files or a csv of transcripts')
    parser.add_argument('-l','--list', nargs='+', help='<Required> Set flag', required=True)
    args = parser.parse_args()
    main(args.audio,args.transcripts,args.list)
