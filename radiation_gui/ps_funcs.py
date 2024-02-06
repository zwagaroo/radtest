#!/usr/bin/env python
# coding: utf-8

import pyvisa 
import time 
import sys 
import os 
import scanf


instrument_connections = {}

rm = pyvisa.ResourceManager();

def get_instrument_connection(address):
    # Check if the connection already exists

    if address in instrument_connections:
        return instrument_connections[address]

    # If not, create a new connection
    instrument = rm.open_resource(address)

    # Store the connection in the dictionary
    instrument_connections[address] = instrument
    print("sucess")

    return instrument


def comm(addr, volt1 = None, curr1= None, volt2 = None, curr2 = None):                               #establish connection with GPIB with resource manager for PS
    addr = int(addr) #turn argument into integer1
    #resource = rm.list_resources() # Returns a tuple of all connected devices matching query

    gpib_inst = get_instrument_connection('GPIB0::{}::INSTR'.format(addr)) #access resource manager for gpib, create insturment object, use USB0 for usb

    gpib_inst.write('INST:COUP:TRIG OFF')
    h =gpib_inst.query('INST:COUP:TRIG?')

    #could hardcode different appl variables for different outputs? INST:SEL OUT{1}
    volt = [volt1, volt2]
    curr = [curr1, curr2]

    if(volt1 is not None):
        i = 0
        j = i + 1

        inst = gpib_inst.write('INST:SEL OUT{}'.format(j))

        instq = gpib_inst.query('INST:SEL?') 
       # appl = igpib_inst.write('APPL 7.0, 2.0')        
        appl = gpib_inst.write('APPL ' + str(volt[i]) + ', ' + str(curr[i]))
        
        applq = gpib_inst.query('APPL?')
    else:
        inst = gpib_inst.write('INST:SEL OUT{}'.format(1))

        instq = gpib_inst.query('INST:SEL?') 
       # appl = igpib_inst.write('APPL 7.0, 2.0')        
        appl = gpib_inst.write('APPL ' + str(0) + ', ' + str(0))
        
        applq = gpib_inst.query('APPL?')
    
    if(volt2 is not None):
        i = 1
        j = i + 1

        inst = gpib_inst.write('INST:SEL OUT{}'.format(j))

        instq = gpib_inst.query('INST:SEL?') 
       # appl = igpib_inst.write('APPL 7.0, 2.0')        
        appl = gpib_inst.write('APPL ' + str(volt[i]) + ', ' + str(curr[i]))
        
        applq = gpib_inst.query('APPL?')
    else:
        inst = gpib_inst.write('INST:SEL OUT{}'.format(2))

        instq = gpib_inst.query('INST:SEL?') 
       # appl = igpib_inst.write('APPL 7.0, 2.0')        
        appl = gpib_inst.write('APPL ' + str(0) + ', ' + str(0))
        
        applq = gpib_inst.query('APPL?')


    if(volt1 is None and volt2 is None):
        raise Exception("both none")
    
    return gpib_inst

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

