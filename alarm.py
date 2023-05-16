import requests

# url = 'http://ichigo.aster1sk.com:5000/uploads/music/Part_02_1684224610147.mp3'
filename = 'alarm.mp3'
url = 'http://ichigo.aster1sk.com:5000/alarm/getAll/1'

response = requests.get(url)
data = response.json()

# JSON 객체 출력
print(data)

with open(filename, 'wb') as file:
    file.write(response.content)
