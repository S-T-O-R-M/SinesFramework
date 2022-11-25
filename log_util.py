import logging as log
import os.path

log_files = [".\Logs\central_server_logs.txt",".\Logs\collection_server_logs.txt",".\Logs\agent_logs.txt"]

def init(log_file_num):

    filename= log_files[log_file_num]

    if os.path.exists(filename):
        print("Log file exists")
        log.basicConfig(filename=".\Logs\central_server_logs.txt", level = log.DEBUG)
    else:
        print("Creating log file")  
        f = open(filename, "w")
        f.close()
        log.debug("Log file created")
        log.basicConfig(filename=".\Logs\central_server_logs.txt", level = log.DEBUG)