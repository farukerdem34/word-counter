import time
import speech_recognition as sr
import argparse


def save_logs(logs):

    with open("logs.txt", "a") as file:
        file.write(logs)
        file.write("\n")


def get_user_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--microphone", dest="mic",
                        help="Index of microphone device. For microphone device list: --microphones", type=str)
    parser.add_argument("--microphones", required=False, default=False,
                        action="store_true", help="List microphones.", dest="microphones")
    parser.add_argument("-l", "--language", dest="lang", default="tr-TR", type=str,
                        help="Language tag. For language list: https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages")
    parser.add_argument("-o", "--output", required=False,
                        default=False, action="store_true")
    parser.add_argument("-w", "--word", dest="word",
                        help="The word the recognize.", type=str)
    parser.add_argument("--clear-logs", action="store_true",
                        dest="clear_logs", required=False)
    parser.add_argument("--verbose",action="store_true",dest="verbose",required=False)
    args = parser.parse_args()
    return args


def recognize_speech_from_mic(recognizer, microphone, language):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance.")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance.")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(
            audio, language=language)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavaliable."
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech."

    return response


def list_microphones():
    mics = sr.Microphone.list_microphone_names()
    n = 0
    for i in mics:
        print(f"[{n}] {str(i)}")
    quit()


def clear_logs():
    try:
        with open("logs.txt", "r") as file:
            file.read()
        with open("logs.txt", "w") as file:
            file.write("")
        quit()
    except FileNotFoundError:
        quit()


if __name__ == "__main__":
    args = get_user_input()

    if args.clear_logs:
        clear_logs()

    if args.microphones:
        list_microphones()

    language = args.lang
    microphone_index = args.mic
    word = args.word

    if len(word.split(" ")) > 1:
        print("You have to type single word.")
        quit()

    word = word.lower()
    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=microphone_index)

    with open("logs.txt", "a") as file:
        file.write(f"The word is: {word.capitalize()}.\n")

    print("Listening...")
    try:
        while True:
            speech = recognize_speech_from_mic(recognizer, microphone, language)
            words = str(speech["transcription"]).split(" ")
            print(words)
            for i in words:
                i = str(i).lower()
                if i == word:
                    prompt = f"[+] You said {i}."
                    print(prompt)
                    save_logs(prompt)
                elif word in i:
                    prompt = f"[?] In the {word}, found {i}. It might be misunderstood."
                    print(prompt)
                    save_logs(prompt)
                elif i in word:
                    prompt = f"[?] In the {i}, found {word}. It might be misunderstood."
                    print(prompt)
                    save_logs(prompt)
                else:
                    if args.verbose:
                        print("Recognized word: " + i)
                    else:
                        pass
    except KeyboardInterrupt:
        print("Quiting.")
        quit()
