#Parse.py
#Parse White Pages entries into respective entries
#Will determine if multiple lines belong to the same entry
#Will then check to see if entries contain a number
#	they may not due to poorly formatted data

import re
import sqlite3 as lite


ALPHA_LETTERS = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")
TOLL_FREE_REG = r"800.[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]"
STANDARD_REG  = r"[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]"

DATABASE_SCHEMA = r"displayName TEXT, associatedNumbers TEXT, allLines TEXT, bannerPath TEXT, hasMultipleNumbers BOOLEAN, hasMultipleLines BOOLEAN"



class RawEntry:
	def __init__(self):
		self.lines = []
		self.containsNumber = False
		self.multiLine = False
		self.associatedNumbers = []
		self.displayName = ""
		self.bannerPath = ""


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
def parseEntries():
	whitePages = file("WhitePages.txt", 'r')
	RawEntries = []
	BusinessEntries = []
	PersonalEntries = []

	for l in whitePages:
		currentLine = l.rstrip()

		if determineSkip(currentLine):
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
			r.multiLine = True
			BusinessEntries.append(r)
		else:
			r.multiLine = False
			PersonalEntries.append(r)

	whitePages.close()

	return [BusinessEntries, PersonalEntries]

#This modifes the entries passed in, setting contains number as necessary
def checkEntriesForNumbers(entries):
	regex = r"[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]"
	compiledReg = re.compile(regex)

	for entry in entries:
		for line in entry.lines:
			regResult = compiledReg.search(line)
			if regResult != None:
				entry.containsNumber = True

def automatedCheck():
	[businessEntries, personalEntries] = parseEntries()
	allEntries = businessEntries + personalEntries
	checkEntriesForNumbers(allEntries)
	for entry in allEntries:
		if entry.containsNumber == False:
			print entry.lines[0]

#matches out all numbers and remove them, place them in phonenumber field
#Run on all, number is only removed from single line entries
def parseAndFormEntries(entries):
	compiledTollFreeReg = re.compile(TOLL_FREE_REG)
	compiledStandardReg = re.compile(STANDARD_REG)

	for entry in entries:
		for line in entry.lines:
			#we search first for toll free numbers so that we dont get dangling 800's
			number =  None
			try:
				number = compiledTollFreeReg.search(line).group()
			except:
				pass

			if number == None:
				try:
					number = compiledStandardReg.search(line).group()
				except:
					print "no number for line: " + line
					if len(entry.lines) == 1: #For one liners with no phone info
						entry.displayName = line
					continue

			entry.associatedNumbers.append(number)
			if entry.multiLine == False:
				entry.displayName = line.replace(number, '') #remove number from entry if is single line
			else:
				entry.displayName = entry.lines[0]


def testParseAndForm():
	[businessEntries, personalEntries] = parseEntries()
	allEntries = businessEntries + personalEntries
	parseAndFormEntries(allEntries)
	sanityCheck(allEntries)


def generateDatabase(entries):
	con = lite.connect('entries.db')
	cur = con.cursor()   
	try:
		cur.execute("DROP TABLE Entries")
	except:
		print "Table does not exist, continuing"

	cur.execute("CREATE TABLE Entries(" + DATABASE_SCHEMA + ")")
	for entry in entries:
		sqlStatement = "INSERT INTO Entries VALUES("
		sqlStatement = sqlStatement + "'" + entry.displayName + "', "
		sqlStatement = sqlStatement + "'" + " ".join(entry.associatedNumbers) + "', "
		sqlStatement = sqlStatement + "'" + "'||CHAR(10)||'".join(entry.lines) + "', "
		sqlStatement = sqlStatement + "'" + entry.bannerPath + "'" + ", "
		sqlStatement = sqlStatement + str(int(len(entry.associatedNumbers) > 1)) + ", "
		sqlStatement = sqlStatement + str(int(len(entry.lines) > 1))
		sqlStatement = sqlStatement + ")"
		
		try:
			cur.execute(sqlStatement)
		except Exception, e:
			print "error: "
			print e
			print sqlStatement

	con.commit()
	con.close()

def testDatabase():
	[businessEntries, personalEntries] = parseEntries()
	allEntries = businessEntries + personalEntries
	parseAndFormEntries(allEntries)
	sanityCheck(allEntries)
	generateDatabase(allEntries)


#just want to check that everything is kosher...
def sanityCheck(entries):
	print "SANITY REPORT: "
	for e in entries:
		if e.displayName == "":
			print e.lines[0] + " has no displayName"
		if len(e.associatedNumbers) <= 0:
			print e.displayName + " has no associatedNumbers"
		if e.multiLine == False and len(e.lines) > 1:
			print e.displayName + " is singleLine with multiple lines"
		if e.multiLine and len(e.lines) < 2:
			print e.displayName + " is multiLine with one line"
		if len(e.lines) < 1:
			print e.displayName + " has no lines"


if __name__ == '__main__':
    testDatabase()