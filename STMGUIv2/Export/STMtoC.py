cout = "Data/CFile.c"

def getDefinesC():
	return """#define uint8 unsigned short
#define int32 int
"""

def getEnumsC(mySTM):
	text = "\ntypedef enum {"
	for st in mySTM.statesDict:
		text += "\n\t" + mySTM.statesDict[st].name + ","
	text = text[:-1]
	text += "\n} MyStm_e;"
	text += "\n\nMyStm_e st;"
	return text

def getInputsC(mySTM):
	text = "\n"
	for inp in  mySTM.inputsDict:
		text += "\nint32 " + inp + " = " + mySTM.inputsDict[inp] + ";"
	return text

def getFuncsC(mySTM):
	text = ""
	for tr in mySTM.transitionsDict:
		text += "\n\nstatic uint8 " + mySTM.transitionsDict[tr].name + "() {\n\treturn "+ mySTM.transitionsDict[tr].cond + ";\n}"

	return text

def getImplementaionC(mySTM):
	casesDict = {}
	for tr in mySTM.transitionsDict:
		casesDict.setdefault(mySTM.transitionsDict[tr].src.name, []).append("\n\t\t\tif (" + mySTM.transitionsDict[tr].name + "()) {\n\t\t\t\tst=" + mySTM.transitionsDict[tr].dest.name + ";\n\t\t\t}")

	text = "\n\nstatic uint8 STM_IMPLEMENTATION() {\n\tswitch (st) {"
	for case in casesDict:
		text += "\n\t\tcase " + case + ":"
		for ifs in casesDict[case]:
			text += ifs
		text += "\n\t\t\tbreak;"
	text += "\n\t}\n}"
	return text

def getMainC():
	text = "\n\nint main() {\n\treturn 0;\n}"
	return text

def updateC(mySTM):
	'''
	Write the STM into a C file
	'''
	cfile = open(cout, "wt")
	cfile.write(getDefinesC())
	cfile.write(getEnumsC(mySTM))
	cfile.write(getInputsC(mySTM))
	cfile.write(getFuncsC(mySTM))
	cfile.write(getImplementaionC(mySTM))
	cfile.write(getMainC())
	print("Updated C file")