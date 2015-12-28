#Converts all .eps files to .jpeg

from os import listdir
from subprocess import call

call(["mkdir", "./converted"])
files = listdir("./EPS")
len(files)
counter = 0
for f in files:
	print counter
	if f[-4:] == ".eps":
		name = f[:-4]
		call(["convert", "-density", "300", "./EPS/" + f, "./converted/" + name + ".jpg"])
	counter = counter + 1
		
