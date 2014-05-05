import MySQLdb
import regidb
import datetime
import string
import socket
import _mysql_exceptions
import sys

def seenOnline(db, nick, addr):

	date = str(datetime.date.today())
	knownNick = regidb.getNick(db, addr)
	if knownNick != None:
		botchk = regidb.botChk(db, knownNick)
	else:
		botchk = None
	db.execute("select * from seen where Address='" + addr + "';")
	seenbefore = db.fetchone()
	if seenbefore == None:
		db.execute("insert into seen values('" + addr + "', 'Y', '" + nick + "', '" + date + "', NULL);")
	elif botchk != None:
		if botchk == "True":
			pass
		else:
			db.execute("update seen set LastSeen='" + date + "', Online='Y', LastNick='" + nick + "' where Address='" + addr + "';")

def seenOffline(db, nick, addr, quit=None):
	try:
		date = str(datetime.date.today())
		knownNick = regidb.getNick(db, addr)
		if knownNick != None:
			botchk = regidb.botChk(db, knownNick)
		else:
			botchk = None
		if botchk != None:
			if botchk == "False":
				if quit == None:
					db.execute("update seen set Online='N', LastNick='" + nick + "' where Address='" + addr + "';")
				else:
					db.execute("update seen set Online='N', LastNick='" + string.replace(nick, "\\", "\\\\") + "', LastQuit='" + quit + "' where Address='" + addr + "';")
	except _mysql_exceptions.ProgrammingError:
		sv.send("PRIVMSG lavacano201014 :Exception thrown in seen.seenOffline(), check logs!\r\n")
                print sys.exc_info()

def updateNick(db, unformatted_addr, nick):
	formatarray_addr = string.split(unformatted_addr, "!")
	addrarray = string.split(formatarray_addr[1], "@")
	addr = addrarray[1]
	db.execute(string.replace("update seen set LastNick='" + nick + "' where Address='" + addr + "';", "\\", "\\\\"))

def identify(db, sv, nickraw, chan):
        nick = nickraw.replace("'", "\'").replace('"', '\"')
	try:
		db.execute("select Address from seen where LastNick='" + string.replace(nick, "\\", "\\\\") + "' and Online='Y';")
		addr = db.fetchone()
		if addr == None:
			sv.send("PRIVMSG " + chan + " :Nick doesn't seem to exist.\r\n")
		else:
			db.execute("select Nick from who where Address='" + addr[0] + "';")
			result = db.fetchone()
			if result == None:
				sv.send("PRIVMSG " + chan + " :I don't know who " + nick + " is.\r\n")
			else:
				sv.send("PRIVMSG " + chan + " :I know " + nick + " as " + result[0] + ".\r\n")
	except _mysql_exceptions.ProgrammingError:
		sv.send("PRIVMSG " + chan + " :Stop trying to fuck with me, KTHX.\r\n")
def seenLookup(db, sv, nick, chan):
	try:
		if nick == "--help":
			sv.send("PRIVMSG " + chan + " :usage - s <nick>\r\n")
		elif nick == "Alice":
			sv.send("PRIVMSG " + chan + " :Alice doesn't live at the restaurant, she lives in the church nearby...\r\n")
		else:
			botchk = regidb.botChk(db, nick)
			if botchk == "NaN":
				sv.send("PRIVMSG " + chan + " :I don't know who " + nick + " is.\r\n")
			elif botchk == "True":
				sv.send("PRIVMSG " + chan + " :" + nick + " is a bot, and therefore ignored.\r\n")
			else:
				addr = regidb.getAddr(db, nick)
				db.execute("select LastSeen, LastNick, Online from seen where Address='" + addr + "';")
				result = db.fetchone()
				if result == None:
					sv.send("PRIVMSG " + chan + " :I know who " + nick + " is, but I haven't seen them since this script was started.\r\n")
				elif result[2] == "Y":
					sv.send("PRIVMSG " + chan + " :" + nick + " is online now. (" + result[1] + ")\r\n")
				else:
					today = str(datetime.date.today())
					if result[0] == today:
						seendate = "today"
					else:
						seendate = result[0]
						sv.send("PRIVMSG " + chan + " :" + nick + " was last seen " + str(seendate) + " (as " + result[1] + ").\r\n")
	except _mysql_exceptions.ProgrammingError:
		sv.send("PRIVMSG " + chan + " :Stop trying to fuck with me, KTHX.\r\n")
