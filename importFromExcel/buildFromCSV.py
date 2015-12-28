# Will import all data from CSV and build a new database from it

import csv
import re
import sqlite3 as lite

ENTRIES_SCHEMA = r"displayName TEXT PRIMARY KEY, associatedNumbers TEXT, allLines TEXT, bannerPath TEXT, hasMultipleNumbers BOOLEAN, hasMultipleLines BOOLEAN"
CATEGORIES_SCHEMA = r"displayName TEXT, category TEXT, FOREIGN KEY(displayName) REFERENCES entries(displayName)"
CATEGORIES_LIST_SCHEMA = r"Category TEXT PRIMARY KEY"
STANDARD_REG  = r"[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]"

entriesCsvName = "EntriesBetaCSV.csv"
categoriesCsvName = "CategoriesAlphaCSV.csv"

entries = []
categories = []

class RawEntry:
	def __init__(self):
		self.allLines = []
		self.containsNumber = False
		self.hasMultipleLines = False
		self.hasMultipleNumbers = False
		self.associatedNumbers = []
		self.displayName = ""
		self.bannerPath = ""



def generateDatabase():
	print "Generating database\n"

	con = lite.connect('entries.db')
	cur = con.cursor()   
	try:
		cur.execute("DROP TABLE Entries")
	except:
		print "Entries does not exist, creating"

	cur.execute("CREATE TABLE Entries(" + ENTRIES_SCHEMA + ")")
	for entry in entries:

		displayName = entry.displayName
		associatedNumbers = entry.associatedNumbers
		bannerPath = entry.bannerPath
		allLines = entry.allLines
		hasMultipleLines = entry.hasMultipleLines
		hasMultipleNumbers = entry.hasMultipleNumbers

		#Form each component as required for SQL

		#displayName and allLines needs double escaped quotes
		# displayName = displayName.replace("'", "''")
		# allLines = allLines.replace("'", "''")

		#associatedNumbers needs to be one string
		associatedNumbers = " ".join(associatedNumbers)

		# Need 0 or 1 for the boolean values
		hasMultipleLines = str(int(hasMultipleLines))
		hasMultipleNumbers = str(int(hasMultipleNumbers))

		#Replace the god forsaken new lines
		# CR_LF = "CHAR(13,10)"
		# allLines = allLines.replace('\r','') #Delete carriage return
		# allLines = allLines.replace('\n', CR_LF) # Replace new lines with the windows style line break

		payload = (displayName, associatedNumbers, allLines, bannerPath, hasMultipleNumbers, hasMultipleLines)





		# sqlStatement = "INSERT INTO Entries VALUES("
		# sqlStatement = sqlStatement + "'" + displayName + "', "
		# sqlStatement = sqlStatement + "'" + associatedNumbers + "', "
		# sqlStatement = sqlStatement + "'" + allLines + "', "
		# sqlStatement = sqlStatement + "'" + entry.bannerPath + "', "
		# sqlStatement = sqlStatement + hasMultipleNumbers + ", "
		# sqlStatement = sqlStatement + hasMultipleLines
		# sqlStatement = sqlStatement + ")"
			
		try:
			cur.execute("INSERT INTO Entries VALUES (?,?,?,?,?,?)", payload)
		except Exception, e:
			print "error: "
			print e
			print displayName

	#generate categories table
	try:
		cur.execute("DROP TABLE categories")
	except:
		print "categories does not exist, creating"

	cur.execute("CREATE TABLE Categories(" + CATEGORIES_SCHEMA + ")")
	for c in categories:
		try:
			cur.execute("INSERT INTO Categories VALUES(?,?)",c)
		except Exception, e:
			print "error: "
			print e
			print c[0]

	#Populate Categories_List with distinct categories from categories
	try:
		cur.execute("DROP TABLE CategoriesList")
	except:
		print "CategoriesList does not exist, creating"
	cur.execute("CREATE TABLE CategoriesList(" + CATEGORIES_LIST_SCHEMA + ")")	
	sqlStatement = "INSERT INTO CategoriesList Select DISTINCT category from CATEGORIES"
	try:
		cur.execute(sqlStatement)
	except Exception, e:
		print "error: "
		print e
		print sqlStatement
	con.commit()
	con.close()


#Returns array of tuple-> (displayName, category)
def populateCategories():
	print "Populating categories..."

	csvFile = file(categoriesCsvName, "r")
	reader = csv.reader(csvFile)
	for row in reader:
		categories.append((row[0], row[1]))

#Populate the entries array from the CSV explorted from excel
def populateEntries():
	print "Populating entries..."

	csvFile = file(entriesCsvName, "rb")
	reader = csv.reader(csvFile)

	for row in reader:
		entry = RawEntry()

		entry.displayName = row[0]
		entry.allLines = row[1]
		entry.bannerPath = row[2]

		# Parse out Associated phone numbers from lines
		entry.associatedNumbers = re.findall(STANDARD_REG, entry.allLines)

		if len(entry.associatedNumbers) < 1:
			entry.containsNumber = False
		else:
			entry.containsNumber = True

		# Determine if has multiple numbers
		if len(entry.associatedNumbers) > 1:
			entry.hasMultipleNumbers = True
		else:
			entry.hasMultipleNumbers = False

		# Determine if has multiple lines
		if '\n' in entry.allLines:
			entry.hasMultipleLines = True
		else:
			entry.hasMultipleLines = False

		# Done, append entry to master list
		entries.append(entry)

# Will check integrity of data
def sanityCheck():
	print "performing sanity checks...\n"

	# Check if all entries have an associated number
	print "##############################"
	print '# checking associatedNumbers #'
	print "##############################"

	for e in entries:
		if e.containsNumber == False:
			print "entry with displayName: '" + e.displayName + "' contains has no associatedNumbers"

	# Check if every display name in categories actually exists in entries
	print "##############################"
	print '#    checking Categories     #'
	print "##############################"
	allDisplayNames = []
	for e in entries:
		allDisplayNames.append(e.displayName)

	for c in categories:
		if c[0] not in allDisplayNames:
			print "Category with displayName: '" + c.displayName + "' does not have corresponding entry in entries"



if __name__ == '__main__':
	populateEntries()
	populateCategories()

	sanityCheck()

	generateDatabase()