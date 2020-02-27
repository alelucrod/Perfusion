#!/usr/bin/env python3


#We import the libraries
import logging
import Adafruit_GPIO
import sys
import time
import inspect, os
import board
import busio
import RPi.GPIO as GPIO
import adafruit_mcp4725
from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import  QWidget, QProgressBar, QPushButton, QApplication, QFileDialog
from PyQt5.QtCore import QBasicTimer


from Adafruit_MAX31856 import MAX31856 as MAX31856

#Define Default Pinout
#It'll be loaded by default

pin_led1 = 23
pin_led2 = 17
pin_led3 = 3

pin_relay1 = 27
pin_relay2 = 22 #alberto

pin_buzzer = 18

pin_i2c_sda = 7
pin_i2c_scl = 8

pin_spi0_mosi = 9
pin_spi0_miso = 10
pin_spi0_sclk = 11
pin_spi0_cs0  = 12
pin_spi0_cs1  = 13
pin_spi0_cs2  = 14

i2c_pump1_addr = '0x00'
i2c_pump2_addr = '0x00'
i2c_pump3_addr = '0x00'

thermo1_type = 'Type K'
thermo2_type = 'Type K'
thermo3_type = 'Type K'

#Define the lang strings
appTitle = 'Perfusion Control Panel'


#Define the system variables
appWidth = 800
appHeight = 500

#Define the GUI and init libraries
qtCreatorFile = "interfaz.ui"


#We create the GUI using .UI Qt designer file
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

#Define GPIO board mode
GPIO.setmode(GPIO.BCM)

# Initialize I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)


# Initialize MCP4725.
dac_a = adafruit_mcp4725.MCP4725(i2c, address=0x60)
dac_b = adafruit_mcp4725.MCP4725(i2c, address=0x61)

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

# Use the raw_value property to directly read and write
# the 12-bit DAC value.  The range of values is
# 0 (minimum/ground) to 4095 (maximum/Vout).
##dac.raw_value = 4095


#alberto--------------------------------------------------
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
#-----------------------------------------------------------



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
  if(tune==3):
    pitches=[392,294,0,392,294,0,392,0,392,392,392,0,1047,262]
    duration=[0.2,0.2,0.2,0.2,0.2,0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.8,0.4]
    for p in pitches:
      self.buzz(p, duration[x])  #feed the pitch and duration to the func$
      time.sleep(duration[x] *0.5)
      x+=1



  GPIO.setup(self.buzzer_pin, GPIO.IN)

#################################################
#     We create a class to Manage the GUI      ##
#################################################

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):

    #Default Function that will be executed when we
    #call the 'MyApp' class
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.closeEvent = self.closeEvent
        self.setupUi(self)

        #global variableS to PROTOCOLS
        self.timera = QBasicTimer()
        self.step_a = 0
        self.timerb = QBasicTimer()
        self.step_b = 0
        
        #Configure the Main Windows that it's going to be shown
        self.setWindowTitle(appTitle)    #Set the main window title
        self.resize(appWidth, appHeight) #Set the main window size
        
        #Add a status bar to notify the user what we are doing
        self.statusBar().showMessage('This is a status bar')

        #Load default profile (Init GUI Values)
        self.loadDefaultProfile()
        
        
        #Add button events (connect .ui element with button fcn action)
        #D#self.btn_start.clicked.connect(self.buttonPress_Start)
        #D#self.btn_stop.clicked.connect(self.buttonPress_Stop)

        self.btn_relay1_on.clicked.connect(self.buttonPress_relay1_on)
        self.btn_relay1_off.clicked.connect(self.buttonPress_relay1_off)
        self.btn_relay2_on.clicked.connect(self.buttonPress_relay2_on)
        self.btn_relay2_off.clicked.connect(self.buttonPress_relay2_off)

        #alberto----------------------------------------------------------------
        self.btn_pump_9.clicked.connect(self.getit_thermo1)
        self.pushButton_28.clicked.connect(self.getit_thermo2)
        self.pushButton_27.clicked.connect(self.getit_thermo3)

        self.pushButton_buzzer.clicked.connect(self.buttonPress_buzzer)

# STEP RESPONSE---------------------------------------------------------------------------------------
#----------PUMP A--------------------------------------------------------------------
        #D#self.btnStart_step_a.clicked.connect(self.startProgress_a)
        #D#self.btnReset_step_a.clicked.connect(self.resetBar_a)
#----------PUMP B--------------------------------------------------------------------
        #D#self.btnStart_step_b.clicked.connect(self.startProgress_b)
        #D#self.btnReset_step_b.clicked.connect(self.resetBar_b)
## RAMP RESPONSE---------------------------------------------------------------------------------------
##----------PUMP A--------------------------------------------------------------------
#        #D#self.btnStart_ramp_a.clicked.connect(self.startProgress)
#        #D#self.btnReset_ramp_a.clicked.connect(self.resetBar)
##----------PUMP B--------------------------------------------------------------------
#        #D#self.btnStart_ramp_b.clicked.connect(self.startProgress)
#        #D#self.btnReset_ramp_b.clicked.connect(self.resetBar)
        
        #-----------------------------------------------------------------------

        self.btn_saveProfile.clicked.connect(self.buttonPress_saveProfile)
        self.btn_loadProfile.clicked.connect(self.buttonPress_loadProfile)
        self.btn_resetProfile.clicked.connect(self.buttonPress_resetProfile)

        self.btn_blink_led1.clicked.connect(self.buttonPress_blink_led1)
        self.btn_blink_led2.clicked.connect(self.buttonPress_blink_led2)
        self.btn_blink_led3.clicked.connect(self.buttonPress_blink_led3)

        self.btn_pump1.clicked.connect(self.buttonPress_pump1)
        self.btn_pump2.clicked.connect(self.buttonPress_pump2)
        #D#self.btn_pump3.clicked.connect(self.buttonPress_pump3)


##Desiré: nuevos botones pestaña protocols--------------------------------------	

        self.pushButton_addHold.clicked.connect(self.buttonPress_pushButton_addHold)
        self.pushButton_addRamp.clicked.connect(self.buttonPress_pushButton_addRamp)

   
        self.start.clicked.connect(self.buttonPress_start)
        self.pause.clicked.connect(self.buttonPress_pause)
        self.reset.clicked.connect(self.buttonPress_reset)
        self.stop.clicked.connect(self.buttonPress_stop)

        self.timeMode.clicked.connect(self.buttonPress_timeMode)
        self.temperatureMode.clicked.connect(self.buttonPress_temperatureMode)
##FIN----------------------------------------------------------------------------------



        # Load default .conf data if exists
        self.buttonPress_loadProfile()
        

    #DEFINES FUNCTION ACTIONS FOR ELEMENTS (BUTTONS; ETC)#

##Desiré: funciones botones pestaña protocols----------------------------------------------------------

    ###########################################################
    ##            'PROTOCOLS' TAB (BUTTONS ACTIONS)      ##
    ###########################################################  


    def buttonPress_pushButton_addHold(self):


    def buttonPress_pushButton_addRamp(self):


    def buttonPress_start(self):
        if self.start.isEnabled():
            self.start.setEnabled(False)
            self.stop.setEnabled(True)
            self.pause.setEnabled(True)
            self.reset.setEnabled(False)
        else:
            self.start.setEnabled(True)
            self.true.setEnabled(False)


    def buttonPress_stop(self):
        if self.stop.isEnabled():
            self.start.setEnabled(True)
            self.stop.setEnabled(False)
            self.pause.setEnabled(False)
            self.reset.setEnabled(True)
        else:
            self.start.setEnabled(False)
            self.true.setEnabled(True)


    def buttonPress_pause(self):
        if self.pause.isEnabled():
            self.pause.setEnabled(False)
            self.stop.setEnabled(False)
            self.reset.setEnabled(True)
            self.start.setEnabled(True)
        else:
            self.start.setEnabled(False)
            self.true.setEnabled(True)


    def buttonPress_reset(self):

        if self.pause.isEnabled():
            self.pause.setEnabled(False)
            self.stop.setEnabled(False)
            self.reset.setEnabled(False)
            self.start.setEnabled(True)
        else:
            self.start.setEnabled(False)
            self.true.setEnabled(True)


    def buttonPress_timeMode(self):
            self.label_6.setEnabled(False)
            self.coolingRate.setEnabled(False)
            self.label_7.setEnabled(False)
            self.stepJump.setEnabled(False)
            self.label_23.setEnabled(True)
            self.duration.setEnabled(True)

    def buttonPress_temperatureMode(self):

            self.label_6.setEnabled(True)
            self.coolingRate.setEnabled(True)
            self.label_7.setEnabled(True)
            self.stepJump.setEnabled(True)
            self.label_23.setEnabled(False)
            self.duration.setEnabled(False) 
    
    def loadDefaultProfile(self):
        list_thermo_module = [
            self.tr('Module 1'),
            self.tr('Module 2'),
            self.tr('Module 3'),
          
        ]


     self.comboBox_thermo1_2_3.clear()

     self.comboBox_thermo1_2_3.addItems(list_thermo_module)
##FIN-------------------------------------------------------------------

    ###########################################################
    ##            'TOOLS AND TEST' TAB (BUTTONS ACTIONS)      ##
    ###########################################################    
    def buttonPress_relay1_on(self):
        GPIO.setup(pin_relay1, GPIO.OUT)
        GPIO.output(pin_relay1, False)
        
    def buttonPress_relay1_off(self):
        GPIO.setup(pin_relay1, GPIO.OUT)
        GPIO.output(pin_relay1, True)
        

    def buttonPress_relay2_on(self):
        GPIO.setup(pin_relay2, GPIO.OUT)
        GPIO.output(pin_relay2, False)

    def buttonPress_relay2_off(self):
        GPIO.setup(pin_relay2, GPIO.OUT)
        GPIO.output(pin_relay2, True)

#alberto--------------------------------------------------

    def getit_thermo1(self):
        temp_1 = sensor_1.read_temp_c()
        internal_1 = sensor_1.read_internal_temp_c()
        self.lineEdit_34.setText(format(temp_1))
        #self.lineEdit_34.setText('5')

    def getit_thermo2(self):
        temp_2 = sensor_2.read_temp_c()
        internal_2 = sensor_2.read_internal_temp_c()
        self.lineEdit_35.setText(format(temp_2))
##        #self.lineEdit_34.setText('5')
##
    def getit_thermo3(self):
        temp_3 = sensor_3.read_temp_c()
        internal_3 = sensor_3.read_internal_temp_c()
        self.lineEdit_36.setText(format(temp_3))
##        #self.lineEdit_34.setText('5')


    def buttonPress_buzzer(self):
        buzzer = Buzzer()
        buzzer.play(3)


#--------------------------------------------------------

    def buttonPress_blink_led1(self):
        GPIO.setup(pin_led1, GPIO.OUT)
        GPIO.output(pin_led1, True)
        time.sleep(1)
        GPIO.output(pin_led1, False)
        
    def buttonPress_blink_led2(self):
        GPIO.setup(pin_led2, GPIO.OUT)
        GPIO.output(pin_led2, False)
        time.sleep(1)
        GPIO.output(pin_led2, True)

    def buttonPress_blink_led3(self):
        GPIO.setup(pin_led3, GPIO.OUT)
        GPIO.output(pin_led3, True)
        time.sleep(1)
        GPIO.output(pin_led3, False)

    def buttonPress_pump1(self):
##        print('Hola, el valor elegido es: ' + int(self.lineEdit_pump1.text()))
        print('Hola, el valor elegido es: ' + self.lineEdit_pump1.text())
        self.writeVoltage_a(self.lineEdit_pump1.text())  

    def buttonPress_pump2(self):
        self.writeVoltage_b(int(self.lineEdit_pump2.text()))  

    def buttonPress_pump3(self):
        self.writeVoltage(int(self.lineEdit_pump3.text()))



    #DEFINES FUNCTION ACTIONS FOR ELEMENTS (BUTTONS; ETC)#
        
    ###########################################################
    ##            'PROTOCOLS' TAB (BUTTONS ACTIONS      ##
    ###########################################################


    def resetBar_a(self):
        self.step_a = 0
        

    def startProgress_a(self):
        if self.timera.isActive():
            self.timera.stop()
            self.btnStart_step_a.setText('START')
        else:
            self.timera.start(100, self)# se parece a una espera de 100 ms
            self.btnStart_step_a.setText('STOP')

    def resetBar_b(self):
        self.step_b = 0
        

    def startProgress_b(self):
        if self.timerb.isActive():
            self.timerb.stop()
            self.btnStart_step_b.setText('START')
        else:
            self.timerb.start(200, self)# se parece a una espera de 100 ms
            self.btnStart_step_b.setText('STOP')

    def timerEvent(self, event):
        if self.step_a < 20:
            dac_b.raw_value =0
        elif self.step_a >= 20 and self.step_a <= 120:
            dac_b.raw_value =4095
        elif self.step_a > 120:
            dac_b.raw_value =0
            self.timera.stop()
            self.btnStart_step_a.setText('START')
            return

        if self.step_b < 10:
            dac_a.raw_value =0
        elif self.step_b >= 10 and self.step_b <= 60:
            dac_a.raw_value =4095
        elif self.step_b > 60:
            dac_a.raw_value =0
            self.timerb.stop()
            self.btnStart_step_b.setText('START')
            return

        self.step_a +=1
        self.step_b +=1
        
       


        
        

    ###########################################################
    ##            'Preferences' TAB (BUTTONS ACTIONS         ##
    ###########################################################

             
    def buttonPress_saveProfile(self):
        
        #We save the config file with the user parameters
        with open('config//' + 'profile.conf', 'w') as f:
              f.write('led1 = '+ self.lineEdit_led1.text()+ '\r')
              f.write('led2 = '+ self.lineEdit_led2.text()+ '\r')
              f.write('led3 = '+ self.lineEdit_led3.text()+ '\r')
              f.write('relay1 = '+ self.lineEdit_relay1.text()+ '\r')
              f.write('relay2 = '+ self.lineEdit_relay2.text()+ '\r')
              f.write('buzzer = '+ self.lineEdit_buzzer.text()+ '\r')
              f.write('i2c_sda = '+ self.lineEdit_i2c_sda.text()+ '\r')
              f.write('i2c_scl = '+ self.lineEdit_i2c_scl.text()+ '\r')
              f.write('spi0_mosi = '+ self.lineEdit_spi0_mosi.text()+ '\r')
              f.write('spi0_miso = '+ self.lineEdit_spi0_miso.text()+ '\r')
              f.write('spi0_sclk = '+ self.lineEdit_spi0_sclk.text()+ '\r')
              f.write('spi0_cs0 = '+ self.lineEdit_spi0_cs0.text()+ '\r')
              f.write('spi0_cs1 = '+ self.lineEdit_spi0_cs1.text()+ '\r')
              f.write('spi0_cs2 = '+ self.lineEdit_spi0_cs2.text()+ '\r')
              f.write('pump1 = '+ str(self.comboBox_i2c_pump1.currentText())+ '\r')
              f.write('pump2 = '+ str(self.comboBox_i2c_pump2.currentText())+ '\r')
              f.write('pump3 = '+ str(self.comboBox_i2c_pump3.currentText())+ '\r')
              f.write('thermo1 = '+ str(self.comboBox_thermo1.currentText())+ '\r')
              f.write('thermo2 = '+ str(self.comboBox_thermo2.currentText())+ '\r')
              f.write('thermo3 = '+ str(self.comboBox_thermo3.currentText())+ '\r')

        ## We call this function to override the globalVars with the qelements        
        self.guiToGlobalVar()


    def buttonPress_loadProfile(self):
        #Check if file exists, if exist load the default conf
        exists = os.path.isfile('config//' + 'profile.conf')
        
        if exists:
            # Store configuration file values
            # We read the .conf file to load the saved previous data        
            file = open('config//' + 'profile.conf', mode = 'r', encoding = 'utf-8-sig')
            lines = file.readlines()
            file.close()
        
            for line in lines:
              line = line.split('=')
              line = [i.strip() for i in line]
              # Check line by line the header to assign the value to the global var
              if(line[0] == 'led1'):
                self.lineEdit_led1.setText(line[1])
              if(line[0] == 'led2'):
                self.lineEdit_led2.setText(line[1])
              if(line[0] == 'led3'):
                self.lineEdit_led3.setText(line[1])
              if(line[0] == 'relay1'):
                self.lineEdit_relay1.setText(line[1])
              if(line[0] == 'relay2'):
                self.lineEdit_relay2.setText(line[1])
#alberto-----------------------------------------------------------------------------------

                
#-------------------------------------------------------------------------------------------
              if(line[0] == 'buzzer'):
                self.lineEdit_buzzer.setText(line[1])
              if(line[0] == 'i2c_sda'):
                self.lineEdit_i2c_sda.setText(line[1])
              if(line[0] == 'i2c_scl'):
                self.lineEdit_i2c_scl.setText(line[1])
              if(line[0] == 'spi0_mosi'):
                self.lineEdit_spi0_mosi.setText(line[1])
              if(line[0] == 'spi0_miso'):
                self.lineEdit_spi0_miso.setText(line[1])
              if(line[0] == 'spi0_sclk'):
                self.lineEdit_spi0_sclk.setText(line[1])
              if(line[0] == 'spi0_cs0'):
                self.lineEdit_spi0_cs0.setText(line[1])
              if(line[0] == 'spi0_cs1'):
                self.lineEdit_spi0_cs1.setText(line[1])
              if(line[0] == 'spi0_cs2'):
                self.lineEdit_spi0_cs2.setText(line[1])
              if(line[0] == 'pump1'):
                index = self.comboBox_i2c_pump1.findText(line[1], QtCore.Qt.MatchFixedString)
                if index >= 0:
                     self.comboBox_i2c_pump1.setCurrentIndex(index)
              if(line[0] == 'pump2'):
                index = self.comboBox_i2c_pump2.findText(line[1], QtCore.Qt.MatchFixedString)
                if index >= 0:
                     self.comboBox_i2c_pump2.setCurrentIndex(index)
              if(line[0] == 'pump3'):
                index = self.comboBox_i2c_pump3.findText(line[1], QtCore.Qt.MatchFixedString)
                if index >= 0:
                     self.comboBox_i2c_pump3.setCurrentIndex(index)
              if(line[0] == 'thermo1'):
                index = self.comboBox_thermo1.findText(line[1], QtCore.Qt.MatchFixedString)
                if index >= 0:
                     self.comboBox_thermo1.setCurrentIndex(index)
              if(line[0] == 'thermo2'):
                index = self.comboBox_thermo2.findText(line[1], QtCore.Qt.MatchFixedString)
                if index >= 0:
                     self.comboBox_thermo2.setCurrentIndex(index)
              if(line[0] == 'thermo3'):
                index = self.comboBox_thermo3.findText(line[1], QtCore.Qt.MatchFixedString)
                if index >= 0:
                     self.comboBox_thermo3.setCurrentIndex(index)

            ## We call this function to override the globalVars with the qelements        
            self.guiToGlobalVar()       

            
        else:
            # Keep presets
            print('Config file does not exists')
        
       


    def guiToGlobalVar(self):
        #We override the global variables
        pin_led1 = int(self.lineEdit_led1.text())
        pin_led2 = int(self.lineEdit_led2.text())
        pin_led3 = int(self.lineEdit_led3.text())
        pin_relay1 = int(self.lineEdit_relay1.text())
        pin_relay2 = int(self.lineEdit_relay2.text())
        pin_buzzer = int(self.lineEdit_buzzer.text())
        pin_i2c_sda = int(self.lineEdit_i2c_sda.text())
        pin_i2c_scl = int(self.lineEdit_i2c_scl.text())
        pin_spi0_mosi = int(self.lineEdit_spi0_mosi.text())
        pin_spi0_miso = int(self.lineEdit_spi0_miso.text())
        pin_spi0_sclk = int(self.lineEdit_spi0_sclk.text())
        pin_spi0_cs0 = int(self.lineEdit_spi0_cs0.text())
        pin_spi0_cs1 = int(self.lineEdit_spi0_cs1.text())
        pin_spi0_cs2 = int(self.lineEdit_spi0_cs2.text())
        i2c_pump1_addr = str(self.comboBox_i2c_pump1.currentText())
        i2c_pump2_addr = str(self.comboBox_i2c_pump2.currentText())
        i2c_pump3_addr = str(self.comboBox_i2c_pump3.currentText())
        thermo1_type = str(self.comboBox_thermo1.currentText())
        thermo2_type = str(self.comboBox_thermo1.currentText())
        thermo3_type = str(self.comboBox_thermo1.currentText())
           

    def buttonPress_resetProfile(self):
        self.loadDefaultProfile()
        
        
    def buttonPress_Pump_1(self):
        if self.btn_pump_1.isEnabled():
            self.btn_pump_1.setText('STOP PUMP 1')
            #self.btn_pump_1.setEnabled(False)
        else:
            self.btn_pump_1.setText('FORCE PUMP 1')
            #self.btn_pump_1.setEnabled(True)

#------------------------------------------------------------------------------
##    @property
##    def state(self):
##        return self._state
##
##    @state.setter
##    def state(self, value):
##        self._state = value
##
##    def on_click(self, event=None):
##        sending_button = self.sender() #getting button name
##        btn_name = str(sending_button.objectName())
##        if btn_name == 'start_step_dac_a':
##            old_state = self.state
##            self.state = 1 #changing state to sampling
##            self.start_step_dac_a.setEnabled(False)
##            self.stop_step_dac_a.setEnabled(True)
##            dac_b.raw_value = 0
##            time.sleep(2.0) #Sleep the main thread 2 s
##            dac_b.raw_value = 4095
##            time.sleep(10.0) #Sleep the main thread 10 s
##            dac_b.raw_value = 0
##        elif btn_name == 'stop_step_dac_a'
##            old_state = self.state
##            self.state = 0 #changing state to idle
##            self.start_step_dac_a.setEnabled(True)
##            self.stop_step_dac_a.setEnabled(False)
##            dac_a.raw_value = 0
            
    
##    def buttonPress_start_step_dac_a(self):
##        if self.start_step_dac_a.isEnabled():
##            self.start_step_dac_a.setEnabled(False)
##            self.stop_step_dac_a.setEnabled(True)
##            dac_a.raw_value = 0
##            time.sleep(2.0) #Sleep the main thread 2 s
##            dac_a.raw_value = 4095
##            time.sleep(2.0) #Sleep the main thread 2 s
##        else:
##            self.start_step_dac_a.setEnabled(True)
##            self.stop_step_dac_a.setEnabled(False)
##            dac_a.raw_value = 0
##
##
##    def buttonPress_stop_step_dac_a(self):
##        if self.stop_step_dac_a.isEnabled():
##            self.start_step_dac_a.setEnabled(True)
##            self.stop_step_dac_a.setEnabled(False)
##            dac_a.raw_value = 0
##        else:
##            self.start_step_dac_a.setEnabled(False)
##            self.stop_step_dac_a.setEnabled(True)
##            dac_a.raw_value = 0
##            time.sleep(2.0) #Sleep the main thread 2 s
##            dac_a.raw_value = 4095
##            time.sleep(2.0) #Sleep the main thread 2 s
            
#----------------------------------------------------------
    def buttonPress_Start(self):
        if self.btn_start.isEnabled():
            self.btn_start.setEnabled(False)
            self.btn_stop.setEnabled(True)
        else:
            self.btn_start.setEnabled(True)
            self.btn_true.setEnabled(False)


    def buttonPress_Stop(self):
        if self.btn_stop.isEnabled():
            self.btn_start.setEnabled(True)
            self.btn_stop.setEnabled(False)
        else:
            self.btn_start.setEnabled(False)
            self.btn_true.setEnabled(True)


    def loadDefaultProfile(self):
        list_thermo_types = [
            self.tr('Type K'),
            self.tr('Type J'),
            self.tr('Type N'),
            self.tr('Type R'),
            self.tr('Type S'),
            self.tr('Type T'),
            self.tr('Type E'),
            self.tr('Type B')
        ]

        list_i2c_addr = [
            self.tr('0x00'),
            self.tr('0x01'),
            self.tr('0x02')
        ]
        
        #First we get the current working path
        directory = os.path.dirname(os.path.realpath(__file__))
        
        #Load Main App "Icon"
        self.setWindowIcon(QtGui.QIcon(directory + '//res//' + 'icon.png'))
        
        #Load "About" tab logo
        pixmap = QPixmap(directory + '//res//' + 'logo_fIII.png')
        self.label_about_logo.setPixmap(pixmap)

        #Load ThermoCouples list
        self.comboBox_thermo1.clear()
        self.comboBox_thermo2.clear()
        self.comboBox_thermo3.clear()

        self.comboBox_thermo1.addItems(list_thermo_types)
        self.comboBox_thermo2.addItems(list_thermo_types)
        self.comboBox_thermo3.addItems(list_thermo_types)

        #Load PUMP Addresses
        self.comboBox_i2c_addr.clear()
        self.comboBox_i2c_pump1.clear()
        self.comboBox_i2c_pump2.clear()
        self.comboBox_i2c_pump3.clear()

        self.comboBox_i2c_addr.addItems(list_i2c_addr)
        self.comboBox_i2c_pump1.addItems(list_i2c_addr)
        self.comboBox_i2c_pump2.addItems(list_i2c_addr)
        self.comboBox_i2c_pump3.addItems(list_i2c_addr)

        #Load default pinout values
        #WE must convert pin integer type to strings 
        self.lineEdit_led1.setText(str(pin_led1))
        self.lineEdit_led2.setText(str(pin_led2))
        self.lineEdit_led3.setText(str(pin_led3))

        self.lineEdit_relay1.setText(str(pin_relay1))
        self.lineEdit_relay2.setText(str(pin_relay2))
        self.lineEdit_buzzer.setText(str(pin_buzzer))

        self.lineEdit_i2c_sda.setText(str(pin_i2c_sda))
        self.lineEdit_i2c_scl.setText(str(pin_i2c_scl))

        self.lineEdit_spi0_mosi.setText(str(pin_spi0_mosi))
        self.lineEdit_spi0_miso.setText(str(pin_spi0_miso))
        self.lineEdit_spi0_sclk.setText(str(pin_spi0_sclk))
        self.lineEdit_spi0_cs0.setText(str(pin_spi0_cs0))
        self.lineEdit_spi0_cs1.setText(str(pin_spi0_cs1))
        self.lineEdit_spi0_cs2.setText(str(pin_spi0_cs2))


        # Load the font:
        QtGui.QFontDatabase.addApplicationFont(directory + '//res//' + 'Tahoma.ttf')
        stylesheet = open(directory + '//res//' + 'mystylesheet.qss').read()
        self.setStyleSheet(stylesheet)
        

    ## DACMCP4725_a Voltage writter
    def writeVoltage_a(self, voltage):
        try:
          dac_a.raw_value = int(voltage)
          print("well")
          print(voltage)
          
        except:
          print("Error with I2C module")
          print(int(voltage))

    ### DACMCP4725_b Voltage writter
    def writeVoltage_b(self, voltage):
        try:
          dac_b.raw_value = int(voltage)
          print("well")
          print(voltage)
          
        except:
          print("Error with I2C module")
          print(int(voltage))
   
    ## Trigger event when we close the form    
    def closeEvent(self, event):
        # Free up GPIOs        
        GPIO.cleanup()
        
#########################################################            
# Default function that will be executed when        ####
# we run this program                                ####
#########################################################

from Plotter import CustomWidget

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #We call 'MyApp' class
    window = MyApp()
    #Show the generated form
    window.show()
    sys.exit(app.exec_())


