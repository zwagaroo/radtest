#!/usr/bin/env python
# coding: utf-8

import pyvisa 
import time 
import sys 
import os 
import scanf
from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QMutexLocker

instrument_connections = {}

instrument_mutexes = {}

rm = pyvisa.ResourceManager()

GPIB_MUTEX = QMutex()

def get_instrument_connection(address):
    # Check if the connection already exists


    if address in instrument_connections:
        return instrument_connections[address]

    # If not, create a new connection

    gpib_address = 'GPIB0::{}::INSTR'.format(address)
    instrument = rm.open_resource(gpib_address)


    # Store the connection in the dictionary
    instrument_connections[address] = instrument
    instrument_mutexes[address] = QMutex()

    return instrument

def setPowerSupplyVoltage(val, address, output):
    inst = get_instrument_connection(address)
    with QMutexLocker(instrument_mutexes[address]):
        inst.write('INST:SEL OUT{}'.format(output))
        inst.write('VOLT ' + val)

def setPowerSupplyCurrent(val, address, output):
    inst = get_instrument_connection(address)
    with QMutexLocker(instrument_mutexes[address]):
        inst.write('INST:SEL OUT{}'.format(output))
        inst.write('CURR ' + val)


def powerOn(address):
    inst = get_instrument_connection(address)
    with QMutexLocker(instrument_mutexes[address]):
        inst.write('OUTP ON')

def powerOff(address):
    inst = get_instrument_connection(address)
    with QMutexLocker(instrument_mutexes[address]):
        inst.write('OUTP OFF')

def getOutputData(address):
    inst = get_instrument_connection(address)
    with QMutexLocker(instrument_mutexes[address]):
        inst.write('INST:SEL OUT1')
        volt1 = inst.query('MEAS:VOLT?')
        curr1 = inst.query('MEAS:CURR?')

        inst.write('INST:SEL OUT2')

        volt2 = inst.query('MEAS:VOLT?')
        curr2 = inst.query('MEAS:CURR?')
    return volt1, curr1, volt2, curr2

def PS_on(addr, volt1 = None, curr1 = None, volt2 = None, curr2 = None):                                   #power on 
    addr = int(addr) #turn argument into integer1

    gpib_inst = get_instrument_connection('GPIB0::{}::INSTR'.format(addr))
    for i in range(1,3):

        if(i == 1 and volt1 is None):
            continue;
        if(i == 2 and volt2 is None):
            continue;
        
        outp = gpib_inst.write('INST:SEL OUT{}'.format(i))
        outpq = gpib_inst.query('INST:SEL?')
        outp_on = gpib_inst.write('OUTP ON')
        outp_onq = gpib_inst.query('OUTP?')
        #print('INST:SEL: ', outpq, 'OUTP: ', outp_onq)
    
    #Include timer 
    #Log File: Power Supply Output ON 

def PS_off(addr, volt1 = None, curr1 =None, volt2=None, curr2= None):                                   #power off 
    addr = int(addr) #turn argument into integer1
    gpib_inst = get_instrument_connection('GPIB0::{}::INSTR'.format(addr))

    outp_off = gpib_inst.write('OUTP OFF')
    outp_offq = gpib_inst.query('OUTP?')
    #print('OUTP: ', outp_offq)

    #Include timer 
    #Log File: Power Supply Output Off 

def IV_meas(addr, volt1 = None, curr1 = None, volt2 = None, curr2 = None):
    nvolt1 = [0]
    nvolt2 = [0]
    ncurr1 = [0]
    ncurr2 = [0]
    gpib_inst = get_instrument_connection('GPIB0::{}::INSTR'.format(addr))
    if(volt1 is not None):
         
        inst1 = gpib_inst.write('INST:SEL OUT1')
        inst1q = gpib_inst.query('INST:SEL?')
        volt1 = gpib_inst.query('MEAS:VOLT?')
        nvolt1 = scanf.scanf("%f", volt1)
        #for ele in nvolt1: 
        #    print(ele)
        curr1 = gpib_inst.query('MEAS:CURR?')
        ncurr1 = scanf.scanf("%f", curr1)
        #print('INST:SEL: ', inst1q, 'VOLT: ', nvolt1[0], 'CURR: ', ncurr1[0])

    if(volt2 is not None):
        inst2 = gpib_inst.write('INST:SEL OUT2')
        inst2q = gpib_inst.query('INST:SEL?')
        volt2 = gpib_inst.query('MEAS:VOLT?')
        nvolt2 = scanf.scanf("%f", volt2)
        curr2 = gpib_inst.query('MEAS:CURR?')
        ncurr2 = scanf.scanf("%f", curr2)
        #print('INST:SEL: ', inst2q, 'VOLT: ', nvolt2[0], 'CURR: ', ncurr2[0])

    return nvolt1, nvolt2, ncurr1, ncurr2

