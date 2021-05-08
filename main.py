from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox

from OpenFiles import *
from functools import partial
from helpers import *
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

        self.createLayout()
        self.createUploadFiles()
        self.createNewRun()
        self.createRunFrame()
        self.createScrollWindow()
        # Load Runs
        loadRuns(self)

    def createLayout(self):
        # create two columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
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
        uploadFileTitle = Label(self.uploadFileFrame, text="Upload New File", font=("TkDefaultFont", 18))
        uploadFileTitle.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=W)

        # TCL upload
        self.tclUploadVar = StringVar(self.uploadFileFrame)
        tclLabel = Label(self.uploadFileFrame, text="TCL File: ").grid(row=1, column=0, sticky=W)
        self.tclStatusLabel = Label(self.uploadFileFrame, textvariable=self.tclUploadVar)
        self.tclStatusLabel.grid(row=1, column=2, sticky=W)
        tclButton = Button(self.uploadFileFrame, text="Select File",
                           command=partial(uploadTCLFile, self))
        tclButton.grid(row=1, column=1, sticky=W, padx=5, pady=5)

        # Testbench upload
        self.tbUploadVar = StringVar(self.uploadFileFrame)
        testBenchLabel = Label(self.uploadFileFrame, text="VHDL Test Bench: ").grid(row=2, column=0, sticky=W)
        self.tbUploadLabel = Label(self.uploadFileFrame, textvariable=self.tbUploadVar)
        self.tbUploadLabel.grid(row=2, column=2, sticky=W)

        testBenchButton = Button(self.uploadFileFrame, text="Select File", command=partial(uploadVHDFile, self))
        testBenchButton.grid(row=2, column=1, sticky=W, padx=5, pady=5)

        # Student List upload
        self.textUploadVar = StringVar(self.uploadFileFrame)
        studentListLabel = Label(self.uploadFileFrame, text="Student List: ").grid(row=3, column=0, sticky=W)
        self.studentListLabel = Label(self.uploadFileFrame, textvariable=self.textUploadVar)
        self.studentListLabel.grid(row=3, column=2, sticky=W)

        studentListButton = Button(self.uploadFileFrame, text="Select File",
                                   command=partial(uploadTextFile, self))
        studentListButton.grid(row=3, column=1, sticky=W, padx=5, pady=5)

    def createNewRun(self):
        self.generateNewRunFrame = Frame(self.leftFrame, highlightthickness=1, highlightbackground="black")
        self.generateNewRunFrame.grid(row=1, column=0, sticky="NSEW", padx=5, pady=5)

        # Title label
        uploadFileTitle = Label(self.generateNewRunFrame, text="Generate New Run", font=("TkDefaultFont", 18))
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
        tclButton = Button(self.generateNewRunFrame, text="Choose Zip File", command=partial(uploadZipFile, self))
        tclButton.grid(row=3, column=0, sticky=W, padx=5, pady=5)

        # testbench label
        chooseTbLabel = Label(self.generateNewRunFrame, text="Choose Testbenches", font=("TkDefaultFont", 12))
        chooseTbLabel.grid(row=4, column=0, columnspan=2, padx=5, sticky=W)

        refreshButton = Button(self.generateNewRunFrame, text="Refresh TBs", command=partial(refreshTBs, self))
        refreshButton.grid(row=4, column=3, padx=5, sticky="NSEW")
        # choose testbenches
        listFrame = Frame(self.generateNewRunFrame, highlightthickness=1, highlightbackground="black")
        listFrame.grid(row=5, column=0, columnspan=2, sticky="NSEW", padx=5, pady=5)

        slide = Scrollbar(listFrame, orient=VERTICAL)
        slide.pack(side=RIGHT, expand=FALSE)

        self.tbListBox = Listbox(listFrame, selectmode="multiple", highlightthickness=1, highlightbackground="black")
        self.tbListBox.pack(side=LEFT, fill=BOTH, expand=TRUE)
        refreshTBs(self)

        # choose generated name
        generationLabel = Label(self.generateNewRunFrame, text="Generation Name: ").grid(row=6, column=0, sticky=W)
        self.generationEntry = Entry(self.generateNewRunFrame, highlightthickness=1, highlightbackground="black")
        self.generationEntry.grid(row=6, column=1, sticky=W, padx=5, pady=5)

        # choose generated name
        generateButton = Button(self.generateNewRunFrame, text="Generate",
                                command=partial(generateRun, self))
        generateButton.grid(row=6, column=3, sticky="NSEW", padx=5, pady=5)

        # error label
        self.errorLabel = Label(self.generateNewRunFrame, text="", fg="red")
        self.errorLabel.grid(row=7, column=0, columnspan=3, sticky=W)

    def createRunFrame(self):
        runFrame = Frame(self.rightFrame, highlightthickness=1, highlightbackground="black")
        runFrame.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)

        runTitle = Label(runFrame, text="Run", font=("TkDefaultFont", 18))
        runTitle.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=W)

        # select run comboBox and button
        self.runComboBox = Combobox(runFrame)
        self.runComboBox.grid(row=1, column=0, sticky="NSEW", padx=5, pady=5)
        self.runComboBox.set('Choose Run')
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

        runButton = Button(runFrame, text="Run Next", command=partial(runStudent, self))
        runButton.grid(row=2, column=2, sticky="NSEW", padx=5, pady=5)

        runButton = Button(runFrame, text="Run All", command=partial(runStudent, self))
        runButton.grid(row=2, column=3, sticky="NSEW", padx=5, pady=5)

        clearWindowButton = Button(runFrame, text="Clear Text", command=partial(clearWindowText, self))
        clearWindowButton.grid(row=2, column=4, sticky="NSEW", padx=5, pady=5)

        self.guiCheckBoxVal = IntVar()
        self.guiCheckBox = Checkbutton(runFrame, variable=self.guiCheckBoxVal, text="gui")
        self.guiCheckBox.grid(row=2, column=5, sticky="NSEW", padx=5, pady=5)


        return

    def createScrollWindow(self):
        # create scrollWindow
        terminalWindowFrame = Frame(self.rightFrame, highlightthickness=1, highlightbackground="black")
        terminalWindowFrame.grid(row=1, column=0, sticky="NSEW", padx=5, pady=5)

        self.terminalScrolledText = ScrolledText(terminalWindowFrame, highlightthickness=1, highlightbackground="black")
        self.terminalScrolledText.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.terminalScrolledText.configure(state='disabled')

        testWindowButton = Button(terminalWindowFrame, text="Add Text", command=partial(addWindowText, self))
        testWindowButton.pack()


# Create directories if they dont exist
if not os.path.exists(os.getcwd() + os.path.join("\\lab_tcl")):
    os.makedirs(os.getcwd() + os.path.join("\\lab_tcl"))

if not os.path.exists(os.getcwd() + os.path.join("\\testbenchces")):
    os.makedirs(os.getcwd() + os.path.join("\\testbenchces"))

if not os.path.exists(os.getcwd() + os.path.join("\\studentlists")):
    os.makedirs(os.getcwd() + os.path.join("\\studentlists"))

if not os.path.exists(os.getcwd() + os.path.join("\\generatedruns")):
    os.makedirs(os.getcwd() + os.path.join("\\generatedruns"))

app = Application()
app.title("Digital Design Grading GUI")
app.iconbitmap(os.getcwd() + os.path.join("\\images\\integrated-circuit.ico"))
app.mainloop()
