#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from Ui_MainWindow import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import datetime
from ETH_CMD_BASE import *
# sys.path.insert(0, "../UART_py3")

import logging
from PyQt5.QtCore import *


# In[ ]:


class StartQT5(QtWidgets.QMainWindow):
    def __init__(self, eth, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow(eth)
        # self.logfile = open('log.txt','a')
        self.ui.setupUi(self)

    def normalOutputWritten(self,text):
        self.ui.textBrowser.moveCursor(QtGui.QTextCursor.End)
        self.ui.textBrowser.insertPlainText(text)
        self.logfile = open('lansce_beamrun_CSM.txt','a')
        self.logfile.write(text)
        # self.logfile = close()


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
        if m == '\n' :
            self.edit.insertPlainText(m)
        else:
            self.edit.insertPlainText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ">>")
            self.edit.insertPlainText(m)
        # if self.color:
        #     self.edit.setTextColor(tc)
        if self.out:
            self.out.write(m)

    def flush(self):
        pass


# In[ ]:


class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        if text == '\n' :
            text = text
        else:
            text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ">>" + text
        self.textWritten.emit(str(text))

    def flush(self):
        pass


# In[ ]:


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # eth = ETH_control("eno1")
    eth = ETH_control("enp0s20f0u7") #?????

    myapp = StartQT5(eth)
    myapp.show()

    # sys.stderr = OutLog(myapp.ui.textBrowser, sys.stderr)
    # sys.stdout = OutLog(myapp.ui.textBrowser, sys.stdout)
    sys.stdout = EmittingStream(textWritten=myapp.normalOutputWritten)
    # logging.basicConfig(format="%(message)s",level=logging.INFO,stream=sys.stdout)
    sys.exit(app.exec_())

