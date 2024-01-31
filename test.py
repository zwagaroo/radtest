import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget)

from test_tab import CustomTab

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
        self.tabWidget.tabCloseRequested.connect(self.closeTab)
        
        # Add the QTabWidget to the layout after the Add New Tab button
        self.layout.addWidget(self.tabWidget)
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dynamic Tabs Example')
        self.addTab('Default Tab')
        self.show()

    def addTab(self, name):
        tab = CustomTab(name)
        self.tabWidget.addTab(tab, name)

    def addNewTab(self):
        dialog = TabDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            newTabName = dialog.getNewTabName()
            if newTabName:
                self.addTab(newTabName)

    def closeTab(self, index):
        self.tabWidget.removeTab(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())
