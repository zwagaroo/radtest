# UDP packet receiver
# need sudo to run the code


import socket
import time
import binascii

r_sock=socket.socket(socket.AF_PACKET,socket.SOCK_RAW)

nic='p1p1'
port=3

r_sock.bind((nic,port))

nPk=0
while True:
	packet=r_sock.recv(1600)
	sender=":".join([binascii.hexlify(i) for i in packet[0:6]])
	recevier= ":".join([binascii.hexlify(i) for i in packet[6:12]])
	length=binascii.hexlify(packet[12:14])
	payload= packet[14:]
	if any(target in ["00:13:3b:0f:d2:77","00:23:20:21:23"] for target in [sender,recevier]):
	
		print "\n\n\n"
		print "==========packet:",str(nPk),"==============="
		print "received from:",sender
		print "to:",recevier
		print "bytes:",length
		print binascii.hexlify(payload)
		print len(binascii.hexlify(payload))
	else:
		print "\n\n\n"                 
		print "xxxxxxxxxxxxxxpacket:",str(nPk),"==============="
		print "received from:",sender
		print "to:",recevier
	nPk=nPk+1


