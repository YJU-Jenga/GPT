#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 2: STT - getVoice2Text """

from __future__ import print_function

import audioop
from ctypes import *

import MicrophoneStream as MS
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import grpc
import user_auth as UA

HOST = 'openapi.gigagenie.ai'
PORT = 50051
RATE = 16000
CHUNK = 512

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    dummy_var = 0


c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)


def generate_request():
    with MS.MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()

        for content in audio_generator:
            message = gigagenieRPC_pb2.reqVoice()
            message.audioContent = content
            yield message

            rms = audioop.rms(content, 2)
            # print_rms(rms)


def getVoice2Text():
    print("\n\n음성인식을 시작합니다.\n\n종료하시려면 Ctrl+\\ 키를 누루세요.\n\n\n")
    channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials())
    stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)
    request = generate_request()
    result_text = ''
    for response in stub.getVoice2Text(request):
        if response.resultCd == 200:  # partial
            print('resultCd=%d | recognizedText= %s'
                  % (response.resultCd, response.recognizedText))
            result_text = response.recognizedText
        elif response.resultCd == 201:  # final
            print('resultCd=%d | recognizedText= %s'
                  % (response.resultCd, response.recognizedText))
            result_text = response.recognizedText
            break
        else:
            print('resultCd=%d | recognizedText= %s'
                  % (response.resultCd, response.recognizedText))
            break

    print("\n\n인식결과: %s \n\n\n" % (result_text))
    return result_text


def main():
    # STT
    text = getVoice2Text()


if __name__ == '__main__':
    main()
