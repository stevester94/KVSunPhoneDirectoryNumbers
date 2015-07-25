#Parse.py
#Parse White Pages entries into respective entries
#Will determine if multiple lines belong to the same entry

ALPHA_LETTERS = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")

class RawEntry:
	def __init__(self):
		self.lines = []

whitePages = file("WhitePages.txt", 'r')
RawEntries = []
BusinessEntries = []
PersonalEntries = []

#determine if the line should be skipped
#expects an rstripped line
def determineSkip(line):
	if line == '':
		return True
	if len(line) == 1:
		return True
	if line[0] in ALPHA_LETTERS and line[1] == '-': 
		return True
	else:
		return False


#iterate over every line in WhitePages.txt
#Determines first if line should be skipped
#Check if begins with a capital letter
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

#Seperate into business entries and personal entries
#Based soley on if has multiple entries
for r in RawEntries:
	if len(r.lines) > 1:
		BusinessEntries.append(r)
	else:
		PersonalEntries.append(r)

for r in BusinessEntries:
	print r.lines[0]
