import pyttsx3 as p
import speech_recognition as sr
from googletrans import Translator

class sWaraNuvad:
    def __init__(self):
        self.engine = p.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices)
        self.translator_enn = None

    def speak(self, audio):
        '''
        The speak() method utilizes the text-to-speech engine to convert text into spoken audio.
        '''
        self.engine.say(audio)
        self.engine.runAndWait()

    def wishme(self):
        '''
        The wishme() method is responsible for greeting the user and asking them in which language they would like to speak.
        '''
        self.speak("Hello. In which language do you have to speak?")


    def takeCommand(self):
        '''
        it's take microphone input from the user and return output as a string
        '''
        global translator_enn

        r = sr.Recognizer()
        with sr.Microphone() as source:
            # user_input = input("select lang: ")
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing...")
            # translator_en = Translator(from_lang=f'{user_input}', to_lang='en')
            query = r.recognize_google(audio, language='en-in')
            # translator_enn = translator_en.translate(query)
            # print(f"User sid: {query}\n")
            # return translator_enn.text

        except Exception as e:
            self.speak("Sorry, Say that again Please...")
            return "None"

        return query


    def lantrans(self):
        '''
        The lantrans() method is the main function that drives the translation process. It prompts the user for input, checks if the input language is supported, 
        and translates the user's subsequent speech into multiple languages using the Translate library. 
        The translations are then printed to the console.
        '''
        self.wishme()

        translationss = []
        
        while True:
            query = self.takeCommand().lower()            

            languages = {"greek": "el", "esperanto": "eo", "english": "en", "afrikaans": "af",
                "swahili": "sw", "catalan": "ca", "italian": "it", "hebrew": "iw",
                "swedish": "sv", "czech": "cs", "welsh": "cy", "arabic": "ar",
                "urdu": "ur", "irish": "ga", "basque": "eu", "estonian": "et",
                "azerbaijani": "az", "indonesian": "id", "spanish": "es", "russian": "ru",
                "galician": "gl", "dutch": "nl", "portuguese": "pt", "latin": "la",
                "turkish": "tr", "filipino": "tl", "latvian": "lv", "lithuanian": "lt",
                "thai": "th", "vietnamese": "vi", "gujarati": "gu", "romanian": "ro",
                "icelandic": "is", "polish": "pl", "tamil": "ta", "yiddish": "yi",
                "belarusian": "be", "french": "fr", "bulgarian": "bg", "ukrainian": "uk",
                "croatian": "hr", "bengali": "bn", "slovenian": "sl", "haitian creole": "ht",
                "danish": "da", "persian": "fa", "hindi": "hi", "finnish": "fi",
                "hungarian": "hu", "japanese": "ja", "georgian": "ka", "telugu": "te",
                "chinese traditional": "zh-TW", "albanian": "sq", "norwegian": "no",
                "korean": "ko", "kannada": "kn", "macedonian": "mk", "chinese simplified": "zh-CN",
                "slovak": "sk", "maltese": "mt", "marathi": "mr","german": "de", "malay": "ms", "serbian": "sr"}


            if query in languages:
                self.speak("Please say something")
                user_lan = languages[query]
                query = self.takeCommand().lower()
                translator_en = Translator()
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print("Listening...")
                    r.pause_threshold = 1
                    audio = r.listen(source)
                try:
                    print("Recognizing...")
                    query = r.recognize_google(audio, language=user_lan)
                    translation_enn = translator_en.translate(query, src=user_lan, dest='en')
                    print(f"User input: {translation_enn.text}\n")

                    translationss = [f"{lan.upper()}: {Translator().translate(translation_enn.text, src='en', dest=lan_code).text}" for lan, lan_code in languages.items() if lan_code != user_lan]
                    return translationss


                except Exception as e:
                    self.speak("Sorry, say that again...")


            elif "stop" == query:
                '''
                The translation process continues until the user says "stop".
                '''
                self.speak('Ok')
                break
            
            else:
                self.speak("The language you said is not in my records. Please tell me another language you know")
            
        return translationss

