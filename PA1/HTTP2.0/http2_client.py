#!/usr/bin/env python3


import socket
import h2.connection
import h2.events
import json
import sys
import time
import statistics

SERVER_NAME = '10.152.56.193'
SERVER_PORT = 8080
path = sys.argv[1]
runs = sys.argv[2]
total_time = 0
throughput = []
file_size = 1000  #size of the file transferred in kb

# generic socket and ssl configuration
socket.setdefaulttimeout(15)

# open a socket to the server and initiate TLS/SSL
s = socket.create_connection((SERVER_NAME, SERVER_PORT))

c = h2.connection.H2Connection()
c.initiate_connection()
s.sendall(c.data_to_send())

headers = [
    (':method', 'GET'),
    (':path', path),
    (':authority', SERVER_NAME),
    (':scheme', 'https'),
]
c.send_headers(1, headers, end_stream=True)
s.sendall(c.data_to_send())

body = b''
response_stream_ended = False
for i in runs:
    start = time.time()
    while not response_stream_ended:
        # read raw data from the socket
        data = s.recv(65536 * 1024)
        if not data:
            break

        # feed raw data into h2, and process resulting events
        events = c.receive_data(data)
        for event in events:
            # print(event)
            if isinstance(event, h2.events.DataReceived):
                # update flow control so the server doesn't starve us
                c.acknowledge_received_data(event.flow_controlled_length, event.stream_id)
                # more response body data received
                body += event.data
            if isinstance(event, h2.events.StreamEnded):
                # response body completed, let's exit the loop
                response_stream_ended = True
                break
        # send any pending data to the server
        s.sendall(c.data_to_send())
    end = time.time()
    total_time += end - start
    throughput.append(8*file_size/(end-start))


print("Response fully received:")
f = open('rec_'+path,'w')
json_file = json.loads(body.decode())
f.write(json_file["body"])

# print("Application data/File data:")
# print(len(json_file) / len(json_file["body"]))

print("Std dev = ", statistics.stdev(throughput))
print("mean = ", statistics.mean(throughput))

# tell the server we are closing the h2 connection
c.close_connection()
s.sendall(c.data_to_send())

# close the socket
s.close()
