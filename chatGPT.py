import os
import openai
import pyaudio
import wave
import requests
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

openai.api_key = "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"
name = "딸기"

audio = pyaudio.PyAudio()
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Speak:")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='ko-KR')
            if name in text:
                print("네")
                playsound("start.mp3")
                audio = r.listen(source)
                text = r.recognize_google(audio, language='ko-KR')
                print("You said: ", text)
                response = openai.Completion.create(
                    model="text-davinci-003",
                    # 사용할 GPT-3 모델의 ID를 나타냅니다. 이 값은 OpenAI API에서 제공되는 모델 ID 중 하나여야 합니다. 위 코드에서는 text-davinci-003 모델을 사용하고 있습니다. 이 모델은 가장 성능이 뛰어난 모델 중 하나입니다.
                    prompt=text,  # 모델이 생성할 텍스트의 시작점이 되는 문장이나 단어를 나타냅니다. 이 값은 모델이 생성할 텍스트의 내용과 방향을 결정하는 데 중요한 역할을 합니다.
                    temperature=0.9,
                    # 모델이 생성한 단어의 다양성 정도를 나타내는 값입니다. 값이 낮을수록 더 일관성 있는 텍스트가 생성되고, 값이 높을수록 더 다양한 텍스트가 생성됩니다.
                    max_tokens=2048,  # 모델이 생성할 최대 단어 수를 나타냅니다. 이 값은 생성되는 텍스트의 길이를 제어하는 데 사용됩니다.
                    top_p=1,  # 다음 단어를 결정할 때 모델이 고려하는 가능성이 높은 상위 p%의 단어를 선택합니다. 값이 높을수록 더 다양한 텍스트가 생성됩니다.
                    frequency_penalty=0.0,  # 자주 등장하는 단어를 사용하지 않도록 하는 정도를 나타내는 값입니다. 값이 높을수록 자주 등장하는 단어를 사용하지 않도록 강제됩니다.
                    presence_penalty=0.6,
                    # 모델이 이전에 생성한 단어를 기억하고 다음 단어를 결정하는 정도를 나타내는 값입니다. 값이 높을수록 이전에 생성한 단어와 다르게 텍스트가 생성됩니다.
                    stop=[" Human:", " AI:"]  # 생성된 텍스트의 끝나는 지점을 나타내는 문자열 리스트입니다. 이 값이 나타날 때까지 모델이 텍스트를 생성합니다.
                )

                message = response.choices[0].text.strip()
                print('message: ', message)

                tts = gTTS(text=message, lang="ko")
                tts.save("gtts.mp3")

                playsound("gtts.mp3")
        except:
            print("Could not recognize your voice")

# for index in range(audio.get_device_count()):
#     desc = audio.get_device_info_by_index(index)
#     print("DEVICE: {device}, INDEX: {index}, RATE: {rate}".format(device=desc["name"], index=index, rate=int(desc["defaultSampleRate"])))
#
# # 음성 녹음을 위한 파라미터 설정
# CHUNK = 1024
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# RECORD_SECONDS = 4
# WAVE_OUTPUT_FILENAME = "output.wav"
#
# # PyAudio 객체 생성
# p = pyaudio.PyAudio()
#
# # 음성 녹음 스트림 열기
# stream = p.open(format=FORMAT,
#                 channels=CHANNELS,
#                 rate=RATE,
#                 input=True,
#                 frames_per_buffer=CHUNK)
#
# print("* 음성 녹음을 시작합니다.")
#
# # 음성 녹음 데이터를 저장할 리스트
# frames = []
#
# # 음성 녹음 데이터 읽기
# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     frames.append(data)
#
# print("* 음성 녹음이 완료되었습니다.")
#
# # 음성 녹음 스트림 닫기
# stream.stop_stream()
# stream.close()
# p.terminate()
#
# # 음성 녹음 데이터를 WAV 파일로 저장
# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()
#
# stream.stop_stream()
# stream.close()
# p.terminate()
#
# data = open("output.wav", "rb")
#
# Lang = "Kor" # Kor / Jan / Chn / Eng
# URL = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + Lang
#
# ID = "nfztp9gjgb"
# SECRET = "UJgcKgooTwOWfig0BQZv4Fc4SCH5g4Qu7RdVieHc"
#
# headers = {
#     "Content-Type": "application/octet-stream", #Fix
#     "X-NCP-APIGW-API-KEY-ID": ID,
#     "X-NCP-APIGW-API-KEY": SECRET,
# }
#
# response = requests.post(URL, data=data, headers=headers)
# rescode = response.status_code
#
# prompt = response.json()
#
# print("입력한 질문 : ", prompt['text'])
