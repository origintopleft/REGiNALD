# REGiDB by Nicholas "Lavacano" O'Connor
# Designed for REGiNALD by Nicholas "Lavacano" O'Connor

# This module contains shortcuts for some very common functions, as well as a
# "new user" type function for REGiNALD itself (to be executed when an unknown
# connects).

# The DB cursor is required to be passed into the functions.

import MySQLdb

def botChk(db, nick):
	db.execute("select Bot from who where Nick = '" + nick + "';")
	result = db.fetchone()
	if result == None:
		return "NaN"
	elif result[0] == "Y":
		return "True"
	else:
		return "False"

def getNick(db, addr):
	db.execute("select Nick from who where Address = '" + addr + "';")
	result = db.fetchone()
	if result == None:
		return None
	else:
		return result[0]

def getAddr(db, nick):
	db.execute("select Address from who where Nick = '" + nick + "';")
	result = db.fetchone()
	if result == None:
		return None
	else:
		return result[0]

def newUser(db, nick, address):
	db.execute("insert into who values('" + nick + "', '" + address + "', 'N');")
