#Parse.py
#Parse White Pages entries into respective entries
#Will determine if multiple lines belong to the same entry
#Will then check to see if entries contain a number
#	they may not due to poorly formatted data

import re
import sqlite3 as lite
import csv
from os import listdir



ALPHA_LETTERS = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")
TOLL_FREE_REG = r"[0-9][0-9][0-9].[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]"
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

#This modifes the entries passed in, setting contains number as necessary
def checkEntriesForNumbers(entries):
	regex = r"[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]"
	compiledReg = re.compile(regex)

	for entry in entries:
		for line in entry.lines:
			regResult = compiledReg.search(line)
			if regResult != None:
				entry.containsNumber = True

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

#Generate CSV files for entry names and formatted image names
def generateCSVs(entries):
	imageNamesFile = file("imageNames.csv", "w")
	entriesNamesFile = file("entryNames.csv", "w")

	imageNamesCSV = csv.writer(imageNamesFile)
	entriesNamesCSV = csv.writer(entriesNamesFile, quoting=csv.QUOTE_ALL)

	files = listdir("./formatted")

	for f in files:
		if f[-4:] == ".jpg":
			f = f[:-4]
		imageNamesCSV.writerow([f])

	for e in entries:
		entriesNamesCSV.writerow([e.displayName])

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

#matches out all numbers and remove them, place them in phonenumber field
#Run on all, number is only removed from single line entries
def parseAndFormEntries(entries):
	compiledTollFreeReg = re.compile(TOLL_FREE_REG)
	compiledStandardReg = re.compile(STANDARD_REG)

	for entry in entries:
		entry.displayName = entry.lines[0]
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
			if line == entry.lines[0]:
				entry.displayName = line.replace(number, '') #remove number from displayName

		if entry.bannerPath == "":
			entry.bannerPath = "no path entered"

		#cut off trailing white space
		while entry.displayName[-1] == ' ' or entry.displayName[-1] == '	':
			entry.displayName = entry.displayName[:-1]

def parseBannerPaths(entries):
	csvFile = file("bannerPaths.csv", "r")
	reader = csv.reader(csvFile)

	for row in reader:
		matchedEntry = None
		for e in entries:
			if e.displayName == row[1]:
				matchedEntry = e
		matchedEntry.bannerPath = row[0]

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

def dumpDisplayNames(entries):
	for e in entries:
		print e.displayName + ";"


if __name__ == '__main__':
	[businessEntries, personalEntries] = parseEntries()
	allEntries = businessEntries + personalEntries
	parseAndFormEntries(allEntries)

	print "options: "
	print "1. run sanity checks"
	print "2. generateDatabase"
	print "3. generateCSVs"
	print "4. parseBannerPath"
	print "5. dumpDisplayNames"
	print "x. exit"

	choice = ""
	while choice != "x":
		choice  = (raw_input("choice: ")).rstrip()

		if choice == "1":
			sanityCheck(allEntries)
		elif choice == "2":
			generateDatabase(allEntries)
		elif choice == "3":
			generateCSVs(allEntries)
		elif choice == "4":
			pass
		elif choice == "5":
			dumpDisplayNames(allEntries)
		elif choice == "x":
			exit()
		else:
			print "Wrong input"

