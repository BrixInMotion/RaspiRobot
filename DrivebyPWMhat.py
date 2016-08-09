#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import sys, termios, atexit
import RPi.GPIO as GPIO
import smbus
from kbhit import *
from Portexpander import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Variablen Kamera-servos
servoMin_h = 300
servoMin_s = 320
servoMax_h = 500
servoMax_s = 550
mitte_h = 410
mitte_s = 425

speed = 10
umdrehungen = 75

# Initialise the PWM device using the default address
#pwm = PWM(0x40, debug=True)
# Addr 0x40 for Adafuit board, 0x55 for XMC board
pwm = PWM(0x40, debug=True)
# Note if you'd like more debug output you can instead run:

FrequenzMotor = 300
FrequenzServo = 60
servoMin = 0        # 0 for wheels, 350 for servos
servoMax = 700      #700 for wheels, 500 for servos
lastPWM = 300
#------------------------Pin-Assigment-------------------------------
# H-Bridge left Motor:
#       IN 1:   CH 1    (backward)
#       IN 2:   CH 0    (forward)
#
# H-Bridge right Motor:
#       IN 1:   CH 3    (forward)
#       IN 2:   CH 2    (backward)
#
# H-Bridge elevator:
#       IN 1:   CH 13    (up)
#       IN 2:   CH 12    (down)
#
#Inhibits to High
#
#Servo tilt:    CH 8
#Servo pan:     CH 9

pwm.setPWMFreq(300)                        # 1000 Hz for wheels, 60 for servos
#--------------------------------------------------------------------
def Set_PWW_Frequency(frequenz):
    global lastPWM
    if lastPWM != frequenz:
        pwm.setPWMFreq(frequenz)
        lastPWM = frequenz
#-----------------------------Tastaturabfrage--------------------------------
atexit.register(set_normal_term)
set_curses_term()
setup()                                     #Setup Portexpanderpins
try:
  while (True):
      if kbhit():
        Richtung = getch()
        #print "i2c Adresse: %02x" % (pwm.i2c.address)
        if Richtung=="w": #vorwaerts
          Set_PWW_Frequency(FrequenzMotor)
          pwm.setPWM(1, 0, servoMin)
          pwm.setPWM(0, 0, servoMax)
          pwm.setPWM(2, 0, servoMin)
          pwm.setPWM(3, 0, servoMax)
        elif Richtung=="r": #VW Beschleunigen
            Set_PWW_Frequency(FrequenzMotor)
            pwm.setPWM(1, 0, servoMin),
            pwm.setPWM(2, 0, servoMin)
            for i in range(500, servoMax):
                pwm.setPWM(0, 0, i),
                pwm.setPWM(3, 0, i)
                time.sleep(0.005)
        elif Richtung=="s": #Stopp
            Set_PWW_Frequency(FrequenzMotor)
            pwm.setPWM(0, 0, servoMin), 
            pwm.setPWM(1, 0, servoMin),
            pwm.setPWM(2, 0, servoMin),
            pwm.setPWM(3, 0, servoMin)
        elif Richtung=="x": #Rueckwaerts
            Set_PWW_Frequency(FrequenzMotor)
            pwm.setPWM(0, 0, servoMin),
            pwm.setPWM(1, 0, servoMax),
            pwm.setPWM(2, 0, servoMax),
            pwm.setPWM(3, 0, servoMin)
        elif Richtung=="a": #links
            Set_PWW_Frequency(FrequenzMotor)
            pwm.setPWM(0, 0, servoMin),
            pwm.setPWM(1, 0, servoMin),
            pwm.setPWM(2, 0, servoMin),
            pwm.setPWM(3, 0, servoMax)
        elif Richtung=="d": #rechts
            Set_PWW_Frequency(FrequenzMotor)
            pwm.setPWM(0, 0, servoMax),
            pwm.setPWM(1, 0, servoMin),
            pwm.setPWM(2, 0, servoMin),
            pwm.setPWM(3, 0, servoMin)
        elif Richtung=="q": #eher links
            Set_PWW_Frequency(FrequenzMotor)
            pwm.setPWM(0, 0, (servoMax-250)),
            pwm.setPWM(1, 0, servoMin),
            pwm.setPWM(2, 0, servoMin),
            pwm.setPWM(3, 0, servoMax)
        elif Richtung=="e": #eher rechts
            Set_PWW_Frequency(FrequenzMotor)
            pwm.setPWM(0, 0, servoMax),
            pwm.setPWM(1, 0, servoMin),
            pwm.setPWM(2, 0, servoMin),
            pwm.setPWM(3, 0, (servoMax-450))
        elif Richtung=="u": #Plattform rauf
            Set_PWW_Frequency(FrequenzMotor)
            pwm.setPWM(13, 0, 2750)
            pwm.setPWM(12, 0, servoMin)
        elif Richtung=="m": #Plattform runter
            Set_PWW_Frequency(FrequenzMotor)
            pwm.setPWM(13, 0, servoMin)
            pwm.setPWM(12, 0, 2000)
        elif Richtung=="j": #Platform halt
            Set_PWW_Frequency(FrequenzMotor)
            pwm.setPWM(12, 0, servoMin),
            pwm.setPWM(13, 0, servoMin)
        elif Richtung=="c": servoMax = 700
        elif Richtung=="v": servoMax = 1000
        elif Richtung=="b": servoMax = 1500
        elif Richtung=="n": servoMax = 2000
        elif Richtung=="t": #drehen um eigene Achse
            Set_PWW_Frequency(FrequenzMotor)
            pwm.setPWM(0, 0, servoMin)
            pwm.setPWM(1, 0, 500)
            pwm.setPWM(2, 0, servoMin)
            pwm.setPWM(3, 0, 550)
        elif Richtung=="l": #Licht an
            sendSPI(SPI_SLAVE_ADDR, SPI_GPIOA, 0b10000000)
        elif Richtung=="o": #Licht aus
            sendSPI(SPI_SLAVE_ADDR, SPI_GPIOA, 0b00000000)
        elif Richtung=="h": #Relais aus
            sendSPI(SPI_SLAVE_ADDR, SPI_GPIOA, 0b00000001)
            time.sleep(0.5)
            sendSPI(SPI_SLAVE_ADDR, SPI_GPIOA, 0b00000000)
        elif Richtung=="g": #Relais an
            sendSPI(SPI_SLAVE_ADDR, SPI_GPIOA, 0b00000010)
            time.sleep(0.5)
            sendSPI(SPI_SLAVE_ADDR, SPI_GPIOA, 0b00000000)
        elif Richtung == "1":                   #Kamera schwenken
            Set_PWW_Frequency(FrequenzServo)
            pwm.setPWM(8, 0, servoMin_h)
            pwm.setPWM(9, 0, servoMin_s)
        elif Richtung == "2":
            Set_PWW_Frequency(FrequenzServo)
            pwm.setPWM(8, 0, servoMin_h)
            pwm.setPWM(9, 0, mitte_s)
        elif Richtung == "3":
            Set_PWW_Frequency(FrequenzServo)
            pwm.setPWM(8, 0, servoMin_h)
            pwm.setPWM(9, 0, servoMax_s)
        elif Richtung == "4":
            Set_PWW_Frequency(FrequenzServo)
            pwm.setPWM(8, 0, mitte_h)
            pwm.setPWM(9, 0, servoMin_s)
        elif Richtung == "5":
            Set_PWW_Frequency(FrequenzServo)
            pwm.setPWM(8, 0, mitte_h)
            pwm.setPWM(9, 0, mitte_s)
        elif Richtung == "6":
            Set_PWW_Frequency(FrequenzServo)
            pwm.setPWM(8, 0, mitte_h)
            pwm.setPWM(9, 0, servoMax_s)
        elif Richtung == "7":
            Set_PWW_Frequency(FrequenzServo)
            pwm.setPWM(8, 0, servoMax_h)
            pwm.setPWM(9, 0, servoMin_s)
        elif Richtung == "8":
            Set_PWW_Frequency(FrequenzServo)
            pwm.setPWM(8, 0, servoMax_h)
            pwm.setPWM(9, 0, mitte_s)
        elif Richtung == "9":
            Set_PWW_Frequency(FrequenzServo)
            pwm.setPWM(8, 0, servoMax_h)
            pwm.setPWM(9, 0, servoMax_s)

except KeyboardInterrupt:   #Grundstellung bei Abbruch durch STRG + C
  pwm.setPWM(0, 0, servoMin),
  pwm.setPWM(1, 0, servoMin),
  pwm.setPWM(2, 0, servoMin),
  pwm.setPWM(3, 0, servoMin),
  pwm.setPWM(12, 0, servoMin),
  pwm.setPWM(13, 0, servoMin)
  GPIO.cleanup()
