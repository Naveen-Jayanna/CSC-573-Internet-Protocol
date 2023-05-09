#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import sys

serverIP = sys.argv[1]

#Create custom HTTPRequestHandler class
class HTTPRequestHandler(BaseHTTPRequestHandler):
    
    #handle GET command
    def do_GET(self):
        print("Serving: ", self.protocol_version)
        rootdir = './data_files/' #file location
        try:
            f = open(rootdir + self.path) #open requested file
            print(rootdir + self.path)
            #send code 200 response
            self.send_response(200)

            data = bytes(f.read(), 'utf-8')
            #send header first
            self.send_header('Content-type','text-html')
            self.send_header('Content-length', str(len(data)))
            self.end_headers()
            #send file content to client
            self.wfile.write(data)
            f.close()
            return
            
        except IOError:
            self.send_error(404, 'file not found')
    
def run():
    print('http server is starting...')

    #ip and port of servr
    #by default http server port is 80
    server_address = (serverIP, 80)

    handler = HTTPRequestHandler
    handler.protocol_version = 'HTTP/1.1' # set HTTP protocol to 1.1 for the handler
    httpd = HTTPServer(server_address, handler)
    
    print('http server is running...')
    httpd.serve_forever()
    
if __name__ == '__main__':
    run()