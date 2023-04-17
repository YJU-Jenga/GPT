import pyaudio
import requests
import pytube
import os
import config
import pygame


def get_youtube_url(video_title: str) -> str:
    api_key = config.youtube_api_key
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&type=video&part=snippet&maxResults=1&q={video_title}"
    res = requests.get(url)
    video_id = res.json()["items"][0]["id"]["videoId"]
    return f"https://www.youtube.com/watch?v={video_id}"


def extract_audio(video_url: str) -> str:
    yt = pytube.YouTube(video_url)
    stream = yt.streams.filter(only_audio=True).first()
    return stream.download()


def play_audio(audio_path):
    pygame.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.quit()


def print_audio_info():
    audio = pyaudio.PyAudio()
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        print("Index: {0}, Name: {1}, Channels: {2}, Max Input Channels: {3}".format(i, info['name'], info['maxInputChannels'], info['maxOutputChannels']))
    audio.terminate()


if __name__ == "__main__":
    print_audio_info()
    video_title = input("영상 제목을 입력하세요: ")
    video_url = get_youtube_url(video_title)
    audio_path = extract_audio(video_url)
    play_audio(audio_path)
    os.remove(audio_path)
