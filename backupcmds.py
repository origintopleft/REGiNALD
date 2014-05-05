import telnetlib
import socket

backupcmdstatusdict = {}

def initbackupcmds():
	backupcmdstatusdict["ts3"] = 0

def backupcmdstatus(sv, chan, setting, command):
	try:
		if setting == "on":
			backupcmdstatus[command] = 1
			sv.send("PRIVMSG " + chan + " :Backup command !" + command + " enabled.\r\n")
		elif setting == "off":
			backupcmdstatus[command] = 0
			sv.send("PRIVMSG " + chan + " :Backup command !" + command + " disabled.\r\n")
	except:
		pass

def backupts3(sv, chan):
	if backupcmdstatusdict["ts3"] == 0:
		return 0
	sv.send("PRIVMSG " + chan + " :Working on !ts3. Please wait.\r\n")
	ts3query = telnetlib.Telnet("fallin-angels.org", 10011)
	ts3query.write("use sid=1\n")
	ts3query.read_until("error id=0 msg=ok", 10)
	ts3query.write("clientlist -away\n")
	results = ts3query.read_until("error id", 10)

	namesList = ""

	for client in results.split("|"):
		isAway = 0
		for keyvalue_string in client.split(" "):
			keyvalue_list = keyvalue_string.split("=")
			key = keyvalue_list[0]
			try:
				value = keyvalue_list[1]
			except:
				pass
			if key == "cid":
				if value == "14":
					isAway = 1
			elif key == "client_nickname":
				if isAway == 1:
					namesList = namesList + value.replace("\s", " ") + " (zZz), "
				else:
					namesList = namesList + value.replace("\s", " ") + ", "
	
	sv.send("PRIVMSG " + chan + " :Current TS3 Clients: " + namesList[:-2] + "\r\n")
	ts3query.write("quit\n")
	try:
		ts3query.close()
	except:
		pass
