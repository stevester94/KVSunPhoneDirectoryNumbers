#Parse.py
#Parse White Pages entries into respective entries
#Will determine if multiple lines belong to the same entry

ALPHA_LETTERS = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")

class RawEntry:
	def __init__(self):
		self.lines = []

whitePages = file("WhitePages.txt", 'r')
RawEntries = []

#determine if the line should be skipped
#expects an rstripped line
def determineSkip(line):
	if len(line) == 2 and line[1] == '-':
		return True
	if line == '':
		return True
	if len(line) == 1:
		return True
	else:
		return False


#iterate over every line in WhitePages.txt
#if the line is blank skip
#if the line begins with a space it is a member of the last entry
#	if so, will append to the lines member of the RawEntry
#Else will begin a new raw entry
for l in whitePages:
	currentLine = l.rstrip()

	if determineSkip(currentLine):
		print "skipped line"
		continue

	if currentLine[0] not in ALPHA_LETTERS:
		RawEntries[-1].lines.append(currentLine)

	else:
		r = RawEntry()
		r.lines.append(currentLine)
		RawEntries.append(r)


for r in RawEntries:
	print r.lines[0]
