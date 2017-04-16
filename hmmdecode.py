import copy
import time
import math
import collections
import sys

def readProbablityModel():
	global initaltransitionprobablity,transitionprobablity,emissionwordcount, tagcount
	index = 0
	file = open( 'hmmmodel.txt', 'r' )
	for eachline in file:
		if (index == 1):
			initaltransitionprobablity=eval(eachline)
		elif (index == 3):
			transitionprobablity=eval(eachline)
		elif (index == 5):
			emissionwordcount=eval(eachline)
		elif (index == 7):
			tagcount=eval(eachline)
		index += 1

readProbablityModel()
#----------------------to fetch the probablities from hmmlearn--------------------
#print emissionwordcount["Branc"]
count = 0
fout = open('hmmoutput.txt', 'w', encoding = "utf-8")
stack = []
developmenttextfo = open ("catalan_corpus_dev_raw.txt", 'r', encoding = "utf-8")
readlinesdevelopmentset = developmenttextfo.readlines()
trackinglist = {}
sequence = {}

for i in range ( len(readlinesdevelopmentset) ):
	count += 1
	spacebreaklist = readlinesdevelopmentset[i].strip().split(" ")
	#if (len(spacebreaklist) > 119):
	#		fout.write(readlinesdevelopmentset[i])
	#		continue
	#print spacebreaklist
	intitialword = spacebreaklist [0]
	#----------------creating initial stack, with initial transition---------------
	templist = []
	if intitialword in emissionwordcount:
		for tags in emissionwordcount[intitialword]:
				templisttoappend = []
				templisttoappend.append ("q0")
				templisttoappend.append (tags)
				templisttoappend.append (intitialword)
				templisttoappend.append (math.log(initaltransitionprobablity[tags] * emissionwordcount [intitialword][tags]))
				stack.append (templisttoappend)
				if intitialword not in sequence:
					sequence ["1"] = []
					templist.append (templisttoappend)
				else:
					templist.append (templisttoappend)
		sequence ["1"] = templist
	else:
		templist = []
		for tags in initaltransitionprobablity:
				transitionsequence = []
				templisttoappend = []
				templisttoappend.append ("q0")
				templisttoappend.append (tags)
				templisttoappend.append (intitialword)
				templisttoappend.append (math.log(initaltransitionprobablity[tags]))
				stack.append (templisttoappend)
				if intitialword not in sequence:
					sequence ["1"] = []
					templist.append (templisttoappend)
				else:
					templist.append (templisttoappend)
		sequence ["1"] = templist
	countcheck = 0

	while ( countcheck != (len (spacebreaklist) - 1 )):
			countcheck += 1
			size = len (stack)
			trackinglist = {}
			transitionsequence = []
			for i in range (size):
				templist = stack. pop(0)
				previousprobablity = templist [3]
				transitionfrom = templist [1]
				transitionfromword = templist [2]
				transitiontoword = spacebreaklist [ countcheck ]
				if (transitiontoword in emissionwordcount):
					for tags in emissionwordcount[transitiontoword]:
						transitiontagstring = transitionfrom + "-" + tags
						if transitiontagstring not in transitionprobablity:
							continue
						else:
							if tags not in trackinglist:
								trackinglist[tags] = []
							templist = []
							currentprobablity = math.log (float(transitionprobablity[transitiontagstring]) * float(emissionwordcount[transitiontoword][tags])) + float(previousprobablity)
							templist = [transitionfrom,currentprobablity,transitiontoword]
							trackinglist [tags].append(templist)

				else:
					for tags in tagcount:
						transitiontagstring = transitionfrom + "-" + tags
						if transitiontagstring not in transitionprobablity:
							continue
						else:
							if tags not in trackinglist:
								trackinglist[tags] = []
							templist = []
							currentprobablity = math.log(float(transitionprobablity[transitiontagstring])) + float(previousprobablity)
							templist = [transitionfrom,currentprobablity,transitiontoword]
							trackinglist [tags].append(templist)
	
			for items in trackinglist:
					maximumvalue = -999999
					for inneritems in trackinglist [items]:
						if (inneritems[1] > maximumvalue):
							maximumvalue = inneritems[1]
							anslist = inneritems
					#print anslist

					templist = []
					templist.append (anslist[0])
					templist.append(items)
					templist.append(anslist[2])
					templist.append(maximumvalue)
					templist.append(countcheck)
					stack.append (templist)
					s = str(countcheck+1)
					if s not in sequence:
						sequence [s] = []
						sequence [s].append(templist)
					else:
						sequence [s].append(templist)
	
	
	maxvalue = -999999
	maxlist = []
	targetlist = []
	
	for items in stack:
		if (items[3] >= maxvalue):
				maxvalue = items [3]
				maxlist = items
	j = len(spacebreaklist) - 1
	targetlist.append(maxlist[1])
	#print sequence["1"]
	#sys.exit()

	for i in range (len(spacebreaklist)-1):
		target = maxlist[0]
		for items in sequence[str(j)]:
			#print j, spacebreaklist[j]
			if items[1] == target:
				maxlist = items
				targetlist.append(maxlist[1])
				break
		j -= 1
	
	targetlist = targetlist[::-1]
	j=0
	s=""

	for items in spacebreaklist:
			if(j != len(spacebreaklist)-1):
					s=s+items + "/" + targetlist[j] + " "
			else:
				s=s+items + "/" + targetlist[j]
			j += 1
	fout.write (s)
	fout.write("\n")
	sequence = {}
	trackinglist = {}
	stack = []

fout.close()

