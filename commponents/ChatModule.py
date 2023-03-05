import speech_recognition as sr
import openai
import pyttsx3


class ChatModule:
    def __init__(self):
        self.sr = sr.Recognizer()
        self.speechEngine = pyttsx3.init()
        openai.api_key = "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"

    def record(self):
        with sr.Microphone() as source:
            audio = self.sr.listen(source)
        return audio

    def recognize_audio(self, audio):
        try:
            text = self.sr.recognize_google(audio, language="pl-PL")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition nie może zrozumieć mowy")
        except sr.RequestError as e:
            print(f"Nie można uzyskać wyników z usługi Google Speech Recognition; {e}")
        return None

    def get_open_ai_response(self, text):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=text,
                max_tokens=256,
                n=1,
                stop=None,
                temperature=0.5,
            )

            return response.choices[0].text
        except openai.Error as e:
            print(f"Error querying OpenAI API: {e}")

    def say(self, text):
        self.speechEngine.setProperty('rate', 180)  # Speed in words per minute
        self.speechEngine.setProperty('volume', 1.0)  # Volume, from 0 to 1
        self.speechEngine.say(text)
        self.speechEngine.runAndWait()

    def run(self):
        self.say("Powiedz coś")
        audio = self.record()
        text = self.recognize_audio(audio)
        print(f"Powiedziałeś: {text}")

        if text is not None:
            response = self.get_open_ai_response(text)
            print(f"Melson: {response}")
            if response is not None:
                self.say(response)
