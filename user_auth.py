#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 2: STT - getVoice2Text """

from __future__ import print_function

import datetime
import hashlib
import hmac
import json
import os

import grpc
import requests

# {"clientId":"STgwMDI4MzY6MTY2OTE4MTE5NTY5OA==","clientKey":"Y2xpZW50X2tleToxNjY5MTgxMTk1Njk4","clientSecret":"Y2xpZW50X3NlY3JldDoxNjY5MTgxMTk1Njk4","certUrl":"https://api.gigagenie.ai/api/v1/aiportal/cert"}
# Config for GiGA Genie Inside gRPC
CLIENT_ID = 'STgwMDI4MzY6MTY2OTE4MTE5NTY5OA=='
CLIENT_KEY = 'Y2xpZW50X2tleV9jYjoxNjY5MTgyMDY5OTc0'
CLIENT_SECRET = 'Y2xpZW50X3NlY3JldF9jYjoxNjY5MTgyMDY5OTc0'

CLIENT_UUID = ''

URL = "https://openapi.gigagenie.ai:9080/api/v1/user"


def getMacAddr():
    stream = os.popen('cat /sys/class/net/eth0/address')
    output = stream.read()
    return output.replace(":", "")


CLIENT_USER_ID = getMacAddr()


# print(CLIENT_USER_ID)


def getUUID():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    message = CLIENT_ID + ':' + CLIENT_KEY + ':' + timestamp
    signature = hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    data = {"clientKey": CLIENT_KEY, "userId": CLIENT_USER_ID, "timestamp": timestamp, "signature": signature}
    res = requests.post(URL, data=data)
    response = json.loads(res.text)
    if response["code"] == 200:
        global CLIENT_UUID
        CLIENT_UUID = response["data"]["uuid"]
    else:
        print("Failed to get UUID")


getUUID()


# COMMON : Client Credentials #
def getMetadata():
    global CLIENT_UUID
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    message = CLIENT_ID + ':' + CLIENT_KEY + ':' + timestamp
    signature = hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    metadata = [('x-auth-uuid', CLIENT_UUID),
                ('x-auth-timestamp', timestamp),
                ('x-auth-signature', signature)]
    # print(metadata)

    return metadata


def credentials(context, callback):
    callback(getMetadata(), None)


def getCredentials():
    ssl_cred = grpc.ssl_channel_credentials()
    auth_cred = grpc.metadata_call_credentials(credentials)
    return grpc.composite_channel_credentials(ssl_cred, auth_cred)

# END OF COMMON #
