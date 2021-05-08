#!/usr/bin/env python
__author__ = "Keeth Smith"

import os
import sys
import glob
import subprocess
from pathlib    import Path
from subprocess import DEVNULL

from tcl_function import tcl_function


def compile_modelsim(studentFile, lab_dir, tclFile, project_mpf, gui, tclPath):

    cmd = ""
    fileList = ""
    studentUserList = []

    with open(studentFile, "r") as f:
        studentList = f.read().splitlines()
        studentList = filter(None, studentList)
        for x in studentList:
            list_name = x.lower().split()
            if (len(list_name) == 3):
                studentUserList.append(list_name[1] + list_name[2] + list_name[0])

            else:
                studentUserList.append(list_name[1] + list_name[0])

    resultList=[]
    # print("\nStudents Found:")
    for x in studentUserList:
        try:
            realStudent = glob.glob(lab_dir+"/*"+x+"*")[0].split('\\''')[-1]
            # print(realStudent)
            dirPath = os.path.join(lab_dir, realStudent)
            result = list(Path(dirPath).glob("*.[vV][hH][dD]"))
            fileList = ""
            for y in result:
                fileList += 'project addfile {' + f'{os.path.abspath(y)}'.replace(os.sep, '/') + '}\n'
                
            resultList.append([fileList, realStudent])
        except:
            pass

    print()

    tcl_function(tclFile, project_mpf, resultList, tclPath)
    #
    # if gui:
    #     cmd  = f'''vsim -gui -l "" -do "{os.path.abspath(tclOutFile)}"'''
    # else:
    #     cmd  = f'''vsim -c -l "" -do "{os.path.abspath(tclOutFile)}"'''
    #
    #
    # try:
    #     subprocess.run(cmd, shell=True, stdout=True, stderr=DEVNULL)
    # except:
    #     print(''' Something didn't work... ¯\_(ツ)_/¯ ''')


