#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
from LCD import Adafruit_CharLCD

GPIO.setmode(GPIO.BOARD) # Board modunda kullanma

lcd = Adafruit_CharLCD() # LCD Ekran sınıfı 

oku= True
kimlik = -1
key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
lcd.begin(16,2)

## GPIO
GPIO.setup(40, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
 
## Ctrl + C yapılması durumunda
def end_read(signal,frame):
    global continue_reading
    print "Akbil sonlandırıldı"
    oku = False
    GPIO.cleanup()
    exit()

#Akbil basıldığında	
def akbil_bas():
     
    for x in range(0,3):
      GPIO.output(40, GPIO.HIGH)
      time.sleep(0.1)
      GPIO.output(40, GPIO.LOW)
    
    
#  Ctrl + C fonksiyonun aktif edilmesi
signal.signal(signal.SIGINT, end_read)

# NFC Sınıfı oluşturulması
MIFAREReader = MFRC522.MFRC522()


lcd.message("OEOI Otobus\nAkbil basiniz") # lcd.message -> LCD Ekrana yazı yazdırır. \n ikinci satıra geçirir

while True: 
     (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)##Okunan kartları bakar. Kart okunması durumunda status MI_OK sonucu verir
     if status == MIFAREReader.MI_OK:
            
       (status,uid) = MIFAREReader.MFRC522_Anticoll()
       lcd.clear()#LCD Ekran temizleme
	   
	   ##Kart okumaya başladığında LED'lerin yanması
       GPIO.output(36, GPIO.HIGH)
       time.sleep(0.5)
       GPIO.output(35, GPIO.HIGH)
	   ##!!
	   
       MIFAREReader.MFRC522_SelectTag(uid)
       status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
       bilgi = MIFAREReader.MFRC522_Read(8)
       time.sleep(0.5)
  
       if not uid:##Okunan kart geçersiz veya sahte ise
         
         GPIO.output(40, GPIO.HIGH)
         lcd.message("GECERSIZ KART") 
         time.sleep(2)
         GPIO.output(40, GPIO.LOW)
        
       else:
         if kimlik != uid[0]:#Önceki okunan kart aynı değil ise
           if bilgi[0] > 0:#Bakiye var ise
             bilgi[0] = bilgi[0]-1##Bakiye düşürülür
             akbil_bas()
             lcd.message("IYI YOLCULUKLAR\nKALAN BAKIYE: "+str(bilgi[0]))
              
             MIFAREReader.MFRC522_Write(8, bilgi)##Yeni bakiye yazılır
             kimlik = uid[0]
           else:#Kartta bakiye yok ise
             lcd.message("YETERSIZ BAKIYE\nBAKIYE YUKLEYIN")
			 ##3 saniye aralıksız ses
             GPIO.output(40, GPIO.HIGH)
             time.sleep(3)
             GPIO.output(40, GPIO.LOW)
             ##!!
			 
       time.sleep(3)
       lcd.clear()
       MIFAREReader.MFRC522_StopCrypto1()##Sonraki kart okumaya hazırlama
       GPIO.output(36, GPIO.LOW)
       GPIO.output(35, GPIO.LOW)
       time.sleep(2)
       lcd.message("OEOI Otobus\nAkbil basiniz")
       

