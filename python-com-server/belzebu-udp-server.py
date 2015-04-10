import socket
import serial
import struct
import fcntl
import json                                 

port = 9005

try:
    UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' - Message: ' + msg[1]
    sys.exit()    

try:
    UDPSock.bind(("", port))
    print 'Socket created on port ' + str(port)
except socket.error, msg:
    print 'Bind failed. Error code: ' +  str(msg[0]) + ' - Message: ' + msg[1]
    
print 'Socket bind complete'

ser = serial.Serial('/dev/ttymxc3',115200,timeout=1)
ser.flushOutput()

# get local ip address on selected interface -----------------------------------------+
#                                                                                     |
#                                                                                     |
#                                                                                     V
ip_this = socket.inet_ntoa(fcntl.ioctl(UDPSock.fileno(),0x8915, struct.pack('256s',"eth0"[:15]))[20:24])
print 'IP address of belzebu server: ' + ip_this


# insert a controll 
while True:
    data, addr = UDPSock.recvfrom(128)
    print addr[0], ' say ', data,  '   bytes: ', ord(data[0])

    if data == "ciao":
        UDPSock.sendto(ip_this, addr)
    else:    
        ser.write(data)
	ser.flushOutput()
    
UDPSock.close()    


# pert il python e json https://docs.python.org/2/library/json.html