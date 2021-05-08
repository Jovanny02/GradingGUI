from tkinter import filedialog, END
from pathlib import Path
from zip_function import *
import subprocess
from subprocess import DEVNULL
from sim_function import compile_modelsim

import os


def generateRun(self):
    # Get variables from app
    selectedTCL = self.tclVar.get()
    selectedStudentList = self.studentListVar.get()
    chosenZip = self.zipVar.get()
    chosenTBs = self.tbListBox.curselection()
    generationName = self.generationEntry.get().replace(" ", "")

    # Error checking
    if selectedTCL == "" or selectedStudentList == "" or chosenZip == "" or generationName == "" or len(chosenTBs) == 0:
        self.errorLabel['text'] = "Please Select All Fields"
        self.errorLabel['fg'] = "red"
        return

    tclPath = os.getcwd() + os.path.join(f"\\generatedruns\\{generationName}\\tcl")
    submissionsPath = os.getcwd() + os.path.join(f'''\\generatedruns\\{generationName}\\submissions''')
    modelsimPath = os.getcwd() + os.path.join(f'''\\generatedruns\\{generationName}\\modelsim''')
    #Create Directory For Run
    if not os.path.exists(os.getcwd() + os.path.join(f"\\generatedruns\\{generationName}")):
        os.makedirs(os.getcwd() + os.path.join(f"\\generatedruns\\{generationName}"))
        os.makedirs(modelsimPath)
        os.makedirs(tclPath)
        os.makedirs(submissionsPath)
    else:
        self.errorLabel['text'] = "Name Already Exists"
        self.errorLabel['fg'] = "red"
        return

    # Extract submissions
    zip_opener(submissionsPath, selectedStudentList, chosenZip, False)

    # create modelsim project
    createProjectCommand = f'''project new "{modelsimPath}" {generationName}'''
    createProjectCommand = createProjectCommand.replace(os.sep, "/")
    # add testbench files
    for index in chosenTBs:
        temp = self.tbListBox.get(index)
        createProjectCommand += '\nproject addfile "' + \
                                (os.getcwd() + os.path.join(f"/testbenchces/{temp}")).replace(os.sep, '/') + '"'
    createProjectCommand += "\nquit\n"

    # temp tcl file to read from to make do command easier
    f = open("createProject.tcl", "w", encoding='utf-8')
    f.write(createProjectCommand)
    f.close()
    # run commands
    cmd = f'''vsim -c -l "" -do "{os.path.abspath("createProject.tcl")}"'''
    subprocess.run(cmd, shell=True, stdout=True, stderr=DEVNULL)

    # remove temp file
    try:
        os.remove("createProject.tcl")
    except OSError:
        pass

    # Generate TCL files
    compile_modelsim(selectedStudentList, submissionsPath.replace(os.sep, '/'), selectedTCL,
                     (modelsimPath + os.path.join("\\" + generationName + ".mpf")).replace(os.sep, '/'), False,
                     tclPath.replace(os.sep, '/'))
    # refreshes runs
    loadRuns(self)

    self.errorLabel['fg'] = "#006400"
    self.errorLabel['text'] = "Succesfully Generated"
    return


def refreshTBs(self):
    self.tbListBox.delete(0, self.tbListBox.size())
    tbDir = os.getcwd() + os.path.join("\\testbenchces")
    try:
        for file in os.listdir(tbDir):
            if file.endswith(".vhd"):
                self.tbListBox.insert(self.tbListBox.size(), file)
    except:
        print("NO TESTBENCH FILES!")


def addWindowText(self):
    numLines = len(self.terminalScrolledText.get('1.0', END).splitlines())
    self.terminalScrolledText.configure(state='normal')
    self.terminalScrolledText.insert(END, " > HELLLO! THIS IS A TEST! INSERT NUMBER: "
                                     + str(numLines) + "\n")
    self.terminalScrolledText.configure(state='disabled')


def clearWindowText(self):
    self.terminalScrolledText.configure(state='normal')
    self.terminalScrolledText.delete('1.0', END)
    self.terminalScrolledText.configure(state='disabled')


def loadRuns(self):
    root = (os.getcwd() + os.path.join(f"\\generatedruns")).replace(os.sep, "/")
    runs = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
    self.runComboBox['values'] = runs


def deleteRun(self):
    if self.runComboBox.get() == "Choose Run":
        return

    shutil.rmtree(os.getcwd() + os.path.join(f"\\generatedruns\\{self.runComboBox.get()}"))
    loadRuns(self)


def loadStudents(self):
    if self.runComboBox.get() == "Choose Run":
        return

    self.studentComboBox.delete(0, self.tbListBox.size())
    studentsDir = os.getcwd() + os.path.join(f"\\generatedruns\\{self.runComboBox.get()}\\tcl")
    students = []
    try:
        for file in os.listdir(studentsDir):
            if file.endswith(".tcl"):
                students.append(file[0: len(file)-4])
    except:
        print("NO TESTBENCH FILES!")

    self.studentComboBox['values'] = students
    self.studentComboBox.set('Choose Student')
    return


def runStudent(self):
    if self.studentComboBox.get() == 'Choose Student':
        return

    studentDir = os.getcwd() + os.path.join(f"\\generatedruns\\{self.runComboBox.get()}\\tcl\\")
    studentDir += os.path.join(self.studentComboBox.get() + ".tcl")
    studentDir = studentDir.replace(os.sep, "/")
    if self.guiCheckBoxVal.get() == 1:
        cmd = f'''vsim -gui -l "" -do "{os.path.abspath(studentDir)}"'''
    elif self.guiCheckBoxVal.get() == 0:
        cmd = f'''vsim -c -l "" -do "{os.path.abspath(studentDir)}"'''
    else:
        return

    try:
        subprocess.run(cmd, shell=True, stdout=True, stderr=DEVNULL)
    except:
        print(''' Something didn't work... ¯\_(ツ)_/¯ ''')
    return
