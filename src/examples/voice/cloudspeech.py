#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google CloudSpeech recognizer."""

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
from twilio.rest import Client

recorder_started = 0

def start_recorder():
    global recorder_started 
    aiy.audio.get_recorder().start()
    recorder_started = 1

def process_cloud_speech():
    global recorder_started
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('turn off the light')
    recognizer.expect_phrase('turn on the light')
    recognizer.expect_phrase('blink')
    recognizer.expect_phrase('text')
    recognizer.expect_phrase('call')

    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    if recorder_started == 0:
        start_recorder()

    client = Client("AC81fc0e660e0e022890b26790fdff8e01", "89d4eb65926f3765fefe704bbf667ec9")

    text = recognizer.recognize()
    if not text:
        print('Sorry, I did not hear you.')
    else:
        print('You said "', text, '"')
        if 'turn on the light' in text:
            led.set_state(aiy.voicehat.LED.ON)
        elif 'turn off the light' in text:
            led.set_state(aiy.voicehat.LED.OFF)
        elif 'blink' in text:
            led.set_state(aiy.voicehat.LED.BLINK)
        elif 'goodbye' in text:
            return
        elif 'text' in text:
            recipient_number = text.split()[3]
            recipient_name = text.split()[1]
            message = " ".join(text.split()[4:])
            print ("Recipient is %s at %s" % (recipient_name, recipient_number))
            aiy.audio.say('Texting %s at %s message %s!'% (recipient_name, recipient_number, message))
            client.messages.create(to="+1%s"% (recipient_number), 
                               from_="+16096148079", 
                               body="Hey %s, %s, Binh's Assistant!" % (recipient_name, message))
        elif 'call' in text:
            recipient_number = text.split()[3]
            recipient_name = text.split()[1]
            aiy.audio.say('Calling %s at %s!'% (recipient_name, recipient_number))
            client.calls.create(url='http://demo.twilio.com/docs/voice.xml',
                                to='+1%s'%recipient_number,                                                                                     from_='+16096148079')
    print ("Done processing cloud speech ...")
    return 0
