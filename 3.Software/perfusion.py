#!/usr/bin/env python3

##Comentario mas

#We import the libraries
import logging
#import Adafruit_GPIO
import digitalio
import sys
import time
import inspect, os
import board
import busio
import RPi.GPIO as GPIO
import adafruit_mcp4725
import adafruit_max31856
from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import  QWidget, QProgressBar, QPushButton, QApplication, QFileDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QMainWindow, QMenu
#from Plotter import CustomWidget

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

numColsMax = 8     #Tabla protocolo

#Define the GUI and init libraries
qtCreatorFile = "forms/interfaz.ui"


#We create the GUI using .UI Qt designer file
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

#Define GPIO board mode
GPIO.setmode(GPIO.BCM)

# Initialize I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

#INIT SPI
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

# allocate a CS pin and set the direction
cs1 = digitalio.DigitalInOut(board.D7)
cs2 = digitalio.DigitalInOut(board.D8)
cs3 = digitalio.DigitalInOut(board.D12)
cs1.direction = digitalio.Direction.OUTPUT
cs2.direction = digitalio.Direction.OUTPUT
cs3.direction = digitalio.Direction.OUTPUT


# Initialize MCP4725.
dac_a = adafruit_mcp4725.MCP4725(i2c, address=0x60)
dac_b = adafruit_mcp4725.MCP4725(i2c, address=0x61)


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


## Raspberry Pi software SPI configuration.
sensor_1 = adafruit_max31856.MAX31856(spi, cs1)
sensor_2 = adafruit_max31856.MAX31856(spi, cs2)
sensor_3 = adafruit_max31856.MAX31856(spi, cs3)
#-----------------------------------------------------------


#-DATALOGGER--------------------------------------------------
logging.basicConfig(
    filename='simpletest.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
_logger = logging.getLogger(__name__)
#-DATALOGGER--------------------------------------------------


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

       
        #Configure the Main Windows that it's going to be shown
        self.setWindowTitle(appTitle)    #Set the main window title
        self.resize(appWidth, appHeight) #Set the main window size
        
        #Add a status bar to notify the user what we are doing
        self.statusBar().showMessage('This is a status bar')

        #Load default profile (Init GUI Values)
        self.loadDefaultProfile()

        self.btn_relay1_on.clicked.connect(self.buttonPress_relay1_on)
        self.btn_relay1_off.clicked.connect(self.buttonPress_relay1_off)
        self.btn_relay2_on.clicked.connect(self.buttonPress_relay2_on)
        self.btn_relay2_off.clicked.connect(self.buttonPress_relay2_off)


        self.btn_pump_9.clicked.connect(self.getit_thermo1)
        self.pushButton_28.clicked.connect(self.getit_thermo2)
        self.pushButton_27.clicked.connect(self.getit_thermo3)

        self.pushButton_buzzer.clicked.connect(self.buttonPress_buzzer)


        self.btn_saveProfile.clicked.connect(self.buttonPress_saveProfile)
        self.btn_loadProfile.clicked.connect(self.buttonPress_loadProfile)
        self.btn_resetProfile.clicked.connect(self.buttonPress_resetProfile)

        self.btn_blink_led1.clicked.connect(self.buttonPress_blink_led1)
        self.btn_blink_led2.clicked.connect(self.buttonPress_blink_led2)
        self.btn_blink_led3.clicked.connect(self.buttonPress_blink_led3)

        self.btn_pump1.clicked.connect(self.buttonPress_pump1)
        self.btn_pump2.clicked.connect(self.buttonPress_pump2)


##Desiré: nuevos botones pestaña protocols--------------------------------------	

        self.pushButton_addHold.clicked.connect(self.buttonPress_pushButton_addHold)
        self.pushButton_addRamp.clicked.connect(self.buttonPress_pushButton_addRamp)

   
        self.start.clicked.connect(self.buttonPress_start)
        self.pause.clicked.connect(self.buttonPress_pause)
        self.reset.clicked.connect(self.buttonPress_reset)
        self.stop.clicked.connect(self.buttonPress_stop)

        self.timeMode.clicked.connect(self.buttonPress_timeMode)
        self.temperatureMode.clicked.connect(self.buttonPress_temperatureMode)


        #Maquetacion de columnas (tabla protocolo)
        self.tableWidget.setColumnCount(numColsMax)

        self.tableWidget.setColumnWidth(0, 80)
        self.tableWidget.setColumnWidth(1, 90)
        self.tableWidget.setColumnWidth(2, 90)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 125)
        self.tableWidget.setColumnWidth(5, 90)
        self.tableWidget.setColumnWidth(6, 110)
        self.tableWidget.setColumnWidth(7, 65)
        
##FIN----------------------------------------------------------------------------------



        # Load default .conf data if exists
        self.buttonPress_loadProfile()        

    #DEFINES FUNCTION ACTIONS FOR ELEMENTS (BUTTONS; ETC)#

    ###########################################################
    ##            'PROTOCOLS' TAB (BUTTONS ACTIONS)      ##
    ###########################################################  


    def buttonPress_pushButton_addHold(self):
        ##agregamos fila vacia
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        ##Seleccionamos el ultimo item y agregamos la info
        self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem("Hold"))
        self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem("-"))
        self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem("-"))
        self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem("-"))
        self.tableWidget.setItem(rowPosition, 4, QTableWidgetItem("-"))
        self.tableWidget.setItem(rowPosition, 5, QTableWidgetItem("-"))
        self.tableWidget.setItem(rowPosition, 6, QTableWidgetItem(self.holdTime.text()))
        self.tableWidget.setItem(rowPosition, 7, QTableWidgetItem("Undone"))


    def buttonPress_pushButton_addRamp(self):
        ##agregamos fila vacia
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)
        ##Seleccionamos el ultimo item y agregamos la info
        self.tableWidget.setItem(rowPosition, 0, QTableWidgetItem("Ramp"))
        self.tableWidget.setItem(rowPosition, 1, QTableWidgetItem(self.fromValue.text()))
        self.tableWidget.setItem(rowPosition, 2, QTableWidgetItem(self.toValue.text()))
        if self.timeMode.isChecked():
            self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem(self.duration.text()))
            self.tableWidget.setItem(rowPosition, 4, QTableWidgetItem("-"))
            self.tableWidget.setItem(rowPosition, 5, QTableWidgetItem("-"))
        elif self.temperatureMode.isChecked():
            self.tableWidget.setItem(rowPosition, 3, QTableWidgetItem("-"))
            self.tableWidget.setItem(rowPosition, 4, QTableWidgetItem(self.coolingRate.text()))
            self.tableWidget.setItem(rowPosition, 5, QTableWidgetItem(self.stepJump.text()))
        self.tableWidget.setItem(rowPosition, 6, QTableWidgetItem("-"))
        self.tableWidget.setItem(rowPosition, 7, QTableWidgetItem("Undone"))
 

    def buttonPress_start(self):
        if self.start.isEnabled():
            self.start.setEnabled(False)
            self.stop.setEnabled(True)
            self.pause.setEnabled(True)
            self.reset.setEnabled(False)


    def buttonPress_stop(self):
        if self.stop.isEnabled():
            self.start.setEnabled(True)
            self.stop.setEnabled(False)
            self.pause.setEnabled(False)
            self.reset.setEnabled(True)
            self.start.setText("START")


    def buttonPress_pause(self):
        if self.pause.isEnabled():
            self.pause.setEnabled(False)
            self.stop.setEnabled(False)
            self.reset.setEnabled(True)
            self.start.setEnabled(True)
            self.start.setText("RESUME")


    def buttonPress_reset(self):

        if self.reset.isEnabled():
            self.pause.setEnabled(False)
            self.stop.setEnabled(False)
            self.reset.setEnabled(False)
            self.start.setEnabled(True)
            self.start.setText("START")
            


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

    def getit_thermo1(self):
        temp_1 = sensor_1.temperature
        self.lineEdit_34.setText("{0:.3f}".format(temp_1))

    def getit_thermo2(self):
        temp_2 = sensor_2.temperature
        self.lineEdit_35.setText("{0:.3f}".format(temp_2))
        
    def getit_thermo3(self):
        temp_3 = sensor_3.temperature
        self.lineEdit_36.setText("{0:.3f}".format(temp_3))

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
        self.writeVoltage_a(self.lineEdit_pump1.text())  

    def buttonPress_pump2(self):
        self.writeVoltage_b(int(self.lineEdit_pump2.text()))  

    def buttonPress_pump3(self):
        self.writeVoltage(int(self.lineEdit_pump3.text()))



    #DEFINES FUNCTION ACTIONS FOR ELEMENTS (BUTTONS; ETC)#
        
    ###########################################################
    ##            'PROTOCOLS' TAB (BUTTONS ACTIONS      ##
    ###########################################################

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        deleteAct = contextMenu.addAction("Delete")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action == deleteAct:
            row = self.tableWidget.currentRow()
            self.tableWidget.removeRow(row)
        
        

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #We call 'MyApp' class
    window = MyApp()
    #Show the generated form
    window.show()
    sys.exit(app.exec_())


