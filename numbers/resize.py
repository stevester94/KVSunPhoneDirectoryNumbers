#resize all images in formatted

from os import listdir
from subprocess import call

files = listdir("./formatted")
len(files)
counter = 0
for f in files:
	print counter
	call(["convert", "./formatted/" + f, "-resize", "600x300!", "./resized/" + f])
	counter = counter + 1
		
