#resize all images in formatted

from os import listdir
from subprocess import call

files = listdir("./formatted")
len(files)
counter = 0
for f in files:
	print counter
	call(["D:\ProgramFiles8\ImageMagick-6.9.1-Q16\convert", "formatted/" + f, "-resize", "600x300!", "resized/" + f], shell=True)
	counter = counter + 1
		
