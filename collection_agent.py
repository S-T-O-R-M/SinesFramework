import socket
import subprocess
import json
import datetime 
import os
import requests
import log_util as lu
import sys

LSERVER = "127.0.0.1"
LPORT = 8081
cIP = "127.0.0.1"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((LSERVER,LPORT))
lu.init(2)

# Server Listening Handling
def server_listen():
    print("Listening on", LSERVER, ":", LPORT)
    lu.log.debug("Listening on "+str(LSERVER)+" "+str(LPORT))
    s.listen(100)
    conn,addr = s.accept()

    msg = conn.recv(1024).decode("utf-8").strip()
    collectionIP, collectionPort = addr

    if (msg == "COLLECT" and verify_collection(collectionIP)):
        lu.log.debug("COLLECT Received. Starting Collection")
        start_collection()

# Trigger Collection
def start_collection():

    native_environment = verify_OS()
    
    if (native_environment == "Linux"):

        lu.log.debug("POSIX Environment Detected")
        #Start Linux Data Collection
        try:
            current_date_time = subprocess.run(["date"], capture_output=True).stdout.decode("utf-8")
            os_info = subprocess.run(["uname", "-a"],capture_output=True).stdout.decode("utf-8")
            current_user = subprocess.run(["id"], capture_output=True).stdout.decode("utf-8")
            network_configuration_ifconfig = subprocess.run(["ifconfig", "-a"],capture_output=True).stdout.decode("utf-8")
            network_configuration_ipa = subprocess.run(["ip", "a"], capture_output=True).stdout.decode("utf-8")
            process_information = subprocess.run(["ps", "-ef"], capture_output=True).stdout.decode("utf-8")
            network_connections = subprocess.run(["netstat", "-rn"], capture_output=True).stdout.decode("utf-8")
            open_files = subprocess.run(["lsof", "-V"], capture_output=True).stdout.decode("utf-8")
            free_space_df = subprocess.run(["df"],capture_output=True).stdout.decode("utf-8")
            free_space_mount = subprocess.run(["mount"], capture_output=True).stdout.decode("utf-8")
            swap_space = subprocess.run(["free"], capture_output=True).stdout.decode("utf-8")
            connected_users = subprocess.run(["w"], capture_output=True).stdout.decode("utf-8")
            login_info = subprocess.run(["last", "-Faiwx"], capture_output=True).stdout.decode("utf-8")
            kernel_modules = subprocess.run(["lsmod"], capture_output=True).stdout.decode("utf-8")
            etc_passwd_data = subprocess.run(["cat", "/etc/passwd"], capture_output=True).stdout.decode("utf-8")
            etc_shadow_data = subprocess.run(["cat", "/etc/shadow"], capture_output=True).stdout.decode("utf-8")
            arp_table = subprocess.run(["arp", "-a"], capture_output=True).stdout.decode("utf-8")
            routing_table = subprocess.run(["route", "-n"], capture_output=True).stdout.decode("utf-8")
            latest_modified_files = subprocess.run(["find", "/", "-type", "f", "-mmin", "-5", "2>/dev/null"], capture_output=True).stdout.decode("utf-8")
            contents_of_tmp = subprocess.run(["ls", "-la" , "/tmp"], capture_output=True).stdout.decode("utf-8")
            cronjobs = subprocess.run(["cat", "/etc/crontab"], capture_output=True).stdout.decode("utf-8")
            hostname = socket.gethostname()
            ip_addr = socket.gethostbyname(hostname)
            os_type = "Linux"

            lu.log.debug("Data Collection for "+str(ip_addr)+" "+"Completed")
            # Building Result Object
            forensic_data = {}
            
            forensic_data[ip_addr] = { "hostname" : hostname, 
                                "Operating System Type": os_type, 
                                "Timestamp": current_date_time, 
                                "OS Info": os_info,
                                "Current User": current_user,
                                "Network Config 1": network_configuration_ifconfig,
                                "Network Config 2": network_configuration_ipa,
                                "Connections": network_connections,
                                "Process Information": process_information,
                                "Open Files":open_files,
                                "Free_Space_DF":free_space_df,
                                "Free_Space_Mount": free_space_mount,
                                "Swap_Information": swap_space,
                                "Connected Users": connected_users,
                                "Login Info": login_info,
                                "Kernel Modules": kernel_modules,
                                "Passwd File Info": etc_passwd_data,
                                "Shadow File Info": etc_shadow_data,
                                "ARP Table":arp_table,
                                "Routing Table": routing_table,
                                "Latest Modified Files":latest_modified_files,
                                "TMP Contents":contents_of_tmp,
                                "Cron Jobs":cronjobs,
                                }

            json_data = json.dumps(forensic_data, indent=4)
            lu.log.debug("JSON Results Built")

            lu.log.debug("Sending Results back to the Collection Server")
            send_results(json_data)

            lu.log("Data Collection and Exfiltration Complete for "+str(ip_addr))
        
        except(Exception):
            print("Something went wrong")

    elif native_environment == "Windows":
        
        lu.log.debug("Windows Environment Detected")

        try:
            #Collecting Data for Windows
            system_information = subprocess.run(["systeminfo"], capture_output=True).stdout.decode("utf-8")
            hostname = subprocess.run(["hostname"], capture_output=True).stdout.decode("utf-8").strip()
            current_user = subprocess.run(["whoami"], capture_output=True).stdout.decode("utf-8")
            net_users = subprocess.run(["net", "users"], capture_output=True).stdout.decode("utf-8")
            net_groups = subprocess.run(["net", "localgroup"], capture_output=True).stdout.decode("utf-8")
            domain_groups = subprocess.run(["net", "group", "/domain"], capture_output=True).stdout.decode("utf-8")
            firewall_state = subprocess.run(["netsh", "firewall", "show", "state"], capture_output=True).stdout.decode("utf-8")
            firewall_config = subprocess.run(["netsh","firewall", "show", "config"],capture_output=True).stdout.decode("utf-8")
            network_config = subprocess.run(["ipconfig", "/all"],capture_output=True).stdout.decode("utf-8")
            routing_table = subprocess.run(["route", "print"],capture_output=True).stdout.decode("utf-8")
            arp_table = subprocess.run(["arp", "-A"], capture_output=True).stdout.decode("utf-8")
            patching_information = subprocess.run(["wmic", "qfe", "get" , "Caption,Description,HotFixID,InstalledOn"], capture_output=True).stdout.decode("utf-8")
            netstat_information = subprocess.run(["netstat","-ano"], capture_output=True).stdout.decode("utf-8")
            scheduled_tasks = subprocess.run(["schtasks", "/query", "/fo", "LIST", "/v"],capture_output=True).stdout.decode("utf-8")
            user_privs = subprocess.run(["whoami","/priv"], capture_output=True).stdout.decode('utf-8')
            administrator_group_info = subprocess.run(["net","localgroup", "Administrator"], capture_output=True).stdout.decode('utf-8')
            net_shares = subprocess.run(["net","shares"], capture_output=True).stdout.decode('utf-8')
            defender_status = subprocess.run(["powershell", "Get-MpComputerStatus"],capture_output=True).stdout.decode('utf-8')
            current_ip = socket.gethostbyname(hostname)
            
            
            lu.log.debug("Data Collection for "+str(current_ip)+" "+"Completed")

            #Building result object
            forensic_data = {}

            forensic_data[str(current_ip)] = {                                 
                                    
                                    "sysinfo": system_information,
                                    "hostname": hostname,
                                    "current_user": current_user,
                                    "net_user_info": net_users,
                                    "net_groups_info": net_groups,
                                    "domain_groups": domain_groups,
                                    "firewall_state": firewall_state,
                                    "firewall_configuration": firewall_config,
                                    "network_configuration": network_config,
                                    "routing_table": routing_table,
                                    "arp_table": arp_table,
                                    "patching_information" : patching_information,
                                    "netstat_info" : netstat_information,
                                    "scheduled_tasks": scheduled_tasks,
                                    "user_privileges": user_privs,
                                    "admin_group": administrator_group_info,
                                    "shares": net_shares,
                                    "defender_status": defender_status,
                                } 
                        
            json_data = json.dumps(forensic_data, indent=4)
            
            lu.log.debug("JSON Results Built")
       
            lu.log.debug("Sending Results back to the Collection Server")
            
            send_results(json_data)

            lu.log.debug("Data Collection and Exfiltration Complete for "+str(current_ip))


        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
# OS Detection

def send_results(forensic_results):
    results_endpoint = "http://127.0.0.1:80/"
    response = requests.post(results_endpoint, json = forensic_results)

    print(response)
    

def verify_OS():
        if os.name == "posix":
            return "Linux"
        if os.name == "nt":
            return "Windows"

# Verify Collection Server IP

def verify_collection(collectionIP):
    if collectionIP == cIP:
        return 1
    print ("Collection Server Check Passed")
    return -1

# Main Mathod

def main():
    server_listen()

# Trigger Main
if __name__ == "__main__":
    print("Hello, World!")
    main()