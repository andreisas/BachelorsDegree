from Tkinter import *
from shutil import copyfile
import ttk
from Config.config import *
import os
import threading
import time
import STMClass

class TkWindowClass:
    def __init__(self, app):
        self.app = app
        self.tkwindow = Tk()
        self.tkwindow.update()
        self.omStateVar = StringVar(self.tkwindow)
        self.omStateVar.set("-select-")
        self.omStateVar.trace("w", self.changeStartState)
        self.omFileVar = StringVar(self.tkwindow)
        self.omFileVar.set("-select-")
        self.omFileVar.trace("w", self.changeImportFile)
        self.tkwindow.title("Menu")
        self.tkwindow.protocol("WM_DELETE_WINDOW", self.disable_event)
        self.tkwindow.geometry(tkWindowSize + "+" + str(tkWindowPosX) + "+" + str(tkWindowPosY))
        self.tkwindow.columnconfigure(0, weight=100)
        self.tkwindow.columnconfigure(1, weight=100)
        self.tabbedpane = ttk.Notebook(self.tkwindow)
        self.tabbedpane.grid(row=0, column=0, columnspan=30, rowspan=30, sticky=N + E + S + W)

        'Pages'

        self.page1 = ttk.Frame(self.tabbedpane)
        self.page1.columnconfigure(0, weight=100)
        self.page1.columnconfigure(1, weight=100)
        self.tabbedpane.add(self.page1, text="CRUD")

        self.page2 = ttk.Frame(self.tabbedpane)
        self.page1.columnconfigure(0, weight=100)
        self.page1.columnconfigure(1, weight=100)
        self.tabbedpane.add(self.page2, text="Animation")

        self.page4 = ttk.Frame(self.tabbedpane)
        self.page1.columnconfigure(0, weight=100)
        self.page1.columnconfigure(1, weight=100)
        self.tabbedpane.add(self.page4, text="Checks")

        self.page3 = ttk.Frame(self.tabbedpane)
        self.page1.columnconfigure(0, weight=100)
        self.page1.columnconfigure(1, weight=100)
        self.tabbedpane.add(self.page3, text="Files")

        'Labels'

        self.label1 = Label(self.page1, text="State name:", fg="black", state=NORMAL)
        self.label1.grid(row=0, column=0, columnspan=2, sticky=N + S + W)
        self.label2 = Label(self.page1, text="", fg="black", state=DISABLED)
        self.label2.grid(row=2, column=0, columnspan=2, sticky=N + S + W)
        self.label3 = Label(self.page1, text="", fg="black", state=DISABLED)
        self.label3.grid(row=4, column=0, columnspan=2, sticky=N + S + W)
        self.label4 = Label(self.page1, text="", fg="black", state=DISABLED)
        self.label4.grid(row=6, column=0, columnspan=2, sticky=N + S + W)
        self.label5 = Label(self.page2, text="Starting state:", fg="black", state=NORMAL)
        self.label5.grid(row=0, column=0, sticky=N + S + W)
        self.label6 = Label(self.page2, text="Steps:", fg="black", state=NORMAL)
        self.label6.grid(row=1, column=0, sticky=N + S + W)
        self.label7 = Label(self.page3, text="Import file: ", fg="black", state=NORMAL)
        self.label7.grid(row=0, column=0, sticky=N + E + S + W)
        self.label8 = Label(self.page3, text="Save as: ", fg="black", state=NORMAL)
        self.label8.grid(row=2, column=0, sticky=N + S + W)
        self.label9 = Label(self.page2, text="Timestep(s): ", fg="black", state=NORMAL)
        self.label9.grid(row=2, column=0, sticky=N + S + W)
        self.terminalLabel = Label(self.page4, text="", fg="black", state=NORMAL)
        self.terminalLabel.grid(row=1, column=1, sticky=N + S + W)
        self.redundantLabel = Label(self.page4, text="", fg="black", state=NORMAL)
        self.redundantLabel.grid(row=2, column=1, sticky=N + S + W)
        self.cyclicLabel = Label(self.page4, text="", fg="black", state=NORMAL)
        self.cyclicLabel.grid(row=3, column=1, sticky=N + S + W)

        'Entries'

        self.entry1 = Entry(self.page1, state=NORMAL)
        self.entry1.grid(row=1, column=0, columnspan=2, sticky=N + E + S + W)
        self.entry2 = Entry(self.page1, state=DISABLED)
        self.entry2.grid(row=3, column=0, columnspan=2, sticky=N + E + S + W)
        self.entry3 = Entry(self.page1, state=DISABLED)
        self.entry3.grid(row=5, column=0, columnspan=2, sticky=N + E + S + W)
        self.entry4 = Entry(self.page1, state=DISABLED)
        self.entry4.grid(row=7, column=0, columnspan=2, sticky=N + E + S + W)
        self.entry5 = Entry(self.page2, state=NORMAL)
        self.entry5.grid(row=1, column=1, sticky=N + E + S + W)
        self.entry6 = Entry(self.page3, state=NORMAL)
        self.entry6.grid(row=2, column=1, sticky=N + E + S + W)
        self.entry7 = Entry(self.page2, state=NORMAL)
        self.entry7.grid(row=2, column=1, sticky=N + E + S + W)

        'Buttons'

        self.addBtn = Button(self.page1, text="Add", bg="SteelBlue1", command=self.addBtnCmd)
        self.addBtn.grid(row=8, column=0, sticky=N + E + S + W)
        self.removeBtn = Button(self.page1, text="Remove", bg="SteelBlue1", command=self.removeBtnCmd)
        self.removeBtn.grid(row=8, column=1, sticky=N + E + S + W)
        self.updateBtn = Button(self.page1, text="Update", bg="SteelBlue1", command=self.updateBtnCmd)
        self.updateBtn.grid(row=9, column=0, sticky=N + E + S + W)
        self.findBtn = Button(self.page1, text="Find", bg="SteelBlue1", command=self.findBtnCmd)
        self.findBtn.grid(row=9, column=1, sticky=N + E + S + W)
        self.toggleCollisionBtn = Button(self.page1, text="Toggle Collision", bg="SteelBlue1",
                                         command=self.toggleCollisionBtnCmd)
        self.toggleCollisionBtn.grid(row=10, column=0, columnspan=2, sticky=N + E + S + W)
        self.toggleInfoBtn = Button(self.page1, text="Toggle Info", bg="SteelBlue1", command=self.toggleInfoBtnCmd)
        self.toggleInfoBtn.grid(row=11, column=0, columnspan=2, sticky=N + E + W)
        self.startBtn = Button(self.page2, text="Start", bg="green", command=self.toggleRunBtnCmd)
        self.startBtn.grid(row=4, column=0, sticky=N + S + E + W)
        self.genInputsBtn = Button(self.page2, text="Generate Inputs", bg="SteelBlue1",
                                   command=self.generateInputsBtnCmd)
        self.genInputsBtn.grid(row=4, column=1, sticky=N + S + E + W)
        self.importBtn = Button(self.page3, text="Import", bg="SteelBlue1", command=self.importFileBtnCmd)
        self.importBtn.grid(row=1, column=0, sticky=N + S + E + W)
        self.saveBtn = Button(self.page3, text="Save", bg="SteelBlue1", command=self.saveFileBtnCmd)
        self.saveBtn.grid(row=3, column=0, sticky=N + E + S + W)

        self.checkTerminalsBtn = Button(self.page4, text="Check terminal states", bg="SteelBlue1",
                                        command=self.checkTerminalsCmd)
        self.checkTerminalsBtn.grid(row=1, column=0, sticky=N + E + S + W)
        self.checkRedundancyBtn = Button(self.page4, text="Check redundant states", bg="SteelBlue1",
                                         command=self.checkRedundancyCmd)
        self.checkRedundancyBtn.grid(row=2, column=0, sticky=N + E + S + W)
        self.checkCyclicBtn = Button(self.page4, text="Check system is cyclic", bg="SteelBlue1",
                                     command=self.checkCyclicCmd)
        self.checkCyclicBtn.grid(row=3, column=0, sticky=N + E + S + W)

        self.clearBtn = Button(self.tkwindow, text="Clear", bg="lightblue", command=self.clearBtnCmd)
        self.clearBtn.grid(row=31, column=0, sticky=N + E + S + W)

        self.statesOptionMenu = OptionMenu(self.page2, self.omStateVar, "")
        self.statesOptionMenu.grid(row=0, column=1, sticky=N + E + S + W)
        self.filesOptionMenu = OptionMenu(self.page3, self.omFileVar, "")
        self.filesOptionMenu.grid(row=0, column=1, sticky=N + E + S + W)

    def changeStartState(self, *args):
        pass

    def changeImportFile(self, *args):
        pass

    def disable_event(self):
        self.app.run = 0

    def emptyEntries(self):
        '''
        Empty the entries from the CRUD page
        '''
        self.entry1.delete(0, END)
        self.entry1.insert(0, "")
        self.entry2.delete(0, END)
        self.entry2.insert(0, "")
        self.entry3.delete(0, END)
        self.entry3.insert(0, "")
        self.entry4.delete(0, END)
        self.entry4.insert(0, "")

    def stateMode(self):
        '''
        Enable only the first entry on the CRUD page
        '''
        self.emptyEntries()
        self.label1.config(text="State name: ", state=NORMAL)
        self.label2.config(text="", state=DISABLED)
        self.label3.config(text="", state=DISABLED)
        self.label4.config(text="", state=DISABLED)
        self.entry1.config(state=NORMAL)
        self.entry2.config(state=DISABLED)
        self.entry3.config(state=DISABLED)
        self.entry4.config(state=DISABLED)

    def transitionMode(self):
        '''
        Enable all the entries on the CRUD page
        '''
        self.emptyEntries()
        self.label1.config(text="Transition name: ", state=NORMAL)
        self.label2.config(text="Condition: ", state=NORMAL)
        self.label3.config(text="Source name: ", state=NORMAL)
        self.label4.config(text="Destination name: ", state=NORMAL)
        self.entry1.config(state=NORMAL)
        self.entry2.config(state=NORMAL)
        self.entry3.config(state=NORMAL)
        self.entry4.config(state=NORMAL)

    def popupmsg(self, msg):
        '''
        Create a pop-up message with the text 'msg'
        '''
        popup = Toplevel()
        popup.title("!")
        popup.geometry(popUpMsgSize + "+" + str(tkWindowPosX + popUpMsgPosX) + "+" + str(tkWindowPosY + popUpMsgPosY))
        message = Message(popup, text=msg)
        message.pack()
        button = Button(popup, text="Ok", command=popup.destroy)
        button.pack()

    def updateStartStateMenu(self):
        '''
        Update the option of the StartStateMenu
        '''
        self.omStateVar.set("-select-")
        menu = self.statesOptionMenu["menu"]
        menu.delete(0, END)
        for st in STMClass.mySTM.statesDict:
            menu.add_command(label=st, command=lambda value=st: self.omStateVar.set(value))
        self.tkwindow.update()

    def updateImportMenu(self):
        '''
        Update the options of the ImportMenu
        '''
        menu = self.filesOptionMenu["menu"]
        menu.delete(0, END)
        for r, d, f in os.walk("Inputs"):
            for file in f:
                if file.split(".")[1] in "xml/c":
                    menu.add_command(label=file, command=lambda value=file: self.omFileVar.set(value))
        self.tkwindow.update()

    def addBtnCmd(self):
        '''
        If it's state mode
            - If possible spawn a state
        If it's transition mode
            - If possible spawn a transition
        Log the event
        '''
        if self.app.modeOption == 1:
            sname = self.entry1.get()
            if sname == "":
                return 0
            result = STMClass.addState(sname)
            if result == "Success":
                self.app.logThisIn(str(time.asctime()) + " - " + "State was added (name: " + sname + ")\n", logfile,
                                   'a')
                self.app.pypart.stateNameToBeSpawned = sname
                self.app.pypart.stateColor[self.app.pypart.stateNameToBeSpawned] = color["pickedup"]
                self.emptyEntries()
                self.updateStartStateMenu()
                self.app.pypart.stateCoordinates[sname] = "100x100"
                threading.Thread(target=self.app.updateSTMFiles).start()
                threading.Thread(target=self.app.updateCoordFile).start()
            else:
                self.popupmsg(result)

        elif self.app.modeOption == 2:
            result = STMClass.addTransition(self.entry1.get(), self.entry2.get(), self.entry3.get(), self.entry4.get())
            if result != "Source or/and destination not existing":
                self.app.logThisIn(
                    str(time.asctime()) + " - " + "Transition was added (name: " + self.entry1.get() + ", condition: " + self.entry2.get() + ", source: " + self.entry3.get() + ", destination: " + self.entry4.get() + ")\n",
                    logfile, 'a')
                threading.Thread(target=self.app.updateSTMFiles).start()
                self.app.pypart.transitionColor[self.entry3.get() + "|" + self.entry4.get()] = color["active"]
                self.emptyEntries()
                self.app.pypart.pyWindowThreadUpdate()
            else:
                self.popupmsg(result)

    def removeBtnCmd(self):
        '''
        If it's state mode:
            - If it's possible remove the state
        If it's transition mode:
            - If it's possible remove the transition
        Log the event
        '''
        if self.app.modeOption == 1:
            sname = self.entry1.get()
            deletedTransitions = STMClass.getTransitionsIncluding(sname)
            result = STMClass.removeState(sname)
            if result == "Success":
                self.app.logThisIn(str(time.asctime()) + " - " + "State was deleted (name: " + sname + ")\n", logfile,
                                   'a')
                del self.app.pypart.stateCoordinates[sname]
                for dt in deletedTransitions:
                    self.app.logThisIn(str(time.asctime()) + " - " + "Transition was deleted (source: " + dt.split("|")[
                        0] + ", destination: " + dt.split("|")[1] + ")\n", logfile, 'a')
                    del self.app.pypart.transitionCoordinates[dt]
                threading.Thread(target=self.app.updateCoordFile).start()
                threading.Thread(target=self.app.updateSTMFiles).start()
                self.emptyEntries()
                self.app.pypart.pyWindowThreadUpdate()
                self.updateStartStateMenu()
            else:
                self.popupmsg(result)
        elif self.app.modeOption == 2:
            src = self.entry3.get()
            dest = self.entry4.get()
            result = STMClass.removeTransition(src, dest)
            if result == "Success":
                self.app.logThisIn(
                    str(time.asctime()) + " - " + "Transition was deleted (source: " + src + ", destination: " + dest + ")\n",
                    logfile, 'a')
                threading.Thread(target=self.app.updateSTMFiles).start()
                del self.app.pypart.transitionCoordinates[src + "|" + dest]
                self.emptyEntries()
                self.app.pypart.pyWindowThreadUpdate()
            else:
                self.popupmsg(result)

    def updateBtnCmd(self):
        '''
        If it's state mode:
            - If possible update the state
        If it's transition mode:
            - If possible update the transition
        Log the event
        '''
        if self.app.modeOption == 1:
            sname = self.entry1.get()
            result = STMClass.updateState(sname)
            if result == "Success":
                self.app.logThisIn(str(time.asctime()) + " - " + "State was updated (name: " + sname + ")\n", logfile,
                                   'a')
                threading.Thread(target=self.app.updateSTMFiles).start()
                self.emptyEntries()
                self.app.pypart.pyWindowThreadUpdate()
            else:
                self.popupmsg(result)
        elif self.app.modeOption == 2:
            result = STMClass.updateTransition(self.entry1.get(), self.entry2.get(), self.entry3.get(), self.entry4.get())
            if result == "Success":
                self.app.logThisIn(
                    str(time.asctime()) + " - " + "Transition was updated (name: " + self.entry1.get() + ", condition: " + self.entry2.get() + ", source: " + self.entry3.get() + ", destination: " + self.entry4.get() + ")\n",
                    logfile, 'a')
                threading.Thread(target=self.app.updateSTMFiles).start()
                self.emptyEntries()
                self.app.pypart.pyWindowThreadUpdate()
            else:
                self.popupmsg(result)

    def findBtnCmd(self):
        '''
        If it's state mode find the state
        If it's transition mode fint the transition
        '''
        if self.app.modeOption == 1:
            result = STMClass.findState(self.entry1.get())
            self.popupmsg(result)
        elif self.app.modeOption == 2:
            result = STMClass.findTransition(self.entry3.get(), self.entry4.get())
            self.popupmsg(result)

    def toggleCollisionBtnCmd(self):
        '''
        Toggle the collision option
        '''
        self.app.pypart.collision *= -1

    def toggleInfoBtnCmd(self):
        '''
        Toggle the info option
        '''
        self.app.pypart.info *= -1
        self.app.pypart.pyWindowThreadUpdate()

    def toggleRunBtnCmd(self):
        '''
        If animation is on, stop it, else, start it
        '''
        if self.app.pypart.animationRun == 0:
            if self.entry5.get() != "" and str(self.omStateVar.get()) != "-select-":
                self.app.pypart.animationStartRun()
        else:
            self.app.pypart.animationStopRun()

    def generateInputsBtnCmd(self):
        '''
        Call generateInputs from the pypart Class
        '''
        self.app.pypart.generateInputs()

    def checkTerminalsCmd(self):
        terminalStates = STMClass.getTerminalStates()
        if terminalStates:
            msg = "The next states are terminals and could cause system crashes: "
            msg = msg + str(terminalStates)
            self.popupmsg(msg)
            self.terminalLabel['text'] = "ISSUE " + str(len(terminalStates))
            self.terminalLabel['fg'] = "red"
        else:
            self.terminalLabel['text'] = "OK"
            self.terminalLabel['fg'] = "green"

    def checkRedundancyCmd(self):
        redundantStates = STMClass.getRedundantStates()
        if redundantStates:
            msg = "The next pairs of states can create redundancies: "
            msg = msg + str(redundantStates)
            self.popupmsg(msg)
            self.redundantLabel['text'] = "ISSUE "
            self.redundantLabel['fg'] = "red"
        else:
            self.redundantLabel['text'] = "OK"
            self.redundantLabel['fg'] = "green"

    def checkCyclicCmd(self):
        cyclic = STMClass.isCyclic()
        if cyclic:
            self.cyclicLabel['text'] = "OK"
            self.cyclicLabel['fg'] = "green"
        else:
            self.cyclicLabel['text'] = "ISSUE"
            self.cyclicLabel['fg'] = "red"

    def importFileBtnCmd(self):
        '''
        Truncate the current STM
        Log the event
        Copy the files selected in the import menu into the Data folder
        Read the coordinates and paint the states and transitions
        Update the startStateMenu
        Update the pyWindow
        '''
        filename = str(self.omFileVar.get())
        if filename != "-select-":
            if filename.split(".")[1] in "xml/c":
                self.clearBtnCmd()
                self.app.logThisIn(str(time.asctime()) + " - " + "Imported " + filename + "\n", logfile, 'a')
                if filename.split(".")[1] == "xml":
                    self.app.initSTMfromXML("Inputs/" + filename.split(".")[0] + "/" + filename)
                elif filename.split(".")[1] == "c":
                    self.app.initSTMfromC("Inputs/" + filename.split(".")[0] + "/" + filename)
                copyfile("Inputs/" + filename.split(".")[0] + "/" + filename.split(".")[0] + "coord.txt",
                         "Data/CoordFile.txt")
                copyfile("Inputs/" + filename.split(".")[0] + "/" + filename.split(".")[0] + "inputs.csv",
                         "Data/inputs.csv")
                self.app.readCoordinates()
                self.app.pypart.paintAllStates(color["active"])
                self.app.pypart.paintAllTransitions(color["inactive"])
                self.updateStartStateMenu()
                self.app.pypart.pyWindowThreadUpdate()

    def saveFileBtnCmd(self):
        '''
        Save the files from the Data folder into the input folder as a new folder representing an STM
        Files saved: XML/C, inputs, coordinates
        '''
        filename = str(self.entry6.get())
        if filename.split(".")[1] in "xml/c":
            self.app.logThisIn(str(time.asctime()) + " - " + "Saved as " + filename + "\n", logfile, 'a')
            if not os.path.isdir("Inputs/" + filename.split(".")[0]):
                os.mkdir("Inputs/" + filename.split(".")[0])
            if filename.split(".")[1] == "c":
                copyfile("Data/CFile.c", "Inputs/" + filename.split(".")[0] + "/" + filename)
            elif filename.split(".")[1] == "xml":
                copyfile("Data/XMLFile.xml", "Inputs/" + filename.split(".")[0] + "/" + filename)
            self.updateImportMenu()
            copyfile("Data/CoordFile.txt",
                     "Inputs/" + filename.split(".")[0] + "/" + filename.split(".")[0] + "coord.txt")
            copyfile("Data/inputs.csv",
                     "Inputs/" + filename.split(".")[0] + "/" + filename.split(".")[0] + "inputs.csv")

    def clearBtnCmd(self):
        '''
        Truncate the STM and all it's relations
        '''
        self.app.logThisIn(str(time.asctime()) + " - " + "Truncate STM" + "\n", logfile, 'a')
        STMClass.truncateSTM()
        self.app.pypart.stateCoordinates = {}
        self.app.pypart.transitionCoordinates = {}
        self.app.pypart.stateColor = {}
        self.app.pypart.transitionColor = {}
        self.updateStartStateMenu()
        self.app.updateSTMFiles()
        threading.Thread(target=self.app.updateCoordFile).start()
        self.app.pypart.pyWindowThreadUpdate()
