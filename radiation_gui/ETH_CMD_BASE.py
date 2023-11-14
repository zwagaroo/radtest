"""Demonstrates how to construct and send raw Ethernet packets on the
network.
You probably need root privs to be able to bind to the network interface,
e.g.:
    $ sudo python sendeth.py
"""

import time
import binascii
# import common

from socket import *

def ethread(interface= 'enp0s20f0u7'):
    s = socket(AF_PACKET, SOCK_RAW)
    s.bind((interface, 4))
    packet = binascii.hexlify(s.recv(150)).decode()
    return packet

def sendeth(src, dst, eth_type, Command, payload, interface= 'enp0s20f0u7'):
    # """Send raw Ethernet packet on interface."""

    # assert (len(src) == len(dst) == 6)  # 48-bit ethernet addresses
    # assert (len(eth_type) == 2)  # 16-bit ethernet type
    # assert (len(Command) == 2)
    s = socket(AF_PACKET, SOCK_RAW)

    # From the docs: "For raw packet
    # sockets the address is a tuple (ifname, proto [,pkttype [,hatype]])"
    s.bind((interface, 0))

    
    send_command = bytes.fromhex(src + dst + eth_type + Command + payload)
    # print(send_command)

    return s.send(send_command)
    # test_str = "\xFE\xED\xFA\xCE\xBE\xEF"
    # return s.send(b'0000000000000000000000000000000000000000000000000000000000')
#   #           "\x00\x23\x20\x21\x22\x23",
#   #           "\x00\x12",
#   #           "\x01\x02",
#   #           # "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
#   #           "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02"
#   #
#   #           )
    # return


# if __name__ == "__main__":
#   # print("Sent %d-byte Ethernet packet on em1" %
#   #   sendeth("\xFE\xED\xFA\xCE\xBE\xEF",
#   #           "\x00\x23\x20\x21\x22\x23",
#   #           "\x00\x12",
#   #           "\x01\x02",
#   #           # "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
#   #           "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02"
#   #
#   #           ))


def hex_str_to_hex_byte(hex_str):  # convert "0102" to "\x01\x02"
    if len(hex_str) % 2 != 0:
        print( "Error the length of string is not 2*N")
        return ''
    # hex_byte = hex_str.decode("hex")
    hex_byte = bytes.fromhex(hex_str).decode()
    # hex_byte = bytes.fromhex(hex_str)
    return hex_byte


def print_hex_byte(hex_byte):
    print( hex_byte.encode("hex"))
    return

def hex_to_bin(hex_str,outbits):
    return format(int(hex_str, 16),'b').zfill(outbits)[-outbits:]

def bin_to_hex(bin_str,outbits):
    return format(int(bin_str, 2),'x').zfill(outbits)[-outbits:]

def zero_str_gen(num):  # Generate num of zeros string
    zero_str = ''
    if num < 0:
        print( '@@@ ERROR! you are trying to gen minus number of zeros!')
    else:
        for i in range(num):
            zero_str += '0'
    return zero_str


class ETH_control():
    def __init__(self,eth_name):
        self.tdo_finding_inprogress = 0
        self.multiboot_inprogress = 0
        self.data_length = int(352 / 4)  # in 4 bits
        self.error_list=[]
        self.mboot_count = -1
        self.eth_name = eth_name
        for i in range(47):
            self.error_list.append('0')

        self.PC_src = "D89EF3241692"
        self.PC_dst = "002320212223"
        self.PC_eth_type = "002e"

#######################################################################
##                              ||                                   ##
##                           \\ || //                                ##
##                            \\||//                                 ##
##                              ><                                   ##
#######################################################################
## Start of 

        # Group for: CC_CONTROL
        self.global_rst =['0']
        self.use_ETH_CMD =['0']
        self.sent_config_back =['0']
        self.sent_config_CMD =['0000000000000000']
        self.cc=[self.sent_config_CMD,self.sent_config_back,self.use_ETH_CMD,self.global_rst]

        # Group for: ETH_CONFIG
        self.DST_MAC_ADDR =['010203040506']
        self.SRC_MAC_ADDR =['0708090a0b0c']

        # Group for: FAKE_DATA_CONTROL
        self.sent_once =['0']
        self.sent_loop =['0']
        self.sent_loop_interval =['0000']

        # Group for: VIO_CONTROL
        self.multi_boot_top     =['0']
        self.rst_logic          =['0']
        self.rst_gen_tdim       =['0']
        self.rst_gen_tmsm       =['0']
        self.rst_gen_tckm       =['0']
        self.rst_gen_ttco       =['0']
        self.rst_chk_tdo_m      =['0']
        self.check_tdo          =['1']
        self.rst_chk_tms_s      =['000000000000000000']
        self.check_tms          =['111111111111111111']
        self.errcnt_rst4ch      =['00000000000']
        self.rst_chk_tck_s      =['000000000000000000']
        self.check_tck          =['111111111111111111']
        self.rst_chk_elinkttc   =['000000']
        self.check_ttc          =['111111']
        self.errcnt_inj         =['0']
        self.jtag_daisychain    =['111111111111111111']
        self.mbt_trigger_minisas=['0']
        self.rst_sma_FE         =['0']
        self.rst_clkdiv         =['0']
        self.vio=[self.rst_clkdiv,self.rst_sma_FE,self.mbt_trigger_minisas,self.jtag_daisychain,self.errcnt_inj,\
            self.rst_chk_elinkttc,self.rst_chk_tck_s,self.errcnt_rst4ch,self.rst_chk_tms_s,self.rst_chk_tdo_m,\
            self.rst_gen_ttco,self.rst_gen_tckm,self.rst_gen_tmsm,self.rst_gen_tdim,\
            self.rst_logic,self.multi_boot_top]

    def update_CC_CONTROL(self):
        payload_bit =''
        for s in self.cc:
            payload_bit += ''.join(s)
        # payload_bit =  self.sent_config_CMD +  self.sent_config_back +  self.use_ETH_CMD +  self.global_rst
        payload = self.payload_packet_bin(payload_bit)
        print("updating CC control: CMD="+self.sent_config_CMD[0]+" config_back="+self.sent_config_back[0]+\
            " use_ETH_CMD="+self.use_ETH_CMD[0]+" global_rst="+self.global_rst[0])
        self.send_eth_packet('0001',payload)

    def update_ETH_CONFIG(self):
        payload_bit =  hex_to_bin(self.SRC_MAC_ADDR[0],48) +  hex_to_bin(self.DST_MAC_ADDR[0],48)
        payload = self.payload_packet_bin(payload_bit)
        print("updating ETH control: SRC_MAC_ADDR="+self.SRC_MAC_ADDR[0]+" DST_MAC_ADDR="+self.DST_MAC_ADDR[0])
        self.send_eth_packet('0002',payload)

    def update_FAKE_DATA_CONTROL(self):
        payload_bit =  hex_to_bin(self.sent_loop_interval[0],16) +  self.sent_loop[0] +  self.sent_once[0]
        payload = self.payload_packet_bin(payload_bit)
        print("updating FAKE_DATA control: loop_interval="+self.sent_loop_interval[0]+" sent_loop="+self.sent_loop[0]+\
            " sent_once="+self.sent_once[0])
        self.send_eth_packet('0003',payload)

    def update_VIO_CONTROL(self):
        payload_bit =''
        for s in self.vio:
            payload_bit += ''.join(s)
        payload = self.payload_packet_bin(payload_bit)
        self.send_eth_packet('0101',payload)



## End of 
#######################################################################
##                              ><                                   ##
##                            //||\\                                 ##
##                           // || \\                                ##
##                              ||                                   ##
#######################################################################



    def send_eth_packet(self, command, payload):  # payload only needs to be a string
        # print( 'Command: '+ command)
        # print( 'Payload: ' + payload)
        sendeth(self.PC_src, self.PC_dst, self.PC_eth_type, command, payload, self.eth_name)
        time.sleep(0.001)

    def payload_packet_bin(self, payload_bit):
        payload_hex = hex(int(payload_bit, 2))[2:]
        payload_hex_len = len(payload_hex)

        if payload_hex[
            payload_hex_len - 1] == 'L':  # When do the hex conversion, python added a "L" at the end whic we don't need.
            payload_hex = payload_hex[:(payload_hex_len - 1)]
        additional_zeros = self.data_length - len(payload_hex)

        if additional_zeros < 0:
            print( '@@@ Following payload is more than you can handle: ')
            print( payload_bit)
            return ''
        else:
            # print(additional_zeros)
            payload = zero_str_gen(additional_zeros) + payload_hex
            # print( payload)
            return payload

    def payload_packet_hex(self, payload_hex):
        additional_zeros = self.data_length - len(payload_hex)
        if additional_zeros < 0:
            print( '@@@ Following payload is more than you can handle: ')
            print( payload_hex)
            return ''
        else:
            payload = zero_str_gen(additional_zeros) + payload_hex
            # print( payload)
            return payload


    def vio_decode(self, packet_full):
        # print(packet_full)
        # print(len(payload_hex))

        if packet_full[0:24]==self.DST_MAC_ADDR[0]+self.SRC_MAC_ADDR[0]: #eth filter
            payload_hex = packet_full[40:]
            payload_bin = format(int(payload_hex,16),'b').zfill(4*len(payload_hex))
            self.error_list[0]   = str(int(payload_bin[2  :3  ],2))   # sem_heartbeat_minisas
            self.error_list[1]   = str(int(payload_bin[3  :4  ],2))   # sem_fatalerr_minisas
            self.error_list[2]   = str(int(payload_bin[4  :7  ],2))   # design_number_minisas
            self.error_list[3]   = str(int(payload_bin[7  :8  ],2))   # locked_vio
            self.error_list[4]   = str(int(payload_bin[8  :32 ],2))   # elink_TTCin_err_reg_5_vio
            self.error_list[5]   = str(int(payload_bin[32 :56 ],2))   # elink_TTCin_err_reg_4_vio
            self.error_list[6]   = str(int(payload_bin[56 :80 ],2))   # elink_TTCin_err_reg_3_vio
            self.error_list[7]   = str(int(payload_bin[80 :104],2))   # elink_TTCin_err_reg_2_vio
            self.error_list[8]   = str(int(payload_bin[104:128],2))   # elink_TTCin_err_reg_1_vio
            self.error_list[9]   = str(int(payload_bin[128:152],2))   # elink_TTCin_err_reg_0_vio
            self.error_list[10]  = str(int(payload_bin[152:176],2))   # tck_err_reg_17_vio
            self.error_list[11]  = str(int(payload_bin[176:200],2))   # tck_err_reg_16_vio
            self.error_list[12]  = str(int(payload_bin[200:224],2))   # tck_err_reg_15_vio
            self.error_list[13]  = str(int(payload_bin[224:248],2))   # tck_err_reg_14_vio
            self.error_list[14]  = str(int(payload_bin[248:272],2))   # tck_err_reg_13_vio
            self.error_list[15]  = str(int(payload_bin[272:296],2))   # tck_err_reg_12_vio
            self.error_list[16]  = str(int(payload_bin[296:320],2))   # tck_err_reg_11_vio
            self.error_list[17]  = str(int(payload_bin[320:344],2))   # tck_err_reg_10_vio
            self.error_list[18]  = str(int(payload_bin[344:368],2))   # tck_err_reg_9_vio
            self.error_list[19]  = str(int(payload_bin[368:392],2))   # tck_err_reg_8_vio
            self.error_list[20]  = str(int(payload_bin[392:416],2))   # tck_err_reg_7_vio
            self.error_list[21]  = str(int(payload_bin[416:440],2))   # tck_err_reg_6_vio
            self.error_list[22]  = str(int(payload_bin[440:464],2))   # tck_err_reg_5_vio
            self.error_list[23]  = str(int(payload_bin[464:488],2))   # tck_err_reg_4_vio
            self.error_list[24]  = str(int(payload_bin[488:512],2))   # tck_err_reg_3_vio
            self.error_list[25]  = str(int(payload_bin[512:536],2))   # tck_err_reg_2_vio
            self.error_list[26]  = str(int(payload_bin[536:560],2))   # tck_err_reg_1_vio
            self.error_list[27]  = str(int(payload_bin[560:584],2))   # tck_err_reg_0_vio
            self.error_list[28]  = str(int(payload_bin[584:608],2))   # tms_err_reg_17_vio
            self.error_list[29]  = str(int(payload_bin[608:632],2))   # tms_err_reg_16_vio
            self.error_list[30]  = str(int(payload_bin[632:656],2))   # tms_err_reg_15_vio
            self.error_list[31]  = str(int(payload_bin[656:680],2))   # tms_err_reg_14_vio
            self.error_list[32]  = str(int(payload_bin[680:704],2))   # tms_err_reg_13_vio
            self.error_list[33]  = str(int(payload_bin[704:728],2))   # tms_err_reg_12_vio
            self.error_list[34]  = str(int(payload_bin[728:752],2))   # tms_err_reg_11_vio
            self.error_list[35]  = str(int(payload_bin[752:776],2))   # tms_err_reg_10_vio
            self.error_list[36]  = str(int(payload_bin[776:800],2))   # tms_err_reg_9_vio
            self.error_list[37]  = str(int(payload_bin[800:824],2))   # tms_err_reg_8_vio
            self.error_list[38]  = str(int(payload_bin[824:848],2))   # tms_err_reg_7_vio
            self.error_list[39]  = str(int(payload_bin[848:872],2))   # tms_err_reg_6_vio
            self.error_list[40]  = str(int(payload_bin[872:896],2))   # tms_err_reg_5_vio
            self.error_list[41]  = str(int(payload_bin[896:920],2))   # tms_err_reg_4_vio
            self.error_list[42]  = str(int(payload_bin[920:944],2))   # tms_err_reg_3_vio
            self.error_list[43]  = str(int(payload_bin[944:968],2))   # tms_err_reg_2_vio
            self.error_list[44]  = str(int(payload_bin[968:992],2))   # tms_err_reg_1_vio
            self.error_list[45]  = str(int(payload_bin[992:1016],2))   # tms_err_reg_0_vio
            self.error_list[46]  = str(int(payload_bin[1016:1040],2))   # tdo_m_err_reg_vio
            return 1 # packet decoded 
        return 0 # no packet passed the filter



