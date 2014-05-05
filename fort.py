import string
import subprocess
import socket

def fort(line, sv):
	if len(line) > 4:
		if line[4] == "o":
			fortune = subprocess.Popen(["fortune", "-os"], stdout=subprocess.PIPE)
		elif line[4] == "a":
			fortune = subprocess.Popen(["fortune", "-as"], stdout=subprocess.PIPE)
		else:
			sv.send("PRIVMSG " + line[2] + " :Unrecognized argument. Valid arguments are \"o\" (for offensive fortunes only) or \"a\" (for all fortunes, offensive or not)\r\n")
			fortune = subprocess.Popen(["fortune", "-s"], stdout=subprocess.PIPE)
	else:
		fortune = subprocess.Popen(["fortune", "-s"], stdout=subprocess.PIPE)
	output = fortune.communicate()
	result = string.replace(output[0], "\n", "\r\nPRIVMSG " + line[2] + " :")
	sv.send("PRIVMSG " + line[2] + " :" + result + "\r\n")
