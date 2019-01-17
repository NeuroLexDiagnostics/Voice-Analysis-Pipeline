# test file must be in same folder as script
#audioFile = path.join(path.dirname(path.realpath(__file__)), "sample.wav")


# transcribe with pocketsphinx (open-source)
def sphinxTranscribe(file):
    r = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = r.record(source)
    try:
        transcript = r.recognize_sphinx(audio)
        return transcript
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

# to test:
# print(sphinxTranscribe(audioFile))
