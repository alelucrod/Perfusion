import RPi.GPIO as GPIO
import time
  
GPIO.setmode(GPIO.BCM)

sensor =  17
GPIO.setup(sensor, GPIO.IN, pull_up_down = GPIO.PUD_UP)
  
  
#Function executed on signal detection
def active(null):
        print("Deteccion")

#Function executed on signal detection
def active2(null):
        print("saliendo")

#On detecting signal (falling edge), active function will be activated.
GPIO.add_event_detect(sensor, GPIO.FALLING, callback=active, bouncetime=100) 
#GPIO.add_event_detect(sensor, GPIO.RISING, callback=active2, bouncetime=100)
# main program loop
try:
        while True:
                time.sleep(1)
  
# Scavenging work after the end of the program
except KeyboardInterrupt:
        GPIO.cleanup()
