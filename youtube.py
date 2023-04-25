import requests
import pytube
import os
import config
import subprocess
import speech_recognition as sr
from gtts import gTTS
import pygame
import time


def get_youtube_url(video_title: str):
    api_key = config.youtube_api_key
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&type=video&part=snippet&maxResults=1&q={video_title}"
    res = requests.get(url)
    video_id = res.json()["items"][0]["id"]["videoId"]
    return f"https://www.youtube.com/watch?v={video_id}"


def extract_audio(video_url: str):
    yt = pytube.YouTube(video_url)
    stream = yt.streams.filter(only_audio=True).first()
    return stream.download()


def play_audio(audio_path):
    subprocess.call(['afplay', audio_path])


def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("음성 명령을 기다리는 중...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language='ko-KR')
        print("음성 명령: {}".format(text))
        return text
    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        print("Google Speech Recognition 서비스에서 오류 발생; {0}".format(e))
    return ""


def text_to_speech(text):
    file_name = "gtts.mp3"
    tts = gTTS(text=text, lang='ko')
    tts.save(file_name)
    tts_sound = pygame.mixer.Sound(file_name)
    tts_sound.play()


if __name__ == "__main__":
    pygame.mixer.init()
    text = ""
    for i in range(3):
        text = speech_to_text()
        if text != "" or i == 2:
            break
        text_to_speech("다시 한번 말해줄래?")
        time.sleep(1)
    if text == "":
        quit()
    video_title = text
    video_url = get_youtube_url(video_title)
    audio_path = extract_audio(video_url)
    play_audio(audio_path)
    os.remove(audio_path)
