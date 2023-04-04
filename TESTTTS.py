import openai
import pyaudio
import config
import build
import pafy
import ffmpeg
import argparse
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

text = "가"

for count in range(0, 1000):
    print(len(text))
    tts = gTTS(text, lang="ko")
    tts.save("gtts.mp3")
    playsound("gtts.mp3")
    text = text + "예아"

