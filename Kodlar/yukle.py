#!/usr/bin/env python
# -*- coding: utf8 -*-

#
# Bu bir akbil bakiye yükleme kodlarıdır.
# Burada LCD kullanılmamıştır.
#

import RPi.GPIO as GPIO
import MFRC522
import signal
import time 

GPIO.setmode(GPIO.BOARD)

oku = True

def end_read(signal,frame):
    global continue_reading
    print "Akbil sonlandırıldı"
    oku = False
    GPIO.cleanup()
    exit()


signal.signal(signal.SIGINT, end_read)

#NFC Sınıfı oluşturulması
MIFAREReader = MFRC522.MFRC522()

print "OEOI Bakiye Yükleme"
bakiye = int(raw_input("Yüklemek istediğiniz bakiye miktarı giriniz: ")) ##Yükleme istenilen bakiye miktarı
print "Bakiye yüklemek istediğiniz kartı koyun"
 
while oku:
   (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
   
   if status == MIFAREReader.MI_OK: 
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
 
    if status == MIFAREReader.MI_OK:
         
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
         
        MIFAREReader.MFRC522_SelectTag(uid)

       
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
        print "\n"
   
        if status == MIFAREReader.MI_OK:
 
            data = []
 
            for x in range(0,16):
                data.append(0x00)

            
            data[0] = bakiye ## Yeni bakiye alınır
            print "Bakiye yüklemesi tamamlandı" 
            MIFAREReader.MFRC522_Write(8, data)## Yeni bakiye karta yazılır
            print "\n"  
			
            MIFAREReader.MFRC522_StopCrypto1()
 
            oku = False
        else:
            print "Kart geçersizdir.!!"
