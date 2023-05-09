OS: Linux
Language: python

Program description:
The network consists of 4 systems/peers, of which one contains the required files(A_10kB, B_10kB.... B_10MB) and the 
other 3 peers fetches any one of the files using the BitTorrent protocol.
Each peer requests each file N number of times and the sender calculates the average throughput and std deviation of 
each file transfer session.

Execution Instructions: 

Step 0:
Check for Python version > 3.0 using
- python -V

Step 1:
Create virtual env 

- python -m venv env
- source env\bin\activate

Step 2:
install required libraries.
a. Install a library to create a .torrent file which is shared to all the peers.
- pip3 install py3createtorrent

b. Install a library to download the required file(s) using .torrent file.
-  pip install torrentp

c. install a library to create sessions and send the file(s) using BitTorrent protocol.
- sudo apt-get install python3-libtorrent


Step 3:
The sender creates the .torrent file and shares it with the peers.
Note: A folder with the name data_files must be present in the CWD with all of the relevant files (A_10kB, B_10kB.... B_10MB)
Usage: py3createtorrent -t udp://tracker.opentrackr.org:1337/announce <path-to-file>
Example:
py3createtorrent -t udp://tracker.opentrackr.org:1337/announce data_files/A_10kB
This creates a torrent file (A_10kB.torrent) that is sent to the peers.

Step 4:
To run the peer (receiver):
Usage: python peer_seed.py <path-to-torrent-file> <total-runs>
Example:
- python peer_seed.py data_files/A_10kB.torrent 333

Step 5:
Change the file_size variable w.r.t the size of the file being transfered.

Run the peer (sender):
Usage: python sender_seed.py <path-to-torrent-file> <total-runs>
Example:
- python sender_seed.py data_files/A_10kB.torrent 333


Note: To run the all the peers on the same LAN, we connected them using an Ethernet cable
and used the associated IP address of the server on eth (can be found using ipconfig).