# vim: ft=python :

import re

controlcodes = ["\x02", "\x09", "\x13", "\x0f", "\x15", "\x1f", "\x16"]

def stripColor(_input):
    outputtmp = re.sub("\x03\d+(,\d+)?", "", _input)
    output = ""
    for i in range(0, len(outputtmp) - 1):
        if not outputtmp[i] in controlcodes:
            output = output + outputtmp[i]

    return output
