import speech_recognition as sr
from gtts import gTTS
import os
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1

        # wait for a second to let the recognizer adjust the
        # energy threshold based on the surrounding noise level

        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        said = ""
        try:
            said = r.recognize_google(audio)
            print(said)
        except sr.UnknownValueError:
            speak("Sorry, I did not get that.")
        except sr.RequestError:
            speak("Sorry, the service is not available")
    return said.lower()

def speak(_text):
    tts = gTTS(text=_text, lang='en')
    filename = "voice.mp3"
    try:
        os.remove(filename)
    except OSError:
        pass
    tts.save(filename)
    # playsound.playsound(filename)

def respond(_text):
    print("Text from get audio: " + _text)
    if 'play' in _text and len(_text) > 5:
        keyword = _text[5:]
        url = f"https://music.youtube.com/search?q={keyword}"
        driver = webdriver.Firefox()
        driver.get(url)
        button = driver.find_element(By.CSS_SELECTOR, "ytmusic-responsive-list-item-renderer a")
        button.click()

speak('Hello, I am your Youtube music bot')
speak('Just say play followed by the name of the music and I will play it')
while True:
    print("I am listening...")
    text = get_audio()
    respond(text)