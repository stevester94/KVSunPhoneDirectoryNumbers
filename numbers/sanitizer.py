#Converts all .eps files to .jpeg
#run on windows

from os import listdir
from subprocess import call
import copy

files = listdir("./converted")
len(files)
counter = 0
for f in files:
	unmodF = copy.deepcopy(f)
	if f[-4:] == ".jpg":
		f = f[:-4]
	sanitizedName = ""
	for c in f:
		if ord(c) > 64 and ord(c) < 91:
			sanitizedName = sanitizedName + chr(ord(c) + 32)
		elif ord(c) > 96 and ord(c) < 123:
			sanitizedName = sanitizedName + c
		elif ord(c) == 32:
			sanitizedName = sanitizedName + '_'
	while sanitizedName[-1] == "_":
		sanitizedName = sanitizedName[:-1]
	print sanitizedName
	print "converted/" + unmodF
	call(["copy",  "./converted/" + unmodF, "./formatted/" + sanitizedName + ".jpg"])
