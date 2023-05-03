import requests
import pytube
import os
import config
import youtube_dl
from playsound import playsound
import subprocess


# 유튜브 URL을 가져오는 함수
def get_youtube_url(video_title):
    url = f"https://www.googleapis.com/youtube/v3/search?key={config.youtube_api_key}&type=video&part=snippet&maxResults=1&q={video_title}"
    res = requests.get(url)
    video_id = res.json()["items"][0]["id"]["videoId"]
    return f"https://www.youtube.com/embed/{video_id}"

# 음성만 추출하는 함수
def extract_audio(video_url):
    output_filename = f"downloaded"
    # stream_url = f"{video_url}?autoplay=1"
    output_path = subprocess.run([
        # "ffmpeg",
        # "-i", stream_url,
        # "-c", "copy",
        # "-bsf:a", "aac_adtstoasc",
        # file_name
        "ffmpeg -i $(youtube-dl -f 140 -g {video_url}) -vn -ar 44100 -ac 2 -ab 192k -f mp3 {output_filename}"
    ])
    return output_path

# 음성 재생 함수
def play_audio(audio_path):
    playsound(audio_path)

# 실행 코드
if __name__ == "__main__":
    try:
        video_title = input("영상 제목을 입력하세요: ")
        video_url = get_youtube_url(video_title)
        print(video_url)
        audio_path = extract_audio(video_url)
        play_audio(audio_path)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)