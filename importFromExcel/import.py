# Will import all data from CSV and build a new database from it

import csv

csvFile = file("excelBook.csv", "rb")
reader = csv.reader(csvFile)

for row in reader:
	print row
