from DigiPsych_API.Feature_Extract_API.transcribe import sphinxTranscribe
import os


output_folder = './Output_Folder/'


def transcribe(path):
    if 'Transcripts' not in os.listdir(output_folder):
        os.mkdir(output_folder + 'Transcripts')
        for audioFile in os.listdir(path):
            if audioFile == '.DS_Store':
                continue
            transcriptName = audioFile[:-4] +'.txt'
            transcriptPath = os.path.join(output_folder + 'Transcripts', transcriptName)
            with open(transcriptPath, "w") as textFile:
                textFile.write(sphinxTranscribe(os.path.join(path, audioFile)))
        print('Transcription(s) Complete!')

def checkpath(path):
    files = os.listdir(path)
    for fi in files:
        #Checks if file is of wav
        if fi == '.DS_Store':
            continue
        if '.wav' not in fi:
            return False
    return True

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
    transcribe(audio_path)

if __name__ == '__main__':
    main()
