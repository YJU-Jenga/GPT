DEVELOPER_KEY = 'KEY'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search(options):
    try:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
        parser = argparse.ArgumentParser()
        parser.add_argument('--q', help='Search term', default=options)
        parser.add_argument('--max-results', help='Max results', default=25)
        args = parser.parse_args()

        search_response = youtube.search().list(q=args.q, part='id,snippet', maxResults=args.max_results).execute()

        videos = []
        url = []

        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                videos.append('%s (%s)' % (search_result['snippet']['title'], search_result['id']['videoId']))
                url.append(search_result['id']['videoId'])

        resultURL = "https://www.youtube.com/watch?v=" + url[0]
        return resultURL

    except:
        print("Youtube Error")


def play_with_url(play_url):
    print(play_url)
    video = pafy.new(play_url)
    best = video.getbestaudio()
    playurl = best.url
    global play_flag
    play_flag = 0

    pya = pyaudio.PyAudio()
    stream = pya.open(format=pya.get_format_from_width(width=2), channels=1, rate=16000, output=True)

    try:
        process = (ffmpeg
                   .input(playurl, err_detect='ignore_err', reconnect=1, reconnect_streamed=1, reconnect_delay_max=5)
                   .output('pipe:', format='wav', audio_bitrate=16000, ab=64, ac=1, ar='16k')
                   .overwrite_output()
                   .run_async(pipe_stdout=True)
                   )

        while True:
            if play_flag == 0:
                in_bytes = process.stdout.read(4096)
                if not in_bytes:
                    break
                stream.write(in_bytes)
        else:
            stream.close()
    finally:
        stream.stop_stream()
        stream.close()