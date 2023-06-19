import os
import jwt
import datetime
import requests
import time
import pygame
import GPT_Kinou2
from pydub import AudioSegment

# 알람 정보를 가져올 URL 설정
url = 'http://ichigo.aster1sk.com:5000/alarm/getAll/1'

# JWT 토큰 설정
expires_in = datetime.timedelta(days=365)  # 만료 시간 설정
exp_time = datetime.datetime.utcnow() + expires_in
exp_timestamp = int(exp_time.timestamp())
iat_timestamp = int(datetime.datetime.utcnow().timestamp())

payload = {
    "sub": "payload",
    "email": "payload",
    "iat": 1516239022,
    "exp": exp_timestamp
}
secret_key = 'at-secretKey'
algorithm = 'HS256'

token = jwt.encode(payload, secret_key, algorithm=algorithm)
token = str(token)
token = token[2:-1]
print("token: " + str(token))

headers = {
    "Content-type": "application/json",
    'Authorization': 'Bearer ' + str(token)
}

pygame.mixer.init()


def get_alarms():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        alarms = response.json()
        return alarms
    else:
        print(f"Request failed with status code {response.status_code}")
        return []


def check_alarm(alarms):
    current_time = datetime.datetime.now()
    current_hour = current_time.hour
    current_minute = current_time.minute
    current_day = current_time.weekday()  # 0: 월요일, 1: 화요일, ... , 6: 일요일
    current_day = (current_day + 1) % 7  # 요일 순서 변경

    for alarm in alarms:
        print("alarm:", alarm)
        alarm_time = datetime.datetime.strptime(alarm['time_id'], "%H%M")
        alarm_hour = alarm_time.hour
        alarm_minute = alarm_time.minute

        repeat_pattern = alarm['repeat']
        is_alarm_day = repeat_pattern[current_day] == '1'

        if current_hour == alarm_hour and current_minute == alarm_minute and is_alarm_day:
            # 알람이 울릴 동작을 여기에 구현합니다.
            text = alarm['sentence']
            GPT_Kinou2.text_to_speech(text)
            if alarm['file']:
                url = "http://ichigo.aster1sk.com:5000/" + alarm['file']
                save_path = 'alarm.wav'
                download_and_convert_audio(url, save_path)
                pygame.mixer.Sound(save_path).play()
                print(f"Downloaded and converted audio file for alarm")
            print(f"알람 '{alarm['name']}'이 울립니다!")


def download_and_convert_audio(url, save_path):
    response = requests.get(url)

    # Determine file extension
    if url.endswith('.m4a'):
        file_extension = 'm4a'
    elif url.endswith('.mp3'):
        file_extension = 'mp3'
    else:
        print("Unsupported file format.")
        return

    # Save the downloaded file
    audio_file_path = f"audio.{file_extension}"
    with open(audio_file_path, 'wb') as file:
        file.write(response.content)

    # Convert to wav
    wav_file_path = save_path

    # Convert m4a to mp3 if the file extension is m4a
    if file_extension == 'm4a':
        mp3_file_path = f"audio.mp3"
        AudioSegment.from_file(audio_file_path, format=file_extension).export(mp3_file_path, format='mp3')
        audio = AudioSegment.from_file(mp3_file_path, format='mp3')
    else:
        audio = AudioSegment.from_file(audio_file_path, format=file_extension)

    audio.export(wav_file_path, format='wav')

    # Clean up temporary files
    os.remove(audio_file_path)
    if file_extension == 'm4a':
        os.remove(mp3_file_path)

    print(f"Downloaded and converted the audio file to {wav_file_path}")


def download_mp3_from_url(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    while True:
        alarms = get_alarms()
        current_time = time.localtime()
        if current_time.tm_sec == 0:
            print("Checking")
            check_alarm(alarms)
        time.sleep(1)
