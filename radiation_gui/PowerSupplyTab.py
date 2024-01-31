import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QCheckBox, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PyQt5.QtCore import QThreadPool
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject
import random

from ps_funcs import * 


class PowerSupplyDataSignals(QObject):
    data_signal = pyqtSignal(np.ndarray)

class PowerSupplyDataThread(QRunnable):
    
    def __init__(self, data):
        super(PowerSupplyDataThread, self).__init__()
        self.signals = PowerSupplyDataSignals()
        self.running = False
        self.data = data

    def run(self):
        self.running = True
        while self.running:
            # Generate random data
            self.data = np.random.rand(100)  # 100 pieces of random data
            self.signals.data_signal.emit(self.data)
            QThread.msleep(1000) # Update every second

    def stop(self):
        self.running = False

class PowerSupplyTab(QWidget):
    def __init__(self, name, parent=None):
        super(PowerSupplyTab, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.dataThread = None
        self.data = []

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
        self.table = QTableWidget(1, 2)  # 1 row, 2 columns
        self.table.setHorizontalHeaderLabels(["Output Name", "Output Value"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setItem(0, 0, QTableWidgetItem("Example Name"))
        self.table.setItem(0, 1, QTableWidgetItem("Example Value"))
        self.layout.addWidget(self.table)

        # Existing setup code for table, graphs, and buttons...
        # Graphs setup
        self.graphLayout = QHBoxLayout()
        self.graph1 = FigureCanvas(Figure(figsize=(5, 3)))
        self.ax1 = self.graph1.figure.add_subplot(111)
        self.graph2 = FigureCanvas(Figure(figsize=(5, 3)))
        self.ax2 = self.graph2.figure.add_subplot(111)
        self.graphLayout.addWidget(self.graph1)
        self.graphLayout.addWidget(self.graph2)
        self.layout.addLayout(self.graphLayout)

        # Buttons setup
        self.buttonLayout = QHBoxLayout()
        self.monitorOnButton = QPushButton('Monitor On')
        self.monitorOffButton = QPushButton('Monitor Off')
        self.monitorOnButton.clicked.connect(self.startMonitoring)
        self.monitorOffButton.clicked.connect(self.stopMonitoring)
        self.buttonLayout.addWidget(self.monitorOnButton)
        self.buttonLayout.addWidget(self.monitorOffButton)
        self.layout.addLayout(self.buttonLayout)

    def startMonitoring(self):
        if (self.dataThread is None) or (not self.dataThread.running):
            self.dataThread = PowerSupplyDataThread(self.data)  # Initialize the thread
            self.dataThread.setAutoDelete(True);
            self.dataThread.signals.data_signal.connect(self.updateGraph)
            QThreadPool.globalInstance().start(self.dataThread)

    def stopMonitoring(self):
        self.dataThread.stop()

    def updateGraph(self, data):
        self.ax1.clear()
        self.ax1.plot(data)
        self.ax1.set_title('Graph 1: Latest 100 Data Points')
        self.graph1.draw()

    def connect(self):

        try:
            print(self.powerSupplyAddrLineEdit.text())
            self.connectedPowerSupply = int(self.powerSupplyAddrLineEdit.text())
            get_instrument_connection(self.connectedPowerSupply)
            self.connectButton.setEnabled(False)
        except Exception as ex:
            if(isinstance(ex, ValueError)):
                self.showError("Address must be a positive integer")
            else:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                self.showError(template.format(type(ex).__name__, ex.args) + "Are you sure the powersupply is connected?")
            return

    def showError(self, msg):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle("Error")
        msgBox.setText(msg)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()
