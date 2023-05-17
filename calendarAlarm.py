import jwt
import datetime as tokendatetime
from datetime import datetime as caldatetime
import requests
import GPT_Kinou2
import ex4_getText2VoiceStream as tts
import MicrophoneStream as MS
import json

url = 'http://ichigo.aster1sk.com:5000/calendar/date'
# url = 'http://13.125.180.187/user/user_all'

# 만료 시간 설정
expires_in = tokendatetime.timedelta(days=365)
exp_time = tokendatetime.datetime.utcnow() + expires_in
exp_timestamp = int(exp_time.timestamp())
iat_timestamp = int(tokendatetime.datetime.utcnow().timestamp())
print(str(exp_time))

payload = {
    "sub": "payload",
    "email": "payload",
    # "iat": 1516239022,
    "iat": iat_timestamp,
    "exp": exp_timestamp
}


secret_key = 'at-secretKey'
algorithm = 'HS256'

token_b = jwt.encode(payload, secret_key, algorithm=algorithm)
# token_b = jwt.encode(payload, secret_key, algorithm=algorithm)
token = str(token_b)
token = token[2:-1]
print(token)
# print(token)

headers = {
    "Content-type": "application/json",
    'Authorization': 'Bearer ' + token
}

# current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
current_date = caldatetime.now().strftime("%Y-%m-%dT00:00:00.000Z")
print("current_date: " + current_date)

# JSON 요청 보낼 데이터
calpayload = {
    "userId": 1,
    "dateString": current_date
}

response = requests.post(url, json=calpayload, headers=headers)

print("status_code: ", response.status_code)

if response.status_code == 200:
    # print(response)
    # print(response.text)
    # data = json.loads(response.text)
    data = response.json()
    print(data)
    # 반환된 JSON 데이터에서 필요한 값을 추출하여 사용합니다.
elif response.status_code == 201:
    data = response.json()
    print(data)
else:
    print(f"Request failed with status code {response.status_code}")

for data in data:
    title_text = str(data['title'])
    description_text = str(data['description'])

    tts.getText2VoiceStream(title_text, "tts.wav")
    MS.play_file("tts.wav")

    tts.getText2VoiceStream(description_text, "tts.wav")
    MS.play_file("tts.wav")

    # GPT_Kinou2.text_to_speech(title_text)
    # GPT_Kinou2.text_to_speech(description_text)

    print(f"알람 '{data['title']}'이 울립니다!")



# import json
# from playsound import playsound
#
# def play_sound_if_condition_met(json_data, condition):
#     # 조건에 따라 소리를 재생시킵니다.
#     if condition in json_data:
#         playsound("sound.wav")
#
# def main():
#     # JSON 파일을 로드합니다.
#     with open('data.json') as f:
#         json_data = json.load(f)
#
#     # 조건을 설정합니다.
#     condition = "example_condition"
#
#     # 조건에 따라 소리를 재생시킵니다.
#     play_sound_if_condition_met(json_data, condition)
#
# if __name__ == "__main__":
#     main()