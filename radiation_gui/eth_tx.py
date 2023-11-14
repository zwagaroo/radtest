from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from ETH_CMD_BASE import *
import random
import time

class eth_tx(object):
    """docstring for eth_tx"""

    def __init__(self,eth,identifier):
        self.eth = eth
        self.jtaglooping = 0
        self.identifier = identifier
        # print(self.eth.rst_chk_tms_s)

    def setupUi(self, MainWindow):
        self.gridLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(400, 0, 400, 250))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        row = 0

        label = QtWidgets.QLabel("DST_MAC_ADDR", self.gridLayoutWidget)
        self.gridLayout.addWidget(label, row, 0, 1, 1)
        self.lineEdit_DST_MAC_ADDR = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit_DST_MAC_ADDR,row,1,1,1)
        self.lineEdit_DST_MAC_ADDR.setText(self.eth.DST_MAC_ADDR[0])
        self.lineEdit_DST_MAC_ADDR.setMaxLength(12)
        self.lineEdit_DST_MAC_ADDR.editingFinished.connect(self.update_eth)
        self.lineEdit_DST_MAC_ADDR.editingFinished.connect(lambda: self.print_str(self.identifier + 'DST_MAC_ADDR=' + \
                                                                                   self.lineEdit_DST_MAC_ADDR.text()))
        row += 1        

        label = QtWidgets.QLabel("SRC_MAC_ADDR", self.gridLayoutWidget)
        self.gridLayout.addWidget(label, row, 0, 1, 1)
        self.lineEdit_SRC_MAC_ADDR = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit_SRC_MAC_ADDR, row, 1, 1, 1)
        self.lineEdit_SRC_MAC_ADDR.setText(self.eth.SRC_MAC_ADDR[0])
        self.lineEdit_SRC_MAC_ADDR.setMaxLength(12)
        self.lineEdit_SRC_MAC_ADDR.editingFinished.connect(self.update_eth)
        self.lineEdit_SRC_MAC_ADDR.editingFinished.connect(lambda: self.print_str(self.identifier + 'SRC_MAC_ADDR=' + \
                                                                                  self.lineEdit_SRC_MAC_ADDR.text()))
        row += 1

        label = QtWidgets.QLabel("sent_loop_interval", self.gridLayoutWidget)
        self.gridLayout.addWidget(label, row, 0, 1, 1)
        self.lineEdit_sent_loop_interval = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.gridLayout.addWidget(self.lineEdit_sent_loop_interval, row, 1, 1, 1)
        self.lineEdit_sent_loop_interval.setMaxLength(4)
        self.lineEdit_sent_loop_interval.setText(self.eth.sent_loop_interval[0])
        self.lineEdit_sent_loop_interval.editingFinished.connect(self.update_fake)
        self.lineEdit_sent_loop_interval.editingFinished.connect(lambda: self.print_str(self.identifier + 'sent_loop_interval=' + \
                                                                            str(self.lineEdit_sent_loop_interval.text())))
        row += 1

        label = QtWidgets.QLabel("use_ETH_CMD", self.gridLayoutWidget)
        self.gridLayout.addWidget(label, row, 0, 1, 1)
        self.checkBox_use_ETH_CMD = QtWidgets.QCheckBox()
        self.gridLayout.addWidget(self.checkBox_use_ETH_CMD, row, 1, 1, 1)
        self.checkBox_use_ETH_CMD.setChecked(self.eth.use_ETH_CMD[0]!='0')
        self.checkBox_use_ETH_CMD.stateChanged.connect(self.update_cc)
        self.checkBox_use_ETH_CMD.stateChanged.connect(lambda: self.print_str(self.identifier + 'use_eth_cmd=' + \
                                                                            str(self.checkBox_use_ETH_CMD.isChecked())))
        row += 1

        label = QtWidgets.QLabel("global_rst", self.gridLayoutWidget)
        self.gridLayout.addWidget(label, row, 0, 1, 1)
        self.checkBox_global_rst = QtWidgets.QCheckBox()
        self.gridLayout.addWidget(self.checkBox_global_rst, row, 1, 1, 1)
        self.checkBox_global_rst.setChecked(self.eth.global_rst[0]!='0')
        self.checkBox_global_rst.stateChanged.connect(self.update_cc)
        self.checkBox_global_rst.stateChanged.connect(lambda: self.print_str(self.identifier + 'global_rst=' +\
                                                                            str(self.checkBox_global_rst.isChecked())))
        row += 1        

        label = QtWidgets.QLabel("sent_config_back", self.gridLayoutWidget)
        self.gridLayout.addWidget(label, row, 0, 1, 1)
        self.checkBox_sent_config_back = QtWidgets.QCheckBox()
        self.gridLayout.addWidget(self.checkBox_sent_config_back, row, 1, 1, 1)
        self.checkBox_sent_config_back.setChecked(self.eth.sent_config_back[0]!='0')
        self.checkBox_sent_config_back.stateChanged.connect(self.update_cc)
        self.checkBox_sent_config_back.stateChanged.connect(lambda: self.print_str(self.identifier + 'sent_config_back=' +\
                                                                            str(self.checkBox_sent_config_back.isChecked())))
        row += 1        
        row += 1

        label = QtWidgets.QLabel("sent_config_CMD", self.gridLayoutWidget)
        self.gridLayout.addWidget(label, row, 0, 1, 1)
        self.lineEdit_sent_config_CMD = QtWidgets.QLineEdit()
        self.gridLayout.addWidget(self.lineEdit_sent_config_CMD, row, 1, 1, 1)
        self.lineEdit_sent_config_CMD.setText(self.eth.sent_config_CMD[0])
        self.lineEdit_sent_config_CMD.setMaxLength(4)
        self.lineEdit_sent_config_CMD.editingFinished.connect(self.update_cc)
        self.lineEdit_sent_config_CMD.editingFinished.connect(lambda: self.print_str(self.identifier + 'sent_config_CMD=' + \
                                                                            str(self.lineEdit_sent_config_CMD.text())))
        row += 1        

        label = QtWidgets.QLabel("sent_once", self.gridLayoutWidget)
        self.gridLayout.addWidget(label, row, 0, 1, 1)
        self.checkBox_sent_once = QtWidgets.QCheckBox()
        self.gridLayout.addWidget(self.checkBox_sent_once, row, 1, 1, 1)
        self.checkBox_sent_once.setChecked(self.eth.sent_once[0]!='0')
        self.checkBox_sent_once.stateChanged.connect(self.update_fake)
        self.checkBox_sent_once.stateChanged.connect(lambda: self.print_str(self.identifier + 'sent_once=' +\
                                                                            str(self.checkBox_sent_once.isChecked())))
        row += 1

        label = QtWidgets.QLabel("sent_loop", self.gridLayoutWidget)
        self.gridLayout.addWidget(label, row, 0, 1, 1)
        self.checkBox_sent_loop = QtWidgets.QCheckBox()
        self.gridLayout.addWidget(self.checkBox_sent_loop, row, 1, 1, 1)
        self.checkBox_sent_loop.setChecked(self.eth.sent_loop[0]!='0')
        self.checkBox_sent_loop.stateChanged.connect(self.update_fake)
        self.checkBox_sent_loop.stateChanged.connect(lambda: self.print_str(self.identifier + 'sent_loop=' +\
                                                                            str(self.checkBox_sent_loop.isChecked())))

        row += 1

        


        self.gridLayoutWidget2 = QtWidgets.QWidget(MainWindow)
        self.gridLayoutWidget2.setGeometry(QtCore.QRect(0, 0, 400, 400))
        self.gridLayout2 = QtWidgets.QGridLayout(self.gridLayoutWidget2)
        row = 0

        # # label = QtWidgets.QLabel("multi_boot_top", self.gridLayoutWidget2)
        # label = QtWidgets.QLabel("", self.gridLayoutWidget2)
        # self.gridLayout2.addWidget(label, row, 0, 1, 1)
        # self.checkBox_multi_boot_top = QtWidgets.QCheckBox()
        # self.gridLayout2.addWidget(self.checkBox_multi_boot_top, row, 1, 1, 1)
        # self.checkBox_multi_boot_top.setChecked(self.eth.multi_boot_top[0]!='0')
        # self.checkBox_multi_boot_top.setEnabled(False)
        # # self.checkBox_multi_boot_top.stateChanged.connect(self.update)
        # # self.checkBox_multi_boot_top.stateChanged.connect(lambda: self.print_str('multi_boot_top='+\
        # #     str(self.checkBox_multi_boot_top.isChecked())))
        # row += 1

        label = QtWidgets.QLabel("rst_logic", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, row, 0, 1, 1)
        self.checkBox_rst_logic = QtWidgets.QCheckBox()
        self.gridLayout2.addWidget(self.checkBox_rst_logic, row, 1, 1, 1)
        self.checkBox_rst_logic.setChecked(self.eth.rst_logic[0]!='0')
        self.checkBox_rst_logic.stateChanged.connect(self.update)
        self.checkBox_rst_logic.stateChanged.connect(lambda: self.print_str(self.identifier+'rst_logic='+\
            str(self.checkBox_rst_logic.isChecked())))
        row += 1

        label = QtWidgets.QLabel("rst_gen_tdim", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, row, 0, 1, 1)
        self.checkBox_rst_gen_tdim = QtWidgets.QCheckBox()
        self.gridLayout2.addWidget(self.checkBox_rst_gen_tdim, row, 1, 1, 1)
        self.checkBox_rst_gen_tdim.setChecked(self.eth.rst_gen_tdim[0]!='0')
        self.checkBox_rst_gen_tdim.stateChanged.connect(self.update)
        self.checkBox_rst_gen_tdim.stateChanged.connect(lambda: self.print_str(self.identifier+'rst_gen_tdim='+\
            str(self.checkBox_rst_gen_tdim.isChecked())))
        row += 1

        label = QtWidgets.QLabel("rst_gen_tmsm", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, row, 0, 1, 1)
        self.checkBox_rst_gen_tmsm = QtWidgets.QCheckBox()
        self.gridLayout2.addWidget(self.checkBox_rst_gen_tmsm, row, 1, 1, 1)
        self.checkBox_rst_gen_tmsm.setChecked(self.eth.rst_gen_tmsm[0]!='0')
        self.checkBox_rst_gen_tmsm.stateChanged.connect(self.update)
        self.checkBox_rst_gen_tmsm.stateChanged.connect(lambda: self.print_str(self.identifier+'rst_gen_tmsm='+\
            str(self.checkBox_rst_gen_tmsm.isChecked())))
        row += 1

        label = QtWidgets.QLabel("rst_gen_tckm", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, row, 0, 1, 1)
        self.checkBox_rst_gen_tckm = QtWidgets.QCheckBox()
        self.gridLayout2.addWidget(self.checkBox_rst_gen_tckm, row, 1, 1, 1)
        self.checkBox_rst_gen_tckm.setChecked(self.eth.rst_gen_tckm[0]!='0')
        self.checkBox_rst_gen_tckm.stateChanged.connect(self.update)
        self.checkBox_rst_gen_tckm.stateChanged.connect(lambda: self.print_str(self.identifier+'rst_gen_tckm='+\
            str(self.checkBox_rst_gen_tckm.isChecked())))
        row += 1

        label = QtWidgets.QLabel("rst_gen_ttco", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, row, 0, 1, 1)
        self.checkBox_rst_gen_ttco = QtWidgets.QCheckBox()
        self.gridLayout2.addWidget(self.checkBox_rst_gen_ttco, row, 1, 1, 1)
        self.checkBox_rst_gen_ttco.setChecked(self.eth.rst_gen_ttco[0]!='0')
        self.checkBox_rst_gen_ttco.stateChanged.connect(self.update)
        self.checkBox_rst_gen_ttco.stateChanged.connect(lambda: self.print_str(self.identifier+'rst_gen_ttco='+\
            str(self.checkBox_rst_gen_ttco.isChecked())))
        row += 1

        label = QtWidgets.QLabel("rst_chk_tdo_m", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, row, 0, 1, 1)
        self.checkBox_rst_chk_tdo_m = QtWidgets.QCheckBox()
        self.gridLayout2.addWidget(self.checkBox_rst_chk_tdo_m, row, 1, 1, 1)
        self.checkBox_rst_chk_tdo_m.setChecked(self.eth.rst_chk_tdo_m[0]!='0')
        self.checkBox_rst_chk_tdo_m.stateChanged.connect(self.update)
        self.checkBox_rst_chk_tdo_m.stateChanged.connect(lambda: self.print_str(self.identifier+'rst_chk_tdo_m='+\
            str(self.checkBox_rst_chk_tdo_m.isChecked())))
        row += 1

        label = QtWidgets.QLabel("errcnt_inj", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, row, 0, 1, 1)
        self.checkBox_errcnt_inj = QtWidgets.QCheckBox()
        self.gridLayout2.addWidget(self.checkBox_errcnt_inj, row, 1, 1, 1)
        self.checkBox_errcnt_inj.setChecked(self.eth.errcnt_inj[0]!='0')
        self.checkBox_errcnt_inj.stateChanged.connect(self.update)
        self.checkBox_errcnt_inj.stateChanged.connect(lambda: self.print_str(self.identifier+'errcnt_inj='+\
            str(self.checkBox_errcnt_inj.isChecked())))
        row += 1

        label = QtWidgets.QLabel("mbt_trigger_minisas", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, row, 0, 1, 1)
        self.checkBox_mbt_trigger_minisas = QtWidgets.QCheckBox()
        self.gridLayout2.addWidget(self.checkBox_mbt_trigger_minisas, row, 1, 1, 1)
        self.checkBox_mbt_trigger_minisas.setChecked(self.eth.mbt_trigger_minisas[0]!='0')
        self.checkBox_mbt_trigger_minisas.stateChanged.connect(self.update)
        self.checkBox_mbt_trigger_minisas.stateChanged.connect(lambda: self.print_str(self.identifier+'mbt_trigger_minisas='+\
            str(self.checkBox_mbt_trigger_minisas.isChecked())))

        row += 1

        # # label = QtWidgets.QLabel("rst_sma_FE", self.gridLayoutWidget2)
        # label = QtWidgets.QLabel("", self.gridLayoutWidget2)
        # self.gridLayout2.addWidget(label, row, 0, 1, 1)
        # self.checkBox_rst_sma_FE = QtWidgets.QCheckBox()
        # self.gridLayout2.addWidget(self.checkBox_rst_sma_FE, row, 1, 1, 1)
        # self.checkBox_rst_sma_FE.setChecked(self.eth.rst_sma_FE[0]!='0')
        # self.checkBox_rst_sma_FE.setEnabled(False)
        # # self.checkBox_rst_sma_FE.stateChanged.connect(self.update)
        # # self.checkBox_rst_sma_FE.stateChanged.connect(lambda: self.print_str('rst_sma_FE='+\
        # #     str(self.checkBox_rst_sma_FE.isChecked())))
        # row += 1

        label = QtWidgets.QLabel("rst_clkdiv", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, row, 0, 1, 1)
        self.checkBox_rst_clkdiv = QtWidgets.QCheckBox()
        self.gridLayout2.addWidget(self.checkBox_rst_clkdiv, row, 1, 1, 1)
        self.checkBox_rst_clkdiv.setChecked(self.eth.rst_clkdiv[0]!='0')
        self.checkBox_rst_clkdiv.stateChanged.connect(self.update)
        self.checkBox_rst_clkdiv.stateChanged.connect(lambda: self.print_str(self.identifier+'rst_clkdiv='+\
            str(self.checkBox_rst_clkdiv.isChecked())))
        row += 1

        label = QtWidgets.QLabel("jtag_daisychain (hex)", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, row, 0, 1, 1)
        self.lineEdit_jtag_daisychain = QtWidgets.QLineEdit(self.gridLayoutWidget2)
        self.gridLayout2.addWidget(self.lineEdit_jtag_daisychain,row,1,1,1)
        self.lineEdit_jtag_daisychain.setText(bin_to_hex(self.eth.jtag_daisychain[0],5))
        self.lineEdit_jtag_daisychain.setMaxLength(5)
        self.lineEdit_jtag_daisychain.editingFinished.connect(self.update)
        self.lineEdit_jtag_daisychain.editingFinished.connect(lambda: self.print_str(self.identifier+'jtag_daisychain='+\
            self.lineEdit_jtag_daisychain.text()))
        
        row += 1

        label = QtWidgets.QLabel("rst_chk_tms_s (hex)", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, row, 0, 1, 1)
        self.lineEdit_rst_chk_tms_s = QtWidgets.QLineEdit(self.gridLayoutWidget2)
        self.gridLayout2.addWidget(self.lineEdit_rst_chk_tms_s,row,1,1,1)
        self.lineEdit_rst_chk_tms_s.setText(bin_to_hex(self.eth.rst_chk_tms_s[0],5))
        self.lineEdit_rst_chk_tms_s.setMaxLength(5)
        self.lineEdit_rst_chk_tms_s.editingFinished.connect(self.update)
        self.lineEdit_rst_chk_tms_s.editingFinished.connect(lambda: self.print_str(self.identifier+'rst_chk_tms_s='+\
            self.lineEdit_rst_chk_tms_s.text()))
        row += 1

        label = QtWidgets.QLabel("rst_chk_tck_s (hex)", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, row, 0, 1, 1)
        self.lineEdit_rst_chk_tck_s = QtWidgets.QLineEdit(self.gridLayoutWidget2)
        self.gridLayout2.addWidget(self.lineEdit_rst_chk_tck_s,row,1,1,1)
        self.lineEdit_rst_chk_tck_s.setText(bin_to_hex(self.eth.rst_chk_tck_s[0],5))
        self.lineEdit_rst_chk_tck_s.setMaxLength(5)
        self.lineEdit_rst_chk_tck_s.editingFinished.connect(self.update)
        self.lineEdit_rst_chk_tck_s.editingFinished.connect(lambda: self.print_str(self.identifier+'rst_chk_tck_s='+\
            self.lineEdit_rst_chk_tck_s.text()))

        row += 1

        label = QtWidgets.QLabel("errcnt_rst4ch (hex)", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, row, 0, 1, 1)
        self.lineEdit_errcnt_rst4ch = QtWidgets.QLineEdit(self.gridLayoutWidget2)
        self.gridLayout2.addWidget(self.lineEdit_errcnt_rst4ch,row,1,1,1)
        self.lineEdit_errcnt_rst4ch.setText(bin_to_hex(self.eth.errcnt_rst4ch[0],3))
        self.lineEdit_errcnt_rst4ch.setMaxLength(3)
        self.lineEdit_errcnt_rst4ch.editingFinished.connect(self.update)
        self.lineEdit_errcnt_rst4ch.editingFinished.connect(lambda: self.print_str(self.identifier+'errcnt_rst4ch='+\
            self.lineEdit_errcnt_rst4ch.text()))
        row += 1

        label = QtWidgets.QLabel("rst_chk_elinkttc (bin)", self.gridLayoutWidget2)
        self.gridLayout2.addWidget(label, row, 0, 1, 1)
        self.lineEdit_rst_chk_elinkttc = QtWidgets.QLineEdit(self.gridLayoutWidget2)
        self.gridLayout2.addWidget(self.lineEdit_rst_chk_elinkttc,row,1,1,1)
        self.lineEdit_rst_chk_elinkttc.setText(self.eth.rst_chk_elinkttc[0])
        self.lineEdit_rst_chk_elinkttc.setMaxLength(6)
        self.lineEdit_rst_chk_elinkttc.editingFinished.connect(self.update)
        self.lineEdit_rst_chk_elinkttc.editingFinished.connect(lambda: self.print_str(self.identifier+'rst_chk_elinkttc='+\
            self.lineEdit_rst_chk_elinkttc.text()))
        row += 1


        self.gridLayoutWidget3 = QtWidgets.QWidget(MainWindow)
        self.gridLayoutWidget3.setGeometry(QtCore.QRect(400, 300, 400, 50))
        self.gridLayout3 = QtWidgets.QGridLayout(self.gridLayoutWidget3)

        label = QtWidgets.QLabel("loop jtag", self.gridLayoutWidget3)
        self.gridLayout3.addWidget(label, 0, 0, 1, 1)
        self.checkBox_loopjtag = QtWidgets.QCheckBox()
        self.gridLayout3.addWidget(self.checkBox_loopjtag, 0, 1, 1, 1)
        self.checkBox_loopjtag.setChecked(False)
        self.checkBox_loopjtag.stateChanged.connect(self.loop_jtag_start)
        self.checkBox_loopjtag.stateChanged.connect(lambda: self.print_str(self.identifier + 'loop jtag=' +\
                                                            self.checkBox_loopjtag.isChecked()))


    def update_cc(self):
        self.eth.global_rst[0] = '1' if self.checkBox_global_rst.isChecked() else '0'
        self.eth.use_ETH_CMD[0] = '1' if self.checkBox_use_ETH_CMD.isChecked() else '0'
        self.eth.sent_config_back[0] = '1' if self.checkBox_sent_config_back.isChecked() else '0'
        self.eth.sent_config_CMD[0] = self.lineEdit_sent_config_CMD.text()
        self.eth.update_CC_CONTROL()

    def update_eth(self):
        print("updated eth")
        self.eth.DST_MAC_ADDR[0] = self.lineEdit_DST_MAC_ADDR.text()
        self.eth.SRC_MAC_ADDR[0] = self.lineEdit_SRC_MAC_ADDR.text()
        self.eth.update_ETH_CONFIG()

    def update_fake(self):
        self.eth.sent_loop_interval[0] = self.lineEdit_sent_loop_interval.text()
        self.eth.sent_loop[0] = '1' if self.checkBox_sent_loop.isChecked() else '0'
        self.eth.sent_once[0] = '1' if self.checkBox_sent_once.isChecked() else '0'
        self.eth.update_FAKE_DATA_CONTROL()



    def update(self):
        # self.eth.multi_boot_top     [0]='1' if self.checkBox_multi_boot_top     .isChecked() else '0'
        self.eth.rst_logic          [0]='1' if self.checkBox_rst_logic          .isChecked() else '0'
        self.eth.rst_gen_tdim       [0]='1' if self.checkBox_rst_gen_tdim       .isChecked() else '0'
        self.eth.rst_gen_tmsm       [0]='1' if self.checkBox_rst_gen_tmsm       .isChecked() else '0'
        self.eth.rst_gen_tckm       [0]='1' if self.checkBox_rst_gen_tckm       .isChecked() else '0'
        self.eth.rst_gen_ttco       [0]='1' if self.checkBox_rst_gen_ttco       .isChecked() else '0'
        self.eth.rst_chk_tdo_m      [0]='1' if self.checkBox_rst_chk_tdo_m      .isChecked() else '0'    
        self.eth.errcnt_inj         [0]='1' if self.checkBox_errcnt_inj         .isChecked() else '0'
        self.eth.mbt_trigger_minisas[0]='1' if self.checkBox_mbt_trigger_minisas.isChecked() else '0'
        # self.eth.rst_sma_FE         [0]='1' if self.checkBox_rst_sma_FE         .isChecked() else '0'
        self.eth.rst_clkdiv         [0]='1' if self.checkBox_rst_clkdiv         .isChecked() else '0'

        self.eth.rst_chk_tms_s      [0]=hex_to_bin(self.lineEdit_rst_chk_tms_s.text(),18)
        self.eth.errcnt_rst4ch      [0]=hex_to_bin(self.lineEdit_errcnt_rst4ch.text(),11)
        self.eth.rst_chk_tck_s      [0]=hex_to_bin(self.lineEdit_rst_chk_tck_s.text(),18)
        self.eth.rst_chk_elinkttc   [0]=self.lineEdit_rst_chk_elinkttc.text()
        self.eth.jtag_daisychain    [0]=hex_to_bin(self.lineEdit_jtag_daisychain.text(),18)
        self.eth.update_VIO_CONTROL()



    def print_str(self,string):
        print(string)

    def random_bin_str(self,bit):
        string = ''
        for i in range(bit):
            string+=str(random.randint(0,1))
        return string


    def loop_jtag_chain(self):
        # self.lineEdit_jtag_daisychain.setText(bin_to_hex(self.random_bin_str(18),5))
        # print("JTAG daisy chain now = "+hex_to_bin(self.lineEdit_jtag_daisychain.text(),18))
        # self.eth.jtag_daisychain[0]=hex_to_bin(self.lineEdit_jtag_daisychain.text(),18)
        self.eth.jtag_daisychain[0]=self.random_bin_str(18)
        self.eth.update_VIO_CONTROL()

    def loop_jtag_start(self):
        if self.checkBox_loopjtag.isChecked():
            self.jtaglooping = 1
            # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = Worker_loopjtag(self, self.identifier)
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            self.thread.started.connect(self.worker.run)
            self.worker.update_GUI.connect(self.vio_update)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            # Step 6: Start the thread
            self.thread.start()
        else:
            self.jtaglooping = 0

    def vio_update(self):
        self.lineEdit_jtag_daisychain.setText(bin_to_hex(self.eth.jtag_daisychain[0],5))
        print(self.identifier+"JTAG daisy chain now = "+self.eth.jtag_daisychain[0])



class Worker_loopjtag(QObject):
    """docstring for Worker"""

    finished = pyqtSignal()
    update_GUI = pyqtSignal()

    def __init__(self, eth_tx, identifier):
        super(Worker_loopjtag, self).__init__()
        self.eth_tx = eth_tx
        self.identifier = identifier

    def run(self): 
        print(self.identifier+"Start to loop jtag randomly!")
        while(self.eth_tx.jtaglooping):
            if self.eth_tx.eth.tdo_finding_inprogress==0:
                self.eth_tx.loop_jtag_chain()
                self.update_GUI.emit()
            time.sleep(300)
        self.finished.emit()
        print(self.identifier+"Jtag random loop stopped!")






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    eth = ETH_control()
    ui = eth_tx(eth)
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
        
