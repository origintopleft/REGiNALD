import socket
import string
import time

urt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
urt.sendto("\xFF\xFF\xFF\xFFrcon fa4allut tracklist", ("fallin-angels.org", 27960))

readbuffer = ""
log = open("robopatbackup.log", "a")

while 1:
	readbuffer = readbuffer + urt.recv(4096)
	temp = string.split(readbuffer, "\n")
	readbuffer = temp.pop()

	for line in temp:
		if not line:
			time.sleep(60)
			urt.sendto("\xFF\xFF\xFF\xFFrcon fa4allut tracklist", ("fallin-angels.org", 27960))
		elif line == "\xFF\xFF\xFF\xFFprint":
			pass
		else:
			log.write(line + "\n")
