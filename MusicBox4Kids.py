#!/usr/bin/env python
#taken form https://github.com/saperlot/jukebox4kids/blob/master/pyjukebox.py


import RPi.GPIO as GPIO
import sys
import os
import serial
import time
import string
import subprocess
import re
import MFRC522
import signal

class MusicBox4Kids:

    def __init__(self):
        self.playlist_dir = "/home/pi/playlists"
        self.track_count = 0
        self.current_track = 1
        self.play_status = 0
        self.initialvolume = 50
        self.gpio_playpause = 12
        self.gpio_volumeup = 11
        self.gpio_volumedown = 13
        self.gpio_next = 16
        self.gpio_previous = 18
        os.system("mpc volume 20")


    def load_playlist(self, pls):
        pls_file = os.path.join(self.playlist_dir, "%s.m3u" % pls)
        print pls_file
        if os.path.exists(pls_file):
            print "loading playlist: %s" % pls
            os.system("mpc stop")
            os.system("mpc clear")
            os.system("mpc volume %s", self.initialvolume)
            os.system("mpc load %s" % pls)
            self.track_count = self.get_track_count()
            self.current_track = 1
            if self.track_count > 0:
                os.system("mpc play 1")
        else:
            print "playlist not found!"
            with open(os.path.join(self.playlist_dir, '%s.todo' % pls), 'w'):
               pass

    def get_track_count(self):
        process = subprocess.Popen(['mpc playlist | wc -l'], shell=True, stdout=subprocess.PIPE)
        (st, er) = process.communicate()
        tcount = 0
        try:
            tcount = int(st.strip())
        except ValueError, ex:
            print '"%s" cannot be converted to an int: %s' % (st, ex)
        return tcount

    def process_button(self, button):
        if self.track_count == 0:
            self.track_count = self.get_track_count()
            if self.track_count > 0:
                self.current_track = 1

        # PREV
        if button == self.gpio_previous:
            if self.current_track > 1:
                self.current_track = self.current_track - 1
                os.system("mpc play %d " % self.current_track)

        # PLAY/PAUSE
        if button == self.gpio_playpause:
            os.system("mpc toggle")

        # NEXT
        if button == self.gpio_next:
            if self.current_track < self.track_count:
                self.current_track = self.current_track + 1
                os.system("mpc play %d " % self.current_track)
        
        # Volume up
        if button == self.gpio_volumeup:
            os.system("mpc volume +5")
            
        # Volume down
        if button == self.gpio_volumedown:
            os.system("mpc volume -5")
    
    def run(self):
        print "Starting MusicBox4Kids"
        print "Configuring GPIO"
        print "Using the NFC reader ..."
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        MIFAREReader = MFRC522.MFRC522()
        GPIO.setup(self.gpio_playpause, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.gpio_volumeup, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.gpio_volumedown, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.gpio_next, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.gpio_previous, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        current_rfid = ""
        while(1):
            try:
                # Scan for cards
                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
                # If a card is found
                if status == MIFAREReader.MI_OK:
                    print "Card detected"
                    # Get the UID of the card
                    (status,uid) = MIFAREReader.MFRC522_Anticoll()
                    # If we have the UID, continue
                    if status == MIFAREReader.MI_OK:
                        # rfid = string.join(uid, "")
                        rfid = ''.join(str(x) for x in uid)
                        print "receiving rfid: %s" % rfid
                        if rfid == current_rfid:
                            print "card already detected -- skipping"
                        else:
                            print "Now using new rfid"
                            current_rfid = rfid
                            self.load_playlist(rfid)    
                # sleep for 10ms
                time.sleep(0.01)
                current_ms = time.time()
            except Exception as ex:
                print 'Error: an error occurred during execution: %s' % (ex)
                current_rfid = ""
                self.current_track = 0
                self.track_count = 0
            # process buttons
            if GPIO.input(self.gpio_playpause) == False:
                print('Button gpio_playpause Pressed')
                self.process_button(self.gpio_playpause)
                time.sleep(0.4)
            if GPIO.input(self.gpio_volumeup) == False:
                print('Button gpio_volumeup Pressed')
                self.process_button(self.gpio_volumeup)
                time.sleep(0.4)
            if GPIO.input(self.gpio_volumedown) == False:
                print('Button gpio_volumedown Pressed')
                self.process_button(self.gpio_volumedown)
                time.sleep(0.4)
            if GPIO.input(self.gpio_next) == False:
                print('Button gpio_next Pressed')
                self.process_button(self.gpio_next)
                time.sleep(0.4)
            if GPIO.input(self.gpio_previous) == False:
                print('Button gpio_prevoius Pressed')
                self.process_button(self.gpio_previous)
                time.sleep(0.4)

def main(argv):
    MusicBox4Kids().run()

if __name__ == "__main__":
    main(sys.argv[1:])