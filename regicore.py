def getRest(count, line):
	returnstring = ""
	while count < len(line):
		returnstring = returnstring + " " + line[count]
		count = count + 1
	return returnstring

def verifyOwner(address):
	ownerfulladdr = ":" + Owner + "!" + OwnerAddr
	if (address == ownerfulladdr):
		return "true"
	else:
		return "false"