import sys
from PyQt5.QtWidgets import (QApplication, QDialog, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QHBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PyQt5.QtCore import QThreadPool
from PyQt5.QtCore import QRunnable, pyqtSignal, QObject
import random


class DataSignals(QObject):
    data_signal = pyqtSignal(np.ndarray)

class DataThread(QRunnable):
    
    def __init__(self):
        super(DataThread, self).__init__()
        self.signals = DataSignals()
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            # Generate random data
            data = np.random.rand(100)  # 100 pieces of random data
            self.signals.data_signal.emit(data)
            QThread.msleep(1000) # Update every second

    def stop(self):
        self.running = False
        self.wait()

class CustomTab(QWidget):
    def __init__(self, name, parent=None):
        super(CustomTab, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.dataThread = DataThread()  # Initialize the thread
        self.dataThread.signals.data_signal.connect(self.updateGraph)

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
        if not self.dataThread.running:
            QThreadPool.globalInstance().start(self.dataThread)

    def stopMonitoring(self):
        self.dataThread.stop()

    def updateGraph(self, data):
        self.ax1.clear()
        self.ax1.plot(data)
        self.ax1.set_title('Graph 1: Latest 100 Data Points')
        self.graph1.draw()
