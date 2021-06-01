from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox, Style

import subprocess
from subprocess import PIPE, Popen, STDOUT
from OpenFiles import *
from functools import partial
from helpers import *

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
        self.style = None
        self.selectedTestbenches = []

        # Create a style
        self.style = Style(self)
        # Import the tcl file
        self.tk.call('source', 'azure-dark.tcl')
        self.tk.call('source', 'azure.tcl')

        # Set the theme with the theme_use method
        self.style.theme_use('azure')

        self.createLayout()
        self.createUploadFiles()
        self.createNewProjectFrame()
        self.createScrollWindow()
        self.createRunProjectFrame()
        # Load Runs
        loadProjects(self)

        style = ttk.Style()
        style.configure("Red.TLabel", foreground="red")
        style2 = ttk.Style()
        style2.configure("Green.TLabel", foreground="green")
        self.updateTimer()

    def createLayout(self):
        # create two columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=5)
        self.grid_rowconfigure(0, weight=1)

        # create left column
        self.leftFrame = ttk.Frame(self)
        self.leftFrame.grid(row=0, column=0, sticky="NSWE")

        # create left column subgrid
        self.leftFrame.grid_columnconfigure(0, weight=1)
        self.leftFrame.grid_rowconfigure(0, weight=1)
        self.leftFrame.grid_rowconfigure(1, weight=3)

        # create right column
        self.rightFrame = ttk.Frame(self)
        self.rightFrame.grid(row=0, column=1, sticky="NSWE")

        # create right column subgrid
        self.rightFrame.grid_columnconfigure(0, weight=1)
        self.rightFrame.grid_rowconfigure(0, weight=1)
        self.rightFrame.grid_rowconfigure(1, weight=6)


    def createUploadFiles(self):
        self.uploadFileFrame = ttk.Frame(self.leftFrame, borderwidth=1,
                                         relief='solid')  # highlightthickness=1, highlightbackground="black")
        self.uploadFileFrame.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)

        # configure columns
        self.uploadFileFrame.grid_columnconfigure(0, weight=1)
        self.uploadFileFrame.grid_columnconfigure(1, weight=1, minsize=100)
        self.uploadFileFrame.grid_columnconfigure(2, weight=1, minsize=100)
        self.uploadFileFrame.grid_columnconfigure(3, weight=4)

        # Titlettk.Label
        uploadFileTitle = ttk.Label(self.uploadFileFrame, text="Copy Files to GUI Directory", font=("TkDefaultFont", 18))
        uploadFileTitle.grid(row=0, column=0, columnspan=3, sticky="NSEW", padx=5, pady=(5, 0))

        # Title sep
        sep = ttk.Separator(self.uploadFileFrame, orient='horizontal')
        sep.grid(row=1, column=0, columnspan=3, padx=5, pady=(0, 5), sticky='NEW')





        # TCL upload
        self.tclUploadVar = StringVar(self.uploadFileFrame)
        # tclLabel = ttk.Label(self.uploadFileFrame, text="TCL Files: ")
        # tclLabel.grid(row=2, column=0, sticky=W)
        self.tclStatusLabel = ttk.Label(self.uploadFileFrame, textvariable=self.tclUploadVar)
        self.tclStatusLabel.grid(row=2, column=1, columnspan=3, sticky=W)
        tclButton = ttk.Button(self.uploadFileFrame, text="Copy TCL Files", style='AccentButton',
                               command=partial(uploadTCLFile, self))
        tclButton.grid(row=2, column=0, sticky=NSEW, padx=5, pady=5)
        # tclButton.pack(side=TOP, fill=BOTH, expand=FALSE, padx=(0, 5), pady=5)


        # Testbench upload
        self.tbUploadVar = StringVar(self.uploadFileFrame)
        # testBenchLabel = ttk.Label(self.uploadFileFrame, text="VHDL Test Benches: ").grid(row=3, column=0, sticky=W)
        self.tbUploadLabel = ttk.Label(self.uploadFileFrame, textvariable=self.tbUploadVar)
        self.tbUploadLabel.grid(row=3, column=1, columnspan=3, sticky=W)

        testBenchButton = ttk.Button(self.uploadFileFrame, style='AccentButton', text="Copy Test Benches",
                                     command=partial(uploadVHDFile, self))
        testBenchButton.grid(row=3, column=0, sticky=NSEW, padx=5, pady=5)
        # testBenchButton.pack(side=TOP, fill=BOTH, expand=FALSE, padx=(0, 5), pady=5)

        # Student List upload
        self.textUploadVar = StringVar(self.uploadFileFrame)
        # studentListLabel = ttk.Label(self.uploadFileFrame, text="Student Lists: ").grid(row=4, column=0, sticky=W)
        self.studentListLabel = ttk.Label(self.uploadFileFrame, textvariable=self.textUploadVar)
        self.studentListLabel.grid(row=4, column=1, columnspan=3, sticky=W)

        studentListButton = ttk.Button(self.uploadFileFrame, text="Copy Student Lists", style='AccentButton',
                                       command=partial(uploadTextFile, self))
        studentListButton.grid(row=4, column=0, sticky=NSEW, padx=5, pady=5)
        #studentListButton.pack(side=TOP, fill=BOTH, expand=FALSE, padx=(0, 5), pady=5)


    def createNewProjectFrame(self):
        self.generateNewRunFrame = ttk.Frame(self.leftFrame, borderwidth=1,
                                             relief='solid')  # highlightthickness=1, highlightbackground="black")
        self.generateNewRunFrame.grid(row=1, column=0, sticky="NSEW", padx=5, pady=5)

        # Titlettk.Label
        uploadFileTitle = ttk.Label(self.generateNewRunFrame, text="Create Grading Project", font=("TkDefaultFont", 18))
        uploadFileTitle.grid(row=0, column=0, columnspan=2, padx=5, pady=(5, 0), sticky=W)

        # Title sep
        sep = ttk.Separator(self.generateNewRunFrame, orient='horizontal')
        sep.grid(row=1, column=0, columnspan=2, padx=5, pady=(0, 5), sticky='NEW')

        # choose TCL
        self.tclVar = StringVar(self.generateNewRunFrame)
        self.chooseTclLabel = ttk.Label(self.generateNewRunFrame, text="")
        self.chooseTclLabel.grid(row=2, column=1, sticky=W)
        tclButton = ttk.Button(self.generateNewRunFrame, style='AccentButton', text="Select TCL Script",
                               command=partial(openTCLFile, self))
        tclButton.grid(row=2, column=0, sticky=EW, padx=5, pady=5)

        # choose student list
        self.studentListVar = StringVar(self.generateNewRunFrame)
        self.chooseStudentsLabel = ttk.Label(self.generateNewRunFrame, text="")
        self.chooseStudentsLabel.grid(row=3, column=1, sticky=W)
        tclButton = ttk.Button(self.generateNewRunFrame, text="Select Student List", style='AccentButton',
                               command=partial(openStudentListFile, self))
        tclButton.grid(row=3, column=0, sticky=EW, padx=5, pady=5)

        # ZIP file upload
        self.zipVar = StringVar(self.generateNewRunFrame)
        self.zipLabel = ttk.Label(self.generateNewRunFrame, text="")
        self.zipLabel.grid(row=4, column=1, sticky=W)
        zipButton = ttk.Button(self.generateNewRunFrame, style='AccentButton', text="Choose Zip File",
                               command=partial(uploadZipFile, self))
        zipButton.grid(row=4, column=0, sticky=EW, padx=5, pady=5)

        self.deleteZipVal = IntVar()
        self.zipCheckBox = ttk.Checkbutton(self.generateNewRunFrame, variable=self.deleteZipVal, style='Switch',
                                           text="delete zip")
        self.zipCheckBox.grid(row=4, column=2, sticky="NSEW", padx=5, pady=5)

        # testbench section
        tbButton = ttk.Button(self.generateNewRunFrame, style='AccentButton', text="Choose Testbenches",
                                    command=partial(chooseVHDFiles, self))
        tbButton.grid(row=5, column=0, sticky=NW, padx=5, pady=5)
        self.tbSelectLabel = ttk.Label(self.generateNewRunFrame, text="")
        self.tbSelectLabel.grid(row=5, column=1, sticky=NSEW)


        # choose generated name
        generationLabel = ttk.Label(self.generateNewRunFrame, text="Grading Project Name: ").grid(row=7, column=0,
                                                                                                  sticky=W)
        self.generationEntry = ttk.Entry(self.generateNewRunFrame)
        self.generationEntry.grid(row=7, column=1, sticky=W, padx=5, pady=5)

        # choose generated name
        generateButton = ttk.Button(self.generateNewRunFrame, text="Create", style='AccentButton',
                                    command=partial(generateProject, self))
        generateButton.grid(row=7, column=2, sticky="NSEW", padx=5, pady=5)

        # error label
        self.errorLabel = Label(self.generateNewRunFrame, text="", fg="red")
        self.errorLabel.grid(row=8, column=0, columnspan=3, sticky=W)

    def createRunProjectFrame(self):
        runFrame = ttk.Frame(self.rightFrame, borderwidth=1,
                             relief='solid')  # highlightthickness=1, highlightbackground="black")
        runFrame.grid(row=0, column=0, columnspan=2, sticky="NSEW", padx=5, pady=5)

        runTitle = ttk.Label(runFrame, text="Load Grading Project", font=("TkDefaultFont", 18))
        runTitle.grid(row=0, column=0, columnspan=2, padx=5, pady=(5, 0), sticky=W)

        # Title sep
        sep = ttk.Separator(runFrame, orient='horizontal')
        sep.grid(row=1, column=0, columnspan=2, padx=5, pady=(0, 5), sticky='NEW')

        # select run comboBox and button
        self.projectComboBox = Combobox(runFrame, state='readonly')
        self.projectComboBox.grid(row=2, column=0, sticky="NSEW", padx=5, pady=5)
        self.projectComboBox.set('Choose Grading Project')
        loadButton = ttk.Button(runFrame, text="Load Project", style='AccentButton',
                                command=partial(loadStudents, self))
        loadButton.grid(row=2, column=1, sticky="NSEW", padx=5, pady=5)

        deleteButton = ttk.Button(runFrame, text="Delete Project", style='AccentButton',
                                  command=partial(deleteProject, self))
        deleteButton.grid(row=2, column=2, sticky="NSEW", padx=5, pady=5)

        self.themeVar = IntVar()
        self.themeCheckBox = ttk.Checkbutton(runFrame, variable=self.themeVar, style='Switch',
                                             text="Dark Mode", command=self.toggleTheme)
        self.themeCheckBox.grid(row=2, column=3, sticky="W", padx=5, pady=5)

        # select student comboBox
        self.studentComboBox = Combobox(runFrame, state='readonly')
        self.studentComboBox.grid(row=3, column=0, sticky="EW", padx=5, pady=5)
        self.studentComboBox.set('Choose Student')

        buttonFrame = ttk.Frame(runFrame)
        buttonFrame.grid(row=3, column=1, columnspan=5, sticky="NSEW", padx=5, pady=5)

        loadButton = ttk.Button(buttonFrame, style='AccentButton', text="Load Result",
                                command=partial(loadStudentResult, self))
        loadButton.pack(side=LEFT, fill=Y, expand=FALSE, padx=(0, 5), pady=5)

        previousButton = ttk.Button(buttonFrame, style='AccentButton', text="Load Previous Result",
                                    command=partial(changeComboBox, self.studentComboBox, -1, self))
        previousButton.pack(side=LEFT, fill=Y, expand=FALSE, padx=(5, 5), pady=5)

        nextButton = ttk.Button(buttonFrame, style='AccentButton', text="Load Next Result",
                                command=partial(changeComboBox,self.studentComboBox, 1, self))
        nextButton.pack(side=LEFT, fill=Y, expand=FALSE, padx=(5, 5), pady=5)

        return

    def createScrollWindow(self):
        # create scrollWindow
        terminalWindowFrame = ttk.Frame(self.rightFrame, borderwidth=1,
                                        relief='solid')
        terminalWindowFrame.grid(row=1, column=0, sticky="NSEW", padx=5, pady=5)

        self.terminalScrolledText = ScrolledText(terminalWindowFrame, highlightthickness=1, highlightbackground="black",
                                                 font=("TkDefaultFont", 9))
        self.terminalScrolledText.pack(side=TOP, fill=BOTH, expand=TRUE)
        self.terminalScrolledText.pack_propagate(False)

        self.windowStatusVar = StringVar(terminalWindowFrame)
        self.windowStatusLabel = ttk.Label(terminalWindowFrame, textvariable=self.windowStatusVar, font=("TkDefaultFont", 9))
        self.windowStatusLabel.pack(side=BOTTOM)

        # Font change for terminal window
        file = os.getcwd() + '\\images\\add.png'
        try:
            self.addIcon = PhotoImage(file=file)
            self.increase = ttk.Button(self.terminalScrolledText, style='AccentButton', image=self.addIcon,
                                    command=partial(changeTerminalFont, self.windowStatusLabel, self.terminalScrolledText, 1))
            self.increase.place(relx=1.0, rely=0.0, x=-2, y=2, anchor="ne")
        except:
            self.increase = ttk.Button(self.terminalScrolledText, style='AccentButton', text='+',
                                    command=partial(changeTerminalFont, self.windowStatusLabel, self.terminalScrolledText, 1))
            self.increase.place(relx=1.0, rely=0.0, x=-2, y=2, anchor="ne", height=40, width=40)

        file = os.getcwd() + '\\images\\subtract.png'
        try:
            self.subIcon = PhotoImage(file=file)
            self.increase = ttk.Button(self.terminalScrolledText, style='AccentButton', image=self.subIcon,
                                    command=partial(changeTerminalFont, self.windowStatusLabel, self.terminalScrolledText, -1))
            self.increase.place(relx=1.0, rely=0.0, x=-45, y=2, anchor="ne")
        except:
            self.increase = ttk.Button(self.terminalScrolledText, style='AccentButton', text='-',
                                    command=partial(changeTerminalFont, self.windowStatusLabel, self.terminalScrolledText, -1))
            self.increase.place(relx=1.0, rely=0.0, x=-45, y=2, anchor="ne", height=40, width=40)




        # Terminal controls
        terminalControlFrame = ttk.Frame(self.rightFrame, borderwidth=1,
                                         relief='solid')  # highlightthickness=1, highlightbackground="black")
        terminalControlFrame.grid(row=2, column=0, sticky="NSEW", padx=5, pady=5)

        runButton = ttk.Button(terminalControlFrame, style='AccentButton', text="Run",
                               command=partial(runStudent, self))
        runButton.pack(side=LEFT, fill=BOTH, padx=5, pady=5)

        runNextButton = ttk.Button(terminalControlFrame, style='AccentButton', text="Run Next",
                                   command=partial(runNextStudent, self))
        runNextButton.pack(side=LEFT, fill=BOTH, padx=5, pady=5)

        runAllButton = ttk.Button(terminalControlFrame, style='AccentButton', text="Run All",
                                  command=partial(runAllStudents, self))
        runAllButton.pack(side=LEFT, fill=BOTH, padx=5, pady=5)

        clearWindowButton = ttk.Button(terminalControlFrame, style='AccentButton', text="Clear Window",
                                       command=partial(clearWindowText, self.terminalScrolledText))
        clearWindowButton.pack(side=LEFT, fill=BOTH, padx=5, pady=5)

        quitWindowButton = ttk.Button(terminalControlFrame, style='AccentButton', text="Stop",
                                      command=partial(stopRunning, self))
        quitWindowButton.pack(side=LEFT, fill=BOTH, padx=5, pady=5)

        self.guiCheckBoxVal = IntVar()
        self.guiCheckBox = ttk.Checkbutton(terminalControlFrame, variable=self.guiCheckBoxVal, style='Switch',
                                           text="gui")
        self.guiCheckBox.pack(side=LEFT, fill=BOTH, padx=5, pady=5)

        self.parseOutputVar = IntVar()
        self.parseOutputCheckBox = ttk.Checkbutton(terminalControlFrame, variable=self.parseOutputVar, style='Switch',
                                                   text="Result Only")
        self.parseOutputCheckBox.pack(side=LEFT, fill=BOTH, padx=5, pady=5)

    def clearSubprocess(self):
        self.subProcess = None

    def assignSubprocess(self, cmd):
        self.subProcess = None
        self.subProcess = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, text=True, universal_newlines=True,
                                creationflags=subprocess.CREATE_NO_WINDOW)
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

    def toggleTheme(self):
        style = self.style.theme_use()
        if self.style.theme_use() == 'azure':
            self.style.theme_use('azure-dark')
            # set window background
            self.terminalScrolledText["bg"] = "#333333"
            self.terminalScrolledText["fg"] = "#ffffff"
            # set label background
            self.errorLabel["bg"] = "#333333"
            # only toggle text color if it is black or white
            if self.errorLabel["fg"] == "#000000":
                self.errorLabel["fg"] = "#ffffff"
            return
        # set ttk element backgrounds
        self.style.theme_use('azure')
        # set other backgrounds that cant be set using style
        # set window background
        self.terminalScrolledText["bg"] = "#ffffff"
        self.terminalScrolledText["fg"] = "#000000"
        # set label background
        self.errorLabel["bg"] = "#ffffff"
        if self.errorLabel["fg"] == "#ffffff":
            self.errorLabel["fg"] = "#000000"

    def updateTimer(self):
        if not self.isRunning and not self.isGenerating:
            self.after(1000, self.updateTimer)
            return


        if self.isRunning:
            self.windowStatusVar.set(
                f'''Running {self.currentStudent}. Time Elapsed: {getTimerText(self.timer, operator.floordiv)}:{getTimerText(self.timer, operator.mod)}''')

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

if not os.path.exists(os.getcwd() + os.path.join("\\testbenches")):
    os.makedirs(os.getcwd() + os.path.join("\\testbenches"))

if not os.path.exists(os.getcwd() + os.path.join("\\studentlists")):
    os.makedirs(os.getcwd() + os.path.join("\\studentlists"))

if not os.path.exists(os.getcwd() + os.path.join("\\grading_projects")):
    os.makedirs(os.getcwd() + os.path.join("\\grading_projects"))

app = Application()
app.title("Digital Design Grading GUI")
app.iconbitmap(os.getcwd() + os.path.join("\\images\\integrated-circuit.ico"))
app.protocol("WM_DELETE_WINDOW", handleClosing)
app.mainloop()
