import logging as log
import os

if os.name =="posix":  
    log_files = ["central_server_logs.txt","collection_server_logs.txt","agent_logs.txt"]
elif os.name == "nt":
    log_files = ["central_server_logs.txt","collection_server_logs.txt","agent_logs.txt"]


def init(log_file_num):

    filename= log_files[log_file_num]

    if os.path.exists(filename):
        print("Log file exists")
        log.basicConfig(filename = log_files[log_file_num], level = log.DEBUG)
    else:
        print("Creating log file")  
        f = open(filename, "w")
        f.close()
        log.debug("Log file created")
        log.basicConfig(filename = log_files[log_file_num], level = log.DEBUG)