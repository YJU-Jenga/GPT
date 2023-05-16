import requests

url = 'http://ichigo.aster1sk.com:5000/uploads/music/Part_02_1684224610147.mp3'
filename = 'alarm.mp3'

response = requests.get(url)
with open(filename, 'wb') as file:
    file.write(response.content)
