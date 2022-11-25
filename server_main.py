from fastapi import FastAPI, Request, Response
import time
import log_util as lu
import socket
import json

DOC_TAGS = ['VPN','VPN1','PAYROLL']
lu.init(0)

def send_data(data_json):
    s=socket.socket() 
    conn = ("localhost",8020)
    lu.log.debug("Sending data")
    s.connect(conn)
    s.sendall(data_json.encode())
    s.close()
    lu.log.debug("Data sent")

def form_dict_and_send(data_dict):

    data_to_send = json.dumps(data_dict,indent=4)
    lu.log.debug("Json data to send: ")
    lu.log.debug(data_to_send)
    send_data(data_to_send)




data = dict()
app = FastAPI()
@app.get("/{doc_tag}")

async def root(request: Request, doc_tag: str, response: Response):

    lu.log.debug("Request received")

    lu.log.debug(doc_tag)
    user_agent= request.headers.get('user-agent')
    lu.log.debug(user_agent)
    ip = str(request.client.host)
    lu.log.debug(ip)
    time_of_alert = int(time.time())
    lu.log.debug(time_of_alert)

    if doc_tag not in DOC_TAGS:
        lu.log.debug("Document tag does not exist")
        return

    if ip not in data:

        lu.log.debug("Adding new IP Address")

        lst = list()
        temp_lst = list()
        dict_to_send = dict()

        temp_lst.append(doc_tag)
        temp_lst.append(time_of_alert)
        temp_lst.append(user_agent)

        lst.append(temp_lst.copy())
        data[ip] = lst

        temp_lst.pop(0)
        temp_lst.append(ip)
        dict_to_send[doc_tag] = temp_lst
        
        print(dict_to_send)

        form_dict_and_send(dict_to_send)

        lu.log.debug(data[ip])

        response.status_code = 200

    else:

        lu.log.debug("IP already exists")

        flag = 0

        for x in data[ip]:
            if x[0] == doc_tag:
                flag +=1
                lu.log.debug("redundant data")
                lu.log.debug (data)
                break

        if flag == 0:
            lu.log.debug("New document tag")

            temp_lst = list()
            dict_to_send = dict()
            
            temp_lst.append(doc_tag)
            temp_lst.append(time_of_alert)
            temp_lst.append(user_agent)
            data[ip].append(temp_lst.copy())

            temp_lst.pop(0)
            temp_lst.append(ip)
            dict_to_send[doc_tag] = temp_lst
            form_dict_and_send(dict_to_send)

            lu.log.debug(data[ip])

