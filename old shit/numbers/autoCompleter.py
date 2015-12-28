#auto completer...
from subprocess import call

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()





numbers = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
import csv

#returns [(entry, possibleEntryItHasBeenMatched to)]
# IE maps entry->possibleEntries
def runAutoCompleter(entriesToMatch, possibleEntries):
	call(["clear"])
	getch = _Getch()
	matches = []
	skipFlag = False

	for entry in entriesToMatch:
		matchedEntry = ""
		oldMatches = []
		possibleMatches = []
		c = ""
		string = ""

		while True:
			call("clear")
			print "entry to match: " + entry

			if c == "|":
				skipFlag = True
				break
			elif len(c) > 0 and ord(c) == 127:
				string = string[:-1]
			elif c in numbers:
				matchedEntry = possibleMatches[int(c)]
				break
			else:
				string = string + c
			possibleMatches = getPossibleMatches(string, possibleEntries)



			index = 0
			for i in range(10):
				try:
					print str(index) + ":" + possibleMatches[i]
				except:
					print str(index) + ":"
				index = index + 1
			print "|: skip"
			print ""

			print string + "_"
			c = getch()
		if not skipFlag:
			matches.append((entry, matchedEntry))
		else:
			skipFlag = False

	print "done"
	for m in matches:
		print m[0] + " : " + m[1]

	return matches

def getPossibleMatches(inS, possibleEntries):
	maxNumEntries = 10
	retAr = []
	for e in possibleEntries:
		if e[:len(inS)].lower() == inS.lower():
			retAr.append(e)
		if len(retAr) >= maxNumEntries:
			break
	return retAr

def writeOutMatches(matches, outFileName):
	outFile = file(outFileName, "w")
	matchesCSV = csv.writer(outFile, quoting=csv.QUOTE_ALL)

	for m in matches:
			matchesCSV.writerow(m)

if __name__ == '__main__':
	possibleEntries = ["the", "lel", "topKek", "top"]	
	entriesToMatch  = ["FUGGGG", "chortle"]

	runAutcompleter(entriesToMatch, possibleEntries, "autoCompleterTest")
