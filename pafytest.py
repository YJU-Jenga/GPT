# importing pafy
import pafy

# url of video
url = "https://www.youtube.com/watch?v=JRwReB8tM4A"

# getting video
video = pafy.new(url)

# getting all the available streams
streams = video.allstreams

# selecting one stream
stream = streams[1]

# downloading stream
stream.download()