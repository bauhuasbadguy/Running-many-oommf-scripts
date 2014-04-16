Running-many-oommf-scripts
==========================

Python module and example shell file for running many oommf files at the same time

Created by Stuart Bowe and Duncan Parkes

###Description

This is a python script that defines the class oommfsettings in order to create a command line which will run a oommf simulation using a pre-existing mif file. The intention is that people will use the script when they have to run many oommf simulations varying some parameter each time.

At the moment the script works fine when used to work windows files but for some reason oommf is hanging untill timeout when run on the HPC. This is a problem which is still under investigation but use extreme caution when using this class in conjunction with unix systems.

###Functions

####Functions for changing the settings of boxsi

*setparams:- This sets a parameter which will be used by the script. It takes a string (parameter name) and then either a string or a value corresponding to the value of that parameter.

*settclpath:- This takes in a string telling oommf where to find the tcl shell file. It checks to see if tcl shell is in the location the user specifies and if it can't find a file there will return an error.

*setoommfpath:- This takes in a string telling the command line where to find oommf.tcl. If python can't find oommf.tcl there it will not alter from the default setting.

*setmifpath:- This takes in a string telling the command line where to find the .mif file you want to run. If python can't find the mif file there it will not alter from the default setting.

*setexitondone:- Takes in a boolean True/False value and will not close boxsi on completion of the script if the input to this function is false.

*setrestart:- Takes in a value for the restart paramter. 0 means start from the beginning, 1 means create a restart file and 2 means use a restart file if you find one.

*setpause:- Asks if the user wants to pause on startup, 0 for no 1 for yes.

*setthreads:- Set the number of threads to use. The default is 4. You normally have access to 2 threads for every core.

*setnice:- Takes in a boolean input and if it is set to 1 it will drop scheduling priority on startup.

*setkilltags:- Not sure what kill tags are but this command takes one in as a string and appends it to the list.

*setnumnodes:- Takes in a list describing which nodes to use

*setshell:- This takes in a string telling the command line where to find the shell file. If python can't find the shell file there it will not alter from the default setting.

*tkon:- takes in a 0 or a 1. If 0 tk will be on if 1 tk will be off.

####Functions for writing sending the commands

*result = x.check(printornot):- checks the oommfsettings class object x and prints out a report on any grevious errors it finds. Will also output a value which can be used by the write_settings function. If printornot is set to 1 the function will not print out the error report.

*commandline=x.write\_settings(testresult):- Creates a line that can be run in boxsi. This line can be imput into run\_commandwindows but run\_command takes it raw.

*run\_commandwindows(commandline):- Sends the command line to be run using windows command prompt

*x.qsub\_run\_command(runs the command on the HPC. THIS IS STILL BEEN WORKED ON USE WITH EXTREME CAUTION.


###Future plans

*Make the thing work with the HPC as originaly intended

*Make it into a module

*understand + fix to work propely killtags and numanodes
