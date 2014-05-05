import socket

def authIn(Server, sv, line, TGTNick):
	if Server == "shuttlecraft":
		AuthCMD = "AX-S :LOGIN REGiNALD "
	elif Server == "irc.gamesurge.net":
		AuthCMD = "AuthServ@Services.Gamesurge.net :AUTH REGiNALD "
        elif Server == "benjeffery.ca":
                AuthCMD = "NickServ :IDENTIFY "
	sv.send("PRIVMSG " + AuthCMD + "[REDACTED]\r\nMODE " + TGTNick + " :+x\r\n")
