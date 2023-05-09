import libtorrent as lt
import time
import sys
import statistics

torr_file = sys.argv[1]
total_time = 0
throughput = []
torr_file = sys.argv[1]
runs = int(sys.argv[2])
flag = False
file_size = 1000		#size of the file transferred in kb
files_recieved = 0

for i in range(runs):
	ses = lt.session({'listen_interfaces': '127.0.0.1:6881l'})
	info = lt.torrent_info(torr_file)
	h = ses.add_torrent({'ti': info, 'save_path': '.'})
	s = h.status()
	while (not s.is_seeding):
		s = h.status()
		if(s.progress != 0.0 and not flag):
			print("\nStarting to send.")
			start = time.time()
			flag = True
		# print('\n%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d) %s' % (
		# 	s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
		# 	s.num_peers, s.state), end=' ')
		print('\r (total_upload: %.2f total_payload_upload: %.2f)' % (
			s.total_upload, s.total_payload_upload), end=' ')
		if(s.progress == 1.0):
			end = time.time()
			total_time += end-start
			print("time taken = ",end-start)
			print("Sent file " + torr_file.split(".")[0] + " for the " + str(i+1) +" time(s).")
			if(end-start != 0):
				throughput.append(8*file_size/(end-start))
			flag = False
			# time.sleep(3)

		# alerts = ses.pop_alerts()
		# for a in alerts:
		# 	if a.category() & lt.alert.category_t.error_notification:
		# 		print(a)

		sys.stdout.flush()

		time.sleep(3)

print(h.status().name, 'complete')
print("Std dev = ", statistics.stdev(throughput))
print("mean = ", statistics.mean(throughput))