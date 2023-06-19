#  Edited for AIMakersKIT
import requests
import pytube
import os

from pydub import AudioSegment
import MicrophoneStream as MS
import config

# 유튜브 URL을 가져오는 함수
def get_youtube_url(video_title):
    api_key = config.youtube_api_key
    url = f"https://www.googleapis.com/youtube/v3/search?key={api_key}&type=video&part=snippet&maxResults=1&q={video_title}"
    res = requests.get(url)
    video_id = res.json()["items"][0]["id"]["videoId"]
    return f"https://www.youtube.com/watch?v={video_id}"
    print

# 음성만 추출하는 함수
def extract_audio(video_url):
    yt = pytube.YouTube(video_url)
    print(yt)
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

# 실행 코드
if __name__ == "__main__":
    audio_path = None  # 초기화
    try:
        video_title = input("영상 제목을 입력하세요: ")
        video_url = get_youtube_url(video_title)
        audio_path = extract_audio(video_url)
        print (video_url)
        play_audio(audio_path)
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if audio_path and os.path.exists(audio_path):  # audio_path가 정의되어 있고, 파일이 존재하면 삭제
            os.remove(audio_path)