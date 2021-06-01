from tkinter import filedialog
from pathlib import Path
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
                self.tclUploadVar.set("")
                return
            tf = open(tf)  # or tf = open(tf, 'r')

            # copy file over to tcl locations
            shutil.copy(tf.name, os.getcwd() + os.path.join("\\lab_tcl"))
            tf.close()
    except:
        self.tclStatusLabel.configure(style="Red.TLabel")
        self.tclUploadVar.set("An Error Occurred")
        return

    if len(files) == 1:
        # Generate an animation for the result
        self.tclStatusLabel.configure(style="Green.TLabel")
        self.tclUploadVar.set("Copied " + files[0][files[0].rfind("/") + 1:len(files[0])])
    elif len(files) > 1:
        self.tclStatusLabel.configure(style="Green.TLabel")
        self.tclUploadVar.set("Copied " + str(len(files)) + " Files")
    elif len(files) == 0:
        self.tclStatusLabel.configure(style="TLabel")
        self.tclUploadVar.set("")

def uploadVHDFile(self):
    files = filedialog.askopenfilenames(
        initialdir=os.getcwd(),
        title="Choose VHD files",
        filetypes=(("VHD Files", "*.vhd"),)
    )
    try:
        for tf in files:
            if tf == "":
                self.tbUploadVar.set("")
                return
            tf = open(tf)  # or tf = open(tf, 'r')

            filename = tf.name[tf.name.rfind("/") + 1:len(tf.name)]
            # copy file over to tcl locations
            if filename.endswith("true_testbench.vhd"):
                shutil.copy(tf.name, os.getcwd() + os.path.join("\\testbenches"))
            else:
                shutil.copy(tf.name, os.getcwd() + os.path.join(f'''\\testbenches\\{filename[0:len(filename)-4]}_true_testbench.vhd''' ))

            tf.close()
    except:
        self.tbUploadLabel.configure(style="Red.TLabel")
        self.tbUploadVar.set("An Error Occurred")
        return

    if len(files) == 1:
        # Generate an animation for the result
        self.tbUploadLabel.configure(style="Green.TLabel")
        self.tbUploadVar.set("Copied " + files[0][files[0].rfind("/") + 1:len(files[0])])

    elif len(files) > 1:
        self.tbUploadLabel.configure(style="Green.TLabel")
        self.tbUploadVar.set("Copied " + str(len(files)) + " Files")
    elif len(files) == 0:
        self.tbUploadLabel.configure(style="TLabel")
        self.tbUploadVar.set("")


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
        self.studentListLabel.configure(style="Red.TLabel")
        self.textUploadVar.set("An Error Occurred")
        return

    if len(files) == 1:
        # Generate an animation for the result
        self.studentListLabel.configure(style="Green.TLabel")
        self.textUploadVar.set("Copied " + files[0][files[0].rfind("/") + 1:len(files[0])])
    elif len(files) > 1:
        self.studentListLabel.configure(style="Green.TLabel")
        self.textUploadVar.set("Copied " + str(len(files)) + " Files")
    elif len(files) == 0:
        self.studentListLabel.configure(style="TLabel")
        self.textUploadVar.set("")


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

def chooseVHDFiles(self):
    files = filedialog.askopenfilenames(
        initialdir=os.getcwd() + '\\testbenches\\',
        title="Choose VHD files",
        filetypes=(("VHD Files", "*.vhd"),)
    )
    labelText = ""
    self.selectedTestbenches = []
    try:
        for tf in files:
            if tf == "":
                self.tbUploadVar.set("")
                return
            tf = open(tf)  # or tf = open(tf, 'r')
            self.selectedTestbenches.append(tf.name)
            labelText += tf.name[tf.name.rfind("/") + 1:len(tf.name)] + '\n'
            tf.close()
    except:
        self.tbSelectLabel['text'] = 'An Error Occured'
        return

    self.tbSelectLabel['text'] = labelText
