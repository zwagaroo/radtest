from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from ETH_CMD_BASE import *
from StyleSheet import *
import time
import datetime


class eth_rx(object):
    """docstring for eth_rx"""

    def __init__(self, eth, identifier):
        self.eth = eth
        self.processing = False
        self.time_total = 0
        self.time_last = 0
        self.total_packet = 0
        self.identifier = identifier

    def setupUi(self, MainWindow):
        self.gridLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 400, 300))  # (top, left, width, height)
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.label_vio_list = []
        self.err_checkbox_list = []
        # for i in range (47):
        #     label = QtWidgets.QLabel("0", self.gridLayoutWidget)


        label = QtWidgets.QLabel("sem_heartbeat", self.gridLayoutWidget)
        self.gridLayout.addWidget(label, 0, 0, 1, 1)

        self.label_sem_heartbeat_led = QtWidgets.QLabel()
        self.gridLayout.addWidget(self.label_sem_heartbeat_led, 0, 1, 1, 1)
        self.label_sem_heartbeat_led.setStyleSheet(LedGray)
        self.label_vio_list.append(self.label_sem_heartbeat_led)

        label = QtWidgets.QLabel("sem_fatalerr", self.gridLayoutWidget)
        self.gridLayout.addWidget(label, 1, 0, 1, 1)
        self.label_sem_fatalerr_led = QtWidgets.QLabel()
        self.gridLayout.addWidget(self.label_sem_fatalerr_led, 1, 1, 1, 1)
        self.label_sem_fatalerr_led.setStyleSheet(LedGray)
        self.label_sem_fatalerr_led.setText('0')
        self.label_vio_list.append(self.label_sem_fatalerr_led)

        label = QtWidgets.QLabel("design_number", self.gridLayoutWidget)
        self.gridLayout.addWidget(label, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel("", self.gridLayoutWidget)
        self.gridLayout.addWidget(self.label, 2, 1, 1, 1)
        self.label_vio_list.append(self.label)


        label = QtWidgets.QLabel("locked_vio", self.gridLayoutWidget)
        self.gridLayout.addWidget(label, 3, 0, 1, 1)
        self.label_locked_vio_led = QtWidgets.QLabel()
        self.gridLayout.addWidget(self.label_locked_vio_led, 3, 1, 1, 1)
        self.label_locked_vio_led.setStyleSheet(LedGray)
        self.label_locked_vio_led.setText('1')
        self.label_vio_list.append(self.label_locked_vio_led)

        label = QtWidgets.QLabel("elink_TTCin_err", self.gridLayoutWidget)
        self.gridLayout.addWidget(label, 4, 0, 1, 1)        



        for i in range (0,6):
            label = QtWidgets.QLabel(str(5-i), self.gridLayoutWidget)
            self.gridLayout.addWidget(label, i+5, 0, 1, 1)
            self.label = QtWidgets.QLabel("", self.gridLayoutWidget)
            self.gridLayout.addWidget(self.label, i+5, 1, 1, 1)
            self.label_vio_list.append(self.label)

            self.checkbox = QtWidgets.QCheckBox()
            self.gridLayout.addWidget(self.checkbox, i+5, 2, 1, 1)
            self.checkbox.setChecked(True if self.eth.check_ttc[0][i]=='1' else False)
            self.checkbox.stateChanged.connect(self.update_checklist)
            self.err_checkbox_list.append(self.checkbox)

        self.gridLayoutWidget4 = QtWidgets.QWidget(MainWindow)
        self.gridLayoutWidget4.setGeometry(QtCore.QRect(0, 300, 300, 100))
        self.gridLayout4 = QtWidgets.QGridLayout(self.gridLayoutWidget4)

        self.pushButton_startEth = QtWidgets.QPushButton()
        self.pushButton_startEth.setText("Start eth")
        self.gridLayout4.addWidget(self.pushButton_startEth, 0, 0, 1, 1)
        self.pushButton_startEth.clicked.connect(self.start_monitor)      

        self.pushButton_stopEth = QtWidgets.QPushButton()
        self.pushButton_stopEth.setText("Stop eth")
        self.gridLayout4.addWidget(self.pushButton_stopEth, 0, 1, 1, 1)
        self.pushButton_stopEth.clicked.connect(self.stop_monitor)

        self.pushButton_clear_timer = QtWidgets.QPushButton()
        self.pushButton_clear_timer.setText("Clear all")
        self.gridLayout4.addWidget(self.pushButton_clear_timer,0,2,1,1)
        self.pushButton_clear_timer.clicked.connect(self.clear_timer)

        # time elapsed
        self.label = QtWidgets.QLabel()
        self.label.setText("Time elapsed total")
        self.gridLayout4.addWidget(self.label, 1, 0, 1, 1)

        self.label_time_total = QtWidgets.QLabel()
        self.label_time_total.setText("0:00:00")
        self.gridLayout4.addWidget(self.label_time_total, 1, 1, 1, 1)

        self.label = QtWidgets.QLabel()
        self.label.setText("Last time")
        self.gridLayout4.addWidget(self.label, 2, 0, 1, 1)

        self.label_time_last = QtWidgets.QLabel()
        self.label_time_last.setText("0:00:00")
        self.gridLayout4.addWidget(self.label_time_last, 2, 1, 1, 1)

        self.gridLayoutWidget2 = QtWidgets.QWidget(MainWindow)
        self.gridLayoutWidget2.setGeometry(QtCore.QRect(300, 0, 700, 400))
        self.gridLayout2 = QtWidgets.QGridLayout(self.gridLayoutWidget2)

        label = QtWidgets.QLabel("TDO err", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, 0, 0, 1, 1)

        label = QtWidgets.QLabel("tck_err", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, 1, 1, 1, 1)

        label = QtWidgets.QLabel("tms_err", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, 1, 3, 1, 1)

        label = QtWidgets.QLabel("tck_err", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, 1, 6, 1, 1)

        label = QtWidgets.QLabel("tms_err", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, 1, 8, 1, 1)

        for i in range(0, 18):
            if i<9:
                label = QtWidgets.QLabel('reg'+str(17 - i), self.gridLayoutWidget2)
                self.gridLayout2.addWidget(label, 2 + i, 0, 1, 1)
            else:
                label = QtWidgets.QLabel('reg'+str(17 - i), self.gridLayoutWidget2)
                self.gridLayout2.addWidget(label, 2 + i-9, 5, 1, 1)

        # tck error
        for i in range(0, 18):
            if i<9:
                self.label = QtWidgets.QLabel('', self.gridLayoutWidget2)
                self.gridLayout2.addWidget(self.label, 2 + i, 1, 1, 1)

                self.checkbox = QtWidgets.QCheckBox()
                self.gridLayout2.addWidget(self.checkbox, 2 + i, 2, 1, 1)
                

            else:
                self.label = QtWidgets.QLabel('', self.gridLayoutWidget2)
                self.gridLayout2.addWidget(self.label, 2 + i-9, 6, 1, 1)

                self.checkbox = QtWidgets.QCheckBox()
                self.gridLayout2.addWidget(self.checkbox,2 + i-9, 7, 1, 1)

            self.label_vio_list.append(self.label)
            self.checkbox.setChecked(True if self.eth.check_tck[0][i]=='1' else False)
            self.checkbox.stateChanged.connect(self.update_checklist)
            self.err_checkbox_list.append(self.checkbox)
            

        # tms error
        for i in range(0, 18):
            if i<9:
                self.label = QtWidgets.QLabel('', self.gridLayoutWidget2)
                self.gridLayout2.addWidget(self.label, 2 + i, 3, 1, 1)

                self.checkbox = QtWidgets.QCheckBox()
                self.gridLayout2.addWidget(self.checkbox, 2 + i, 4, 1, 1)
            else:
                self.label = QtWidgets.QLabel('', self.gridLayoutWidget2)
                self.gridLayout2.addWidget(self.label, 2 + i-9, 8, 1, 1)

                self.checkbox = QtWidgets.QCheckBox()
                self.gridLayout2.addWidget(self.checkbox,2 + i-9, 9, 1, 1)
            self.label_vio_list.append(self.label)
            self.checkbox.setChecked(True if self.eth.check_tms[0][i]=='1' else False)
            self.checkbox.stateChanged.connect(self.update_checklist)
            self.err_checkbox_list.append(self.checkbox)

        #tdo error
        self.label = QtWidgets.QLabel("", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(self.label, 0, 1, 1, 1)
        self.label_vio_list.append(self.label)

        self.checkbox = QtWidgets.QCheckBox()
        self.gridLayout2.addWidget(self.checkbox,0, 2, 1, 1)
        self.checkbox.setChecked(True if self.eth.check_tdo[0]=='1' else False)
        self.checkbox.stateChanged.connect(self.update_checklist)
        self.err_checkbox_list.append(self.checkbox)

        #multiboot time
        self.label = QtWidgets.QLabel("Mboot count", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(self.label, 0, 3, 1, 1)

        self.label_mboot_count = QtWidgets.QLabel("0", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(self.label_mboot_count, 0, 4, 1, 1)




    def vio_update(self):
        self.total_packet += 1
        # print('singal connect success!')
        if 0<self.total_packet<10 or self.total_packet%100==0:
            print(self.identifier+"Received "+str(self.total_packet) +" packets!")
        if 9<self.total_packet<100 and self.total_packet%10==0:
            print(self.identifier+"Received "+str(self.total_packet) +" packets!")

        self.label_vio_list[0]. setStyleSheet(LedGreen if self.eth.error_list[0]=='1' else LedGray)

        # print('fatal error label text = '+self.label_vio_list[1].text())
        # print('fatal error reg = '+self.eth.error_list[1])
        if self.label_vio_list[1].text()=='0' and self.eth.error_list[1]=='1': 
            if self.eth.multiboot_inprogress==0:
                print(self.identifier+"---FATAL ERROR!!---")
                # self.eth.multiboot_inprogress=1
                # self.multi_boot()
                # time.sleep(5)
                # self.eth.multiboot_inprogress=0

        self.label_vio_list[1].setText(self.eth.error_list[1])
        self.label_vio_list[1].setStyleSheet(LedRed if self.eth.error_list[1]=='1' else LedGray)
        self.label_vio_list[3].setStyleSheet(LedGreen if self.eth.error_list[3] == '1' else LedGray)
        self.label_time_last.setText(str(datetime.timedelta(seconds=self.time_last))[:7])
        self.label_time_total.setText(str(datetime.timedelta(seconds=self.time_total))[:7])      
        for i in range (2,47):
            if self.eth.error_list[i]!=self.label_vio_list[i].text():                                     
                if i==2:
                    self.label_vio_list[2]. setText(self.eth.error_list[2])
                    print(self.identifier+'design number changed to '+self.eth.error_list[2])
                    if self.eth.error_list[2]!='7':
                        self.eth.mboot_count += 1
                        self.label_mboot_count.setText(str(self.eth.mboot_count))
                        print(self.identifier+"Multiboot count=%d" %(self.eth.mboot_count))
                if i==3:
                    self.label_vio_list[i].setText(self.eth.error_list[i])
                    print(self.identifier+'vio locked' if self.eth.error_list[3]=='1' else self.identifier+'vio unlocked')
                if 3<i<10:                    
                    self.label_vio_list[i].setText(self.eth.error_list[i])
                    if self.eth.check_ttc[0][i-4]=='1':
                        print(self.identifier+'TTCin_err_reg_'+str(9-i)+'='+self.eth.error_list[i])
                if 9<i<28:    
                    self.label_vio_list[i].setText(self.eth.error_list[i])
                    if self.eth.check_tck[0][i-10]=='1':                        
                        print(self.identifier+'TCK_err_reg_'+str(27-i)+'='+self.eth.error_list[i])
                if 27<i<46:
                    self.label_vio_list[i].setText(self.eth.error_list[i])
                    if self.eth.check_tms[0][i-28]=='1':                    
                        print(self.identifier+'TMS_err_reg_'+str(45-i)+'='+self.eth.error_list[i])
                if i==46:
                    self.label_vio_list[i].setText(self.eth.error_list[i])
                    if self.eth.check_tdo[0]=='1':                    
                        print(self.identifier+'TDO_err_reg='+self.eth.error_list[i])


    def update_checklist(self):
        checklist_str = ''
        for i in range(43):
            checklist_str += '1' if self.err_checkbox_list[i].isChecked() else '0'
        print(self.identifier+'error_check_list now ='+checklist_str)
        self.eth.check_ttc[0] = checklist_str[0:6]
        self.eth.check_tck[0] = checklist_str[6:24]
        self.eth.check_tms[0] = checklist_str[24:42]
        self.eth.check_tdo[0] = checklist_str[42]


    def multi_boot(self):
        self.eth.check_tms[0]           = '000000000000000000'
        self.eth.check_tck[0]           = '000000000000000000'
        self.eth.check_ttc[0]           = '000000'
        self.eth.check_tdo[0]           = '0'
        self.eth.update_VIO_CONTROL()
        for i in range (10):
            print(self.identifier+"multi_boot in %d second(s)!"%(10-i))
            time.sleep(1)
        print(self.identifier+"multi_boot in progress!")
        self.eth.mbt_trigger_minisas[0] = '1'
        self.eth.update_VIO_CONTROL()
        time.sleep(2)
        self.eth.mbt_trigger_minisas[0] = '0'
        self.eth.errcnt_rst4ch     [0] = '11111111111'
        self.eth.update_VIO_CONTROL()
        time.sleep(2)
        self.eth.errcnt_rst4ch[0]       = '00000000000'
        self.update_checklist()
        self.eth.update_VIO_CONTROL()
        print(self.identifier+"multi_boot finished!")


    def start_monitor(self):    

        # Step 2: Create a QThread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker_eth_read(self,self.identifier)
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Step 6: Start the thread
        self.thread.start()
        self.pushButton_startEth.setEnabled(False)
        self.pushButton_clear_timer.setEnabled(False)
        self.thread.finished.connect(lambda: self.pushButton_startEth.setEnabled(True))
        self.thread.finished.connect(lambda: self.pushButton_clear_timer.setEnabled(True))

        self.worker.update_GUI.connect(self.vio_update)


        # Step 2: Create a QThread object
        self.thread2 = QThread()
        # Step 3: Create a worker object
        self.worker2 = Worker_find_tdo(self, self.identifier)
        # Step 4: Move worker to the thread
        self.worker2.moveToThread(self.thread2)
        # Step 5: Connect signals and slots
        self.thread2.started.connect(self.worker2.run)
        self.worker2.finished.connect(self.thread2.quit)
        self.worker2.finished.connect(self.worker2.deleteLater)
        self.thread2.finished.connect(self.thread2.deleteLater)
        # Step 6: Start the thread
        self.thread2.start()


        # Step 2: Create a QThread object
        self.thread3 = QThread()
        # Step 3: Create a worker object
        self.worker3 = Worker_error_monitor(self,self.identifier)
        # Step 4: Move worker to the thread
        self.worker3.moveToThread(self.thread3)
        # Step 5: Connect signals and slots
        self.thread3.started.connect(self.worker3.run)
        self.worker3.finished.connect(self.thread3.quit)
        self.worker3.finished.connect(self.worker3.deleteLater)
        self.thread3.finished.connect(self.thread3.deleteLater)
        # Step 6: Start the thread
        self.thread3.start()

        

    def stop_monitor(self):
        self.processing = False  

    def clear_timer(self):
        self.time_total = 0
        self.time_last = 0
        self.total_packet = 0
        self.label_time_total.setText("0:00:00")
        self.label_time_last.setText("0:00:00")

    def error_sum(self):
        total_error=0
        for i in range(4,46):
            if 3<i<10:                    
                if self.eth.check_ttc[0][i-4]=='1':
                    total_error+= int(self.eth.error_list[i])
            if 9<i<28:    
                if self.eth.check_tck[0][i-10]=='1':                        
                    total_error+= int(self.eth.error_list[i])
            if 27<i<46:
                if self.eth.check_tms[0][i-28]=='1':                    
                    total_error+= int(self.eth.error_list[i])
        return total_error

 
class Worker_eth_read(QObject):
    """docstring for Worker"""

    finished = pyqtSignal()
    update_GUI = pyqtSignal()

    def __init__(self, eth_rx, identifier):
        super(Worker_eth_read, self).__init__()
        self.eth_rx = eth_rx
        self.identifier = identifier


    def run(self):   
        self.eth_rx.time_last = 0   
        self.eth_rx.processing = True        
        time_accu =  self.eth_rx.time_total
        # crc_cal_tmp = crc_cal(self.eth_rx.TDC_inst)  
        print(self.identifier+"Monitoring error counters!")
        start = time.time()
        while self.eth_rx.processing:
            packet_full = ethread(self.eth_rx.eth.eth_name)
            decode_success = self.eth_rx.eth.vio_decode(packet_full)
            if decode_success==1:
                self.update_GUI.emit()           
            end = time.time()
            self.eth_rx.time_last = end-start
            self.eth_rx.time_total = time_accu + self.eth_rx.time_last
        print(self.identifier+"Monitoring stopped.")
        print(self.identifier+"Monitoring time: " +str(end-start))
        self.finished.emit()


class Worker_find_tdo(QObject):
    """docstring for Worker"""

    finished = pyqtSignal()


    def __init__(self, eth_rx, identifier):
        super(Worker_find_tdo, self).__init__()
        self.eth_rx = eth_rx
        self.tdo_error = int(self.eth_rx.eth.error_list[46])
        self.tdo_error_pre = int(self.eth_rx.eth.error_list[46])
        self.identifier = identifier

    def run(self): 
        time.sleep(2)  # wait for first packet to be received
        while self.eth_rx.processing:
            if self.eth_rx.eth.check_tdo[0] == '1':
                self.tdo_error_pre = self.tdo_error
                self.tdo_error = int(self.eth_rx.eth.error_list[46])
                # print('tdo_error='+str(self.tdo_error))
                # print('tdo_error_pre='+str(self.tdo_error_pre))
                time.sleep(1)  #  first packet
                self.tdo_error_pre = self.tdo_error
                self.tdo_error = int(self.eth_rx.eth.error_list[46])
                # print('tdo_error='+str(self.tdo_error))
                # print('tdo_error_pre='+str(self.tdo_error_pre))
                if self.tdo_error-self.tdo_error_pre>10000:
                    self.eth_rx.eth.tdo_finding_inprogress = 1
                    print(self.identifier+'tdo_error='+str(self.tdo_error))
                    print(self.identifier+'tdo_error_pre='+str(self.tdo_error_pre))
                    print(self.identifier+"TDO link failed! Now start to check. TTC, TCK and TMS check disabled.")
                    self.eth_rx.eth.check_tms[0]           = '000000000000000000'
                    self.eth_rx.eth.check_tck[0]           = '000000000000000000'
                    self.eth_rx.eth.check_ttc[0]           = '000000'
                    self.eth_rx.eth.check_tdo[0]           = '1'                    
                    jtag_working_chain = ''
                    for i in range (18):
                        if self.eth_rx.processing:
                            jtag_daisy_chain = ''                    
                            for j in range (18):
                                jtag_daisy_chain += '1' if i==j else '0'
                            print(self.identifier+"jtag_daisy_chain="+jtag_daisy_chain)
                            self.eth_rx.eth.jtag_daisychain[0]=jtag_daisy_chain
                            self.eth_rx.eth.update_VIO_CONTROL()
                            time.sleep(1)
                            self.tdo_error_pre = self.tdo_error
                            self.tdo_error = int(self.eth_rx.eth.error_list[46])
                            time.sleep(1)
                            self.tdo_error_pre = self.tdo_error
                            self.tdo_error = int(self.eth_rx.eth.error_list[46])
                            jtag_working_chain += '1' if self.tdo_error==self.tdo_error_pre else '0'
                    jtag_daisy_chain = '000000000000000000'
                    print(self.identifier+"jtag_working_chain="+jtag_working_chain)
                    self.eth_rx.eth.jtag_daisychain[0]=jtag_daisy_chain
                    self.eth_rx.eth.update_VIO_CONTROL()
                    self.eth_rx.eth.multiboot_inprogress = 1
                    self.eth_rx.multi_boot()
                    time.sleep(5)
                    self.eth_rx.eth.multiboot_inprogress = 0
                    self.eth_rx.eth.tdo_finding_inprogress = 0
            time.sleep(1)
        self.finished.emit()


class Worker_error_monitor(QObject):
    """docstring for Worker"""

    finished = pyqtSignal()


    def __init__(self, eth_rx, identifier):
        super(Worker_error_monitor, self).__init__()
        self.eth_rx = eth_rx
        self.all_error = 0
        self.all_error_pre = 0
        self.prepare_to_multiboot = 0
        self.identifier = identifier
        

    def run(self): 
        time.sleep(2)  # wait for first packet to be received
        while self.eth_rx.processing:
            if self.eth_rx.eth.tdo_finding_inprogress == 1:
                self.prepare_to_multiboot = 0
            self.all_error_pre = self.all_error
            self.all_error = self.eth_rx.error_sum()          
            time.sleep(1)
            self.all_error_pre = self.all_error
            self.all_error = self.eth_rx.error_sum()
            if self.all_error-self.all_error_pre>10000 or self.all_error-self.all_error_pre<0:
                data_error = 1
            else:
                data_error = 0
            if data_error==1 and self.eth_rx.eth.multiboot_inprogress ==0\
                and self.eth_rx.eth.tdo_finding_inprogress == 0:
                self.prepare_to_multiboot += 1
                print(self.identifier + "Massive errors found for %d time(s)!" %(self.prepare_to_multiboot))
            else:
                self.prepare_to_multiboot  = 0

            if self.prepare_to_multiboot>=5:
                if self.eth_rx.eth.tdo_finding_inprogress == 0:
                    self.eth_rx.eth.multiboot_inprogress = 1
                    self.eth_rx.multi_boot()
                    time.sleep(5)
                    self.eth_rx.eth.multiboot_inprogress = 0
                self.prepare_to_multiboot = 0


        self.finished.emit()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    eth = ETH_control()
    ui = eth_rx(eth)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
        
