import re
import time
import speech_recognition as sr
import pygame
import GPT_Kinou2


def set_timer():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("말씀해주세요.")
        audio = r.listen(source)

    try:
        voice_text = r.recognize_google(audio, language="ko-KR")
        print("인식된 음성:", voice_text)

        if "타이머" in voice_text:
            timer_duration = extract_timer_duration(voice_text)
            print("timer_duration:", timer_duration)
            if timer_duration is not None:
                print(f"{timer_duration}초 타이머를 설정합니다.")
                time.sleep(timer_duration)
                print("타이머 종료")
                pygame.mixer.Sound("start.wav").play()  # 알람 소리 재생
            else:
                print("타이머의 시간을 인식하지 못했습니다.")
        else:
            print("타이머 설정이 아닌 명령입니다.")

    except sr.UnknownValueError:
        print("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        print(f"Google Speech Recognition 서비스에 오류가 발생했습니다: {e}")


def extract_timer_duration(text):
    pattern = r"(\d+)\s*([시분초])"
    matches = re.findall(pattern, text)

    if not matches:
        return None

    total_seconds = 0
    for match in matches:
        value, unit = match
        value = int(value)
        if unit == '시':
            total_seconds += value * 3600
        elif unit == '분':
            total_seconds += value * 60
        elif unit == '초':
            total_seconds += value

    return total_seconds


if __name__ == '__main__':
    pygame.mixer.init()
    pygame.mixer.Sound("start.wav").play()
    GPT_Kinou2.print_audio_info()
    set_timer()
