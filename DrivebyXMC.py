# -*- coding: utf-8 -*-

from Adafruit_PWM_Servo_Driver import PWM
import time
import sys, termios, atexit
import smbus
import RPi.GPIO as GPIO
from kbhit import *
from Portexpander import *

GPIO.setmode(GPIO.BCM)  #GPIO-Nummerierung
GPIO.setwarnings(False) #Fehlermeldungen unterdruecken
#---------------------------------Variables----------------------------
#Variables Kamera-servos
servoMin_h = 270    #ch8: hoehe, servoMin: unten
servoMin_s = 320    #ch9: seite, servoMin: links
servoMax_h = 500
servoMax_s = 550
mitte_h = 410
mitte_s = 425
h = mitte_h
s = mitte_s
temp_h = mitte_h
temp_s = mitte_s
schrittweite = 15
speed = 10

FrequenzMotor = 300 #300 Hz
FrequenzServo = 60  #60 Hz
servoMin = 0        # 0 for wheels, 350 for servos
servoMax = 700      #700 for wheels, 500 for servos
lastPWM = 300
lastAddr = 0x40

# Registers of XMC:
SpeedLeftMotor = 0x01
SpeedRightMotor = 0x02
SpeedElevator = 0x03
WaitStep = 0x04
SpeedStepPlus = 0x05
SpeedStepMinus = 0x06

# Addr 0x40 for Adafuit board, 0x55 for XMC board<-<-<-<-<-<-<-<-<-<-<-<-<-<-I2C-Addresses
pwm = PWM(0x40, debug=True)
pwm.setPWMFreq(60)                        # 1000 Hz for wheels, 60 for servos
bus = smbus.SMBus(1)
address_xmc = 0x55
setup()

#bus.write_byte_data(address_xmc,register,value)
#--------------------------------------------------------------------
def Set_PWW_Frequency(frequenz):
    global lastPWM
    if lastPWM != frequenz:
        pwm.setPWMFreq(frequenz)
        lastPWM = frequenz
#--------------------------------------------------------------------
def Set_I2C_Address(ADAaddress):
    global lastAddr
    if lastAddr != ADAaddress:
        pwm = PWM(ADAaddress, debug=True)
        lastAddr = ADAaddress
        print ("I2C Addresse: ", ADAaddress)
#--------------------------------------------------------------------
atexit.register(set_normal_term)
set_curses_term()
try:
  while (True):
      if kbhit():
        Richtung = getch()
        #print "i2c Adresse: %02x" % (pwm.i2c.address)  
        bus.write_byte_data(address_xmc,WaitStep, 0xa0)
        bus.write_byte_data(address_xmc,SpeedStepPlus, 0x02)
        bus.write_byte_data(address_xmc,SpeedStepMinus, 0x04)
        if Richtung=="w": #vorwaerts (MSD 0: 0x01..0x7F)
            bus.write_byte_data(address_xmc,SpeedLeftMotor, 0x28)
            bus.write_byte_data(address_xmc,SpeedRightMotor,0x28)
        elif Richtung=="s": #Stopp
            bus.write_byte_data(address_xmc,SpeedLeftMotor,0)
            bus.write_byte_data(address_xmc,SpeedRightMotor,0)
        elif Richtung=="x": #Rueckwaerts (MSD gesetzt: 0x81..0xFF) 
            bus.write_byte_data(address_xmc,SpeedLeftMotor, 0xa8)
            bus.write_byte_data(address_xmc,SpeedRightMotor,0xa8)
        elif Richtung=="a": #links drehen
            bus.write_byte_data(address_xmc,SpeedLeftMotor, (0x80 + 0x20))
            bus.write_byte_data(address_xmc,SpeedRightMotor,0x20)
        elif Richtung=="d": #rechts drehen
            bus.write_byte_data(address_xmc,SpeedLeftMotor, 0x20)
            bus.write_byte_data(address_xmc,SpeedRightMotor,(0x80 + 0x20))
        elif Richtung=="q": #links vorwärts
            bus.write_byte_data(address_xmc,SpeedLeftMotor, 0x18)
            bus.write_byte_data(address_xmc,SpeedRightMotor,0x28)
        elif Richtung=="e": #rechts vorwärts
            bus.write_byte_data(address_xmc,SpeedLeftMotor, 0x28)
            bus.write_byte_data(address_xmc,SpeedRightMotor,0x18)
        elif Richtung=="y": #links rückwärts
            bus.write_byte_data(address_xmc,SpeedLeftMotor, (0x80 + 0x18))
            bus.write_byte_data(address_xmc,SpeedRightMotor,(0x80 + 0x28))
        elif Richtung=="c": #rechts rückwärts
            bus.write_byte_data(address_xmc,SpeedLeftMotor, (0x80 + 0x28))
            bus.write_byte_data(address_xmc,SpeedRightMotor,(0x80 + 0x18))        
        elif Richtung=="u": #Plattform rauf
            bus.write_byte_data(address_xmc,SpeedElevator, 0x40)
        elif Richtung=="m": #Plattform runter
            bus.write_byte_data(address_xmc,SpeedElevator, (0x80 + 0x40))
        elif Richtung=="j": #Platform halt
            bus.write_byte_data(address_xmc,SpeedElevator, 0x00)
        #elif Richtung=="c": servoMax = 700
        #elif Richtung=="v": servoMax = 1000
        #elif Richtung=="b": servoMax = 1500
        #elif Richtung=="n": servoMax = 2000
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
        elif Richtung == "1":
            pwm.setPWM(8, 0, servoMin_h)
            pwm.setPWM(9, 0, servoMin_s)
            temp_h = servoMin_h
            temp_s = servoMin_s
        elif Richtung == "2":
            if temp_h > (servoMin_h+schrittweite-1):
              pwm.setPWM(8, 0, (temp_h-schrittweite))
              temp_h -= schrittweite
              #pwm.setPWM(8, 0, servoMin_h)
              #pwm.setPWM(9, 0, mitte_s)
        elif Richtung == "3":
            pwm.setPWM(8, 0, servoMin_h)
            pwm.setPWM(9, 0, servoMax_s)
            temp_h = servoMin_h
            temp_s = servoMax_s
        elif Richtung == "4":
            if temp_s > (servoMin_h+schrittweite-1):
              pwm.setPWM(9, 0, (temp_s-schrittweite))
              temp_s -= schrittweite
                #pwm.setPWM(8, 0, mitte_h)
                #pwm.setPWM(9, 0, servoMin_s)
        elif Richtung == "5":
            pwm.setPWM(8, 0, mitte_h)
            pwm.setPWM(9, 0, mitte_s)
            temp_h = mitte_h
            temp_s = mitte_s
        elif Richtung == "6":
            if temp_s < (servoMax_h-schrittweite-1):
              pwm.setPWM(9, 0, (temp_s+schrittweite))
              temp_s += schrittweite
            #pwm.setPWM(8, 0, mitte_h)
            #pwm.setPWM(9, 0, servoMax_s)
        elif Richtung == "7":
            pwm.setPWM(8, 0, servoMax_h)
            pwm.setPWM(9, 0, servoMin_s)
            temp_h = servoMax_h
            temp_s = servoMin_s
        elif Richtung == "8":
            if temp_h < (servoMax_h-schrittweite-1):
              pwm.setPWM(8, 0, (temp_h+schrittweite))
              temp_h += schrittweite
            #pwm.setPWM(8, 0, servoMax_h)
            #pwm.setPWM(9, 0, mitte_s)
        elif Richtung == "9":
            pwm.setPWM(8, 0, servoMax_h)
            pwm.setPWM(9, 0, servoMax_s)
            temp_h = servoMax_h
            temp_s = servoMax_s

except KeyboardInterrupt:
    #Set_I2C_Address(0x55)
    #pwm.setPWM(0, 0, servoMin),
    #pwm.setPWM(1, 0, servoMin),
    #pwm.setPWM(2, 0, servoMin),
    #pwm.setPWM(3, 0, servoMin),
    Set_I2C_Address(0x40)
    pwm.setPWM(12, 0, servoMin),
    pwm.setPWM(13, 0, servoMin)
    GPIO.cleanup()

#raw_input("Richtung: ")
