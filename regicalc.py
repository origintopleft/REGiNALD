import string
import socket

operators = ["+", "-", "*", "/"]

def regicalc(sv, chan, nick, evaluator):
	calc = string.lstrip(evaluator, ":").replace(",", "")
        if evaluator.rstrip()[-1] in operators:
                sv.send("PRIVMSG " + chan + " :" + nick + ": Sorry, I don't (currently!) support Reverse Polish Notation. It's not off the table however!\r\n")
        else:
                try:
	    	        result = eval(calc)
        	except:
	        	return
                #returnstring = str(result) # TODO - group digits in result
        	sv.send("PRIVMSG " + chan + " :" + nick + ": " + str(result) + "\r\n")
