#  Edited for AIMakersKIT
import requests
import pytube
import os

from pydub import AudioSegment
import MicrophoneStream as MS
import config
import speech_recognition as sr
import pygame
from gtts import gTTS


# 유튜브 URL을 가져오는 함수
def get_youtube_url(video_title):
    api_key = config.youtube_api_key
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&type=video&part=snippet&maxResults=1&q={video_title}"
    res = requests.get(url)
    video_id = res.json()["items"][0]["id"]["videoId"]
    return f"https://www.youtube.com/watch?v={video_id}"


# 음성만 추출하는 함수
def extract_audio(video_url):
    yt = pytube.YouTube(video_url)
    stream = yt.streams.filter(only_audio=True).first()
    output_path = stream.download()

    # pydub 라이브러리를 사용하여 RIFF 형식으로 변환
    audio = AudioSegment.from_file(output_path, format="mp4")
    new_file = os.path.splitext(output_path)[0] + ".wav"
    audio.export(new_file, format="wav")

    return new_file


# 음성 재생 함수
def play_audio(audio_path):
    MS.play_file(audio_path)


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


mp3_file = "gtts.mp3"
wav_file = "gtts.wav"


def text_to_speech(text):
    file_name = "gtts.mp3"
    tts = gTTS(text=text, lang='ko')
    tts.save(file_name)
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format="wav")
    tts_sound = pygame.mixer.Sound(wav_file)
    tts_sound.play()


# 실행 코드
if __name__ == "__main__":
    audio_path = None  # 초기화
    try:
        video_title = speech_to_text()
        video_url = get_youtube_url(video_title)
        audio_path = extract_audio(video_url)
        play_audio(audio_path)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if audio_path and os.path.exists(audio_path):  # audio_path가 정의되어 있고, 파일이 존재하면 삭제
            os.remove(audio_path)
