import jwt
import datetime
import requests
import json
import time
import pygame
import GPT_Kinou2

# url = 'http://ichigo.aster1sk.com:5000/user/user_all'
# url = 'http://13.125.180.187/user/user_all'
url = 'http://ichigo.aster1sk.com:5000/alarm/getAll/1'

# 만료 시간 설정
expires_in = datetime.timedelta(days=365)
exp_time = datetime.datetime.utcnow() + expires_in
exp_timestamp = int(exp_time.timestamp())
iat_timestamp = int(datetime.datetime.utcnow().timestamp())
print(str(exp_time))

payload = {
    "sub": "payload",
    "email": "payload",
    "iat": 1516239022,
    "exp": exp_timestamp
}
secret_key = 'at-secretKey'
algorithm = 'HS256'

token_b = jwt.encode(payload, secret_key, algorithm=algorithm)
# token_b = jwt.encode(payload, secret_key, algorithm=algorithm)
# token = str(token_b)
# token = token[2:-1]
print(token_b)

headers = {
    "Content-type": "application/json",
    'Authorization': 'Bearer ' + token_b
}

response = requests.get(url, headers=headers)

print("status_code: ", response.status_code)

if response.status_code == 200:
    # print(response)
    # print(response.text)
    # data = json.loads(response.text)
    alarms = response.json()
    print(alarms)
    # 반환된 JSON 데이터에서 필요한 값을 추출하여 사용합니다.
else:
    print(f"Request failed with status code {response.status_code}")


def check_alarm():
    current_time = datetime.datetime.now()
    current_hour = current_time.hour
    current_minute = current_time.minute
    current_day = current_time.weekday()  # 0: 월요일, 1: 화요일, ... , 6: 일요일
    current_day = (current_day + 1) % 7  # 요일 순서 변경

    for alarm in alarms:
        alarm_time = datetime.datetime.strptime(alarm['time_id'], "%H%M")
        alarm_hour = alarm_time.hour
        alarm_minute = alarm_time.minute

        repeat_pattern = alarm['repeat']
        is_alarm_day = repeat_pattern[current_day] == '1'

        print("alarm_hour", alarm_hour, alarm_minute, is_alarm_day)

        if current_hour == alarm_hour and current_minute == alarm_minute and is_alarm_day:
            # 알람이 울릴 동작을 여기에 구현합니다.
            text = alarm['sentence']
            GPT_Kinou2.text_to_speech(text)
            print(f"알람 '{alarm['name']}'이 울립니다!")


def is_alarm_set(repeat_pattern):
    current_day = datetime.datetime.now().weekday()  # 0: 월요일, 1: 화요일, ... , 6: 일요일
    current_day = (current_day + 1) % 7  # 요일 순서 변경

    # repeat_pattern에서 현재 요일에 해당하는 문자를 가져옵니다.
    current_day_alarm = repeat_pattern[current_day]

    # 해당 요일의 알람 설정 여부를 판별합니다.
    return current_day_alarm == '1'


pygame.mixer.init()
while True:
    current_time = time.localtime()
    if current_time.tm_sec == 0:  # 매 분 정각인 경우에만 실행
        # 실행할 함수 호출
        print("Checking")
        check_alarm()
    time.sleep(1)