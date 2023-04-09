import requests
import pytube
import os
import config
from playsound import playsound

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
    return output_path

# 음성 재생 함수
def play_audio(audio_path):
    playsound(audio_path)

# 실행 코드
if __name__ == "__main__":
    video_title = input("영상 제목을 입력하세요: ")
    video_url = get_youtube_url(video_title)
    audio_path = extract_audio(video_url)
    play_audio(audio_path)
    os.remove(audio_path)  # 임시 파일 삭제