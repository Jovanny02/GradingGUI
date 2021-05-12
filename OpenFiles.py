from tkinter import filedialog
from pathlib import Path
from helpers import refreshTBs
import os
import shutil


def uploadTCLFile(self):
    tf = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Choose TCL file",
        filetypes=(("TCL Files", "*.tcl"),)
    )
    try:
        if tf == "":
            self.tclUploadVar.set("")
            return
        tf = open(tf)  # or tf = open(tf, 'r')

        # copy file over to tcl locations
        shutil.copy(tf.name, os.getcwd() + os.path.join("\\lab_tcl"))

        # Generate an animation for the result
        self.tclUploadVar.set("Uploaded " + tf.name[tf.name.rfind("/") + 1:len(tf.name)])
        self.tclStatusLabel['fg'] = "#006400"

        tf.close()
    except:
        tf.close()
        self.tclUploadVar.set("An Error Occurred")
        self.tclStatusLabel['fg'] = "red"


def uploadVHDFile(self):
    tf = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Choose VHD file",
        filetypes=(("VHD Files", "*.vhd"),)
    )
    try:
        if tf == "":
            self.tbUploadVar.set("")
            return
        tf = open(tf)  # or tf = open(tf, 'r')

        # copy file over to tcl locations
        shutil.copy(tf.name, os.getcwd() + os.path.join("\\testbenchces"))

        # Generate an animation for the result
        self.tbUploadVar.set("Uploaded " + tf.name[tf.name.rfind("/") + 1:len(tf.name)])
        self.tbUploadLabel['fg'] = "#006400"
        tf.close()
    except:
        tf.close()
        self.tbUploadVar.set("An Error Occurred")
        self.tbUploadLabel['fg'] = "red"

    refreshTBs(self)


def uploadTextFile(self):
    tf = filedialog.askopenfilename(
        initialdir=os.getcwd(),
        title="Choose Text file",
        filetypes=(("Text Files", "*.txt"),)
    )
    try:
        if tf == "":
            self.textUploadVar.set("")
            return
        tf = open(tf)  # or tf = open(tf, 'r')

        # copy file over to tcl locations
        shutil.copy(tf.name, os.getcwd() + os.path.join("\\studentlists"))

        # Generate an animation for the result
        self.textUploadVar.set("Uploaded " + tf.name[tf.name.rfind("/") + 1:len(tf.name)])
        self.studentListLabel['fg'] = "#006400"
        tf.close()
    except:
        tf.close()
        self.textUploadVar.set("An Error Occurred")
        self.studentListLabel['fg'] = "red"


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
