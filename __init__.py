"""
skill laugh

Copyright (C) 2018 JarbasAI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.

"""

from mycroft import MycroftSkill, intent_file_handler, intent_handler
from adapt.intent import IntentBuilder
from mycroft.audio import wait_while_speaking, is_speaking
from mycroft.util import play_wav, play_mp3, play_ogg
from os import listdir
from os.path import join, abspath, dirname
import random
from datetime import timedelta, datetime
from mycroft.util.parse import match_one, normalize, extract_duration
import wave
import contextlib
import pytz
import math
import time

class WhiteNoise(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.endtime = None;
        self.process = None
        
    def initialize(self):
        #Build play list
        self.play_list = {
            'ocean': join(abspath(dirname(__file__)), 'sounds', 'ocean.wav'),    
            'wind': join(abspath(dirname(__file__)), 'sounds', 'wind.wav'),
            'train': join(abspath(dirname(__file__)), 'sounds', 'rain.wav'),
        
        }
        
    #Play random noise or a specific noise from list
    @intent_file_handler('noise.white.intent')
    def handle_single_whitenoise(self, message):
        print("inside handler")
        wait_while_speaking()
        print (message.data.get('sound'))
        if message.data.get('sound') is not None:
            print("inside not None")
            title = message.data.get('sound')
            score = match_one(title, self.play_list)
            print(score)
            if score[1] > 0.5:
                self.process = play_wav(score[0])
            else:
                self.speak('Sorry I could not find that sound in my library')
                return None            
        else:
            print("inside None")
            sound_file = list(self.play_list.values())
            sound_file = random.choice(sound_file)
            print(sound_file)
            #if os.path.isfile(sound_file):
            wait_while_speaking()
            self.process = play_wav(sound_file)
    #Handles Loop Call
    @intent_file_handler('whitenoiseloop.intent')
    def handle_loop_whitenoise(self, message):
        print("inside loop handler")
        wait_while_speaking()
        print (message.data.get('sound'))
        if message.data.get('sound') is not None:
            print("inside not None")
            title = message.data.get('sound')
            score = match_one(title, self.play_list)
            print(score)
            if score[1] > 0.5:
                self.process = play_wav(score[0])
            else:
                return None
                self.speak('Sorry I could not find that sound in my library')
        else:
            print("inside None")
            sound_file = list(self.play_list.values())
            sound_file = random.choice(sound_file)
            print(sound_file)
            #if os.path.isfile(sound_file):
            wait_while_speaking()
            self.process = play_wav(sound_file)
            fname = sound_file
        
        #Extract Time and Duration of Audio Play
        utt = normalize(message.data.get('utterance', "").lower())
        extract = extract_duration(utt)
        print (extract)
        if extract:
            total_duration = extract[0]
            self.endtime = extract[0]
            utt = extract[1]
        utc=pytz.UTC
        print("Current Duration:" )
        secs = self.endtime.total_seconds()
        now = datetime.now()
        time_expires = now + timedelta(seconds=secs)
        self.timer = {
                 "duration": secs,
                 "expires": time_expires
                 }
        self.update_time(None)
                
                    
    def update_time(self, message):
        print("inside update_time")
        # Check if there is an expired timer
        now = datetime.now()
        # Calc remaining time and show using faceplate
        if (self.timer["expires"] > now):
            # Timer still running
            remaining = (self.timer["expires"] - now).seconds
            print (remaining)
            self.cancel_scheduled_event('ShowTimer')
            self.schedule_repeating_event(self.update_time,
                                          None, 1,
                                          name='ShowTimer')
        else:
            # Timer has expired but not been cleared, flash eyes
            overtime = (now - self.timer["expires"]).seconds
            print (overtime)
            if stopped!= True:
                self.speak("Playtime is over!")
            self.cancel_scheduled_event('ShowTimer')
            self.stop()
    def stop_playing(self):
        if self.process is not None:
            self.process.terminate()
            return True
        return False
    @intent_handler(IntentBuilder("")
      .require("Stop")
    )
    def stop(self):
        # abort current laugh
        stopped = self.stop_playing()    
        return stopped


def create_skill():
    return WhiteNoise()
