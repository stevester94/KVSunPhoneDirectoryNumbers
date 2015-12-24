#!/bin/bash
sqlite3 -header -csv entries.db "select * from Entries;" > entries.csv
sqlite3 -header -csv entries.db "select * from Categories;" > categories.csv
sqlite3 -header -csv entries.db "select * from CategoriesList;" > categoryList.csv