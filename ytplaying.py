import pafy
import vlc
import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context

url = "https://www.youtube.com/watch?v=JRwReB8tM4A"
response = urllib.request.urlopen(url, context=ssl._create_unverified_context())
video = pafy.new(url)
best = video.getbest()
playurl = best.url
player = vlc.MediaPlayer(playurl)
player.play()