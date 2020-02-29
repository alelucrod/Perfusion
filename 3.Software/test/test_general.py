#!/usr/bin/env python3
import RPi.GPIO as GPIO
# Global Imports
import logging          #para los termopares
import time             #para el tiempo
import Adafruit_GPIO    #para los termopares
import board            #para los MCP4725
import busio            #para los MCP4725   
import adafruit_mcp4725  #para los MCP4725

# Local Imports
from Adafruit_MAX31856 import MAX31856 as MAX31856  #para los termopares

########Para los termopares##################### solo cambiar la configuracion
###solo cambiar la configuracion "cs" en el caso de que se quieran utilizar otros pines
logging.basicConfig(
    filename='simpletest.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_logger = logging.getLogger(__name__)

# Uncomment one of the blocks of code below to configure your Pi to use software or hardware SPI.

## Raspberry Pi software SPI configuration.
software_spi_1 = {"clk": 11, "cs": 7, "do": 9, "di": 10}
sensor_1 = MAX31856(software_spi=software_spi_1, tc_type=MAX31856.MAX31856_K_TYPE)

software_spi_2 = {"clk": 11, "cs": 8, "do": 9, "di": 10}
sensor_2 = MAX31856(software_spi=software_spi_2, tc_type=MAX31856.MAX31856_K_TYPE)

software_spi_3 = {"clk": 11, "cs": 12, "do": 9, "di": 10}
sensor_3 = MAX31856(software_spi=software_spi_3, tc_type=MAX31856.MAX31856_K_TYPE)

# Raspberry Pi hardware SPI configuration.
#SPI_PORT   = 0
#SPI_DEVICE = 0
#sensor = MAX31856(hardware_spi=Adafruit_GPIO.SPI.SpiDev(SPI_PORT, SPI_DEVICE), tc_type=MAX31856.MAX31856_K_TYPE)

##############################################




############Para los MCP4725###########################
# Initialize I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize MCP4725_a.
dac_a = adafruit_mcp4725.MCP4725(i2c, address=0x60)
# Optionally you can specify a different addres if you override the A0 pin.
#amp = adafruit_max9744.MAX9744(i2c, address=0x60)

# There are a three ways to set the DAC output, you can use any of these:
dac_a.value = 65500  # Use the value property with a 16-bit number just like
                   # the AnalogOut class.  Note the MCP4725 is only a 12-bit
                   # DAC so quantization errors will occur.  The range of
                   # values is 0 (minimum/ground) to 65535 (maximum/Vout).

dac_a.raw_value = 4095  # Use the raw_value property to directly read and write
                      # the 12-bit DAC value.  The range of values is
                      # 0 (minimum/ground) to 4095 (maximum/Vout).

dac_a.normalized_value = 1.0  # Use the normalized_value property to set the
                            # output with a floating point value in the range
                            # 0 to 1.0 where 0 is minimum/ground and 1.0 is
                            # maximum/Vout.


# Initialize MCP4725_b.
dac_b = adafruit_mcp4725.MCP4725(i2c, address=0x61)
# Optionally you can specify a different addres if you override the A0 pin.
#amp = adafruit_max9744.MAX9744(i2c, address=0x60)

# There are a three ways to set the DAC output, you can use any of these:
dac_b.value = 65500  # Use the value property with a 16-bit number just like
                   # the AnalogOut class.  Note the MCP4725 is only a 12-bit
                   # DAC so quantization errors will occur.  The range of
                   # values is 0 (minimum/ground) to 65535 (maximum/Vout).

dac_b.raw_value = 4095  # Use the raw_value property to directly read and write
                      # the 12-bit DAC value.  The range of values is
                      # 0 (minimum/ground) to 4095 (maximum/Vout).

dac_b.normalized_value = 1.0  # Use the normalized_value property to set the
                            # output with a floating point value in the range
                            # 0 to 1.0 where 0 is minimum/ground and 1.0 is
                            # maximum/Vout.


#######################################################




## Establecemos el sistema de numeracion que queramos, en mi caso BCM
GPIO.setmode(GPIO.BCM)

## Definimos pines a usar
RelayPin_1 = 27
RelayPin_2 = 22

led_pins = [5,6,13]

## Configurar GPIOS como salidas
GPIO.setup(RelayPin_1, GPIO.OUT)
GPIO.setup(RelayPin_2, GPIO.OUT)


for x in led_pins:
    GPIO.setup(x, GPIO.OUT)
    GPIO.output(x, GPIO.LOW)


#####################################################################
####  DEFINICION DE CLASES COMO OBJETOS                    #########
####################################################################
class Buzzer(object):
 def __init__(self):
  GPIO.setmode(GPIO.BCM)
  self.buzzer_pin = 18 #set to GPIO pin 18
  GPIO.setup(self.buzzer_pin, GPIO.IN)
  GPIO.setup(self.buzzer_pin, GPIO.OUT)
  print("buzzer ready")

 def __del__(self):
  class_name = self.__class__.__name__
  print (class_name, "finished")

 def buzz(self,pitch, duration):   #create the function “buzz” and feed it the pitch and duration)

  if(pitch==0):
   time.sleep(duration)
   return
  period = 1.0 / pitch     #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
  delay = period / 2     #calcuate the time for half of the wave
  cycles = int(duration * pitch)   #the number of waves to produce is the duration times the frequency

  for i in range(cycles):    #start a loop from 0 to the variable “cycles” calculated above
   GPIO.output(self.buzzer_pin, True)   #set pin 18 to high
   time.sleep(delay)    #wait with pin 18 high
   GPIO.output(self.buzzer_pin, False)    #set pin 18 to low
   time.sleep(delay)    #wait with pin 18 low

 def play(self, tune):
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(self.buzzer_pin, GPIO.OUT)
  x=0

  print("Playing tune ",tune)
  if(tune==1):
    pitches=[262,294,330,349,392,440,494,523, 587, 659,698,784,880,988,1047]
    duration=0.1
    for p in pitches:
      self.buzz(p, duration)  #feed the pitch and duration to the function, “buzz”
      time.sleep(duration *0.5)
    for p in reversed(pitches):
      self.buzz(p, duration)
      time.sleep(duration *0.5)

  elif(tune==2):
    pitches=[262,330,392,523,1047]
    duration=[0.2,0.2,0.2,0.2,0.2,0,5]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the function, “buzz”
      time.sleep(duration[x] *0.5)
      x+=1
  elif(tune==3):
    pitches=[392,294,0,392,294,0,392,0,392,392,392,0,1047,262]
    duration=[0.2,0.2,0.2,0.2,0.2,0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.8,0.4]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the func$
      time.sleep(duration[x] *0.5)
      x+=1

  elif(tune==4):
    pitches=[1047, 988,659]
    duration=[0.1,0.1,0.2]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the func$
      time.sleep(duration[x] *0.5)
      x+=1

  elif(tune==5):
    pitches=[1047, 988,523]
    duration=[0.1,0.1,0.2]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the func$
      time.sleep(duration[x] *0.5)
      x+=1

  GPIO.setup(self.buzzer_pin, GPIO.IN)


######################################################
###############    INICIO DEL PROGRAMA        #######
#####################################################

if __name__ == "__main__":

 try:

   #Reproducirá infinatemente el test de los dispositivos
   while True:

        #####################################################
        #Testeando relés (USa logica inversa)
        #por lo que cuando el voltaje que se manda es 0
        #el modulo se activa y si se mandan 5v se desactiva
        ######################################################
        print ("Encendiendo Rele 1...")
        GPIO.output(RelayPin_1, False) ## Enciendo el RelayPin_1
        time.sleep(3) ## Esperamos 3 segundos
        print ("Apagando Rele 1...")
        GPIO.output(RelayPin_1, True) ## Apago el RelayPin_1

        time.sleep(2) ## Esperamos 2 segundos

        print ("Encendiendo Rele 2...")
        GPIO.output(RelayPin_2, False) ## Enciendo el RelayPin_2
        time.sleep(3) ## Esperamos 3 segundos
        print ("Apagando Rele 2...")
        GPIO.output(RelayPin_2, True) ## Apago el RelayPin_2

        #Esperamos 2 segundos y pasamos al siguiente test
        time.sleep(2) ## Esperamos 2 segundos


        #####################################################
        #Testeando LEDS
        ######################################################
        # Turn on this GPIO then off
        for x in led_pins:
            print ("Encendiendo led del pin %s" % (str(x)) )
            GPIO.output(x, GPIO.HIGH)
            time.sleep(1)
            print ("Apagando led del pin %s" % (str(x)) )
            GPIO.output(x, GPIO.LOW)
            time.sleep(1)

        #Esperamos 2 segundos y pasamso al siguiente test
        # No LED GPIOS now (Estamos fuera del bucle)
        time.sleep(2) ## Esperamos 2 segundos



        ####################################################
        # Test dle buzzer
        ######################################################
        #Inicializamos el objeto de la clase Buzzer()
        buzzer = Buzzer()
        #Llamasmo a la funcion PLay de la clase Buzzer diciendole
        #que queremso reproducir la melodia 3 de las 5 que nos deja
        print ("Reproduciendo melodia")
        buzzer.play(3)
        print ("Melodia finalizada")


        #Esperamos 2 segundos y pasamso al siguiente test
        # No LED GPIOS now (Estamos fuera del bucle)
        time.sleep(2) ## Esperamos 2 segundos



        ####################################################
        # Test de los termopares
        ######################################################
        # lectura de cada termopar 4 veces cada segundo. Se utilizan 4 bucles for
        for i in range(4):
            temp = sensor_1.read_temp_c()
            internal = sensor_1.read_internal_temp_c()
            print('Thermocouple Temperature_1: {0:0.3F}*C'.format(temp))
            print('    Internal Temperature_1: {0:0.3F}*C'.format(internal))
            print ("\n") #New line spacing
            time.sleep(1.0) #Sleep the main thread 1 s

        for j in range(4):
            temp = sensor_2.read_temp_c()
            internal = sensor_2.read_internal_temp_c()
            print('Thermocouple Temperature_2: {0:0.3F}*C'.format(temp))
            print('    Internal Temperature_2: {0:0.3F}*C'.format(internal))
            print ("\n") #New line spacing
            time.sleep(1.0) #Sleep the main thread 1 s

        for k in range(4):
            temp = sensor_3.read_temp_c()
            internal = sensor_3.read_internal_temp_c()
            print('Thermocouple Temperature_3: {0:0.3F}*C'.format(temp))
            print('    Internal Temperature_3: {0:0.3F}*C'.format(internal))
            print ("\n") #New line spacing
            time.sleep(1.0) #Sleep the main thread 1 s

        ####################################################
        # Test de los MCP4725. Conectar las bombas a las bornas de la placa
        ######################################################


        #MPP4725_a
        # Go up the 12-bit raw range.
        print(' MCP4725_a Going up 0-3.3V...')
        for i in range(4095):
            dac_a.raw_value = i
        time.sleep(2.0) #Sleep the main thread 2 s
        # Go back down the 12-bit raw range.
        print(' MCP4725_a Going down 3.3-0V...')
        for i in range(4095, -1, -1):
            dac_a.raw_value = i
        time.sleep(3.0) #Sleep the main thread 3 s


        #MCP4725_b
        # Go up the 12-bit raw range.
        print(' MCP4725_b Going up 0-3.3V...')
        for i in range(4095):
            dac_b.raw_value = i
        time.sleep(2.0) #Sleep the main thread 2 s
        # Go back down the 12-bit raw range.
        print(' MCP4725_b Going down 3.3-0V...')
        for i in range(4095, -1, -1):
            dac_b.raw_value = i
        time.sleep(3.0) #Sleep the main thread 1 s
    



 except KeyboardInterrupt:
       #Para parar el codigo basta con hacer CTRL+C
       print ("\nKeyboardInterrupt has been caught.")
       # Hago una limpieza de los GPIO
       print ("GPio cleanup")
       GPIO.cleanup()
