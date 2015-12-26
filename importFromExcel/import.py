# Will import all data from CSV and build a new database from it

import csv
import re
import sqlite3 as lite

ENTRIES_SCHEMA = r"displayName TEXT PRIMARY KEY, associatedNumbers TEXT, allLines TEXT, bannerPath TEXT, hasMultipleNumbers BOOLEAN, hasMultipleLines BOOLEAN"
CATEGORIES_SCHEMA = r"displayName TEXT, category TEXT, FOREIGN KEY(displayName) REFERENCES entries(displayName)"
CATEGORIES_LIST_SCHEMA = r"Category TEXT PRIMARY KEY"

def generateDatabase(entries):
	con = lite.connect('entries.db')
	cur = con.cursor()   
	try:
		cur.execute("DROP TABLE Entries")
	except:
		print "Table does not exist, continuing"

	cur.execute("CREATE TABLE Entries(" + ENTRIES_SCHEMA + ")")
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

	#generate categories table
	try:
		cur.execute("DROP TABLE categories")
	except:
		print "Table does not exist, continuing"

	cur.execute("CREATE TABLE Categories(" + CATEGORIES_SCHEMA + ")")
	for row in parseCategoryCSV():
		if row[0] == "":
			continue
		sqlStatement = "INSERT INTO Categories VALUES("
		sqlStatement = sqlStatement + "'" + row[0] + "', "
		sqlStatement = sqlStatement + "'" + row[1] + "')"
		try:
			cur.execute(sqlStatement)
		except Exception, e:
			print "error: "
			print e
			print sqlStatement

	#Populate Categories_List with distinct categories from categories
	try:
		cur.execute("DROP TABLE CategoriesList")
	except:
		print "Table does not exist, continuing"
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

csvFile = file("excelBook.csv", "rb")
reader = csv.reader(csvFile)

for row in reader:
	print row
