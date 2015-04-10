import socket
import serial
import struct
import fcntl

try:
    UDPSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' - Message: ' + msg[1]
    sys.exit()    

try:
    UDPSock.bind(("", 9002))
except socket.error, msg:
    print 'Bind failed. Error code: ' +    str(msg[0]) + ' - Message: ' + msg[1]
    
print 'Socket bind complete'

ser = serial.Serial('/dev/ttymxc3',9600,timeout=1)
ser.flushOutput()

ip_this = socket.inet_ntoa(fcntl.ioctl(UDPSock.fileno(),0x8915, struct.pack('256s',"wlan0"[:15]))[20:24])
print 'IP address of this server: ' + ip_this

from subprocess import call
call(["set_alpha", "fb0", "0"])

while True:
    data, addr = UDPSock.recvfrom(4)
    print data, ' ', addr[0], '  bytes: ', ord(data[3]), ' ', ord(data[2]), ' ', ord(data[1]), ' ', ord(data[0])
    if data == "ciao":
        UDPSock.sendto(ip_this, addr )
    elif ord(data[3]) == 208:
		fileToPlay = "uri=file:///home/ubuntu/videos/" + str(ord(data[0])) + ".mp4";
		from subprocess import call
		call(["gst-launch-0.10", "playbin2", fileToPlay])
    else:    
        ser.write(data)
	ser.flushOutput()
    
UDPSock.close()    
