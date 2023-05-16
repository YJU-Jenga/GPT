import jwt
import datetime
import requests
import json

url = 'http://ichigo.aster1sk.com:5000/user/user_all'
# url = 'http://13.125.180.187/user/user_all'

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
token = str(token_b)
print("b : "+token_b)
token = token_b
# token = token[2:-1]
# print(token)

headers = {
    "Content-type": "application/json",
    'Authorization': 'Bearer ' + token
}

response = requests.get(url, headers=headers)

print("status_code: ", response.status_code)

if response.status_code == 200:
    # print(response)
    # print(response.text)
    # data = json.loads(response.text)
    data = response.json()
    print(data)
    # 반환된 JSON 데이터에서 필요한 값을 추출하여 사용합니다.
else:
    print(f"Request failed with status code {response.status_code}")