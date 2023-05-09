#!/usr/bin/env python

# import httplib
import http.client
import sys
import time
import statistics

serverIP = sys.argv[1]
filename = sys.argv[2]
runs = sys.argv[3]
total_time = 0
throughput = []
file_size = 1000  #size of the file transferred in kb

conn = http.client.HTTPConnection(serverIP)

for i in range(runs):
    cmd = "GET "+ filename
    cmd = cmd.split()

    if cmd[0] == 'exit': #tipe exit to end it
        break
   
    #request command to server
    start = time.time()
    conn.request(cmd[0], cmd[1])

    #get response from server
    rsp = conn.getresponse()
    end = time.time()

    total_time += end - start
    if(end-start != 0):
        throughput.append(8*file_size/(end-start))

data_received = rsp.read()
print("Size of file received: ", len(data_received))
print("Application Layer Data/File Data: ", (len(rsp.msg) + len(data_received))/len(data_received))

# write the data to the file after last transfer
with open(filename, mode="ab") as f:
    f.write(data_received)

print("Std dev = ", statistics.stdev(throughput))
print("mean = ", statistics.mean(throughput))
   
conn.close()