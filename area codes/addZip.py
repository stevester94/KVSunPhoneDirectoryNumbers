import re
import sqlite3 as lite

NO_ZIP_REG = r"\s[0-9]{3}-[0-9]{4}"
compiledReg = re.compile(NO_ZIP_REG)

def retPrependedZip(associatedNumbers, allLines):
	results = compiledReg.findall(allLines)

	for r in results:
		match = "".join(r.split()) #remove all whitespace
		allLines = allLines.replace(match, '760-' + match)
		associatedNumbers = associatedNumbers.replace(match, '760-' + match)

	return (associatedNumbers, allLines)



con = lite.connect('entries.db')
cur = con.cursor()

# Sanity check, don't want numbers inside of entry name
# Exits if found
for row in con.execute("select * from Entries"):
	e = row[0]
	s = unicode(e)
	results = compiledReg.findall(s)
	if(len(results) > 0):
		print e
		exit(0)

for row in con.execute("select displayName, associatedNumbers, allLines from entries"):
	displayName = row[0]
	associatedNumbers = row[1]
	allLines = row[2]

	[associatedNumbers, allLines] = retPrependedZip(associatedNumbers, allLines)

	query = "UPDATE entries SET "
	query = query + r'associatedNumbers= "' + associatedNumbers + r'", '
	query = query + 'allLines="' + allLines + '" '
	query = query + 'WHERE displayName = "' + displayName + '"'

	print query









con.commit()
con.close()