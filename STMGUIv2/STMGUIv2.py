from Tkinter import *
import STMClass
import pygame
import os
import inspect
import time
from Import import CtoSTM as fromC
from Import import XMLtoSTM as fromXML
from Config.config import *
from GUI.PyWindow import PyWindowClass
from GUI.TkWindow import TkWindowClass

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


class AppClass:
	def __init__(self):
		self.run = True
		self.apptime = time.time()
		self.modeOption = 1 
		self.pypart = PyWindowClass(self)
		self.tkpart = TkWindowClass(self)

	def initApp(self):
		'''
		Reads the STM from the xml file
		Initiate the Color dictionaries for states and transitions
		Update the menus
		Read the coordinates
		Update the pyWindow
		'''
		self.initSTMfromXML(xmlin)
		self.pypart.paintAllStates(color["active"])
		self.pypart.paintAllTransitions(color["inactive"])
		self.tkpart.updateStartStateMenu()
		self.readCoordinates()
		self.tkpart.updateImportMenu()
		self.pypart.pyWindowThreadUpdate()

	def toggleMode(self):
		'''
		According to the mode modify the colors of states and transitions (active/inactive) 
		Update the pyWindow
		'''
		if self.modeOption == 1:
			self.modeOption = 2
			self.tkpart.transitionMode()
			self.pypart.paintAllStates(color["inactive"])
			self.pypart.paintAllTransitions(color["active"])
			self.pypart.pyWindowThreadUpdate()
		else:
			self.modeOption = 1
			self.tkpart.stateMode()
			self.pypart.paintAllStates(color["active"])
			self.pypart.paintAllTransitions(color["inactive"])
			self.pypart.pyWindowThreadUpdate()

	def readCoordinates(self):
		'''
		Read the coordinates and add them to stateCoordinates
		'''
		auxList = []
		needUpdate = 0
		f = open(coordFile, "rt")
		for line in f:
			self.pypart.stateCoordinates[line.split(" ")[0]] = line.replace("\n", "").split(" ")[1]
			auxList.append(line.split(" ")[0])
		for st in STMClass.mySTM.statesDict:
			if st not in auxList:
				self.pypart.stateCoordinates[st] = "100x100"
				needUpdate = 1
		if needUpdate:
			self.updateCoordFile()

	def updateSTMFiles(self):
		'''
		Update the STM files to the current STM
		'''
		STMClass.updateFiles()

	def updateCoordFile(self):
		'''
		Write the current coordinates into the coordinate file
		'''
		f = open(coordFile, "wt")
		text = ""
		for st in STMClass.mySTM.statesDict:
			text += st + " " + self.pypart.stateCoordinates[st] + "\n"
		f.write(text)
		f.close()

	def logThisIn(self, text, file, mode):
		'''
		Write 'text' into 'file' by 'mode'
		'''
		f = open(file, mode)
		f.write(text)
		f.close()

	def runOnModes(self):
		self.pypart.statePickedMode()

	def initSTMfromXML(self, file):
		'''
		Initiate the STM from XML file
		'''
		STMClass.addStatesList(fromXML.getStatesList(file))
		STMClass.addTransitionsList(fromXML.getTransitionsList(file))
		self.updateSTMFiles()

	def initSTMfromC(self, file):
		'''
		Initiate the STM from C file
		'''
		STMClass.addStatesList(fromC.getStatesList(file))
		STMClass.addTransitionsList(fromC.getTransitionsList(file))
		self.updateSTMFiles()

app = AppClass()
app.initApp()

while app.run == True:
	app.tkpart.tkwindow.update()
	app.runOnModes()
	app.pypart.verifyTimeEvents()
	app.pypart.verifyKeyEvents()
	app.pypart.showSystemInfo()
	pygame.display.update()
