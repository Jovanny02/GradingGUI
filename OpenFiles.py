from tkinter import filedialog
from pathlib import Path
from helpers import refreshTBs
import os
import shutil


def uploadTCLFile(self):
    files = filedialog.askopenfilenames(
        initialdir=os.getcwd(),
        title="Choose TCL files",
        filetypes=(("TCL Files", "*.tcl"),)
    )
    try:
        for tf in files:
            if tf == "":
                self.textUploadVar.set("")
                return
            tf = open(tf)  # or tf = open(tf, 'r')

            # copy file over to tcl locations
            shutil.copy(tf.name, os.getcwd() + os.path.join("\\lab_tcl"))
            tf.close()
    except:
        self.textUploadVar.set("An Error Occurred")
        self.studentListLabel['fg'] = "red"

    if len(files) == 1:
        # Generate an animation for the result
        self.textUploadVar.set("Uploaded " + files[0].name[files[0].name.rfind("/") + 1:len(files[0].name)])
        self.studentListLabel['fg'] = "#006400"
    elif len(files) > 1:
        self.textUploadVar.set("Uploaded " + str(len(files)) + " Files")
        self.studentListLabel['fg'] = "#006400"


def uploadVHDFile(self):
    files = filedialog.askopenfilenames(
        initialdir=os.getcwd(),
        title="Choose VHD files",
        filetypes=(("VHD Files", "*.vhd"),)
    )
    try:
        for tf in files:
            if tf == "":
                self.textUploadVar.set("")
                return
            tf = open(tf)  # or tf = open(tf, 'r')

            # copy file over to tcl locations
            shutil.copy(tf.name, os.getcwd() + os.path.join("\\testbenchces"))
            tf.close()
    except:
        self.textUploadVar.set("An Error Occurred")
        self.studentListLabel['fg'] = "red"

    if len(files) == 1:
        # Generate an animation for the result
        self.textUploadVar.set("Uploaded " + files[0].name[files[0].name.rfind("/") + 1:len(files[0].name)])
        self.studentListLabel['fg'] = "#006400"
    elif len(files) > 1:
        self.textUploadVar.set("Uploaded " + str(len(files)) + " Files")
        self.studentListLabel['fg'] = "#006400"

    refreshTBs(self)


def uploadTextFile(self):
    files = filedialog.askopenfilenames(
        initialdir=os.getcwd(),
        title="Choose Text files",
        filetypes=(("Text Files", "*.txt"),)
    )
    try:
        for tf in files:
            if tf == "":
                self.textUploadVar.set("")
                return
            tf = open(tf)  # or tf = open(tf, 'r')

            # copy file over to tcl locations
            shutil.copy(tf.name, os.getcwd() + os.path.join("\\studentlists"))
            tf.close()
    except:
        self.textUploadVar.set("An Error Occurred")
        self.studentListLabel['fg'] = "red"

    if len(files) == 1:
        # Generate an animation for the result
        self.textUploadVar.set("Uploaded " + files[0].name[files[0].name.rfind("/") + 1:len(files[0].name)])
        self.studentListLabel['fg'] = "#006400"
    elif len(files) > 1:
        self.textUploadVar.set("Uploaded " + str(len(files)) + " Files")
        self.studentListLabel['fg'] = "#006400"

def uploadZipFile(self):
    tf = filedialog.askopenfilename(
        initialdir=str(Path.home() / "Downloads"),
        title="Choose Zip file",
        filetypes=(("Zip Files", "*.zip"),)
    )
    if tf == "":
        self.zipVar.set("")
        self.zipLabel['text'] = ""
        return
    tf = open(tf)  # or tf = open(tf, 'r')

    self.zipVar.set(tf.name)
    self.zipLabel['text'] = tf.name[tf.name.rfind("/") + 1:len(tf.name)]
    tf.close()


def openTCLFile(self):
    tf = filedialog.askopenfilename(
        initialdir=os.getcwd() + os.path.join("\\lab_tcl"),
        title="Choose TCL file",
        filetypes=(("TCL Files", "*.tcl"),)
    )
    if tf == "":
        self.tclVar.set("")
        self.chooseTclLabel['text'] = ""
        return

    tf = open(tf)

    self.tclVar.set(tf.name)
    self.chooseTclLabel['text'] = tf.name[tf.name.rfind("/") + 1:len(tf.name)]

    tf.close()


def openStudentListFile(self):
    tf = filedialog.askopenfilename(
        initialdir=os.getcwd() + os.path.join("\\studentlists"),
        title="Choose Student List file",
        filetypes=(("Text Files", "*.txt"),)
    )
    if tf == "":
        self.studentListVar.set("")
        self.chooseStudentsLabel['text'] = ""
        return

    tf = open(tf)  # or tf = open(tf, 'r')

    self.studentListVar.set(tf.name)
    self.chooseStudentsLabel['text'] = tf.name[tf.name.rfind("/") + 1:len(tf.name)]
    tf.close()
