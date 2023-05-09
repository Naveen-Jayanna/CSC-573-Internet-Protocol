import libtorrent as lt
import time
import sys
import os

torr_file = sys.argv[1]
runs = int(sys.argv[2])
flag = False
files_recieved = 0
print("\n Waiting connect.")
while 1:
	ses = lt.session({'listen_interfaces': '127.0.0.1:6882l'})
	info = lt.torrent_info(torr_file)
	h = ses.add_torrent({'ti': info, 'save_path': '.'})
	s = h.status()

	while (not s.is_seeding):
		s = h.status()

		if(s.progress != 0.0 and flag):
			print("\nStarted to receive the file for the "+str(files_recieved)+" time.")
			flag = True
		if(s.progress == 1.0):
			files_recieved += 1
			print("\nReceived file for the "+str(files_recieved)+" time.")
			flag = False
			if(files_recieved == runs):
				print("\n Done")
				exit()
			os.remove(torr_file.split(".")[0])
			# time.sleep(3)

		sys.stdout.flush()
		time.sleep(3)