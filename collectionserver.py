#to connect to the central server
import socket
import log_util as lu
from fastapi import FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import json


filename_mapping = dict() 
filename_mapping["VPN"] = "IP ADDRESS 1"
filename_mapping["VPN1"] = "IP ADDRESS 2"

collections = list()
counter  = 0

lu.init(1)

def getFilenameMapping(document_tag):
    f=open(".\File_Mapping.json")
    file_ips = json.load(f)
    if document_tag in file_ips:
        print(file_ips[document_tag])
        return(file_ips[document_tag])

def send_collect_request(IP):
    print("Sending collect request")
    try:
        #print(filename_mapping[document_tag])
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 8081))
        s.send(b'COLLECT')
    except:
        print("Unable to collect. Error sending request.")
        

#Input mapping = {"VPN1": [1669419177,"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36","127.0.0.1"]}
#filename_mapping : {"VPN": "IP address"}
# 0 - time, 1- User agent, 2- IP

app = FastAPI()
@app.post("/Document_Tag")
async def root(request: Request):
    print("Request received")
    doc_tag_data = await request.json()
    input_data = json.loads(doc_tag_data)
    print(input_data)
    for x in input_data:
        send_collect_request(getFilenameMapping(x))
    

@app.post("/Collection/{ID}")
async def root(request : Request, ID = str):
    print("request Received")



# @app.get("/Machine_Extract/")
# async def root(request: Request, doc_tag: str, response: Response):


# def Receiver():
#     print("In")
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     #port number
#     port = 8020
#     #binding the server to a port
#     s.bind(('',port))
#     s.listen(1)
#     while True:
#         conn, addr = s.accept()
#         print("in 2")
#         print("Connection established from ",addr)
#         data=conn.recv(1024).decode()
#         parsed_data = json.loads(data)
#         print(parsed_data)
#         for x in parsed_data:
#             print("doc_tag:",x)
#             print("time : ",parsed_data[x][0])
#             print("user agent : ",parsed_data[x][1])
#             print("Access_IP : ",parsed_data[x][2])
#             response = input  ("Do you want to collect data?(Y/N)")
#             if response.lower() == "y":
#                 send_collect_request(x)
#             else:
#                 print("YOU ARE SAFE")
#         conn.close()


# Receiver()

#response from the user







