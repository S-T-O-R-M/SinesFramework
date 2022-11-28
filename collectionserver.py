#to connect to the central server
import socket
import log_util as lu
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
import json

collections = list()

lu.init(1)
def writeJsonFile(ip,data):
    filename = ".\\" + ip + ".txt"
    lu.log.debug("Creating under filename:"+filename)
    with open(filename, 'w') as f:
        f.write(data)

def getFilenameMapping(document_tag):
    f=open(".\File_Mapping.json")
    file_ips = json.load(f)
    if document_tag in file_ips:
        lu.log.debug(file_ips[document_tag])
        collections.append(file_ips[document_tag])
        return(file_ips[document_tag])
    else:
        return 0

def send_collect_request(IP):
    lu.log.debug("Sending collect request")
    if IP==0:
        lu.log.debug("IP Address not found for document tag")
        return
    try:
        #lu.log.debug(filename_mapping[document_tag])
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((IP, 8081))
        s.send(b'COLLECT')
    except:
        lu.log.debug("Unable to collect. Error sending request.")
        

#Input mapping = {"VPN1": [1669419177,"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36","127.0.0.1"]}
#filename_mapping : {"VPN": "IP address"}
# 0 - time, 1- User agent, 2- IP

app = FastAPI()
@app.post("/Document_Tag")
async def root(request: Request):
    lu.log.debug("Request received")
    doc_tag_data = await request.json()
    input_data = json.loads(doc_tag_data)
    lu.log.debug(input_data)
    for x in input_data:
        send_collect_request(getFilenameMapping(x))
    

@app.post("/Collection")
async def root(coll_req : Request ):
    ip = str(coll_req.client.host)
    collect = await coll_req.json()
    Collection_data = json.loads(collect)
    lu.log.debug(Collection_data)
    if ip in collections:
        lu.log.debug("Collection Data Received from :\r")
        lu.log.debug(ip)
        writeJsonFile(ip,json.dumps(Collection_data,indent=4))

    else:
        lu.log.debug("Unexpected IP sending data\r")
        lu.log.debug(ip)
    