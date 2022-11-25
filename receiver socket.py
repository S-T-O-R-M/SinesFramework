import socket
import json

def Receiver():
    recv_data=""
    s=socket.socket()
    s.bind(("localhost",8020))
    s.listen()
    print("Listening in port 8020")
    while True:
        print("opening")
        conn, addr = s.accept()
        print("Connection established from ",addr)
        data=conn.recv(1024).decode()
        parsed_data = json.loads(data)
        print(parsed_data)
        for x in parsed_data:
            print("doc_tag:",x)
            print("time : ",parsed_data[x][0])
            print("user agent : ",parsed_data[x][1])
            print("Access_IP : ",parsed_data[x][2])
        # data_proc = data.decode("utf-8")
        # print(data_proc)
        # for x in data_proc:
        #     print("x:",x)
        conn.close()

Receiver()