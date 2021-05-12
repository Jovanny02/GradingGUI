import sys
import threading
import time
from tkinter import filedialog, END
from concurrent.futures import *
from zip_function import *
import subprocess
from subprocess import DEVNULL, PIPE, Popen, STDOUT
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
    # Create Directory For Run
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
    deleteZip = False
    if self.deleteZipVal.get() == 1:
        deleteZip = True
    zip_opener(submissionsPath, selectedStudentList, chosenZip, deleteZip)

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


def clearWindowText(terminalScrolledText):
    terminalScrolledText.configure(state='normal')
    terminalScrolledText.delete('1.0', END)
    terminalScrolledText.configure(state='disabled')


def loadRuns(self):
    root = (os.getcwd() + os.path.join(f"\\generatedruns")).replace(os.sep, "/")
    runs = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
    self.runComboBox['values'] = runs


def deleteRun(self):
    if self.runComboBox.get() == "'Choose Grading Project'":
        return

    shutil.rmtree(os.getcwd() + os.path.join(f"\\generatedruns\\{self.runComboBox.get()}"))
    loadRuns(self)
    self.runComboBox.set('Choose Grading Project')


def loadStudents(self):
    if self.runComboBox.get() == 'Choose Grading Project':
        return

    self.studentComboBox.delete(0, self.tbListBox.size())
    studentsDir = os.getcwd() + os.path.join(f"\\generatedruns\\{self.runComboBox.get()}\\tcl")
    students = []
    try:
        for file in os.listdir(studentsDir):
            if file.endswith(".tcl"):
                students.append(file[0: len(file) - 4])
    except:
        print("NO TESTBENCH FILES!")

    self.currentProject = self.runComboBox.get()
    self.studentComboBox['values'] = students
    self.studentComboBox.set('Choose Student')
    return


def checkOutputLoop(text, process, student):
    clearWindowText(text)
    tempData, err = process.communicate()
    for line in tempData.split("\n"):
        text.configure(state='normal')
        text.insert(END, line + "\n")

    text.insert(END, f"Results for {student}\n")
    text.configure(state='disabled')
    process.terminate()
    text.yview(END)
    sys.exit()


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
        self.subProcess = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, text=True, universal_newlines=True)


    except:
        print(''' Something didn't work... ¯\_(ツ)_/¯ ''')

    # self.runThread = threading.Thread(target=checkOutputLoop, name="windowThread",
    #                                   args=(self.terminalScrolledText, self.subProcess, self.studentComboBox.get()))
    # self.runThread.daemon = True
    # self.runThread.start()
    with ThreadPoolExecutor() as executor:
        self.runThread = executor.submit(checkOutputLoop, self.terminalScrolledText, self.subProcess,
                                         self.studentComboBox.get())

    return


def runNextStudent(self):
    nextIndex = self.studentComboBox.current() + 1
    if nextIndex >= len(self.studentComboBox["values"]):
        return

    self.studentComboBox.current(nextIndex)
    runStudent(self)


def runAllStudents(self):
    self.runALlThread = threading.Thread(target=runAllStudentsHelper, name="runAllThread",
                                         args=(self.terminalScrolledText, self.studentComboBox,
                                               self.guiCheckBoxVal, self.currentProject, self.exitFlag))
    self.runALlThread.daemon = True
    self.runALlThread.start()
    return


def runAllStudentsHelper(text, studentComboBox, useGuiCheckBox, currProject, exitFlag):
    if currProject is None:
        return

    projectDir = os.getcwd() + os.path.join(f"\\generatedruns\\{currProject}\\tcl\\")

    for x in range(studentComboBox.current(), len(studentComboBox["values"])):
        if x == -1:
            continue

        if exitFlag:
            break
        # set current index
        studentComboBox.current(x)
        currStudent = studentComboBox.get()
        # get the files for each student
        currDir = projectDir + os.path.join(currStudent + ".tcl")
        currDir = currDir.replace(os.sep, "/")
        if useGuiCheckBox.get() == 1:
            cmd = f'''vsim -gui -l "" -do "{os.path.abspath(currDir)}"'''
        else:
            cmd = f'''vsim -c -l "" -do "{os.path.abspath(currDir)}"'''
        try:
            subProcess = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT, text=True, universal_newlines=True)
        except:
            print(''' Something didn't work... ¯\_(ツ)_/¯ ''')
            continue

        tempData, err = subProcess.communicate()
        clearWindowText(text)
        for line in tempData.split("\n"):
            text.configure(state='normal')
            text.insert(END, line + "\n")

        text.insert(END, f"Results for {currStudent}\n")
        text.configure(state='disabled')
        text.yview(END)
        time.sleep(1)

    # kill thread
    sys.exit()


def stopRunning(self):
    exitFlag = True
