
Project Assignment 3: Packet sniffer

Team Unity ID: 
Swetha Sairamakrishnan - ssairam
Naveen Jayanna - njayann

Language: Python 3
OS: Ubuntu 22.04 (Downward compatible upto 16.04)

Packages used: socket, struct, time 
(pip installations are not required as they come by default with python3)

Steps for Execution:
Extract the zip file and move into the HW3 directory

Run the below command:
sudo python3 sniffer_njayann.py

The sniffer runs for 30 seconds and calculates the number of packets of types : IP, UDP, TCP, HTTP, HTTPS, QUIC, DNS and ICMP. 
The results are stored in a CSV file -> sniffer_njayann.csv

The total time for packet collection can be customized by setting the constant
EXP_TIME in the script.