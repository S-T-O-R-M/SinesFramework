#to connect to the central server
import socket
from tkinter import Y
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#port number
port = 8000
#binding the server to a port
s.bind(('',port))
s.listen(1)
#msg = s.recv(1024)  #doc tag from the central server
s.close()

#creating a json list 
filename_to_ip = [{"filename":"VPN", "IP":"1.1.1.1"}, {"filename":"VPN1","IP":"2.2.2.2"}]
for x in filename_to_ip:
    if x[ "filename" ] == "VPN1":
        a=x["IP"]
        print(x["IP"])


#response from the user
response = input  ("Do you want to collect data?(Y/N)")
if response == "Y":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((a,8000))
    s.send(b'COLLECT')
    s.close()
else:
    print("YOU ARE SAFE")






