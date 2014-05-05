import socket
import string
import random

def choose(sv, chan, itemstring):
	itemstring = string.lstrip(itemstring, " :")
	items = string.split(itemstring, " or ")
	if (len(items) > 1):
		choice = random.randint(0, len(items) - 1)
		sv.send("PRIVMSG " + chan + " :" + items[choice] + "\r\n")
	elif (len(items) == 1):
		sv.send("PRIVMSG " + chan + " :Error: Need more than one item. [ch <item1> or <item2> [or <item3> [...]]\r\n")
