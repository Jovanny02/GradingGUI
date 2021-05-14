import sys
import threading
import operator
from tkinter import filedialog, END
from zip_function import *
import subprocess
from subprocess import DEVNULL, PIPE, Popen, STDOUT
from sim_function import compile_modelsim

import os


def generateRun(self):
    # Get variables from app
    self.isGenerating = True
    selectedTCL = self.tclVar.get()
    selectedStudentList = self.studentListVar.get()
    chosenZip = self.zipVar.get()
    chosenTBs = self.tbListBox.curselection()
    generationName = self.generationEntry.get().replace(" ", "")

    # Error checking
    if selectedTCL == "" or selectedStudentList == "" or chosenZip == "" or generationName == "" or len(chosenTBs) == 0:
        self.setIsGenerating(False)
        self.errorLabel['text'] = "Please Select All Fields"
        self.errorLabel['fg'] = "red"
        return

    tclPath = os.getcwd() + os.path.join(f"\\grading_projects\\{generationName}\\tcl")
    submissionsPath = os.getcwd() + os.path.join(f'''\\grading_projects\\{generationName}\\submissions''')
    modelsimPath = os.getcwd() + os.path.join(f'''\\grading_projects\\{generationName}\\modelsim''')
    resultspath = os.getcwd() + os.path.join(f'''\\grading_projects\\{generationName}\\results''')

    # Create Directory For Run
    if not os.path.exists(os.getcwd() + os.path.join(f"\\grading_projects\\{generationName}")):
        os.makedirs(os.getcwd() + os.path.join(f"\\grading_projects\\{generationName}"))
        os.makedirs(modelsimPath)
        os.makedirs(tclPath)
        os.makedirs(submissionsPath)
        os.makedirs(resultspath)
    else:
        self.setIsGenerating(False)
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
    loadProjects(self)

    self.setIsGenerating(False)
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


def loadProjects(self):
    root = (os.getcwd() + os.path.join(f"\\grading_projects")).replace(os.sep, "/")
    runs = [item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))]
    self.projectComboBox['values'] = runs


def deleteProject(self):
    if self.projectComboBox.get() == "'Choose Grading Project'":
        return

    shutil.rmtree(os.getcwd() + os.path.join(f"\\grading_projects\\{self.projectComboBox.get()}"))
    loadProjects(self)
    self.projectComboBox.set('Choose Grading Project')


def loadStudents(self):
    if self.projectComboBox.get() == 'Choose Grading Project':
        return

    self.studentComboBox.delete(0, self.tbListBox.size())
    studentsDir = os.getcwd() + os.path.join(f"\\grading_projects\\{self.projectComboBox.get()}\\tcl")
    students = []
    try:
        for file in os.listdir(studentsDir):
            if file.endswith(".tcl"):
                students.append(file[0: len(file) - 4])
    except:
        print("NO TESTBENCH FILES!")

    self.windowStatusVar.set(f'''Loaded {self.projectComboBox.get()}''')
    self.currentProject = self.projectComboBox.get()
    self.studentComboBox['values'] = students
    self.studentComboBox.set('Choose Student')
    return


def checkOutputLoop(text, process, student, resultsDirectory, statusLabel, getTimer, setRunning, setExitFlag, parseOut):
    clearWindowText(text)
    tempData, err = process.communicate()

    # parse output if needed
    if parseOut.get() == 1:
        index = tempData.rfind("STARTING SIMULATION")
        if index != -1:
            tempData = tempData[index:len(tempData)]

    # write data to terminal
    text.configure(state='normal')
    text.insert(END, tempData + "\n")
    text.insert(END, f"Results for {student}\n")
    text.configure(state='disabled')
    # write data to results file
    try:
        f = open(resultsDirectory + student + ".txt", "w", encoding='utf-8')
        f.write(tempData)
        f.close()
    except:
        print("Could not write results to file")

    process.terminate()
    text.yview(END)
    statusLabel.set(f'''Completed {student}. Time Elapsed: {getTimerText(getTimer(), operator.floordiv) }:{getTimerText(getTimer(), operator.mod)}''')
    setRunning(False)
    setExitFlag(False)
    sys.exit()


def runStudent(self):
    if self.studentComboBox.get() == 'Choose Student' or self.isRunning:
        return
    # if a lock on the project exists, remove it
    deleteModelsimLock(os.getcwd() + os.path.join(f"\\grading_projects\\{self.projectComboBox.get()}"))

    resultsDir = os.getcwd() + os.path.join(f"\\grading_projects\\{self.projectComboBox.get()}\\results\\")
    studentDir = os.getcwd() + os.path.join(f"\\grading_projects\\{self.projectComboBox.get()}\\tcl\\")
    studentDir += os.path.join(self.studentComboBox.get() + ".tcl")
    studentDir = studentDir.replace(os.sep, "/")
    if self.guiCheckBoxVal.get() == 1:
        cmd = f'''vsim -gui -l "" -do "{os.path.abspath(studentDir)}"'''
    elif self.guiCheckBoxVal.get() == 0:
        cmd = f'''vsim -c -l "" -do "{os.path.abspath(studentDir)}"'''
    else:
        return

    try:
        self.assignSubprocess(cmd)
        clearWindowText(self.terminalScrolledText)
        self.clearTimer()
        self.setIsRunning(True)
    except:
        print(''' Something didn't work... ¯\_(ツ)_/¯ ''')
        self.setIsRunning(False)


    self.currentStudent = self.studentComboBox.get()
    self.runThread = threading.Thread(target=checkOutputLoop, name="windowThread",
                                      args=(self.terminalScrolledText, self.subProcess, self.currentStudent, resultsDir,
                                            self.windowStatusVar, self.getTimer, self.setIsRunning, self.setExitFlag,
                                            self.parseOutputVar ))
    self.runThread.daemon = True
    self.runThread.start()
    return


def runNextStudent(self):
    nextIndex = self.studentComboBox.current() + 1
    if nextIndex >= len(self.studentComboBox["values"]) or nextIndex < 0:
        return
    if self.isRunning:
        return

    self.studentComboBox.current(nextIndex)
    runStudent(self)


def runAllStudents(self):
    # dont run if another process is running
    if self.isRunning:
        return

    self.clearSubprocess()
    self.runALlThread = threading.Thread(target=runAllStudentsHelper, name="runAllThread",
                                         args=(self.terminalScrolledText, self.studentComboBox,
                                               self.guiCheckBoxVal, self.currentProject, self.getExitFlag,
                                               self.setExitFlag, self.assignSubprocess, self.setCurrStudent,
                                               self.clearTimer, self.getTimer, self.setIsRunning, self.windowStatusVar,
                                               self.parseOutputVar))
    self.runALlThread.daemon = True
    self.runALlThread.start()
    return


def runAllStudentsHelper(text, studentComboBox, useGuiCheckBox, currProject, getExitFlag, setExitFlag,
                         subProcess, setCurrStudent, clearTimer, getTimer, setIsRunning, windowStatus, parseOut):
    if currProject is None:
        return

    deleteModelsimLock(os.getcwd() + os.path.join(f"\\grading_projects\\{currProject}"))
    setIsRunning(True)
    clearTimer()
    resultsDir = os.getcwd() + os.path.join(f"\\grading_projects\\{currProject}\\results\\")
    projectDir = os.getcwd() + os.path.join(f"\\grading_projects\\{currProject}\\tcl\\")
    clearWindowText(text)

    for x in range(studentComboBox.current(), len(studentComboBox["values"])):
        if x == -1:
            continue

        if getExitFlag():
            break
        clearTimer()
        # set current index
        studentComboBox.current(x)
        setCurrStudent(studentComboBox.get())
        currStudent = studentComboBox.get()
        # get the files for each student
        currDir = projectDir + os.path.join(currStudent + ".tcl")
        currDir = currDir.replace(os.sep, "/")
        if useGuiCheckBox.get() == 1:
            cmd = f'''vsim -gui -l "" -do "{os.path.abspath(currDir)}"'''
        else:
            cmd = f'''vsim -c -l "" -do "{os.path.abspath(currDir)}"'''
        try:
            process = subProcess(cmd)
        except:
            print(''' Something didn't work... ¯\_(ツ)_/¯ ''')
            continue

        tempData, err = process.communicate()

        # parse output if needed
        if parseOut.get() == 1:
            index = tempData.rfind("STARTING SIMULATION")
            if index != -1:
                tempData = tempData[index:len(tempData)]

        text.configure(state='normal')
        text.insert(END, tempData + "\n")
        text.insert(END, f"Results for {currStudent}\n")
        text.configure(state='disabled')

        # write to file
        try:
            f = open(resultsDir + currStudent + ".txt", "w", encoding='utf-8')
            f.write(tempData)
            f.close()
        except:
            print("Could not write results to file")

        text.yview(END)

    # kill thread
    windowStatus.set(f'''Completed {studentComboBox.get()}. Time Elapsed: {getTimerText(getTimer(), operator.floordiv) }:{getTimerText(getTimer(), operator.mod)}''')
    setExitFlag(False)
    setIsRunning(False)
    sys.exit()


def stopRunning(self):
    if self.subProcess is None:
        return
    self.subProcess.terminate()
    self.exitFlag = True
    self.setIsRunning(False)

def deleteModelsimLock(modelsimProjectDir):
    path = os.path.abspath(modelsimProjectDir + os.path.join("\\modelsim\\work\\_lock"))
    try:
        if os.path.exists(path):
            os.remove(path)
    except:
        print("Couldn't Delete _lock file")


def getTimerText(timerVal, op):
    value = op(timerVal, 60)
    if value < 10:
        return "0" + str(value)

    return str(value)



