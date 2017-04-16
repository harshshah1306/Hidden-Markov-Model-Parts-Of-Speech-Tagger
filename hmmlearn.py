import sys
import string

traindatafo = open ( "catalan_corpus_train_tagged.txt", 'r', encoding = "utf-8" )
readlinestraindata = traindatafo.readlines()

initialtransitionprobablitycount = {}
transitionprobablitycount = {}
tagcount = {}
emissiontagcount = {}
onlytaglist = {}
totalintialcount = 0;
emissionwordcount = {} 
transitionstringwithtag = {}
for i in range ( len(readlinestraindata) ):
	spacebreaklist = readlinestraindata[i].strip().split(" ")
	
	'''The loop below is to calculate the initial probablity i.e of the intial state to the first word'''
	wordtagfirstword = spacebreaklist [0][len(spacebreaklist[0])-2:len(spacebreaklist[0])]
	if (wordtagfirstword in initialtransitionprobablitycount):
		initialtransitionprobablitycount [wordtagfirstword] = initialtransitionprobablitycount [wordtagfirstword]+1
	else:
		initialtransitionprobablitycount [wordtagfirstword] = 1

	'''the loop below is to calculate the transition counts i.e NN-VB in the entire dataset'''
	for j in range ( len(spacebreaklist)-1):
		transitionfrom = spacebreaklist [j][len(spacebreaklist[j])-2:len(spacebreaklist[j])]
		transitionto = spacebreaklist [j+1][len(spacebreaklist[j+1])-2:len(spacebreaklist[j+1])]
		transitionstring = transitionfrom + "-" + transitionto
		if (transitionstring in transitionprobablitycount):
			transitionprobablitycount[transitionstring] = transitionprobablitycount [transitionstring] + 1
		else:
			transitionprobablitycount [transitionstring] = 1

		if transitionfrom in transitionstringwithtag:
			if (transitionstring not in transitionstringwithtag [transitionfrom]):
				transitionstringwithtag [transitionfrom].append(transitionstring)
		else:
			transitionstringwithtag [transitionfrom] = []
			transitionstringwithtag [transitionfrom].append(transitionstring)

	'''count for individual tags ignoring the last words'''
	for k in range ( len(spacebreaklist)-2):
		tagforcount = spacebreaklist [k][len(spacebreaklist[k])-2:len(spacebreaklist[k])]
		if tagforcount in tagcount:
			tagcount [tagforcount] = tagcount [tagforcount] + 1
		else:
			tagcount [tagforcount] = 1

	'''below loop counts the individual tags for emmision calculation'''
	for k in range ( len(spacebreaklist)-1):
		tagforcount = spacebreaklist [k][len(spacebreaklist[k])-2:len(spacebreaklist[k])]
		if tagforcount in emissiontagcount:
			emissiontagcount [tagforcount] = emissiontagcount [tagforcount] + 1
		else:
			emissiontagcount [tagforcount] = 1
	
	'''the loop above is to calculate the count for each word as a VB or NN'''
''' the loop below calculates the intial count of tags, i.e first tag NN = 100'''
for words in tagcount:
	if words in initialtransitionprobablitycount:
		initialtransitionprobablitycount[words] = initialtransitionprobablitycount[words] + 1
	else:
		initialtransitionprobablitycount[words] = 1


for items in initialtransitionprobablitycount:
	totalintialcount = totalintialcount + initialtransitionprobablitycount[items]

'''below loop calculates the initial transition probablities from q0 -> VB = 0.11'''
initaltransitionprobablity = {}
for items in initialtransitionprobablitycount:
	value = initialtransitionprobablitycount[items]/(1.0 * totalintialcount)
	initaltransitionprobablity [items] = value

s = ""
transitiontagcount = {}
for items in tagcount:
	templist = []
	for innteritems in tagcount:
		transitiontagcount[items] = []
		s = items + "-" + innteritems
		templist.append(s)
	transitiontagcount[items] = templist

for items in transitiontagcount:
	for innteritems in transitiontagcount[items]:
		if innteritems in transitionprobablitycount:
			transitionprobablitycount[innteritems] = transitionprobablitycount[innteritems] + 1
		else:
			transitionprobablitycount[innteritems] = 1

transitionprobablity = {}
for items in transitionprobablitycount:
	transitionfrom = items[0:2]
	value = transitionprobablitycount[items] / (1.0 * (tagcount [transitionfrom]) + len(tagcount))
	transitionprobablity [items] = value
'''-------------------------------------------------------------------------------------'''
'''Emmision probablity calculation'''
for i in range ( len(readlinestraindata) ):
	spacebreaklist = readlinestraindata[i].strip().split(" ")
	for k in range ( len(spacebreaklist)-1):	
			tagforcount = spacebreaklist [k][len(spacebreaklist[k])-2:len(spacebreaklist[k])]
			wordforcount = spacebreaklist [k][0:len(spacebreaklist[k])-3]
			if wordforcount not in emissionwordcount:
				emissionwordcount [wordforcount] ={}
			if tagforcount in emissionwordcount [wordforcount]:
				emissionwordcount [wordforcount][tagforcount] = emissionwordcount [wordforcount][tagforcount] + 1
			else:
				emissionwordcount [wordforcount][tagforcount] = 1

for items in emissionwordcount:
	for tags in emissionwordcount[items]:
		emissionwordcount[items][tags] = emissionwordcount[items][tags]/(1.0*emissiontagcount[tags])


fout = open ("hmmmodel.txt", "w")
fout.write ("Initaltransitionprobablity\n")
fout.write ( str(initaltransitionprobablity) + "\n" )
fout.write ("Transitionprobablity\n")
fout.write ( str(transitionprobablity) + "\n" )
fout.write ("EmissionProbablity\n")
fout.write ( str(emissionwordcount) + "\n" )
fout.write ("Transitionprobablitywithtag\n")
fout.write ( str(tagcount))
fout.close()