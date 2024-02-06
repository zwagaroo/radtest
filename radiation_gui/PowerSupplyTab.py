import datetime
import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QCheckBox, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal, QMutex
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PyQt5.QtCore import QThreadPool
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject
import random
import pandas as pd
import os
import csv

from PowerSupplyControlFunctions import * 




class PowerSupplyDataSignals(QObject):
    data_signal = pyqtSignal()

class PowerSupplyDataThread(QRunnable):
    
    def __init__(self, powerSupplyTab):
        super(PowerSupplyDataThread, self).__init__()
        self.signals = PowerSupplyDataSignals()
        self.running = False
        self.powerSupplyTab = powerSupplyTab

    def run(self):
        self.running = True
        while self.running:

            #get the current data
            volt1, curr1, volt2, curr2 = getOutputData(self.powerSupplyTab.connectedPowerSupply)
            
            if(len(self.powerSupplyTab.data) >= 100):
                self.powerSupplyTab.data.drop(index=0, inplace=True)
                
            self.powerSupplyTab.data = pd.concat([self.powerSupplyTab.data, pd.DataFrame({
                "datetime": [datetime.datetime.now().strftime("%d-%b-%Y %H:%M:%S")],
                "run_time": [time.time() - self.powerSupplyTab.monitoringStartTime],
                "volt1": [float(volt1)],
                "curr1": [float(curr1)],
                "volt2": [float(volt2)],
                "curr2": [float(curr2)]
            })], ignore_index = True)
            #modify data tell the thing to update
            
            
            self.signals.data_signal.emit()

            if(self.powerSupplyTab.logCheckBox.isChecked()):
                with open(self.powerSupplyTab.dataLogPathLineEdit.text(), 'a') as csv_file:
                    fieldnames = ['datetime','run_time', 'volt1', 'curr1', 'volt2', 'curr2']
                    writer = csv.DictWriter(csv_file, fieldnames=fieldnames,lineterminator='\n')
                    writer.writerow(self.powerSupplyTab.data.iloc[-1].to_dict())
 




    def stop(self):
        self.running = False

class PowerSupplyTab(QWidget):
    def __init__(self, name, parent=None):
        super(PowerSupplyTab, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.dataThread = None
        self.data = pd.DataFrame()
        self.monitoringStartTime = None
        self.connectedPowerSupply = None

        # Configurations Section
        self.configurationLayout = QVBoxLayout()
        
        # Label for the file path input


        #Powersupply Configs!!!
        self.powerSupplyConfigurationLayout = QVBoxLayout()

        self.connectionConfigurationLayout = QHBoxLayout()

        self.powerSupplyAddrLabel = QLabel("Power Supply Address")
        self.connectionConfigurationLayout.addWidget(self.powerSupplyAddrLabel)

        self.powerSupplyAddrLineEdit = QLineEdit()
        self.connectionConfigurationLayout.addWidget(self.powerSupplyAddrLineEdit)

        self.connectButton = QPushButton("Connect")
        self.connectionConfigurationLayout.addWidget(self.connectButton)
        self.connectButton.clicked.connect(self.connect)

        self.powerSupplyConfigurationLayout.addLayout(self.connectionConfigurationLayout)

        #output 1
        self.output1Layout = QHBoxLayout()
        self.maxVoltage1Label = QLabel("Max Voltage Output 1")
        self.output1Layout.addWidget(self.maxVoltage1Label)

        self.maxVoltage1LineEdit = QLineEdit()
        self.output1Layout.addWidget(self.maxVoltage1LineEdit)

        self.maxCurrent1Label = QLabel("Max Current Output 1")
        self.output1Layout.addWidget(self.maxCurrent1Label)

        self.maxCurrent1LineEdit = QLineEdit()
        self.output1Layout.addWidget(self.maxCurrent1LineEdit)

        self.setOutput1Button = QPushButton("Set")

        def setOutput1():
            self.setVoltage(1)
            self.setCurrent(1)

        self.setOutput1Button.clicked.connect(setOutput1)
        self.output1Layout.addWidget(self.setOutput1Button)

        self.powerSupplyConfigurationLayout.addLayout(self.output1Layout)



        #output 2

        self.output2Layout = QHBoxLayout()
        self.maxVoltage2Label = QLabel("Max Voltage Output 2")
        self.output2Layout.addWidget(self.maxVoltage2Label)

        self.maxVoltage2LineEdit = QLineEdit()
        self.output2Layout.addWidget(self.maxVoltage2LineEdit)

        self.maxCurrent2Label = QLabel("Max Current Output 2")
        self.output2Layout.addWidget(self.maxCurrent2Label)

        self.maxCurrent2LineEdit = QLineEdit()
        self.output2Layout.addWidget(self.maxCurrent2LineEdit)

        self.setOutput2Button = QPushButton("Set")
        self.output2Layout.addWidget(self.setOutput2Button)

        def setOutput2():
            self.setVoltage(2)
            self.setCurrent(2)

        self.setOutput2Button.clicked.connect(setOutput2)

        self.powerSupplyConfigurationLayout.addLayout(self.output2Layout)


        self.configurationLayout.addLayout(self.powerSupplyConfigurationLayout)

        #LOGGING CONFIGS
        self.loggingConfigurationLayout = QHBoxLayout()

        self.dataLogPathLabel = QLabel("Data Log Path:")
        self.loggingConfigurationLayout.addWidget(self.dataLogPathLabel)
        
        # Line edit for file path input
        self.dataLogPathLineEdit = QLineEdit()
        self.loggingConfigurationLayout.addWidget(self.dataLogPathLineEdit)

        
        self.eventLogPathLabel = QLabel("Event Log Path:")
        self.loggingConfigurationLayout.addWidget(self.eventLogPathLabel)

        # Line edit for file path input
        self.eventLogPathLineEdit = QLineEdit()
        self.loggingConfigurationLayout.addWidget(self.eventLogPathLineEdit)
        
        # Checkbox for enabling logging
        self.loggingCheckBox = QLabel("Enable Logging")
        self.loggingConfigurationLayout.addWidget(self.loggingCheckBox)
        self.logCheckBox = QCheckBox()
        self.loggingConfigurationLayout.addWidget(self.logCheckBox)
        
        self.configurationLayout.addLayout(self.loggingConfigurationLayout)

        # Add the input section layout to the main layout
        self.layout.addLayout(self.configurationLayout)

        # Table setup
        self.table = QTableWidget(4, 2)  # 1 row, 2 columns
        self.table.setHorizontalHeaderLabels(["Output Name", "Output Value"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setItem(0, 0, QTableWidgetItem("Voltage 1"))
        self.table.setItem(0, 1, QTableWidgetItem(""))
        self.table.setItem(1, 0, QTableWidgetItem("Current 1"))
        self.table.setItem(1, 1, QTableWidgetItem(""))
        self.table.setItem(2, 0, QTableWidgetItem("Voltage 2"))
        self.table.setItem(2, 1, QTableWidgetItem(""))
        self.table.setItem(3, 0, QTableWidgetItem("Current 2"))
        self.table.setItem(3, 1, QTableWidgetItem(""))
        self.layout.addWidget(self.table)

        # Existing setup code for table, graphs, and buttons...
        # Graphs setup
        self.graphLayout = QVBoxLayout()
        self.voltGraphLayout = QHBoxLayout()
        self.graph1 = FigureCanvas(Figure(figsize=(8, 4)))
        self.ax1 = self.graph1.figure.add_subplot(111)
        self.ax1.get_yaxis().get_major_formatter().set_useOffset(False)
        self.graph2 = FigureCanvas(Figure(figsize=(8, 4)))

        self.ax2 = self.graph2.figure.add_subplot(111)
        self.ax2.get_yaxis().get_major_formatter().set_useOffset(False)
        self.voltGraphLayout.addWidget(self.graph1)
        self.voltGraphLayout.addWidget(self.graph2)

        self.currGraphLayout = QHBoxLayout()
        self.graph3 = FigureCanvas(Figure(figsize=(8, 3.5)))
        self.ax3 = self.graph3.figure.add_subplot(111)
        self.ax3.get_yaxis().get_major_formatter().set_useOffset(False)
        self.graph4 = FigureCanvas(Figure(figsize=(8, 3.5)))
        self.ax4 = self.graph4.figure.add_subplot(111)
        self.ax4.get_yaxis().get_major_formatter().set_useOffset(False)
        self.currGraphLayout.addWidget(self.graph3)
        self.currGraphLayout.addWidget(self.graph4)
        
        
        self.graphLayout.addLayout(self.voltGraphLayout)
        self.graphLayout.addLayout(self.currGraphLayout)
        self.layout.addLayout(self.graphLayout)

        # Buttons setup
        self.buttonLayout = QHBoxLayout()
        self.powerOnButton = QPushButton('Power On')
        self.powerOffButton = QPushButton('Power Off')
        self.powerOnButton.clicked.connect(self.powerOn)
        self.powerOffButton.clicked.connect(self.powerOff)
        self.buttonLayout.addWidget(self.powerOnButton)
        self.buttonLayout.addWidget(self.powerOffButton)
        self.monitorOnButton = QPushButton('Monitor On')
        self.monitorOffButton = QPushButton('Monitor Off')
        self.monitorOnButton.clicked.connect(self.startMonitoring)
        self.monitorOffButton.clicked.connect(self.stopMonitoring)
        self.buttonLayout.addWidget(self.monitorOnButton)
        self.buttonLayout.addWidget(self.monitorOffButton)
        self.layout.addLayout(self.buttonLayout)

        #tab closed events


    def powerOn(self):
        powerOn(self.connectedPowerSupply)

    def powerOff(self):
        powerOff(self.connectedPowerSupply)

    def startMonitoring(self):
        if (self.dataThread is None) or (not self.dataThread.running):
            self.data = pd.DataFrame()
            self.dataThread = PowerSupplyDataThread(self)  # Initialize the thread
            self.dataThread.setAutoDelete(True)
            self.dataThread.signals.data_signal.connect(lambda : self.update())
            QThreadPool.globalInstance().start(self.dataThread)
            self.monitoringStartTime = time.time()

            self.dataLogPathLineEdit.setEnabled(False)
            self.eventLogPathLineEdit.setEnabled(False)

    def stopMonitoring(self):
        self.dataThread.stop()
        self.dataLogPathLineEdit.setEnabled(True)
        self.eventLogPathLineEdit.setEnabled(True)

    def update(self):
        self.ax1.clear()
        self.ax1.get_yaxis().get_major_formatter().set_useOffset(False)
        self.ax1.plot(self.data["run_time"], self.data["volt1"])
        self.ax1.set_title('Voltage of Output 1 (V)')
        self.graph1.draw()

        self.ax2.clear()
        self.ax2.get_yaxis().get_major_formatter().set_useOffset(False)
        self.ax2.plot(self.data["run_time"], self.data["volt2"])
        self.ax2.set_title('Voltage of Output 2 (V)')
        self.graph2.draw()

        self.ax3.clear()
        self.ax3.get_yaxis().get_major_formatter().set_useOffset(False)
        self.ax3.plot(self.data["run_time"], self.data["curr1"])
        self.ax3.set_title('Current of Output 1 (A)')
        self.graph3.draw()

        self.ax4.clear()
        self.ax4.get_yaxis().get_major_formatter().set_useOffset(False)
        self.ax4.plot(self.data["run_time"], self.data["curr2"])
        self.ax4.set_title('Current of Output 2 (A)')
        self.graph4.draw()

        self.table.item(0,1).setText(str(self.data["volt1"].iloc[-1]))
        self.table.item(1,1).setText(str(self.data["curr1"].iloc[-1]))
        self.table.item(2,1).setText(str(self.data["volt2"].iloc[-1]))
        self.table.item(3,1).setText(str(self.data["curr2"].iloc[-1]))

    def connect(self):

        try:
            print(self.powerSupplyAddrLineEdit.text())
            get_instrument_connection(int(self.powerSupplyAddrLineEdit.text()))
            self.connectedPowerSupply = int(self.powerSupplyAddrLineEdit.text())
            self.connectButton.setEnabled(False)

        except Exception as ex:
            if(isinstance(ex, ValueError)):
                self.showError("Address must be a positive integer")
            else:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                self.showError(template.format(type(ex).__name__, ex.args) + "Are you sure the powersupply is connected?")
            return
        
    def setVoltage(self, output):
        try:
            val = None
            if output == 1:
                val = self.maxVoltage1LineEdit.text()
            else:
                val = self.maxVoltage2LineEdit.text()
            if(val == None):
                raise Exception()
            setPowerSupplyVoltage(val, self.connectedPowerSupply, output)
        except Exception as ex:
            if(isinstance(ex, ValueError)):
                self.showError("Address must be a positive float")
            else:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                self.showError(template.format(type(ex).__name__, ex.args) + "Are you sure you entered correctly")
            return

    def setCurrent(self, output):
        try:
            val = None
            if output == 1:
                val = self.maxCurrent1LineEdit.text()
            else:
                val = self.maxCurrent2LineEdit.text()

            if(val == None):
                raise Exception()
            setPowerSupplyCurrent(val, self.connectedPowerSupply, output)
        except Exception as ex:
            if(isinstance(ex, ValueError)):
                self.showError("Address must be a positive float")
            else:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                self.showError(template.format(type(ex).__name__, ex.args) + "Are you sure you entered correctly")
            return


    def showError(self, msg):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle("Error")
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()
