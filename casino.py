import random
import socket

StartBalance = 500

def balance(nick, op, myNick, amount=0):
	balfile = open("/var/" + myNick + "/db/casino/" + nick, "r+")
	initial = int(balfile.read())
	if op == "check":	
		result = initial
	else:
		if op == "add":
			result = initial + amount
		elif op == "sub":
			result = initial - amount
		else:
			result = initial
			print "The argument passed for op in casino.balance() was " + op + ", probably a typo."
		balfile.write(str(result))
	return result

def startMeUp(nick, myNick): # the mick jagger function
	balfile = open("/var/" + myNick + "/db/casino/" + nick, "w")
	balfile.write(str(StartBalance))
