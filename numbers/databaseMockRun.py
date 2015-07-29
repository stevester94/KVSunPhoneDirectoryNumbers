#Database w/ mock numbers testing

import sqlite3 as lite
import sys
from parse import parseEntries

con = lite.connect('mockNumbers.db')
cur = con.cursor()
cur.execute('drop table if exists numbers')
cur.execute("CREATE TABLE numbers(Entry TEXT)")

[businessEntries, personalEntries] = parseEntries()

for entry in personalEntries[1:]:
	line = entry.lines[0]
	print line
	cur.execute("INSERT INTO numbers VALUES ('" + line + "')")

con.commit()
con.close()
