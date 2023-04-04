import openai
import pyaudio
import config
import build
import pafy
import ffmpeg
import argparse
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
# import RPi.GPIO as GPIO # 차후 라즈베리에서 사용하기 위한 GPIO 컨트롤러

## youtube part

DEVELOPER_KEY = config.youtube_api_key
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

## youtube part end


name = "딸기"

openai.api_key = config.openai_api_key

audio = pyaudio.PyAudio()
r = sr.Recognizer()

with sr.Microphone() as source:
    print("Speak:")
    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language='ko-KR')
            if name in text:
                print("네")
                playsound("start.mp3")
                audio = r.listen(source)
                text = r.recognize_google(audio, language='ko-KR')
                print("You said: ", text)

                # if '동화' and ('재생' or '읽어' or '틀어') in text:
                #     tts = gTTS(text="어떤 동화를 읽어드릴까요?", lang="ko")
                #     tts.save("gtts.mp3")
                #     playsound("gtts.mp3")
                #     audio = r.listen(source)
                #     bookname = r.recognize_google(audio, language='ko-KR')
                #     if '금도끼' or '은도끼' in bookname:
                #         tts = gTTS(text="금도끼와 은도끼를 읽어드릴게요", lang="ko")
                #         playsound("./Stories/Original/kindok2.mp3")
                #     elif '견우' or '직녀' in bookname:
                #         tts = gTTS(text="견우와 직녀를 읽어드릴게요", lang="ko")
                #         playsound("./Stories/Original/kyeonwoo_wa_jiknyeo.mp3")
                #     elif '미운' or '아기' or '오리' in bookname:
                #         tts = gTTS(text="미운 아기 오리를 읽어드릴게요", lang="ko")
                #         playsound("./Stories/Original/miwoon_agi_ori.mp3")
                #     else:
                #         tts = gTTS(text="제가 잘 이해하지 못 했어요.", lang="ko")
                #
                # elif ('엄마' and '아빠') and ('재생' or '읽어' or '틀어') in text:
                #     tts = gTTS(text="어떤 동화를 읽어드릴까요?", lang="ko")
                #     tts.save("gtts.mp3")
                #     playsound("gtts.mp3")
                #
                # elif '유튜브' and ('재생' or '읽어' or '틀어') in text:
                #     tts = gTTS(text="", lang="ko")
                #     tts.save("gtts.mp3")
                #     playsound("gtts.mp3")
                #     if text.find("재생") >= 0 or text.find("일어") >= 0 or text.find("틀어") >= 0:
                #         split_text = text.split(" ")
                #         serach_text = split_text[split_text.index("를") - 1]
                #         output_file = "search_text.wav"
                #         tts = gTTS(text = "유튜브에서 " + serach_text + "를 재생합니다.", lang="ko")
                #         tts.save("gtts.mp3")
                #         playsound("gtts.mp3")
                #
                #
                #         result_url = youtube_search(serach_text)
                #         play_with_url(result_url)
                #     else:
                #         tts = gTTS(text="제가 잘 이해하지 못 했어요.", lang="ko")
                #         tts.save("gtts.mp3")
                #         playsound("gtts.mp3")

                if '유튜브' in text:
                    tts = gTTS(text="", lang="ko")
                    tts.save("gtts.mp3")
                    playsound("gtts.mp3")
                    if text.find("재생") >= 0 or text.find("틀어") >= 0:
                        split_text = text.split(" ")
                        serach_text = split_text[split_text.index("재생", "틀어") - 1]
                        output_file = "search_text.wav"
                        tts = gTTS(text = "유튜브에서 " + serach_text + "를 재생합니다.", lang="ko")
                        tts.save("gtts.mp3")
                        playsound("gtts.mp3")
                        result_url = youtube_search(serach_text)
                        play_with_url(result_url)
                        print(serach_text)
                        print(result_url)


                else:
                    response = openai.Completion.create(
                        model="text-davinci-003",
                        # 사용할 GPT-3 모델의 ID를 나타냅니다. 이 값은 OpenAI API에서 제공되는 모델 ID 중 하나여야 합니다. 위 코드에서는 text-davinci-003 모델을 사용하고 있습니다. 이 모델은 가장 성능이 뛰어난 모델 중 하나입니다.
                        prompt=text,  # 모델이 생성할 텍스트의 시작점이 되는 문장이나 단어를 나타냅니다. 이 값은 모델이 생성할 텍스트의 내용과 방향을 결정하는 데 중요한 역할을 합니다.
                        temperature=0.9,
                        # 모델이 생성한 단어의 다양성 정도를 나타내는 값입니다. 값이 낮을수록 더 일관성 있는 텍스트가 생성되고, 값이 높을수록 더 다양한 텍스트가 생성됩니다.
                        max_tokens=2048,  # 모델이 생성할 최대 단어 수를 나타냅니다. 이 값은 생성되는 텍스트의 길이를 제어하는 데 사용됩니다.
                        top_p=1,  # 다음 단어를 결정할 때 모델이 고려하는 가능성이 높은 상위 p%의 단어를 선택합니다. 값이 높을수록 더 다양한 텍스트가 생성됩니다.
                        frequency_penalty=0.0,  # 자주 등장하는 단어를 사용하지 않도록 하는 정도를 나타내는 값입니다. 값이 높을수록 자주 등장하는 단어를 사용하지 않도록 강제됩니다.
                        presence_penalty=0.6,
                        # 모델이 이전에 생성한 단어를 기억하고 다음 단어를 결정하는 정도를 나타내는 값입니다. 값이 높을수록 이전에 생성한 단어와 다르게 텍스트가 생성됩니다.
                        stop=[" Human:", " AI:"]  # 생성된 텍스트의 끝나는 지점을 나타내는 문자열 리스트입니다. 이 값이 나타날 때까지 모델이 텍스트를 생성합니다.
                    )

                    message = response.choices[0].text.strip()
                    print('message: ', message)

                    tts = gTTS(text=message, lang="ko")
                    tts.save("gtts.mp3")

                    playsound("gtts.mp3")
        except:
            print("Could not recognize your voice")
