import time
import speech_recognition as sr

def recognize_speech_from_mic(recognizer,microphone):
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
        response["transcription"] = recognizer.recognize_google(audio,language="tr-TR")
    except  sr.RequestError:
        response["success"] = False
        response["error"] = "API unavaliable."
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech."
    
    return response


if __name__ == "__main__":
    word = "öyle"
    word = word.lower()
    print("Listening...")
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=1)

    while True:
        speech = recognize_speech_from_mic(recognizer,microphone)
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
