import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget)

from PowerSupplyTab import PowerSupplyTab

from ps_funcs import *

class TabDialog(QDialog):
    def __init__(self, parent=None):
        super(TabDialog, self).__init__(parent)
        self.setWindowTitle('New Tab Name')
        self.layout = QVBoxLayout(self)
        self.lineEdit = QLineEdit(self)
        self.button = QPushButton('OK', self)
        self.button.clicked.connect(self.accept)
        self.layout.addWidget(self.lineEdit)
        self.layout.addWidget(self.button)

    def getNewTabName(self):
        return self.lineEdit.text()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        # Create the Add New Tab button and set its text
        self.addTabButton = QPushButton('Add New Tab')
        self.addTabButton.clicked.connect(self.addNewTab)
        
        # Add the Add New Tab button to the layout before the QTabWidget
        self.layout.addWidget(self.addTabButton)
        
        # Initialize the QTabWidget and make tabs closable
        self.tabWidget = QTabWidget(self)
        self.tabWidget.setTabsClosable(True)
        
        
        self.tabWidget.tabCloseRequested.connect(self.onTabCloseRequested)
        
        # Add the QTabWidget to the layout after the Add New Tab button
        self.layout.addWidget(self.tabWidget)
        
        self.initUI()
        self.resize(800, 600)



    def onTabCloseRequested(self, index):
        # Retrieve the widget (tab content) for the tab being closed
        widget = self.tabWidget.widget(index)

        # Perform cleanup operations for the tab
        # For example, if you have a reference to a thread in your tab widget, stop it
        if hasattr(widget, 'dataThread'):
            if(widget.dataThread is not None):
                widget.dataThread.stop()  # Assuming your thread class has a 'stop' method

        # Finally, remove the tab from the tab widget
        self.tabWidget.removeTab(index)

 

    def initUI(self):
        self.setWindowTitle('ZWs Extraordinary Power Supply Monitor')
        self.show()

    def addTab(self, name):
        tab = PowerSupplyTab(name)
        self.tabWidget.addTab(tab, name)

    def addNewTab(self):
        dialog = TabDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            newTabName = dialog.getNewTabName()
            if newTabName:
                self.addTab(newTabName)



    def closeEvent(self, event):
        # Perform cleanup for each tab before the window closes
        for i in range(self.tabWidget.count()):
            widget = self.tabWidget.widget(i)
            if hasattr(widget, 'cleanup'):
                widget.cleanup()  # Call the cleanup method for each tab

        # You can also do other necessary cleanup for the main window itself
        # ...

        event.accept()  # Accept the close event to allow the window to close


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
