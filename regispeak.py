def cmdResult(db, sv, nick, chan, message):
	db.execute("select Quiet, AddressMe, PMresult from opts where Address='" + regidb.getAddr(db, nick) + "';")
