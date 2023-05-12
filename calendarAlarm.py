import requests
import json

login_url = 'http://ichigo.aster1sk.com/auth/login/signin'
json_url = 'https://ichigo.aster1sk.com/calendar/week'

# 우선 로그인
headers = {
    'Content-Type': 'application/json'
}

login_data = {
    'email': 'user@gmail.com',
    'password': '*qW23456'
}
session = requests.session()
response = session.post(login_url, json=login_data, headers=headers)

print('session', session)
print('session.post', session.post)
print('response', response)
print('response.status_code = ', response.status_code)

if response.status_code == 200:
    # JSON 요청 보낼 데이터
    payload = {
        "userId": 1,
        "dateString": "2023-04-17T09:00:00.000Z"
    }

    # JSON 요청 보내기
    response = session.post(json_url, data=json.dumps(payload))

    # 응답 받은 데이터 출력
    print(response.json())
else:
    print('로그인 실패')









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