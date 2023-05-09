
OS: Windows 64-bit
Language: python

Program description:
The client code can be used to retrieve any one of the files A_10kB, B_10kB.... B_1MB from the server.
The client requests the file N number of times and calculates average throughput and std deviation.

Execution Instructions: 

Step 0:
Check for Python version > 3.0 using
- python -V
A folder with the name data_files must be present in the CWD with all of the relevant files (A_10kB, B_10kB.... B_1MB)

Step 1:
Create virtual env 

- python -m venv env
- env\Scripts\activate
- pip install h2

Step 2:

Set these variables in the client to your own IP and port number:
SERVER_NAME = 'your IP'
SERVER_PORT = 8080

For the server, set your IP address in the following line (195):
coro = loop.create_server(H2Protocol, 'your IP', 8080)

From the current directory -
Run the server:
Usage: python http2_server.py server-IP-address 
Example:
- python http2_server.py

Step 3:
Change the file_size variable w.r.t the size of the file being transfered.

To run the client:
Usage: python http2_client.py filename no-of-transfers
Example:
- python http2_client.py A_10MB 1000

Note: To run client and server on the same LAN, we connected them using an Ethernet cable
and used the associated IP address of the server on eth (can be found using ipconfig)



							