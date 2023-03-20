import json
import requests
import pyaudio
import time

audio = pyaudio.PyAudio()

for index in range(audio.get_device_count()):
    desc = audio.get_device_info_by_index(index)
    print("DEVICE: {device}, INDEX: {index}, RATE: {rate}".format(device=desc["name"], index=index, rate=int(desc["defaultSampleRate"])))

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 4
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Start to record the audio.")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording is finished.")

stream.stop_stream()
stream.close()
p.terminate()

start = time.time()

data = open("output.wav", "rb")

Lang = "Kor" # Kor / Jan / Chn / Eng
URL = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + Lang

ID = "nfztp9gjgb"
SECRET = "UJgcKgooTwOWfig0BQZv4Fc4SCH5g4Qu7RdVieHc"

headers = {
    "Content-Type": "application/octet-stream", #Fix
    "X-NCP-APIGW-API-KEY-ID": ID,
    "X-NCP-APIGW-API-KEY": SECRET,
}

response = requests.post(URL, data=data, headers=headers)
rescode = response.status_code

end = time.time()

NAME = "귀여운 딸기"

print(response.text)

if(rescode == 200):
    Obj = response.json()
    if(Obj['text']=='안녕하세요'):
        print('안녕하세요 '+NAME+"님")
    print(f"{end - start:.5f} sec")
else:
    print("Error : "+ response.text)

#오류 코드
# HttpStatusCode	ErrorCode	ErrorMessage	Description
# 413	STT000	Request Entity Too Large	허용 음성데이터 용량을 초과 ( 최대 3MB )
# 413	STT001	Exceed Sound Data length	허용 음성데이터 길이를 초과 ( 60초 )
# 400	STT002	Invalid Content Type	application/octet-stream 이외의 content-type인 경우 발생
# 400	STT003	Empty Sound Data	음성 데이터가 입력되지 않음
# 400	STT004	Empty Language	언어 파라미터가 입력되지 않음
# 400	STT005	Invalid Language	정해진 언어 이외의 언어 값이 입력
# 500	STT006	Failed to pre-processing	음성인식 전처리 중 오류가 발생. 음성 데이터가 정상적인 wav, mp3, flac 인지 확인이 필요
# 400	STT007	Too Short Sound Data	음성 데이터 길이가 너무 짧음
# 500	STT998	Failed to STT	음성인식 중 오류가 발생. 고객지원으로 문의 필요
# 500	STT999	Internal Server Error	알 수 없는 오류 발생. 고객지원으로 문의 필요

