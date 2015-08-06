#Parse Yellow Pages
import autoCompleter
import csv
class Category:
	def __init__(self):
		self.categoryName = ""
		self.categoryEntries = []

def testYellowPages(associatedNames):
	allCategories = parseText("YellowPagesPatched.txt")
	unmatched = getUnmatchedEntries(allCategories, associatedNames)
	intelligentlyMatched = intelligentlyMatch(unmatched, associatedNames)
	sumC = 0
	for c in allCategories:
		sumC = sumC + len(c.categoryEntries)
	print "All possible: " + str(sumC) 
	print "length unmatched: " + str(len(unmatched))

	print "intelligentlyMatched: " + str(len(intelligentlyMatched))
	newUnmatched = removeIntelligentlyMatched(unmatched, intelligentlyMatched)
	print "new length unmatched: " + str(len(newUnmatched))

	allCategories = parseText("YellowPagesPatched.txt")
	unmatched = getUnmatchedEntries(allCategories, associatedNames)
	print "len post patched: " + str(len(unmatched))
	for u in unmatched:
		print u

def applyPatch(inFileName="Yellow Pages.txt", outFileName="YellowPagesPatched.txt"):
	inFile = file(inFileName, "r")
	outFile = file(outFileName, "w")
	matches = getPatchMatches()

	for line in inFile:
		for m in matches:
			if line.rstrip() == m[0].rstrip():
				line = m[1].rstrip()
		outFile.write(line.rstrip() + "\n")

def categoriesSanityCheck(associatedNames):
	categoriesFile = file("categories.csv", "r")
	categoriesCSV = csv.reader(categoriesFile)
	print "RUNNING CATEGORIES SANITY CHECK"
	for row in categoriesCSV:
		if row[0] not in associatedNames:
			print row[0] + "does not exist in displayNames!"
	print "CATEGORIES SANITY CHECK FINISHED"

#CSV in format (entry, category it belongs to)
def generateCategoriesCSV():
	allCategories = parseText("YellowPagesPatched.txt")
	categoriesFile = file("categories.csv", "w")
	categoriesCSV = csv.writer(categoriesFile, quoting=csv.QUOTE_ALL)

	for c in allCategories:
		for e in c.categoryEntries:
			categoriesCSV.writerow((e, c.categoryName))

def getUnmatchedEntries(allCategories, associatedNames):
	unmatchedCatEntries = []

	for c in allCategories:
		for e in c.categoryEntries:
			if e not in associatedNames:
				unmatchedCatEntries.append(e)
	return list(set(unmatchedCatEntries))

def getPatchMatches():
	patchFile = file("yellowPagesPatch.csv")
	patchCSV = csv.reader(patchFile)
	matches = []
	for row in patchCSV:
		matches.append(row)

	return matches

def intelligentlyMatch(unmatched, associatedNames):
	matches = []
	for u in unmatched:
		for a in associatedNames:
			newu = u.lower().replace(" ", "")
			newa = a.lower().replace(" ", "")
			if newa in newu or newu in newa:
				matches.append((u, a))

	return matches

#returns array of Category
def parseText(inFile="Yellow Pages.txt"):
	yellowPagesFile = file(inFile, "r")
	isNewCategory = True
	allCategories = []

	for line in yellowPagesFile:
		if line.rstrip() =="":
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

def removeIntelligentlyMatched(unmatched, intelligentlyMatched):
	allIntelligentlyMatched = []
	actuallyUnmatched = []
	for i in intelligentlyMatched:
		allIntelligentlyMatched.append(i[0])

	for u in unmatched:
		if u not in allIntelligentlyMatched:
			actuallyUnmatched.append(u)
	return actuallyUnmatched