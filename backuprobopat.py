import socket
import subprocess

def backupLogOn(sv, owner):
	sv.send("PRIVMSG " + owner + " :Robo-PaT is gone, starting a backup log now.\r\n")
	logproc = subprocess.Popen(["python", "/home/nick/pybot/backuprobopat.logproc.py"])
	return logproc

def backupLogOff(sv, logproc, owner):
	sv.send("PRIVMSG " + owner + " :Robo-PaT has returned, ending backup logging\r\n")
	logproc.kill()
