#image tools
from os import listdir
from subprocess import call
import copy

def convertToJPG():
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

def resize():
	files = listdir("./formatted")
	len(files)
	counter = 0
	for f in files:
		print counter
		call(["convert", "./formatted/" + f, "-resize", "600x300!", "./resized/" + f])
		counter = counter + 1

def sanitize():
	files = listdir("./converted")
	call(["mkdir", "sanitized"])
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

		sanitizedName = sanitizedName.replace("__", "_") #fuck it
		sanitizedName = sanitizedName.replace("__", "_")
		sanitizedName = sanitizedName.replace("__", "_")


		print sanitizedName
		print "converted/" + unmodF
		call(["cp",  "./converted/" + unmodF, "./sanitized/" + sanitizedName + ".jpg"])


if __name__ == '__main__':

	choice = ""
	while choice != "x":
		print "options: "
		print "1. convertToJPG"
		print "2. resize"
		print "3. sanitize"
		print "x. exit"

		choice  = (raw_input("choice: ")).rstrip()

		if choice == "1":
			convertToJPG()
		elif choice == "2":
			resize()
		elif choice == "3":
			sanitize()
		elif choice == "x":
			exit()
		else:
			print "Wrong input"