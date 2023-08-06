import speech_recognition as sr
from gtts import gTTS
import playsound
import os
from characterai import PyCAI

flac_path = "/opt/homebrew/bin/flac"
sr.Recognizer().flac_converter = flac_path

class Character:
    def __init__(self, client, id):
        data_pass_through = False
        while not data_pass_through:
            try:
                data_pass_through = True
                self.ID = id  # place the id of your desired character here
                self.client = PyCAI(client)
                self.chat = self.client.chat.get_chat(self.ID)
            except:
                continue
    def send_message(self, message):
        message_pass_through = False
        while not message_pass_through:
            try:
                message_pass_through = True
                data = self.client.chat.send_message(self.ID, message)
                text = data['replies'][0]['text']
                return text
            except:
                continue

    def speak(self, text):
        if text:
            tts = gTTS(text=text, lang="en")
            tts.save("output.mp3")
            playsound.playsound("output.mp3")
            os.remove("output.mp3")
        else:
            self.speak("There was no response from the API.")

class Listener:
    def __init__(self):
        # sets the default minimum of volume for the microphone to pick up input
        self.power_min = sr.Recognizer().energy_threshold = 5000
        self.mic = sr.Microphone()
    def record(self, source, duration):
        if source and duration:
            r = sr.Recognizer()
            audio_data = r.record(source, duration)
            try:
                message = r.recognize_google(audio_data)
                return message
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                pass

    def listen(self, source):
        if source:
            r = sr.Recognizer()
            audio_data = r.listen(source)
            try:
                message = r.recognize_google(audio_data)
                return message
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                pass
