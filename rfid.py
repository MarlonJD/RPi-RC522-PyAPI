import signal
import time
import sys
import json
import RPi.GPIO as GPIO

from pirc522 import RFID
from http.server import BaseHTTPRequestHandler, HTTPServer

import sqlite3

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
buzzer_pin = 7
GPIO.setup(buzzer_pin, GPIO.IN)
GPIO.setup(buzzer_pin, GPIO.OUT)

notes = {
    'B0' : 31,
    'C1' : 33, 'CS1' : 35,
    'D1' : 37, 'DS1' : 39,
    'EB1' : 39,
    'E1' : 41,
    'F1' : 44, 'FS1' : 46,
    'G1' : 49, 'GS1' : 52,
    'A1' : 55, 'AS1' : 58,
    'BB1' : 58,
    'B1' : 62,
    'C2' : 65, 'CS2' : 69,
    'D2' : 73, 'DS2' : 78,
    'EB2' : 78,
    'E2' : 82,
    'F2' : 87, 'FS2' : 93,
    'G2' : 98, 'GS2' : 104,
    'A2' : 110, 'AS2' : 117,
    'BB2' : 123,
    'B2' : 123,
    'C3' : 131, 'CS3' : 139,
    'D3' : 147, 'DS3' : 156,
    'EB3' : 156,
    'E3' : 165,
    'F3' : 175, 'FS3' : 185,
    'G3' : 196, 'GS3' : 208,
    'A3' : 220, 'AS3' : 233,
    'BB3' : 233,
    'B3' : 247,
    'C4' : 262, 'CS4' : 277,
    'D4' : 294, 'DS4' : 311,
    'EB4' : 311,
    'E4' : 330,
    'F4' : 349, 'FS4' : 370,
    'G4' : 392, 'GS4' : 415,
    'A4' : 440, 'AS4' : 466,
    'BB4' : 466,
    'B4' : 494,
    'C5' : 523, 'CS5' : 554,
    'D5' : 587, 'DS5' : 622,
    'EB5' : 622,
    'E5' : 659,
    'F5' : 698, 'FS5' : 740,
    'G5' : 784, 'GS5' : 831,
    'A5' : 880, 'AS5' : 932,
    'BB5' : 932,
    'B5' : 988,
    'C6' : 1047, 'CS6' : 1109,
    'D6' : 1175, 'DS6' : 1245,
    'EB6' : 1245,
    'E6' : 1319,
    'F6' : 1397, 'FS6' : 1480,
    'G6' : 1568, 'GS6' : 1661,
    'A6' : 1760, 'AS6' : 1865,
    'BB6' : 1865,
    'B6' : 1976,
    'C7' : 2093, 'CS7' : 2217,
    'D7' : 2349, 'DS7' : 2489,
    'EB7' : 2489,
    'E7' : 2637,
    'F7' : 2794, 'FS7' : 2960,
    'G7' : 3136, 'GS7' : 3322,
    'A7' : 3520, 'AS7' : 3729,
    'BB7' : 3729,
    'B7' : 3951,
    'C8' : 4186, 'CS8' : 4435,
    'D8' : 4699, 'DS8' : 4978,
}

melody = [
    notes['E7'], notes['E7']
]
tempo = [
    12, 12, 12, 12,
]
twinkle_twinkle_melody = [
    notes['G4'], notes['G4'],
]

twinkle_twinkle_tempo = [
    2, 2,
]

def buzz(frequency, length):	 #create the function "buzz" and feed it the pitch and duration)

	if(frequency==0):
		time.sleep(length)
		return
	period = 1.0 / frequency 		 #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
	delayValue = period / 2		 #calcuate the time for half of the wave
	numCycles = int(length * frequency)	 #the number of waves to produce is the duration times the frequency
	
	for i in range(numCycles):		#start a loop from 0 to the variable "cycles" calculated above
		GPIO.output(buzzer_pin, True)	 #set pin 27 to high
		time.sleep(delayValue)		#wait with pin 27 high
		GPIO.output(buzzer_pin, False)		#set pin 27 to low
		time.sleep(delayValue)		#wait with pin 27 low

def play(melody,tempo,pause,pace=0.800):
    for i in range(0, len(melody)):
        noteDuration = pace/tempo[i]
        buzz(melody[i],noteDuration)

        pauseBetweenNotes = noteDuration * pause
        time.sleep(pauseBetweenNotes)

run = True
rdr = RFID()
util = rdr.util()
util.debug = True

def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    GPIO.cleanup()
    sys.exit()

signal.signal(signal.SIGINT, end_read)

eskiKart = "54564"
yeniKart = "5456465"

print("Starting")
while run:
    rdr.wait_for_tag()
    
    (error, data) = rdr.request()
    (error, uid) = rdr.anticoll()
    if not error:
        #print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
        yeniKart = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
        time.sleep(0.2)

        if (yeniKart != eskiKart):
            print("Yeni Kart")
            print(yeniKart)
            eskiKart = yeniKart
            play(melody, tempo, 1.3, 0.800)
            conn = sqlite3.connect('cardData.db')
            c = conn.cursor()
            # Create table
            #c.execute('''CREATE TABLE cards
            #             (card text, uuid int)''')
            # Insert a row of data
            #c.execute("INSERT INTO cards VALUES ('rfid', %s);" % yeniKart)
            c.execute("UPDATE cards SET uuid = %s WHERE card = 'rfid';" % yeniKart)
            # Save (commit) the changes
            conn.commit()
            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.
            conn.close()
        else:
            play(twinkle_twinkle_melody, twinkle_twinkle_tempo, 0.30, 0.900)


