# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow_trying.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
                             QAction, QFileDialog, QApplication)
import sys
import subprocess
from pathlib import Path
import xml.etree.ElementTree as ET
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtCore



# # import UART functions
# sys.path.insert(0, "../UART_py3")
#
#
from eth_rx import *
from eth_tx import *
# from rad_tab import *

import time
timestr = time.strftime("%Y-%m-%d-%H%M%S")

class Ui_MainWindow(object):

    def __init__(self, eth):
        self.eth = eth
        self.val = 0
        self.val_2 = 0

    def setupUi(self, MainWindow, identifier):

        # MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(1150, 850)
        # self.centralwidget = QtWidgets.QWidget(MainWindow)

        #general printout layout
        self.logLayoutWdiget = QtWidgets.QWidget(MainWindow)
        self.logLayoutWdiget.setGeometry(QtCore.QRect(20, 550, 1100, 200))  # (left, top, width, height)
        self.logLayout = QtWidgets.QVBoxLayout(self.logLayoutWdiget)
        self.logLayout.setContentsMargins(0, 0, 0, 0)

        self.label = QtWidgets.QLabel("Run Info", self.logLayoutWdiget)
        self.logLayout.addWidget(self.label)
        self.textBrowser = QtWidgets.QTextBrowser(self.logLayoutWdiget)
        self.logLayout.addWidget(self.textBrowser)
        # MainWindow.setCentralWidget(self.centralwidget)


        # QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #tab setup
        self.tabWidget = QtWidgets.QTabWidget(MainWindow)
        self.tabWidget.setGeometry(QtCore.QRect(20, 20, 1100, 450))

        self.tab_eth_rx = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_eth_rx, "eth_rx")

        self.tab_eth_tx = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab_eth_tx, "eth_tx")


        # self.EthLayoutWidget = QtWidgets.QWidget(MainWindow)
        # self.EthLayoutWidget.setGeometry(QtCore.QRect(50, 50, 500, 500))  # (left, top, width, height)



        self.eth_rx_inst = eth_rx(self.eth, identifier)
        self.eth_rx_inst.setupUi(self.tab_eth_rx)

        self.eth_tx_inst = eth_tx(self.eth, identifier)
        self.eth_tx_inst.setupUi(self.tab_eth_tx)






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    eth = ETH_control()
    ui = Ui_MainWindow(eth)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())