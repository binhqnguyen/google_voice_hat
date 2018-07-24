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


def main():
    recognizer = aiy.cloudspeech.get_recognizer()
    recognizer.expect_phrase('turn off the light')
    recognizer.expect_phrase('turn on the light')
    recognizer.expect_phrase('blink')
    recognizer.expect_phrase('text')
    recognizer.expect_phrase('call')
    recognizer.expect_phrase('ok')

    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    aiy.audio.get_recorder().start()
    
    client = Client("Twilio client ID", "key")

    listening = 0
    print("Say OK ...")
    while True:
        #print('Press the button and speak')
        #button.wait_for_press()
        #print('Listening...')
        text = recognizer.recognize()
        if not text:
            print('Sorry, I did not hear you.')
        else:
            if 'ok' in text:
                listening = 1
                print ("Listening ...")
                continue
            elif listening == 0:
                print("Say OK ...")
                continue
            print('You said "', text, '"')
            if 'turn on the light' in text:
                led.set_state(aiy.voicehat.LED.ON)
            elif 'turn off the light' in text:
                led.set_state(aiy.voicehat.LED.OFF)
            elif 'blink' in text:
                led.set_state(aiy.voicehat.LED.BLINK)
            elif 'goodbye' in text:
                break
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
            listening = 0


if __name__ == '__main__':
    main()
