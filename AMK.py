import os, sys
import pygame
import pygame.midi
import pygame.fastevent
import array
import ctypes
import math
import time
import ImageGrab
from os import popen
from array import array
from pygame.locals import *

# Controls:
# 0x00 - 0x07: sliders
# 0x10 - 0x17: knobs
# 0x20 - 0x27: S buttons
# 0x30 - 0x37: M buttons
# 0x40 - 0x47: R buttons



class AMK:
    
    def __init__(self, width=640,height=480):
        pygame.midi.init()

    # both display all attached midi devices, and look for ones matching nanoKONTROL2
    def findNanoKontrol(self):
        print "ID: Device Info"
        print "---------------"
        in_id = None
        out_id = None
        for i in range( pygame.midi.get_count() ):
            r = pygame.midi.get_device_info(i)
            (interf, name, input, output, opened) = r
            
            in_out = ""
            if input:
                in_out = "(input)"
            if output:
                in_out = "(output)"
            
            if name == "nanoKONTROL2 SLIDER/KNOB" and input:
                in_id = i
            elif name == "nanoKONTROL2 CTRL" and output:
                out_id = i
            
            print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
                   (i, interf, name, opened, in_out))
            
        return (in_id, out_id)

    # turn a LED on or off
    def light(self, btn, on):
        if on:
            out = 127
        else:
            out = 0
        self.midi_out.write_short(176, btn, out)

    def MainLoop(self):
        # attempt to autodetect nanokontrol
        (in_device_id, out_device_id) = self.findNanoKontrol()

        # allow IDs to be passed in on commandline
        if len(sys.argv) > 1:
            in_device_id = int(sys.argv[1])
        if len(sys.argv) > 2:
            out_device_id = int(sys.argv[2])
    
        # if none of the above, use system default IDs
        if in_device_id is None:
            in_device_id = pygame.midi.get_default_input_id()

        if out_device_id is None:
            out_device_id = pygame.midi.get_default_output_id()

        midi_in = self.midi_in = pygame.midi.Input( in_device_id )
        print "using input  id: %s" % in_device_id
        midi_out = self.midi_out = pygame.midi.Output(out_device_id, 0)
        print "using output id: %s" % out_device_id


        sliders = [0]*8;        # Create an array of 8 elements.
        nobs    = [0]*8;        # Create an array of 8 elements.
        buttons = [0]*40;       # Create an array of 40 elements.
        

        # Loop forever and ever
        while True:
            # waste time so that we don't eat too much CPU
            pygame.time.wait(1)

#            for event in pygame.event.get():
#                if event.type == pygame.QUIT: 
#                    sys.exit()

            # Look for midi events
            if midi_in.poll():
                midi_events = midi_in.read(100)
                midi_evs = pygame.midi.midis2events(midi_events, midi_in.device_id)
                # process all recieved events

                #print "Events: " + str(midi_evs)
                for event in midi_evs:
                    if event.data1 >=0 and event.data1 <= 7:
                        # Slider event.
                        sliders[event.data1] = event.data2
                        
                    elif event.data1 >=16 and event.data1 <= 23:
                        # rotary nob event
                        nobs[event.data1-16] = event.data2
                        
                    elif event.data1 >=32 and event.data1 <= 71:
                        # button event
                        if event.data2 > 0:
                            buttons[event.data1-32] = 1
                        else:
                            buttons[event.data1-32] = 0
                        
                #print "Sliders: " + str(sliders) + " Nobs: " + str(nobs) + " Buttons: " + str(buttons)
                print " Buttons: " + str(buttons)
                



if __name__ == '__main__':
    am = AMK()
    am.MainLoop()
