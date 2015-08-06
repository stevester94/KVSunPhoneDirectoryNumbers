#Parse Yellow Pages

class Category:
	def __init__(self):
		self.categoryName = ""
		self.categoryEntries = []

def testParseText(allEntries):
	allCategories = parseText()
	checkAgainstAllEntries(allCategories, allEntries)


def parseText():
	yellowPagesFile = file("Yellow Pages.txt", "r")
	isNewCategory = True
	allCategories = []

	for line in yellowPagesFile:
		if line == "\n" or line == "\r\n":

			isNewCategory = True
			continue
		elif not line[0].isalpha(): #Skip line begins with a space (generally if is additional info)
			continue
		elif isNewCategory:
			c = Category()
			c.categoryName = line.rstrip()
			allCategories.append(c)
			isNewCategory = False
		else:
			allCategories[-1].categoryEntries.append(line.rstrip())

	return allCategories

def checkAgainstAllEntries(allCategories, allEntries):
	associatedNames = []

	for e in allEntries:
		associatedNames.append(e.displayName)
	for c in allCategories:
		for e in c.categoryEntries:
			if e not in associatedNames:
				print e + ";"
