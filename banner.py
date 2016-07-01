# python 2.x
# coding= utf-8

import socket
import sys

# get the banner of the service running
# at the given IP/Port couple
def getBanner(ip, port):
    try:
        # creation of the socket
        socket.setdefaulttimeout(3)     # 3 sec of timeout
        soc = socket.socket()

        print("[+] Connecting to " + str(ip) + " port " + str(port))
        soc.connect((ip, port))
        print("COUCOU")
        # here we get the banner of the service runnning
        banner = soc.recv(1024)
        
        # display of the banner and the port associated
        print("[+] "+ str(port) + " ==> " + banner)

        soc.close()

    except Exception as e:
        print("[E] " + str(e))

# checking the arguments
if len(sys.argv) < 2:
    print("Give at least an IP address you stupid dickhead !")
    exit()
elif len(sys.argv) == 2:
    port_list = [21,22,23,80]
elif len(sys.argv) == 3:
    port_list = []
    port_list.append(sys.argv[2])

ip = sys.argv[1]
print("IP to check : " + ip)
print("Port(s) to check :", end="")
print(str(port_list).strip('[').strip(']'))

for port in port_list:         # lets connect to each port !
    getBanner(ip, port)

# penser à rajouter une condition :
# si on reçoit autre chose qu'un RST alors le port
# est écouté !
