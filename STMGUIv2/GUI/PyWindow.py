import os
import pygame
import threading
import math
import time
import STMClass
from itertools import cycle
from Config.config import *

class PyWindowClass:
	def __init__(self, app):
		self.app = app
		self.inputsHash = {}
		self.mouseLeftPressed = 0
		self.lastMousePressedTime = time.time()
		self.timeStep = 0.1
		self.stateNameToBeSpawned = ""
		self.collision = 1
		self.info = 1
		self.animationRun = 0
		self.animationSteps = 0
		self.animationTime = 0
		self.animationTrace = []
		self.animationLog = ""
		self.currAnimationState = ""
		self.stateCoordinates = {} #statename: XposxYpos (left corner)
		self.transitionCoordinates = {} #src|dest: XposxYpos (circle's center)
		self.stateColor = {}#statename: (R, G, B)
		self.transitionColor = {}#src|dest: (R, G, B)
		os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (pyWindowPosX,pyWindowPosY)
		pygame.init()
		pygame.display.set_icon(pygame.image.load('Config/icon.ico'))
		self.pywindow = pygame.display.set_mode(pyWindowSize)
		self.pywindow.fill(color["background"])
		pygame.display.set_caption("STM View")

		pygame.mouse.set_cursor(*pygame.cursors.tri_left)
		self.paintAllStates(color["active"])
		self.paintAllTransitions(color["inactive"])


	def paintAllTransitions(self, color):
		'''
		Change all transition colors in transitionColor to 'color'
		'''
		self.transitionColor = {x: color for x in STMClass.mySTM.transitionsDict}

	def paintAllStates(self, color):
		'''
		Change all state colors in stateColor to 'color'
		'''
		self.stateColor = {x: color for x in STMClass.mySTM.statesDict}

	def updatePyWindow(self):
		'''
		Draw all the states and transitions of the STM
		'''
		self.pywindow.fill(color["background"])
		for tr in STMClass.mySTM.transitionsDict:
			srcx, srcy = self.stateCoordinates[STMClass.mySTM.transitionsDict[tr].src.name].split("x")
			destx, desty = self.stateCoordinates[STMClass.mySTM.transitionsDict[tr].dest.name].split("x")
			self.spawnTransitionLine(self.getCenterOfShape(int(srcx), int(srcy)), self.getCenterOfShape(int(destx), int(desty)), tr)
		for sc in self.stateCoordinates:
			x, y = self.stateCoordinates[sc].split("x")
			self.spawnStateRect(int(x), int(y), str(sc))

	def pyWindowThreadUpdate(self):
		'''
		Update using threads
		'''
		pyUpdateThread = threading.Thread(target=self.updatePyWindow)
		pyUpdateThread.start()
		pyUpdateThread.join()

	def getCenterOfShape(self, x, y):
		'''
		Returns the center of a state rectangle having the upper left corner at (x, y)
		'''
		cx = x + stateRectWidth/2
		cy = y + stateRectHeight/2
		return cx, cy

	def spawnTransitionName(self, x, y, name):
		'''
		Write the name of a transition at (x, y)
		'''
		font = pygame.font.SysFont("arial", fontSize, False)
		text = font.render(name, True, (0,0,0))
		self.pywindow.blit(text, (x, y))

	def spawnTransitionLine(self, p1, p2, name):
		'''
		Draw a transition as a line with an arrow and a name on it
		'''
		if name.split("|")[0] > name.split("|")[1]:
			srcx = p1[0]
			srcy = p1[1] + stateRectHeight/4
			destx = p2[0]
			desty = p2[1] + stateRectHeight/4
		else:
			srcx = p1[0]
			srcy = p1[1] - stateRectHeight/4
			destx = p2[0]
			desty = p2[1] - stateRectHeight/4
		H = 10
		L = 20
		ix = (srcx + destx)//2
		ix = (ix + destx)//2
		iy = (srcy + desty)//2
		iy = (iy + desty)//2
		if ix != srcx or iy != srcy:
			dX = ix - srcx
			dY = iy - srcy
			lineLen = math.sqrt(dX**2 + dY**2)
			udX = dX / lineLen
			udY = dY / lineLen
			perpX = -udY
			perpY = udX
			leftX = ix - L * udX + H * perpX
			leftY = iy - L * udY + H * perpY
			rightX = ix - L * udX - H * perpX
			rightY = iy - L * udY - H * perpY
			pygame.draw.line(self.pywindow, self.transitionColor[name], (srcx, srcy), (destx,desty), 3)
			pygame.draw.line(self.pywindow, self.transitionColor[name], (leftX, leftY), (ix, iy), 5)
			pygame.draw.line(self.pywindow, self.transitionColor[name], (rightX, rightY), (ix, iy), 5)
			self.transitionCoordinates[name] = str(int((ix + leftX + rightX)/3)) + "x" + str(int((iy + leftY + rightY)/3))
			self.spawnTransitionName(int((ix + leftX + rightX)/3), int((iy + leftY + rightY)/3), STMClass.mySTM.transitionsDict[name].name + " (" + STMClass.mySTM.transitionsDict[name].cond + ")")

	def spawnStateRect(self, x, y, name):
		'''
		Draw a state as a rectangle and a name
		'''
		pygame.draw.rect(self.pywindow, self.stateColor[name], (x,y,stateRectWidth,stateRectHeight))
		font = pygame.font.SysFont("arial", fontSize, True)
		text = font.render(name, True, color["fontcolor"])
		self.pywindow.blit(text, (x + (stateRectWidth/2 - text.get_width()/2), y + (stateRectHeight/2 - text.get_height()/2)))

	def spawnInfoRect(self, x, y, name, color):
		'''
		Draw a rectangle with text in it
		'''
		pygame.draw.rect(self.pywindow, color, (x,y,infoRectWidth,infoRectHeight))
		font = pygame.font.SysFont("arial", 15)
		text = font.render(name, True, (0,0,0))
		self.pywindow.blit(text, (x + (infoRectWidth/2 - text.get_width()/2), y + (infoRectHeight/2 - text.get_height()/2)))

	def isEmptySpace(self, x, y):
		'''
		Verify if a state rectangle can be placed at (x, y) by verifying the colors at it's corners
		'''
		if self.collision == -1:
			return True
		cond4 = 0
		if x + stateRectWidth >= pyWindowSize[0]:
			return False
		if y + stateRectHeight >= pyWindowSize[1]:
			return False
		okColors = [color["background"], color["inactive"], color["pickedup"], color["running"]]
		if self.pywindow.get_at((x, y))[:3] in okColors:
			cond4 += 1
		if self.pywindow.get_at((x+stateRectWidth, y))[:3] in okColors:
			cond4+= 1
		if self.pywindow.get_at((x+stateRectWidth, y+stateRectHeight))[:3] in okColors:
			cond4+= 1
		if self.pywindow.get_at((x, y+stateRectHeight))[:3] in okColors:
			cond4+= 1
		if cond4 == 4:
			return True
		else:
			return False

	def getTransitionNameAtPos(self, x, y):
		'''
		Return the name of the transition located at (x, y)
		'''
		for tc in self.transitionCoordinates:
			tx, ty = self.transitionCoordinates[tc].split("x")
			if math.sqrt((x - int(tx))**2 + (y - int(ty))**2) <= 30:
				return tc
		return None

	def getStateNameAtPos(self, x, y):
		'''
		Return the name of the state located at (x, y)
		'''
		for sc in self.stateCoordinates:
			sx, sy = self.stateCoordinates[sc].split("x")
			if x >= int(sx) and x <= int(sx)+stateRectWidth and y >= int(sy) and y <= int(sy)+stateRectHeight:
				return sc
		return None

	def statePickedMode(self):
		'''
		If there is a picked-up state and the space is empty change the location of that state to the current one and refresh the window
		'''
		if self.stateNameToBeSpawned != "":
			if self.isEmptySpace(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
				self.stateCoordinates[self.stateNameToBeSpawned] = str(pygame.mouse.get_pos()[0]+1) + "x" + str(pygame.mouse.get_pos()[1]+1)
				self.pyWindowThreadUpdate()

	def statePick(self):
		'''
		If animation is off, the leftMouseButton is pressed a certain amount of time, the click is on a state and there is not other state
		That needs to be spawned, pick the clicked state (put it's name into stateNameToBeSpawned)
		'''
		if self.animationRun == 0:
			if time.time() - self.lastMousePressedTime >= statePickTime and self.mouseLeftPressed == 1 and self.stateNameToBeSpawned == "" and self.getStateNameAtPos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) != None:
				self.stateNameToBeSpawned = self.getStateNameAtPos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
				self.stateColor[self.stateNameToBeSpawned] = color["pickedup"]
				pygame.mouse.set_cursor(*pygame.cursors.diamond)

	def stateRelease(self):
		'''
		The state needs to be released so empty the stateNameToBeSpawned and change the color to active
		'''
		threading.Thread(target=self.app.updateCoordFile).start()
		self.stateColor[self.stateNameToBeSpawned] = color["active"]
		self.stateNameToBeSpawned = ""
		pygame.mouse.set_cursor(*pygame.cursors.tri_left)
		self.pyWindowThreadUpdate()

	def selectState(self):
		'''
		Select a state
			- If in state mode, put it's name in the first entry
			- If in transition mode, write the text from destination entry into the source entry and write the name of the state into the destination entry
		'''
		mx, my = pygame.mouse.get_pos()
		whatIsClicked = self.getStateNameAtPos(mx, my)
		if whatIsClicked != self.stateNameToBeSpawned:
			if whatIsClicked != None:
				if self.app.modeOption == 1:
					self.app.tkpart.entry1.delete(0, 'end')
					self.app.tkpart.entry1.insert(0, whatIsClicked)
				elif self.app.modeOption == 2:
					self.app.tkpart.entry3.delete(0, 'end')
					self.app.tkpart.entry3.insert(0, self.app.tkpart.entry4.get())
					self.app.tkpart.entry4.delete(0, 'end')
					self.app.tkpart.entry4.insert(0, whatIsClicked)

	def selectTransition(self):
		'''
		Select a transition and fill all the entries with it's data
		'''
		mx, my = pygame.mouse.get_pos()
		whatIsClicked = self.getTransitionNameAtPos(mx, my)
		if whatIsClicked != None:
			tname = STMClass.mySTM.transitionsDict[whatIsClicked].name
			tcond = STMClass.mySTM.transitionsDict[whatIsClicked].cond
			tsrc = STMClass.mySTM.transitionsDict[whatIsClicked].src.name
			tdest = STMClass.mySTM.transitionsDict[whatIsClicked].dest.name
			self.app.tkpart.entry1.delete(0, 'end')
			self.app.tkpart.entry1.insert(0, tname)
			self.app.tkpart.entry2.delete(0, 'end')
			self.app.tkpart.entry2.insert(0, tcond)
			self.app.tkpart.entry3.delete(0, 'end')
			self.app.tkpart.entry3.insert(0, tsrc)
			self.app.tkpart.entry4.delete(0, 'end')
			self.app.tkpart.entry4.insert(0, tdest)

	def showSystemInfo(self):
		'''
		If system info is enabled show: Cursor coordinates, mode, collision
		'''
		if self.info == 1:
			self.showCursorCoordinates()
			self.showMode()
			self.showCollisionInfo()

	def showCursorCoordinates(self):
		'''
		Spawn an info rectangle with the cursor coordinates
		'''
		self.spawnInfoRect(0, 0, str(pygame.mouse.get_pos()[0]) + ", " + str(pygame.mouse.get_pos()[1]), color["info"])

	def showMode(self):
		'''
		Spawn an info rectangle with the current mode
		'''
		if self.app.modeOption == 1:
			self.spawnInfoRect(infoRectWidth+2, 0, "State Mode", color["info"])
		elif self.app.modeOption == 2:
			self.spawnInfoRect(infoRectWidth+2, 0, "Transition Mode", color["info"])

	def showCollisionInfo(self):
		'''
		Spawn an info rectangle showing if the collision is on or off
		'''
		if self.collision == 1:
			self.spawnInfoRect(2*infoRectWidth+3, 0, "Collision: On", color["info"])
		else:
			self.spawnInfoRect(2*infoRectWidth+3, 0, "Collision: Off", color["info"])

	def verifyTimeEvents(self):
		'''
		At the specified period (time.Step) do the necessary time events
		'''
		if time.time() - self.animationTime >= self.timeStep:
			self.animationTime = time.time()
			self.animationTryStep()

	def verifyKeyEvents(self):
		'''
		Manage the pressing and releasing of the keys
		'''
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				self.app.run = False
			if event.type == pygame.KEYDOWN:
				if event.scancode == key["enter"]:
					self.app.tkpart.addBtnCmd()
				elif event.scancode == key["delete"] or event.scancode == key["backspace"]:
					self.app.tkpart.removeBtnCmd()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if self.app.modeOption == 1:
					self.mouseLeftPressed = 1
					self.lastMousePressedTime = time.time()
				elif self.app.modeOption == 2:
					self.selectTransition()
				self.selectState()
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				if self.app.modeOption == 1:
					self.mouseLeftPressed = 0
					self.stateRelease()
			if event.type == pygame.MOUSEBUTTONDOWN and event.button in [4, 5]:
				self.app.toggleMode()
			if self.mouseLeftPressed == 1:
				self.statePick()

	def animationStartRun(self):
		'''
		Get from the entries: the start state, the nr of steps and the timeStep
		Update the inputHash
		Make the trace according to the inputHash and cycle it
		If a timeStep is not given, the last one will be used
		Update the pyWindow
		'''
		self.animationTime = time.time()
		self.app.tkpart.startBtn.config(text="Stop", bg="red")
		self.animationRun = 1
		self.currAnimationState = str(self.app.tkpart.omStateVar.get())
		self.stateColor[self.currAnimationState] = color["running"]
		self.animationSteps = int(self.app.tkpart.entry5.get())
		self.updateInputsHash()
		trace = self.updateTrace(self.currAnimationState, self.animationSteps)
		self.animationTrace = cycle(trace)
		if self.app.tkpart.entry7.get() != "":
			self.timeStep = float(self.app.tkpart.entry7.get())
		self.animationLog += "Run - " + str(time.asctime()) + "\nIn state " + self.currAnimationState
		self.pyWindowThreadUpdate()

	def animationStopRun(self):
		'''
		Paint the states and transitions according to the current mode
		Log the event
		Update the pyWindow
		'''
		self.app.tkpart.startBtn.config(text="Start", bg="green")
		self.animationRun = 0
		if self.app.modeOption == 1:
			self.paintAllStates(color["active"])
			self.paintAllTransitions(color["inactive"])
		elif self.app.modeOption == 2:
			self.paintAllStates(color["inactive"])
			self.paintAllTransitions(color["active"])
		self.app.logThisIn(self.animationLog, runlogfile, 'w')
		self.animationLog = ""
		self.pyWindowThreadUpdate()

	def animationTryStep(self):
		'''
		If the animation runs and there are states left in the trace, color the state and the coresponding transition
		A step is made even if the animation remains on the same state
		If all the steps have been made, stop the animation
		'''
		nextstate = ""
		if self.animationRun == 1:
			if self.animationSteps > 0:
				nextstate = next(self.animationTrace)
				self.animationSteps -= 1
				if nextstate != None:
					self.animationLog += "\nIn state " + nextstate
					self.transitionColor[self.currAnimationState + "|" + nextstate] = color["running"]
					self.stateColor[self.currAnimationState] = color["active"]
					self.currAnimationState = nextstate
					self.stateColor[self.currAnimationState] = color["running"]
					self.pyWindowThreadUpdate()
			else:
				self.animationStopRun()

	def updateTrace(self, startState, steps):
		'''
		Return a full trace according to the inputs in the inputHash
		'''
		currState = startState
		trace = [currState]
		for i in range(steps):
			STMClass.updateInputsDict(self.inputsHash[i].keys(), self.inputsHash[i].values())
			nextState = STMClass.getNextStateFrom(currState)
			trace.append(nextState)
			currState = nextState
		return trace

	def updateInputsHash(self):
		'''
		Read the input csv and insert it into the inputHash
		'''
		self.inputsHash = {}
		for i in range(self.animationSteps):
			self.inputsHash[i] = {}
		f = open(inputsFile, 'r')
		line = f.readline()
		for line in f:
			inputVals = line.replace("\n", "").split(",")
			for i in range(1, self.animationSteps+1):
				self.inputsHash[i-1][inputVals[0]] = inputVals[i]

	def generateInputs(self):
		'''
		Get from the entries, the startState, the nr of steps and the timeStep
		Generate a set of inputs which make possible a trace through the STM that includes as many different states as possible
		Write the inputs along with a times list into the CSV file
		'''
		if self.app.tkpart.omStateVar.get() == "-select-" or self.app.tkpart.entry5.get() == "" or self.app.tkpart.entry7.get() == "":
			return 0
		currState = self.app.tkpart.omStateVar.get()
		nrOfSteps = int(self.app.tkpart.entry5.get())
		self.timeStep = float(self.app.tkpart.entry7.get())
		inputChangeTimes = []
		self.inputsHash = {}
		trace = STMClass.fullTraceFrom(currState, nrOfSteps)
		for inp in STMClass.mySTM.inputsDict:
			self.inputsHash[inp] = []
		for i in range(1, len(trace)):
			nextState = trace[i]
			transitionCond = STMClass.mySTM.transitionsDict[currState + "|" + nextState].cond
			STMClass.modifyInputsToFit(transitionCond)
			changeTime = (i-2)*self.timeStep + self.timeStep/2
			if changeTime < 0:
				changeTime = 0
			inputChangeTimes.append(changeTime)

			for inp in STMClass.mySTM.inputsDict:
				self.inputsHash[inp].append(STMClass.mySTM.inputsDict[inp])

			currState = nextState

		f = open(inputsFile, "w")
		f.write("0")
		for t in inputChangeTimes:
			f.write(","+str(t))
		for inp in self.inputsHash:
			f.write("\n"+str(inp))
			for i in self.inputsHash[inp]:
				f.write(","+str(i))
		f.close()
