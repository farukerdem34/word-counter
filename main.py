import time
import speech_recognition as sr
import argparse

def get_user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m","--microphone",dest="mic",help="Index of microphone device. For microphone device list: --microphones",type=str)
    parser.add_argument("--microphones",required=False,default=False,action="store_true",help="List microphones.")
    parser.add_argument("-l","--language",dest="lang",default="tr-TR",type=str,help="Language tag. For language list: https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages")
    args = parser.parse_args()
    return args
    

def recognize_speech_from_mic(recognizer,microphone,language):
    if not isinstance(recognizer,sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance.")
    if not isinstance(microphone,sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance.")
    
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)


    response = {
            "success":True,
            "error":None,
            "transcription":None
        }

    try:
        response["transcription"] = recognizer.recognize_google(audio,language=language)
    except  sr.RequestError:
        response["success"] = False
        response["error"] = "API unavaliable."
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech."
    
    return response


if __name__ == "__main__":
    args = get_user_input()
    if args.microphones:
        mics = sr.Microphone.list_microphone_names()
        n=0
        for i in mics:
            print(f"[{n}] {str(i)}")
        quit()

    language = args.lang
    microphone_index = args.mic

    word = "öyle"
    word = word.lower()
    print("Listening...")
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=microphone_index)
    
    while True:
        speech = recognize_speech_from_mic(recognizer,microphone,language)
        words = str(speech["transcription"]).split(" ")  
        print(words)
        for i in words:
            i = str(i).lower()
            if i == word:
                print(f"[+] You said {i}.")
            elif word in i:
                print(f"[?] In the {word}, found {i}. It might be misunderstood.")
            elif i in word:
                print(f"[?] In the {i}, found {word}. It might be misunderstood.")
            else:
                pass
