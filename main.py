import functools
import signal
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox

from OpenFiles import *
from functools import partial
from helpers import *
from signal import SIGTERM
from os import *

__author__ = "Jovanny Vera"


class Application(Tk):
    def __init__(self):
        super().__init__()
        self.minsize(1000, 600)
        # init attributes
        self.leftFrame = None
        self.rightFrame = None
        self.uploadFileFrame = None
        self.generateNewRunFrame = None
        self.subProcess = None
        self.terminalScrolledText = None
        self.exitFlag = False
        self.runThread = None
        self.runAllThread = None
        self.currentProject = None
        self.isRunning = False
        self.timer = 0
        self.currentStudent = None
        self.isGenerating = False


        self.createLayout()
        self.createUploadFiles()
        self.createNewProjectFrame()
        self.createScrollWindow()
        self.createRunProjectFrame()
        # Load Runs
        loadRuns(self)
        self.updateTimer()

    def createLayout(self):
        # create two columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)

        # create left column
        self.leftFrame = Frame(self)
        self.leftFrame.grid(row=0, column=0, sticky="NSWE")

        # create left column subgrid
        self.leftFrame.grid_columnconfigure(0, weight=1)
        self.leftFrame.grid_rowconfigure(0, weight=2)
        self.leftFrame.grid_rowconfigure(1, weight=2)

        # create right column
        self.rightFrame = Frame(self)
        self.rightFrame.grid(row=0, column=1, sticky="NSWE")

        # create right column subgrid
        self.rightFrame.grid_columnconfigure(0, weight=1)
        self.rightFrame.grid_rowconfigure(0, weight=1)
        self.rightFrame.grid_rowconfigure(1, weight=4)



    def createUploadFiles(self):
        self.uploadFileFrame = Frame(self.leftFrame, highlightthickness=1, highlightbackground="black")
        self.uploadFileFrame.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)

        # Title label
        uploadFileTitle = Label(self.uploadFileFrame, text="Upload New Files", font=("TkDefaultFont", 18))
        uploadFileTitle.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=W)

        # TCL upload
        self.tclUploadVar = StringVar(self.uploadFileFrame)
        tclLabel = Label(self.uploadFileFrame, text="TCL Files: ").grid(row=1, column=0, sticky=W)
        self.tclStatusLabel = Label(self.uploadFileFrame, textvariable=self.tclUploadVar)
        self.tclStatusLabel.grid(row=1, column=2, sticky=W)
        tclButton = Button(self.uploadFileFrame, text="Select Files",
                           command=partial(uploadTCLFile, self))
        tclButton.grid(row=1, column=1, sticky=W, padx=5, pady=5)

        # Testbench upload
        self.tbUploadVar = StringVar(self.uploadFileFrame)
        testBenchLabel = Label(self.uploadFileFrame, text="VHDL Test Benches: ").grid(row=2, column=0, sticky=W)
        self.tbUploadLabel = Label(self.uploadFileFrame, textvariable=self.tbUploadVar)
        self.tbUploadLabel.grid(row=2, column=2, sticky=W)

        testBenchButton = Button(self.uploadFileFrame, text="Select Files", command=partial(uploadVHDFile, self))
        testBenchButton.grid(row=2, column=1, sticky=W, padx=5, pady=5)

        # Student List upload
        self.textUploadVar = StringVar(self.uploadFileFrame)
        studentListLabel = Label(self.uploadFileFrame, text="Student Lists: ").grid(row=3, column=0, sticky=W)
        self.studentListLabel = Label(self.uploadFileFrame, textvariable=self.textUploadVar)
        self.studentListLabel.grid(row=3, column=2, sticky=W)

        studentListButton = Button(self.uploadFileFrame, text="Select Files",
                                   command=partial(uploadTextFile, self))
        studentListButton.grid(row=3, column=1, sticky=W, padx=5, pady=5)

    def createNewProjectFrame(self):
        self.generateNewRunFrame = Frame(self.leftFrame, highlightthickness=1, highlightbackground="black")
        self.generateNewRunFrame.grid(row=1, column=0, sticky="NSEW", padx=5, pady=5)

        # Title label
        uploadFileTitle = Label(self.generateNewRunFrame, text="Create Grading Project", font=("TkDefaultFont", 18))
        uploadFileTitle.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=W)

        # choose TCL
        self.tclVar = StringVar(self.generateNewRunFrame)
        self.chooseTclLabel = Label(self.generateNewRunFrame, text="")
        self.chooseTclLabel.grid(row=1, column=1, sticky=W)
        tclButton = Button(self.generateNewRunFrame, text="Select TCL Script", command=partial(openTCLFile, self))
        tclButton.grid(row=1, column=0, sticky=W, padx=5, pady=5)

        # choose student list
        self.studentListVar = StringVar(self.generateNewRunFrame)
        self.chooseStudentsLabel = Label(self.generateNewRunFrame, text="")
        self.chooseStudentsLabel.grid(row=2, column=1, sticky=W)
        tclButton = Button(self.generateNewRunFrame, text="Select Student List",
                           command=partial(openStudentListFile, self))
        tclButton.grid(row=2, column=0, sticky=W, padx=5, pady=5)

        # ZIP file upload
        self.zipVar = StringVar(self.generateNewRunFrame)
        self.zipLabel = Label(self.generateNewRunFrame, text="")
        self.zipLabel.grid(row=3, column=1, sticky=W)
        zipButton = Button(self.generateNewRunFrame, text="Choose Zip File", command=partial(uploadZipFile, self))
        zipButton.grid(row=3, column=0, sticky=W, padx=5, pady=5)

        self.deleteZipVal = IntVar()
        self.zipCheckBox = Checkbutton(self.generateNewRunFrame, variable=self.deleteZipVal, text="delete zip")
        self.zipCheckBox.grid(row=3, column=2, sticky="NSEW", padx=5, pady=5)

        # testbench label
        chooseTbLabel = Label(self.generateNewRunFrame, text="Choose Testbenches", font=("TkDefaultFont", 12))
        chooseTbLabel.grid(row=4, column=0, columnspan=2, padx=5, sticky=W)

        refreshButton = Button(self.generateNewRunFrame, text="Refresh TBs", command=partial(refreshTBs, self))
        refreshButton.grid(row=4, column=2, padx=5, sticky="NSEW")
        # choose testbenches
        listFrame = Frame(self.generateNewRunFrame, highlightthickness=1, highlightbackground="black")
        listFrame.grid(row=5, column=0, columnspan=2, sticky="NSEW", padx=5, pady=5)

        self.tbListBox = Listbox(listFrame, selectmode="multiple", highlightthickness=1, highlightbackground="black")
        self.tbListBox.pack(side=LEFT, fill=BOTH, expand=TRUE)

        slide = Scrollbar(listFrame, orient=VERTICAL)
        slide.pack(side=RIGHT, fill=Y)  # expand=FALSE)

        self.tbListBox.configure(yscrollcommand=slide.set)
        slide.configure(command=self.tbListBox.yview)

        refreshTBs(self)

        # choose generated name
        generationLabel = Label(self.generateNewRunFrame, text="Grading Project Name: ").grid(row=6, column=0, sticky=W)
        self.generationEntry = Entry(self.generateNewRunFrame, highlightthickness=1, highlightbackground="black")
        self.generationEntry.grid(row=6, column=1, sticky=W, padx=5, pady=5)

        # choose generated name
        generateButton = Button(self.generateNewRunFrame, text="Create",
                                command=partial(generateRun, self))
        generateButton.grid(row=6, column=2, sticky="NSEW", padx=5, pady=5)

        # error label
        self.errorLabel = Label(self.generateNewRunFrame, text="", fg="red")
        self.errorLabel.grid(row=7, column=0, columnspan=3, sticky=W)

    def createRunProjectFrame(self):
        runFrame = Frame(self.rightFrame, highlightthickness=1, highlightbackground="black")
        runFrame.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)

        runTitle = Label(runFrame, text="Run Grading Project", font=("TkDefaultFont", 18))
        runTitle.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=W)

        # select run comboBox and button
        self.projectComboBox = Combobox(runFrame)
        self.projectComboBox.grid(row=1, column=0, sticky="NSEW", padx=5, pady=5)
        self.projectComboBox.set('Choose Grading Project')
        loadButton = Button(runFrame, text="Load", command=partial(loadStudents, self))
        loadButton.grid(row=1, column=1, sticky="NSEW", padx=5, pady=5)

        deleteButton = Button(runFrame, text="Delete", command=partial(deleteRun, self))
        deleteButton.grid(row=1, column=2, sticky="NSEW", padx=5, pady=5)

        # select student comboBox
        self.studentComboBox = Combobox(runFrame)
        self.studentComboBox.grid(row=2, column=0, sticky="NSEW", padx=5, pady=5)
        self.studentComboBox.set('Choose Student')
        runButton = Button(runFrame, text="Run", command=partial(runStudent, self))
        runButton.grid(row=2, column=1, sticky="NSEW", padx=5, pady=5)

        runButton = Button(runFrame, text="Run Next", command=partial(runNextStudent, self))
        runButton.grid(row=2, column=2, sticky="NSEW", padx=5, pady=5)

        runButton = Button(runFrame, text="Run All", command=partial(runAllStudents, self))
        runButton.grid(row=2, column=3, sticky="NSEW", padx=5, pady=5)

        clearWindowButton = Button(runFrame, text="Clear Window", command=partial(clearWindowText, self.terminalScrolledText))
        clearWindowButton.grid(row=2, column=4, sticky="NSEW", padx=5, pady=5)

        quitWindowButton = Button(runFrame, text="Stop", command=partial(stopRunning, self))
        quitWindowButton.grid(row=2, column=5, sticky="NSEW", padx=5, pady=5)

        self.guiCheckBoxVal = IntVar()
        self.guiCheckBox = Checkbutton(runFrame, variable=self.guiCheckBoxVal, text="gui")
        self.guiCheckBox.grid(row=2, column=6, sticky="NSEW", padx=5, pady=5)


        return

    def createScrollWindow(self):
        # create scrollWindow
        terminalWindowFrame = Frame(self.rightFrame, highlightthickness=1, highlightbackground="black")
        terminalWindowFrame.grid(row=1, column=0, sticky="NSEW", padx=5, pady=5)

        self.windowStatusVar = StringVar(terminalWindowFrame)
        windowStatusLabel = Label(terminalWindowFrame, textvariable=self.windowStatusVar)
        windowStatusLabel.pack(side=BOTTOM)

        self.terminalScrolledText = ScrolledText(terminalWindowFrame, highlightthickness=1, highlightbackground="black")
        self.terminalScrolledText.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.terminalScrolledText.configure(state='disabled')



    def clearSubprocess(self):
        self.subProcess = None

    def assignSubprocess(self, cmd):
        self.subProcess = None
        self.subProcess = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, text=True, universal_newlines=True)
        return self.subProcess

    def setCurrStudent(self, student):
        self.currentStudent = student

    def getTimer(self):
        return self.timer

    def setExitFlag(self, flag):
        self.exitFlag = flag

    def setIsGenerating(self, val):
        self.isGenerating = val

    def getExitFlag(self):
        return self.exitFlag

    def clearTimer(self):
        self.timer = 0

    def updateTimer(self):
        if not self.isRunning and not self.isGenerating:
            self.after(1000, self.updateTimer)
            return

        if self.isGenerating:
            self.errorLabel['fg'] = "black"
            self.errorLabel['text'] = f'''Generating... {getTimerText(self.timer, operator.floordiv) }:{getTimerText(self.timer, operator.mod)}'''
        if self.isRunning:
            self.windowStatusVar.set(f'''Running {self.currentStudent}. Time Elapsed: {getTimerText(self.timer, operator.floordiv) }:{getTimerText(self.timer, operator.mod)}''')

        # update time
        self.timer += 1
        self.after(1000, self.updateTimer)

    def setIsRunning(self, val):
        self.isRunning = val


def handleClosing():
    app.exitFlag = True
    if app.subProcess is not None:
        app.subProcess.terminate()
    app.destroy()


# Create directories if they dont exist
if not os.path.exists(os.getcwd() + os.path.join("\\lab_tcl")):
    os.makedirs(os.getcwd() + os.path.join("\\lab_tcl"))

if not os.path.exists(os.getcwd() + os.path.join("\\testbenchces")):
    os.makedirs(os.getcwd() + os.path.join("\\testbenchces"))

if not os.path.exists(os.getcwd() + os.path.join("\\studentlists")):
    os.makedirs(os.getcwd() + os.path.join("\\studentlists"))

if not os.path.exists(os.getcwd() + os.path.join("\\grading_projects")):
    os.makedirs(os.getcwd() + os.path.join("\\grading_projects"))

app = Application()
app.title("Digital Design Grading GUI")
app.iconbitmap(os.getcwd() + os.path.join("\\images\\integrated-circuit.ico"))
app.protocol("WM_DELETE_WINDOW", handleClosing)
app.mainloop()
