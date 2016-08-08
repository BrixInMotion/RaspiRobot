#!/usr/bin/python

import time
import RPi.GPIO as GPIO

class SPI:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    SPI_SLAVE_ADDR = 0x40
    SPI_IOCTRL     = 0x0A
    SPI_IODIRA     = 0x00
    SPI_IODIRB     = 0x01
    SPI_GPIOA      = 0x12
    SPI_GPIOB      = 0x13

    #MCP23S17-Pins
    SCLK    = 11
    MOSI    = 10
    MISO    = 9
    CS      = 22
    #----------------------------------------------------------
	def setup():
		#GPIO Initialisierung
		GPIO.setup(SCLK, GPIO.OUT)
		GPIO.setup(MOSI, GPIO.OUT)
		GPIO.setup(MISO, GPIO.IN)
		GPIO.setup(CS, GPIO.OUT)

		GPIO.output(CS, GPIO.HIGH)
		GPIO.output(SCLK, GPIO.LOW)
		
		sendSPI(SPI_SLAVE_ADDR, SPI_IODIRA, 0x00)   #A als Ausgaenge
		sendSPI(SPI_SLAVE_ADDR, SPI_IODIRB, 0xFF)   #B als Eingaenge
		sendSPI(SPI_SLAVE_ADDR, SPI_GPIOA, 0x00)
	#----------------------------------------------------------
    def sendValue(value):
        for i in range(8):
            if (value & 0x80):
                GPIO.output(MOSI, GPIO.HIGH)
            else:
                GPIO.output(MOSI, GPIO.LOW)
            GPIO.output(SCLK, GPIO.HIGH)
            GPIO.output(SCLK, GPIO.LOW)
            value <<= 1
    #----------------------------------------------------------
    def sendSPI(opcode, addr, data):
        GPIO.output(CS, GPIO.LOW)
        sendValue(opcode)
        sendValue(addr)
        sendValue(data)
        GPIO.output(CS, GPIO.HIGH)
    #----------------------------------------------------------
    def readSPI(opcode, addr):
        GPIO.output(CS, GPIO.LOW)
        sendValue(opcode|SPI_SLAVE_ADDR)
        sendValue(addr)
        value = 0
        for i in range(8):
            value <<= 1
            if(GPIO.input(MISO)):
                value |= 0x01
            GPIO.output(SCLK, GPIO.HIGH)
            GPIO.output(SCLK, GPIO.LOW)
        GPIO.output(CS, GPIO.HIGH)
        return value
    #----------------------------------------------------------
