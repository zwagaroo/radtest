#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# pyqt modules
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
# plotting
from pyqtgraph import PlotWidget, plot, mkPen
import pyqtgraph as pg
# miscellaneous modules
import sys
import os
from main_funcs import *
from Ui_MainWindow import *
from ETH_CMD_BASE import *


# In[ ]:


class MyWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MyWindow, self).__init__(*args, **kwargs)
        self.setObjectName("GUI")
        self.resize(1500, 1000)
        self.initUI()
        return							#create window

    # noinspection PyAttributeOutsideInit
    def initUI(self):								#create tabs for PS
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(20, 20, 1450, 950))

        # self.tab_func = QtWidgets.QWidget(self)
        # self.tabWidget.addTab(self.tab_func, "Functionality GUI")
        self.tab_powersup = QtWidgets.QWidget(self)
        self.tabWidget.addTab(self.tab_powersup, "Power Supply GUI")

        ''' # CSM
        self.tabCSM = QtWidgets.QTabWidget(self.tab_func)
        self.tabCSM.setGeometry(QtCore.QRect(20, 20, 1450, 950))
        self.CSM = QtWidgets.QWidget(self)
        self.tabCSM.addTab(self.CSM, "CSM Board")
        self.eth = ETH_control("enp0s20f0u6")          #user input for ethernet?
        self.csmui = Ui_MainWindow(self.eth)
        self.csmui.setupUi(self.CSM, '1, ')
        '''
        # Power Supply
        self.tabPS = QtWidgets.QTabWidget(self.tab_powersup)
        self.tabPS.setGeometry(QtCore.QRect(20, 20, 1450, 950))

        self.ps_tab_inst = MyWindowPS()
        self.ps_tab_inst.initUI(self.tabPS, '3, ')


# In[ ]:


    def normalOutputWritten(self, text):
            if len(text) > 24:
                if text[21:24] == '0, ':
                    pass
                elif text[21:24] == '1, ':
                    pass
                elif text[21:24] == '2, ':
                    pass
                elif text[21:24] == '3, ':
                    text = text[:21] + text[24:] + '\n'
                    self.ps_tab_inst.textBrowser.moveCursor(QtGui.QTextCursor.End)
                    self.ps_tab_inst.textBrowser.insertPlainText(text)
                    self.logfile = open('lansce_beamrun_PowerSupply.txt', 'a')          #write data to log file
                    self.logfile.write(text)
        
    def closeEvent(self, event):
        close = QMessageBox.question(self,
                                     "QUIT",
                                     "Sure?",
                                      QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            for v in instrument_connections.values():
                v.write('INST:SEL OUT{}'.format(1))
                v.write('OUTP OFF')
                v.write('INST:SEL OUT{}'.format(2))
                v.write('OUTP OFF')
                v.close();
            rm.close();

                
            event.accept()
        else:
            event.ignore()

# In[ ]:


class OutLog:
    def __init__(self, edit, out=None, color=None):
        """(edit, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        self.edit = edit
        self.out = out
        self.color = color

    def write(self, m):
        # if self.color:
        #     tc = self.edit.textColor()
        #     self.edit.setTextColor(self.color)
        # e = datetime.datetime.now()
        # m = "%s %s %s %s:%s:%s>>" %(e.month, e.day, e.year, e.hour, e.minute, e.second) + m
        # m = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ">>" + m
        self.edit.moveCursor(QtGui.QTextCursor.End)
        if m == '\n':
            self.edit.insertPlainText(m)
        else:
            self.edit.insertPlainText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ">>")
            self.edit.insertPlainText(m)
        # if self.color:
        #     self.edit.setTextColor(tc)
        if self.out:
            self.out.write(m)


# In[ ]:


class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        if text == '\n':
            text = text
        else:
            text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ">>" + text
        self.textWritten.emit(str(text))

    def flush(self):
        pass

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.stdout = EmittingStream(textWritten=win.normalOutputWritten)
    sys.exit(app.exec_())

window()

