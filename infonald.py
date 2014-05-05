import MySQLdb
import _mysql_exceptions
import socket

import _colorsupport

LastKeyword = ""
LastDef = ""

def infoIsLocked(db, sv, keyword):
        db.execute("select Locked from infonald where Keyword='" + keyword + "';")
        result = db.fetchone()

        if result == None:
                return False
        elif result[0] == "Y":
                return True
        else:
                return False

def infoLock(db, sv, chan, keywordraw):
        keyword = keywordraw.replace("'", "\\'").replace('"', '\\"').replace(";", "")

        try:
                db.execute("update infonald set Locked='Y' where Keyword='" + keyword + "';")
                sv.send("PRIVMSG " + chan + " :Keyword " + keywordraw + " successfully locked.\r\n")
        except _mysql_exceptions.ProgrammingError:
                pass

def infoUnlock(db, sv, chan, keywordraw):
        keyword = keywordraw.replace("'", "\\'").replace('"', '\\"').replace(";", "")

        try:
                db.execute("update infonald set Locked='N' where Keyword='" + keyword + "';")
                sv.send("PRIVMSG " + chan + " :Keyword " + keywordraw + " successfully unlocked.\r\n")
        except _mysql_exceptions.ProgrammingError:
                pass

def infoDefine(db, sv, chan, keywordraw, definitionraw):
        keyword = keywordraw.replace("'", "\\'").replace('"', '\\"').replace(";", "")
        definition = definitionraw.replace("'", "\\'").replace('"', '\\"').replace(";", "")

        if infoIsLocked(db, sv, keyword):
                sv.send("PRIVMSG " + chan + " :Definition is locked.\r\n")
                return

	db.execute("select * from infonald where Keyword='" + keyword + "';")
	check = db.fetchone()
	if check == None:
		try:
			db.execute("insert into infonald values('" + keyword + "', '" + definition + "', 'N');")
			sv.send("PRIVMSG " + chan + " :Keyword " + keywordraw + " successfully defined.\r\n")
		except _mysql_exceptions.ProgrammingError:
			sv.send("PRIVMSG " + chan + " :Stop trying to fuck with me, KTHX\r\n")
	else:
		try:
			db.execute("update infonald set Definition='" + definition + "' where Keyword='" + keyword + "';")
			sv.send("PRIVMSG " + chan + " :Keyword " + keywordraw + " successfully updated.\r\n")
		except _mysql_exceptions.ProgrammingError:
			sv.send("PRIVMSG " + chan + " :Stop trying to fuck with me, KTHX\r\n")

def infoLookup(db, sv, chan, keywordraw):
        global LastKeyword
        global LastDef
	keyword = keywordraw.replace("'", "\\'").replace('"', '\\"').replace(";", "")
	try:
		db.execute("select Definition from infonald where Keyword='" + keyword + "';")
		result = db.fetchone()
	except _mysql_exceptions.ProgrammingError:
		sv.send("PRIVMSG " + chan + " :Stop trying to fuck with me, KTHX")
		return None
	if result != None:
		definition = result[0]
                sv.send("PRIVMSG " + chan + " :[" + keywordraw + "] " + definition + "\r\n")
                LastKeyword = keywordraw
                LastDef = definition
        else:
                sv.send("PRIVMSG " + chan + " :Keyword " + keywordraw + " doesn't seem to exist.\r\n")

def infoLookupLastNoColor(db, sv, chan):
        global LastDef
        if LastDef != "":
            definition = _colorsupport.stripColor(LastDef)

            sv.send("PRIVMSG " + chan + " :[" + LastKeyword + "] " + definition + "\r\n")
            sv.send("PRIVMSG " + chan + " :The above definition contains color codes, which were stripped due to receiving numeric 404. (The channel is probably +c)\r\n")

            LastDef = "" # Prevent repeating

def infoJoinline(db, sv, nick, realnick, chan):
	db.execute("select Definition from infonald where Keyword='" + realnick + "';")
	result = db.fetchone()
	if result != None:
		sv.send("PRIVMSG " + chan + " :[" + nick + " | " + realnick + "] " + result[0] + "\r\n")
