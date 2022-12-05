# SinesFramework
Sines Framework - A fast forensic evidence collection framework

Setup:
1) We have listed the dependencies for our project in "requirements.txt". The "pip install -r requirements.txt" command can be run ton get the dependencies. 

2) "File_Mapping.json" contains the document tag to agent machine IP mapping which is used by the collection server.

3) "Intern payroll information.xlsx" and "VPN.docx" are honeypot files with embedded APIs. 

Startup:

Run the following commands to start each module

1) Central server: python3 -m uvicorn server_main:app 0.0.0.0 --port 8020 --reload
2) Collection server: python3 -m uvicorn collectionserver:app 0.0.0.0 --port 8040 --reload
3) Agent: python3 colllection_agent.py
