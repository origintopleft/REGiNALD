#!/usr/bin/env python

# REGiNALD
# by Nicholas "Lavacano" O'Connor
# Purpose: Simple Python Bot

# Initally based off code from http://oreilly.com/pub/h/1968

import os
import sys
import socket
import string
import MySQLdb
from time import sleep
import datetime

# regidb is specific to REGiNALD, but still considered "required" for some of
# it's functionality.
import regidb

# Configuration
Server = "benjeffery.ca"
Port = 6667
Nick = "REGiNALD"
Ident = "reginald"
Realname = "You call these bagels?!"
Owner = "lavacano201014"
# Do not include the ~ in OwnerAddr anymore - you're set to ignore it
OwnerAddr = "nick@host--B3B66BE1.disorg.net"
HomeChannel = "#cipwttkt"
AdtlChannels = ["#bagboys"]
LogPingPong = 0
# End Configuration

# List bot modules here. Make sure you give them the proper elifs in the actual
# code as well.
import fort
import auth
import seen
import infonald
import choose
import regicalc
import backupcmds

# The reading buffer.
readbuffer="" # Obviously it's going to start blank >:-/

# Set up a connection to MySQL
mysqlconn = MySQLdb.connect(
		host = "localhost",
		user = "reginald",
                passwd = "reginald",
		db = "reginald")

# Set up a cursor for the MySQL connection.
db = mysqlconn.cursor()

# Clear the seen DB
db.execute("update seen set Online='N' where Online='Y';")

# Connect to the server.
sv = socket.socket()
sv.connect((Server, Port))
TGTNick = Nick
sv.send("NICK " + TGTNick + "\r\n")
sv.send("USER " + Ident + " " + Server + " bla :" + Realname + "\r\n")

def getRest(count, line):
	returnstring = ""
	while count < len(line):
		returnstring = returnstring + " " + line[count]
		count = count + 1
	return returnstring.lstrip()

logFile = open(Nick + "." + Server + ".log", "a")

def toLog(message):
	theTime = datetime.datetime.now()
        if theTime.hour < 10:
            hour = "0" + str(theTime.hour)
        else:
            hour = str(theTime.hour)
        if theTime.minute < 10:
            minute = "0" + str(theTime.minute)
        else:
            minute = str(theTime.minute)

	print "[", hour + ":" + minute, "]", message
	logFile.write(message + "\n")
	logFile.flush()
	os.fsync(logFile)

def verifyOwner(address):
	ownerfulladdr = ":" + Owner + "!" + OwnerAddr
	if (address.replace("~", "") == ownerfulladdr):
		return "true"
	else:
		return "false"

IsConnected = "F"

# We want each backup command to start off.
backupcmds.initbackupcmds()

# We've connected and defined functions, commence listening!
while 1:
	readbuffer = readbuffer + sv.recv(1024)
	temp = string.split(readbuffer, "\n")
	readbuffer = temp.pop()

	for line in temp:
		line = string.rstrip(line)
		line = string.split(line)

		if (line[0] == "PING"):
			sv.send("PONG " + line[1] + "\r\n")
			if (LogPingPong == 1):
				toLog("Received a PING, sending corresponding PONG")
		elif (line[0] == ""):
			pass
		elif (line[0] == "NOTICE"):
			if (line[1] == "AUTH"):
				toLog("Server's OnConnect Notice received.")
			else:
				toLog("NOTICE from " + line[1] + ": " + getRest(2, line))
		elif (line[0] == "ERROR"):
			toLog("ERROR from Server: " + getRest(1, line))
			if (line[1] == ":Closing"):
				toLog("Disconnecting socket.")
				sv.close()
				toLog("Waiting a few seconds before reconnecting.")
				sleep(5)
				toLog("Reconnecting.")
				sv = socket.socket()
				sv.connect((Server, Port))
				TGTNick = Nick
				sv.send("NICK " + TGTNick + "\r\n")
				sv.send("USER " + Ident + " " + Server + " bla: " + RealName + "\r\n")
		else:
			if (line[1] == "NOTICE"):
				toLog("Notice from " + line[0] + getRest(3, line))
			elif (line[1] == "001"):
				pass
			elif (line[1] == "002"):
				pass
			elif (line[1] == "003"):
				pass
			elif (line[1] == "004"):
				auth.authIn(Server, sv, line, TGTNick)
				sv.send("JOIN :" + HomeChannel + "\r\n")
				canGo = "f"
				try:
					if (sys.argv[1] == "-1"):
						toLog("Argument -1 was passed, skipping Additional Channels.")
					else:
						canGo = "t"
				except:
					canGo = "t"
				if canGo == "t":
					count = 0
					while count < len(AdtlChannels):
						sleep(3)
						sv.send("JOIN :" + AdtlChannels[count] + "\r\n")
						count = count + 1

				sv.send("PRIVMSG " + Owner + " :I have connected and am awaiting orders.\r\n")
			elif (line[1] == "005"):
				toLog("Connection to " + Server + " established.")
				IsConnected = "T"
			elif (line[1] == "251"):
				toLog("sv(251)" + getRest(3, line))
			elif (line[1] == "252"):
				toLog("sv(252)" + getRest(3, line))
			elif (line[1] == "254"):
				toLog("sv(254)" + getRest(2, line))
			elif (line[1] == "255"):
				toLog("sv(255)" + getRest(3, line))
			elif (line[1] == "332"):
				toLog("Topic for " + line[2] + " is" + getRest(3,line))
			elif (line[1] == "333"):
				toLog("sv(333)" + getRest(3, line))
			elif (line[1] == "352"):
				seen.seenOnline(db, line[7], string.strip(line[5], ":"))
				toLog(line[5] + " " + line[6] + "@" + line[5])
			elif (line[1] == "353"):
				toLog("/NAMES" + getRest(3, line))
			elif (line[1] == "366"):
				toLog("/NAMES list retrieved")
			elif (line[1] == "372"):
				pass
			elif (line[1] == "376"):
				toLog("End of MOTD received.")
			elif (line[1] == "401"):
				toLog("Nick " + line[3] + " does not exist")
                        elif (line[1] == "404"):
                                toLog("Numeric 404 received from " + line[3] + " - probably +c.")
                                infonald.infoLookupLastNoColor(db, sv, line[3])
			elif (line[1] == "422"):
				toLog("sv(422)" + getRest(3, line))
			elif (line[1] == "433"):
				TGTNick = TGTNick + "_"
				sv.send("NICK " + TGTNick + "\r\n")
			elif (line[1] == "PRIVMSG"):
				toLog(line[2] + "/" + line[0] + getRest(3, line))
				if (line[3] == "'\1'VERSION'\1'"):
					recvnick = line[0].explode("@")[0].explode(":")[1]
					sv.send("NOTICE " + recvnick + " :'\1'VERSION 'REGiNALD. by lavacano201014' Gentoo nrfoconnor@gmail.com'\1'\r\n")
				if (verifyOwner(line[0]) == "true"):
					if (line[2] == TGTNick):
						if (line[3] == ":exeunt"):
							if (len(line) > 4):
								sv.send("QUIT :" + getRest(4, line) + "\r\n")
								toLog("Exit from PM: " + getRest(4, line))
							else:
								sv.send("QUIT :Quit from PM (no reason given)\r\n")
								toLog("Exit from PM: No reason given.")
							db.close()
							mysqlconn.close()
							sys.exit()
						elif (line[3] == ":join"):
							sv.send("JOIN :" + line[4] + "\r\n")
						elif (line[3] == ":rawcmd"):
							sv.send(getRest(4, line) + "\r\n")
				if (line[3] == ":f"):
					fort.fort(line, sv)
				elif (line[3] == ":s"):
					if (len(line) > 4):
						seen.seenLookup(db, sv, string.strip(line[4], "'"), line[2])
				elif (line[3] == ":id"):
					if (len(line) > 4):
						seen.identify(db, sv, line[4], line[2])
				elif (line[3] == ":?"):
					if (len(line) > 4):
                                            infonald.infoLookup(db, sv, line[2], line[4])
				elif (line[3] == ":=?"):
					if (len(line) > 5):
						infonald.infoDefine(db, sv, line[2], line[4], getRest(5, line))
                                elif (line[3] == ":l?" and verifyOwner(line[0]) == "true"):
                                        if (len(line) > 4):
                                                infonald.infoLock(db, sv, line[2], line[4])
                                elif (line[3] == ":u?" and verifyOwner(line[0]) == "true"):
                                        if (len(line) > 4):
                                                infonald.infoUnlock(db, sv, line[2], line[4])
				elif (line[3] == ":c"):
					regicalc.regicalc(sv, line[2], line[0].split("!")[0], getRest(4, line))
				elif (line[3] == ":ch"):
					choose.choose(sv, line[2], getRest(4, line))
				elif (line[3] == ":bcmd"):
					backupcmds.backupcmdstatus(sv, line[2], line[4], line[5])
				elif (line[3] == ":!ts3"):
					backupcmds.backupts3(sv, line[2])
			elif (line[1] == "TOPIC"):
				toLog("Topic change for " + line[2] + " by " + line[0])
			elif (line[1] == "MODE"):
				toLog(line[2] + "/mode" + getRest(3,line) + " by " + line[0])
			elif (line[1] == "KICK"):
				toLog(line[2] + "/" + line[3] + ": KICK by " + line[0])
				if (line[3] == TGTNick):
					sv.send("JOIN :" + line[2] + "\r\n")
			elif (line[1] == "JOIN"):
				joinaddr = string.strip(line[0], ":")
				joinaddrarray = string.split(joinaddr, "!")
				joinnick = joinaddrarray[0]
				joinaddrarray = string.split(joinaddrarray[1], "@")
				joinhost = joinaddrarray[1]
				hostcheck = regidb.getNick(db, joinhost)
				nickcheck = regidb.getAddr(db, joinnick)
				if (joinnick == TGTNick):
					sv.send("WHO :" + line[2] + "\r\n")
				elif (hostcheck == None):
					if (nickcheck == None):
						db.execute("insert into who values('" + joinnick + "', '" + joinhost + "', 'N');")
						toLog(joinnick + " added to DB")
				if (joinnick != TGTNick):
					seen.seenOnline(db, joinnick, joinhost)
					#infonald.infoJoinline(db, sv, joinnick, hostcheck[0], line[2])
				toLog(line[0] + " joined " + line[2])
			elif (line[1] == "NICK"):
				toLog(line[0] + " change nick to " + line[2])
				seen.updateNick(db, line[0], string.strip(line[2], ":"))
			elif (line[1] == "QUIT"):
				quitaddr = string.strip(line[0], ":")
				quitaddrarray = string.split(quitaddr, "!")
				quitnick = quitaddrarray[0]
				quitaddrarray = string.split(quitaddrarray[1], "@")
				quithost = quitaddrarray[1]
				toLog("QUIT " + line[0] + getRest(2, line))
				seen.seenOffline(db, quitnick, quithost, getRest(2, line))
			else:	
				toLog(" !!! [[ " + getRest(1, line) + " ]] " + line[0])
                try:
                        mysqlconn.commit()
                except:
                        toLog("Exception flung with mysqlconn.commit()")
