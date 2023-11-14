from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from TDC_config_low_level_function import *
from crc8_D81 import *
from StyleSheet import *
import time
import datetime


class rad_tab(object):
    """docstring for rad_tab"""

    def __init__(self, MainWindow, TDC_inst):
        self.TDC_inst = TDC_inst
        self.refresh_rate = 1
        self.processing = False
        self.setup_UI(MainWindow)
        self.time_total = 0
        self.time_last = 0
        self.SEU_count = 0
        

    def setup_UI(self, MainWindow):
        
        self.gridLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 300, 200))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        #CRC_cal
        self.label = QtWidgets.QLabel()
        self.label.setText("CRC_cal")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_CRC_cal = QtWidgets.QLabel()
        self.gridLayout.addWidget(self.label_CRC_cal, 0, 1, 1, 1)
        self.label_CRC_cal.setText(crc_cal(self.TDC_inst))

        #CRC
        self.label = QtWidgets.QLabel()
        self.label.setText("CRC_JTAG")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_CRC_JTAG = QtWidgets.QLabel()
        self.gridLayout.addWidget(self.label_CRC_JTAG, 1, 1, 1, 1)
        self.label_CRC_JTAG.setText(format(int(self.TDC_inst.CRC[0], 2), '08X'))   

        #CRC status
        # instruction error
        self.label = QtWidgets.QLabel()
        self.label.setText("CRC_Status")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.label_CRC_status = QtWidgets.QLabel()
        self.gridLayout.addWidget(self.label_CRC_status, 2, 1, 1, 1)
        self.label_CRC_status.setStyleSheet(LedRed)

        #update_CRC
        self.pushButton_update_CRC = QtWidgets.QPushButton()
        self.pushButton_update_CRC.setText("Update CRC")
        self.gridLayout.addWidget(self.pushButton_update_CRC,3,0,1,1)
        self.pushButton_update_CRC.clicked.connect(self.update_CRC)

        #TRST
        self.pushButton_TRST = QtWidgets.QPushButton()
        self.pushButton_TRST.setText("TRST")
        self.gridLayout.addWidget(self.pushButton_TRST,3,1,1,1)
        self.pushButton_TRST.clicked.connect(self.TRST)

        #CRC_monitor start
        self.pushButton_start_monitor = QtWidgets.QPushButton()
        self.pushButton_start_monitor.setText("Start Monitoring")
        self.gridLayout.addWidget(self.pushButton_start_monitor,4,0,1,1)
        self.pushButton_start_monitor.clicked.connect(self.start_monitor)
        #CRC_monitor stop
        self.pushButton_stop_monitor = QtWidgets.QPushButton()
        self.pushButton_stop_monitor.setText("Stop Monitoring")
        self.gridLayout.addWidget(self.pushButton_stop_monitor,4,1,1,1)
        self.pushButton_stop_monitor.clicked.connect(self.stop_monitor)

        #enable hit SEU
        self.label = QtWidgets.QLabel()
        self.label.setText("Hit SEU enable")
        self.gridLayout.addWidget(self.label, 5, 0, 1, 1)

        self.checkBox_enable_hit_SEU = QtWidgets.QCheckBox()
        self.checkBox_enable_hit_SEU.setChecked(False)
        self.gridLayout.addWidget(self.checkBox_enable_hit_SEU,5,1,1,1)
        self.checkBox_enable_hit_SEU.stateChanged.connect(self.hit_SEU)


        self.gridLayoutWidget2 = QtWidgets.QWidget(MainWindow)
        self.gridLayoutWidget2.setGeometry(QtCore.QRect(400, 20, 200, 150))
        self.gridLayout2 = QtWidgets.QGridLayout(self.gridLayoutWidget2)
        self.gridLayout2.setContentsMargins(0, 0, 0, 0)

        # time elapsed
        self.label = QtWidgets.QLabel()
        self.label.setText("Time elapsed total")
        self.gridLayout2.addWidget(self.label, 0, 0, 1, 1)

        self.label_time_total = QtWidgets.QLabel()
        self.label_time_total.setText("0:00:00")
        self.gridLayout2.addWidget(self.label_time_total, 0, 1, 1, 1)

        self.label = QtWidgets.QLabel()
        self.label.setText("Last time")
        self.gridLayout2.addWidget(self.label, 1, 0, 1, 1)

        self.label_time_last = QtWidgets.QLabel()
        self.label_time_last.setText("0:00:00")
        self.gridLayout2.addWidget(self.label_time_last, 1, 1, 1, 1)

         # SEE COUNT
        self.label = QtWidgets.QLabel()
        self.label.setText("SEE total")
        self.gridLayout2.addWidget(self.label, 2, 0, 1, 1)

        self.label_see_total = QtWidgets.QLabel()
        self.label_see_total.setText("0")
        self.gridLayout2.addWidget(self.label_see_total, 2, 1, 1, 1)

        #CRC_monitor start
        self.pushButton_clear_all = QtWidgets.QPushButton()
        self.pushButton_clear_all.setText("Clear all")
        self.gridLayout2.addWidget(self.pushButton_clear_all,3,0,1,1)
        self.pushButton_clear_all.clicked.connect(self.clear_all)



    def update_CRC(self):
        self.TDC_inst.read_status_0()
        crc_cal_tmp = crc_cal(self.TDC_inst)
        # print(crc_cal_tmp)
        crc_jtag = format(int(self.TDC_inst.CRC[0], 2), '08X')
        # print(crc_jtag)
        self.label_CRC_cal.setText(crc_cal_tmp)
        self.label_CRC_JTAG.setText(crc_jtag)
        self.label_CRC_status.setStyleSheet(LedGreen if crc_cal_tmp==crc_jtag else LedRed)

    def start_monitor(self):    

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker(self)
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Step 6: Start the thread
        self.thread.start()
        self.pushButton_start_monitor.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.pushButton_start_monitor.setEnabled(True)
        )

    def stop_monitor(self):
        self.processing = False

    #TRST button
    def TRST(self):
        # self.TDC_inst.reset_all_reg()
        trst_0(self.TDC_inst.ser)
        trst_1(self.TDC_inst.ser)

    def rewrite_SETUP0(self):
        str_GUI = ''
        for s in self.TDC_inst.setup_0:
            str_GUI = str_GUI + ''.join(s)
        str_JTAG = self.TDC_inst.update_setup_0()
        count,str_xor = self.str_XOR(str_GUI,str_JTAG)
        if count:
            self.SEU_count += count
            self.label_see_total.setText(str(self.SEU_count))
            print("SETUP0 XOR: "+str_xor)
            print("SEU_count = "+str(self.SEU_count))

    def rewrite_SETUP1(self):
        str_GUI = ''
        for s in self.TDC_inst.setup_1:
            str_GUI = str_GUI + ''.join(s)
        str_JTAG = self.TDC_inst.update_setup_1()
        count,str_xor = self.str_XOR(str_GUI,str_JTAG)
        if count:
            self.SEU_count += count
            self.label_see_total.setText(str(self.SEU_count))
            print("SETUP1 XOR: "+str_xor)
            print("SEU_count = "+str(self.SEU_count))

    def rewrite_SETUP2(self):
        str_GUI = ''
        for s in self.TDC_inst.setup_2:
            str_GUI = str_GUI + ''.join(s)
        str_JTAG = self.TDC_inst.update_setup_2()
        count,str_xor = self.str_XOR(str_GUI,str_JTAG)
        if count:
            self.SEU_count += count
            self.label_see_total.setText(str(self.SEU_count))
            print("SETUP2 XOR: "+str_xor)
            print("SEU_count = "+str(self.SEU_count))

    def rewrite_CONTROL0(self):
        str_GUI = ''
        for s in self.TDC_inst.control_0:
            str_GUI = str_GUI + ''.join(s)
        str_JTAG = self.TDC_inst.update_control_0()
        count,str_xor = self.str_XOR(str_GUI,str_JTAG)
        if count:
            self.SEU_count += count
            self.label_see_total.setText(str(self.SEU_count))
            print("CONTROL0 XOR: "+str_xor)
            print("SEU_count = "+str(self.SEU_count))

    def rewrite_CONTROL1(self):
        str_GUI = ''
        for s in self.TDC_inst.control_1:
            str_GUI = str_GUI + ''.join(s)
        str_JTAG = self.TDC_inst.update_control_1()
        count,str_xor = self.str_XOR(str_GUI,str_JTAG)
        if count:
            self.SEU_count += count
            self.label_see_total.setText(str(self.SEU_count))
            print("CONTROL1 XOR:"+str_xor)
            print("SEU_count = "+str(self.SEU_count))

    def rewrite_JTAG(self):
        hit_stop(self.TDC_inst.ser)
        # self.checkBox_enable_hit_SEU.setChecked(False)     

        disable_bcr(self.TDC_inst.ser)
        print("Hit stopped!")
        print("Hit SEU disabled!")
        # time.sleep(3)
        self.rewrite_SETUP0()
        self.rewrite_SETUP1()
        self.rewrite_SETUP2()
        self.rewrite_CONTROL0()
        self.rewrite_CONTROL1()
        hit_start(self.TDC_inst.ser)
        print("Hit started!")
        time.sleep(1)
        # self.checkBox_enable_hit_SEU.setChecked(True)
        enable_bcr(self.TDC_inst.ser)
        print("Hit SEU enabled!")
        time.sleep(1)

    def str_XOR(self, str1, str2):
        str_xor = ''
        count_1 = 0
        if(len(str1)==len(str2)):
            if(str1==str2):
                return 0,''
            else:
                for i in range(len(str1)):
                    if str1[i]==str2[i]:
                        str_xor += '0'
                    else:
                        str_xor += '1'
                        count_1 += 1
                return count_1,str_xor
        else:
            print("Error: string length not equal!")


    def clear_all(self):
        self.time_total = 0
        self.time_last = 0
        self.SEU_count = 0
        self.label_time_total.setText("0:00:00")
        self.label_time_last.setText("0:00:00")
        self.label_see_total.setText(str(self.SEU_count))


    def hit_SEU(self):
        if self.checkBox_enable_hit_SEU.isChecked() == True:
            enable_bcr(self.TDC_inst.ser)
            print("Hit SEU enabled!")
        else:
            disable_bcr(self.TDC_inst.ser)
            print("Hit SEU disabled!")


class Worker(QObject):
    """docstring for Worker"""

    finished = pyqtSignal()

    def __init__(self, rad_tab):
        super(Worker, self).__init__()
        self.rad_tab = rad_tab

    def run(self):   
        self.rad_tab.update_CRC() 
        self.rad_tab.time_last = 0   
        self.rad_tab.processing = True        
        time_accu =  self.rad_tab.time_total
        crc_cal_tmp = crc_cal(self.rad_tab.TDC_inst)  
        print("Monitoring JTAG CRC started!") 
        start = time.time()
        while self.rad_tab.processing:
            self.rad_tab.TDC_inst.read_status_0()
            crc_jtag = format(int(self.rad_tab.TDC_inst.CRC[0], 2), '08X')
            self.rad_tab.label_CRC_JTAG.setText(crc_jtag)
            if crc_cal_tmp==crc_jtag:
                self.rad_tab.label_CRC_status.setStyleSheet(LedGreen)
            else:
                # do a second CRC readback, in case UART transmission error recognized as SEE
                self.rad_tab.TDC_inst.read_status_0()
                crc_jtag = format(int(self.rad_tab.TDC_inst.CRC[0], 2), '08X')                
                if crc_cal_tmp!=crc_jtag:
                    self.rad_tab.label_CRC_status.setStyleSheet(LedRed)                    
                    self.rad_tab.rewrite_JTAG()
            time.sleep(10)
            end = time.time()
            self.rad_tab.time_last = end-start
            self.rad_tab.time_total = time_accu + self.rad_tab.time_last
            self.rad_tab.label_time_last.setText(str(datetime.timedelta(seconds=self.rad_tab.time_last))[:11])
            self.rad_tab.label_time_total.setText(str(datetime.timedelta(seconds=self.rad_tab.time_total))[:11])
        print("Monitoring stopped.")        
        print("Monitoring time: " +str(end-start))
        self.finished.emit()






    

    


        




