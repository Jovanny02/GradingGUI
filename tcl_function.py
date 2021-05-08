#!/usr/bin/env python
__author__ = "Keeth Smith"

import os


def tcl_function(tclFile, project_mpf, resultList, tclPath):

    with open(os.path.abspath(tclFile), "r") as f:
        tclScript = f.read()
    

    basetcl = 'project open {' + f'{os.path.abspath(project_mpf)}' + '}\n\n'

    basetcl += '''onElabError {resume}\nonerror {resume}\n\n'''
    
    basetcl += '''proc currStudent {lines student} {
            set retry 1
            while {$retry == 1} {
                set retry 0
                flush stdout
                set in [gets stdin]
                if {$in == "q"} {
                    set result [string map -nocase {"\} \{" "\}\\n\{" "\} " "\}\\n" ".vhd " ".vhd\\n"} [project filenames]] 
                    set lines [split $result "\\n"]

                    foreach x $lines {
                        if {[string match *true_testbench.vhd* $x] == 1} {
                            set z 1
                        } else {
                            eval project removefile [string map -nocase { "\{\{" "\{" "\}\}" "\}" } $x]
                        }
                    } 
                    quit -f
                    }
                if {$in == "n"} {
                    return
                    }
                    vdel -all
                    vlib work
                for {set i 1} {$i<=2} {incr i} {
                    puts "\n--------------COMPILE ATTEMPT: $i--------------\n"
                    foreach x $lines {
                    try {
                        eval $x
                             
                        } on error {msg} {
                            puts ""
                        }
                        
                    } 
                    if {$i == 2} {
                        puts "COMPILE PASSED SUCCESSFULLY\n\n--------------STARTING SIMULATION--------------\n"
                    }
                }
                   
'''
    basetcl += tclScript + '''\n}\n}\n'''

    for x in resultList:
        currtcl = basetcl
        currtcl += ''' 
quietly set result [string map -nocase {"\} \{" "\}\\n\{" "\} " "\}\\n" ".vhd " ".vhd\\n"} [project filenames]] 
quietly set lines [split $result "\\n"]

foreach x $lines {
   if {[string match *true_testbench.vhd* $x] == 1} {
      set z 1
   } else {
    #   puts "REMOVED"
      eval project removefile $x
   }
} 

'''
        currtcl += x[0]
        currtcl += '''
quietly set ret [project compileall -n]
quietly set result [string map {explicit "quiet -suppress 1195,1194" \\\ / } $ret]
quietly set lines [split $result "\\n"]'''
        currtcl += f'''\ncurrStudent $lines {x[1]};\n\n'''
        currtcl += 'exit'

        f = open(tclPath + "/" + x[1] + ".tcl", "w", encoding='utf-8')
        f.write(currtcl)
        f.close()
    # tcl += 'exit'

    return
