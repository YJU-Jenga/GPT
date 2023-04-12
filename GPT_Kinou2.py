import subprocess
import openai
import pyaudio
import pygame
import time
import speech_recognition as sr
import pymysql
import re

from gtts import gTTS

import config
from config import db_config


# 동화 Database 생성
# subprocess.run(['python', 'crawling.py'])

# 동화 Database 연결
def connect_database(config):
    """
    Database를 연결하는 함수
    """
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "SELECT title, detail FROM jenga.book"
    cursor.execute(sql)
    datas = cursor.fetchall()
    database_list = [data for data in datas]
    db.close()
    return database_list


def init_pyaudio():
    """
    마이크와 스피커의 정보를 알려주는 함수
    """
    pygame.mixer.init()
    audio = pyaudio.PyAudio()
    for index in range(audio.get_device_count()):
        desc = audio.get_device_info_by_index(index)
        print("DEVICE: {device}, INDEX: {index}, RATE: {rate} ".format(
            device=desc["name"], index=index, rate=int(desc["defaultSampleRate"])))


def get_text_from_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("음성 명령을 기다리는 중...")
        audio_data = r.listen_in_background(source, speak_text)
    text = ""
    try:
        text = r.recognize_google(audio_data, language='ko-KR')
        print("음성 명령: {}".format(text))
    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        print("Google Speech Recognition 서비스에서 오류 발생; {0}".format(e))
    return text


def get_cleaned_text(text):
    """
    받은 문자열에서 한글만 추출하고 공백과 구두점을 제거하는 함수
    """
    cleaned_text = re.sub(r"[^가-힣]", "", text)
    return cleaned_text


def speak_text(text):
    """
    받은 문자열을 TTS로 음성합성하는 함수
    """
    tts = gTTS(text=text, lang='ko')
    tts.save('gtts.mp3')
    pygame.mixer.Sound('gtts.mp3').play()


def play_fairy_tale(database_list):
    """
    Database에 존재하는 동화를 읽어주는 함수
    """
    source = sr.Microphone()
    with source:
        tts = gTTS(text="어떤 동화를 들려드릴까요?", lang="ko")
        tts.save("gtts.mp3")
        pygame.mixer.Sound("gtts.mp3").play()
        time.sleep(2)
        print("마이크를 통해 동화 제목을 말씀해주세요.")
        text = r.listen(source, phrase_time_limit=5)
        try:
            text = r.recognize_google(text, language="ko-KR")
            text = get_cleaned_text(text)
            print(text)
            for tale_title, tale_content in database_list:
                if tale_title == text:
                    print(tale_content)
                    tts = gTTS(text="동화를 들려줄께요.", lang="ko")
                    tts.save("gtts.mp3")
                    pygame.mixer.Sound("gtts.mp3").play()
                    tts = gTTS(text=tale_content, lang="ko")
                    tts.save("gtts.mp3")
                    pygame.mixer.Sound("gtts.mp3").play()
                    break
            else:
                tts = gTTS(text="그런 동화는 없어요.", lang="ko")
                tts.save("gtts.mp3")
                pygame.mixer.Sound("gtts.mp3").play()
        except sr.UnknownValueError:
            tts = gTTS(text="죄송해요, 제가 듣지 못했어요.", lang="ko")
            tts.save("gtts.mp3")
            pygame.mixer.Sound("gtts.mp3").play()


def main():
    openai.api_key = config.openai_api_key
    DOLL_NAME = "딸기"
    init_pyaudio()
    database_list = connect_database(db_config)
    print("Speak:")
    while True:
        try:
            text = get_text_from_speech()
            if DOLL_NAME in text:
                print(pygame.mixer.get_busy())
                if pygame.mixer.get_busy():
                    pygame.mixer.stop()
                print("네")
                pygame.mixer.Sound("start.mp3").play()
                text = get_text_from_speech()
                if '동화' in text:
                    play_fairy_tale(database_list)
                else:
                    response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=text,
                        temperature=0.9,
                        max_tokens=2048,
                        top_p=1,
                        frequency_penalty=0.0,
                        presence_penalty=0.6,
                    )
                    message = response.choices[0].text.strip()
                    print('message: ', message)

                    tts = gTTS(text=message, lang="ko")
                    tts.save("gtts.mp3")

                    pygame.mixer.Sound("gtts.mp3").play()
        except sr.UnknownValueError:
            print("음성을 인식할 수 없음")
        except sr.RequestError as e:
            print("Google 음성 인식 서비스에서 결과를 요청할 수 없음; {0}".format(e))
        except Exception as e:
            print("음성 명령을 처리하는 동안 오류가 발생; {0}".format(e))


if __name__ == "__main__":
    pygame.init()
    r = sr.Recognizer()
    db = connect_database(db_config)
    for i in range(len(db)):
        print(db[i][0])
    main()
