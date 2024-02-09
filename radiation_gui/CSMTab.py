from ETH_CMD_BASE import *
import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QCheckBox, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal, QMutex
from eth_rx import *
from eth_tx import *

class CSMTab(QWidget):
    def __init__(self, parent=None):
        super(CSMTab, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.eth = ETH_control()

        self.eth_rx_inst = eth_rx(self.eth, self)

        self.eth_rx_inst.pushButton_startEth.setEnabled(False)
        self.eth_tx_inst = eth_tx(self.eth)


        self.configurationLayout = QHBoxLayout()


        self.identifierLabel = QLabel("Identifier")
        self.configurationLayout.addWidget(self.identifierLabel)
        
        self.identifierLineEdit = QLineEdit()
        self.configurationLayout.addWidget(self.identifierLineEdit)

        self.ethAddressLabel = QLabel("Ethernet Addr")
        self.configurationLayout.addWidget(self.ethAddressLabel)
        self.ethAddressLineEdit = QLineEdit()
        self.configurationLayout.addWidget(self.ethAddressLineEdit)

        self.logPathLabel = QLabel("Log Path")
        self.configurationLayout.addWidget(self.logPathLabel)

        self.logPathLineEdit = QLineEdit()
        self.configurationLayout.addWidget(self.logPathLineEdit)

        self.setConfigurationButton = QPushButton("Set")

        self.configurationLayout.addWidget(self.setConfigurationButton)


        self.logPath = None

        def setConfigurations():
            self.eth.eth_name = self.ethAddressLineEdit.text()
            self.eth_tx_inst.identifier = self.identifierLineEdit.text()
            self.eth_rx_inst.identifier = self.identifierLineEdit.text()

            self.logPath = self.logPathLineEdit.text()

            self.eth_rx_inst.pushButton_startEth.setEnabled(True)


        self.setConfigurationButton.clicked.connect(setConfigurations)

        self.layout.addLayout(self.configurationLayout)


        self.tabWidget = QTabWidget()
        self.tab_eth_rx = QWidget()
        self.tabWidget.addTab(self.tab_eth_rx, "eth_rx")

        self.tab_eth_tx = QWidget()
        self.tabWidget.addTab(self.tab_eth_tx, "eth_tx")

        self.eth_rx_inst.setupUi(self.tab_eth_rx)

        self.eth_tx_inst.setupUi(self.tab_eth_tx)

        self.layout.addWidget(self.tabWidget)



        # self.EthLayoutWidget = QtWidgets.QWidget(MainWindow)
        # self.EthLayoutWidget.setGeometry(QtCore.QRect(50, 50, 500, 500))  # (left, top, width, height)

