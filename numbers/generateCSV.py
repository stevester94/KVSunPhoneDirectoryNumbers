#generate csv files
import csv
from os import listdir

def generateCSVs(entries):
	imageNamesFile = file("imageNames.csv", "w")
	entriesNamesFile = file("entryNames.csv", "w")

	imageNamesCSV = csv.writer(imageNamesFile)
	entriesNamesCSV = csv.writer(entriesNamesFile)

	files = listdir("./formatted")

	for f in files:
		if f[-4:] == ".jpg":
			f = f[:-4]
		imageNamesCSV.writerow([f])

	for e in entries:
		entriesNamesCSV.writerow(e.displayName)

