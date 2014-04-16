#Runoommfonhpc
#Class designed to take in a series of settings from a user in order to send a series of commands to a shell
#script on the HPC in order to run oommf programs. The eventual aim is a easly used method for sending multiple,
#similar jobs to the HPC which can be adapted by different people for their own purposes
import subprocess
import os
import sys
class oommfsettings:
    miffile = 'Not set mif file'
    threadno = 4
    tclroot = 'Not set tcl root'
    oommfroot = 'Not set oommf root'
    nice = 0
    exitdone = 1
    killtags = 'Kill tags not set'
    numanodes = 'Not set numnodes'
    restart = 0
    parameters = 'No set parameters'
    parameternames = []
    parametersforhpc = 'No set parameters'
    pause = 0
    shellfile = 'No shell file set'
    tk = 1

#=======================================================================================================
#This first function checks to see if the oommf object contains enough data to run a .mif script when
#it is used to write the shell script command file. It outputs error messages in order to help the user
#with debugging. The result must also be fed into the command line writer to make it go.
#=======================================================================================================

    def check(self,printornot = 0):
        majorfaults = 0
        #This function runs through the parameters of the oommf object and makes sure it can actually run
        #if the paths to oommf, tclshell or the mif file are not set right then the function will stop
        #increment the number of major errors and complain. If you set printornot to 1 the function will
        #not print anything if no major errors are detected
        if printornot == 0:
            print '============================================================'
        if self.miffile == 'Not set mif file':
            print 'You need to set the mif file to use'
            majorfaults += 1
        elif not os.path.isfile(self.miffile):
            print 'Can\'t find mif file at ' + repr(self.miffile)

        #Check tcl root is OK
        if self.tclroot == 'Not set tcl root':
            print 'You need to set the root to the tcl file'
            majorfaults += 1
        elif not os.path.isfile(self.tclroot):
            print 'Can\'t find tclshell, make sure you\'ve used the correct tclshell root'
            majorfaults += 1

        #Check shell file is OK
        if self.shellfile == 'No shell file set':
            print 'You need to set a shell file, at the moment you can only run this code in windows'
            majorfaults += 1
        elif not os.path.isfile(self.shellfile):
            print 'Can\'t find shell file at ' + repr(self.shellfile)
            majorfaults += 1

        #Check oommf file is OK
        if self.oommfroot == 'Not set oommf root':
            print 'You need to set the root to oommf.tcl'
            majorfaults += 1
        elif not os.path.isfile(self.oommfroot):
            print 'Can\'t find oommf.tcl, make sure you\'ve used the correct oommf.tcl root'
            majorfaults += 1

        #underline the major faults section of the readout
        if printornot == 0:
            print '============================================================'
            
        #Tells the user if the parameters have not been set manually
        if self.parameters == 'No set parameters':
            if printornot == 0:
                print 'WARNING:No parameters have been set, using defaults in script'
        else:
            if printornot == 0:
                print 'You have set:'
                for i in self.parameternames:
                    print i
                print 'as your parameters'

        #Underline the parameters section of the script
        if printornot == 0:
            print '============================================================'
        #Telling user which minor parameters are not manually set
        if printornot == 0:
            if self.exitdone == 1:
                print 'Exitdone not set manually, reverting to default (on)'
            if self.killtags == 'Kill tags not set':
                print 'Kill tags not set manually, reverting to defaults'
            if self.nice == 0:
                print 'Nice not set manually, reverting to 0'
            if self.pause == 0:
                print 'Pause not set manually, reverting to 0'
            if self.restart == 0:
                print 'Restart not set manually, reverting to 0'
            if self.threadno == 4:
                print 'Number of threads not set manually, reverting to default'
            if self.numanodes == 'Not set numnodes':
                print 'Nodes not set manually, reverting to default'

        #tell the user if there is a serious flaw in their program
        #Underline the light warnings
        if printornot == 0:
            print '============================================================'
        
            if majorfaults == 0:
                print 'No major faults detected, you may well be good to go'
            elif majorfaults > 1:
                print 'WARNING:There were ' + repr(majorfaults) + ' major faults, this code will not work until these faults are addressed'
            elif majorfaults == 1:
                print 'WARNING:There was a major fault, this code will not run until this fault is addressed'

            print '============================================================'
        return majorfaults


#=================================================================================================
#The next section of code is a series of functions designed to prepare and sanitize data to be
#used in the command line.
#=================================================================================================

    def setparams(self,parameter,value):
        if type(value) == str:
            if self.parameters == 'No set parameters':
                self.parameters = parameter
                self.parameters = self.parameters + ' ' + value
                self.parametersforhpc = parameter + '="'
                self.parametersforhpc = self.parametersforhpc + value + '"'
                self.parameternames.append(parameter)
            else:
                self.parameters = self.parameters + ' ' + parameter
                self.parameters = self.parameters + ' ' + value
                self.parametersforhpc = self.parametersforhpc + ', ' + parameter + '="'
                self.parametersforhpc = self.parametersforhpc + value + '"'
                self.parameternames.append(parameter)

        elif type(value) == float or type(value) == int:
            if self.parameters == 'No set parameters':
                self.parameters = parameter
                self.parameters = self.parameters + ' ' + repr(value)
                self.parametersforhpc = parameter + '="'
                self.parametersforhpc = self.parametersforhpc + repr(value) + '"'
                self.parameternames.append(parameter)
            else:
                self.parameters = self.parameters + ' ' + parameter
                self.parameters = self.parameters + ' ' + repr(value)
                self.parametersforhpc = self.parametersforhpc + ', ' + parameter + '="'
                self.parametersforhpc = self.parametersforhpc + repr(value) + '"'
                self.parameternames.append(parameter)

        else:
            print 'ERROR:Value is not a string, float or int'
    #sets the parameters, at the moment parameters have to be programmed in individually
    #I hope to improve on this in the future.

            
    def settclpath(self,tclroot):
        if os.path.isfile(tclroot):
            self.tclroot = tclroot
        else:
            print 'Can\'t find tclshell at that address, check the path is right'
    #sets the location of tclshell and tells the user if the program can't find it.


    def setoommfpath(self,oommfpath):
        if os.path.isfile(oommfpath):
            self.oommfroot = oommfpath
        else:
            print 'Can\'t find oommf.tcl at that address, check the path is right'
    #sets the location of oommf and tells the user if the program can't find it.

    
    def setmifpath(self,mifpath):
        if os.path.isfile(mifpath):
            self.miffile = mifpath
        else:
            print 'Can\'t find the mif file at that address, check the path is right'
    #sets the mif file and tells the user if the program can't find it


    def setexitondone(self,yn):
        if yn == False:
            self.exitdone == 0
    #takes in a boolean data type to say if boxsi should shut down once it has finished the
    #problem, the default is yes.

            
    def setrestart(self,restartno):
        self.restart = restartno
    #takes in a number for the restart condition, default is 0.


    def setpause(self,pause):
        if pause:
            self.pause = 1
    #Takes in a boolean data type and turns the pause on and off accordingly.


    def setthreads(self,threadno):
        self.threadno = threadno
    #takes in the number of threads the user wants to use and then uses that
    #many threads.


    def setnice(self,niceornot):
        if niceornot:
            self.nice = 1
    #takes in a boolean data thread if true it sets nice to 1 saying that on
    #startup boxsi will drop its scheduling priority


    def setkilltags(self,killtags):
        self.tags = ''
        for tags in killtags:
            self.tags = self.tags + tag + ' ' 

    #I'm not exactly sure what kill tags but the boxsi help describes them as destinations
    #so I assume that boxsi expects a list of paths here. In order to accomodate this the
    #function takes in a list of strings and turns them into one long string.

    
    def setnumnodes(self,nonums):
        self.numanodes = '"'
        for n in numanodes:
            self.numanodes = self.numanodes + repr(n) + ', '
        self.numanodes = self.numanodes + '"'

    def setshell(self,shellname):
        if os.path.isfile(shellname):
            self.shellfile = shellname
        else:
            print 'Can\'t find shell file at that address, check the path is right'
    def tkon(self,yn):
        if not yn:
            self.tk = 0
        else:
            self.tk = 1

#=================================================================================================
#The next section of code contains functions to build and execute the command lines to run boxsii.
#It is STRONGLY recomended that you use the result of the check command as the testresult for
#write_settings since it will help with your debugging.
#=================================================================================================

#this function writes all the properties of the oommf file into a string which is used to run boxsi
    def write_settings(self, testresult):
        if testresult == 0 or testresult == 1:
            command_line = self.tclroot
            command_line = command_line + ' ' + self.oommfroot + ' boxsi '
            if not self.tk == 1:
                command_line = command_line + '-tk 0 '
            if not self.exitdone == 1:
                command_line = command_line + '-exitondone ' + repr(self.exitdone) + ' '
            if not self.killtags == 'Kill tags not set':
                command_line = command_line + '-kill tags ' + self.killtags + ' '
            if not self.nice == 0:
                command_line = command_line + '-nice ' + repr(self.nice) + ' '
            if not self.parameters == 'No set parameters':
                command_line = command_line + '-parameters "' + self.parameters + '" '
            if not self.pause == 0:
                command_line = command_line + '-pause ' + repr(self.pause) + ' '
            if not self.restart == 0:
                command_line = command_line + '-restart ' + repr(self.restart) + ' '
            if not self.threadno == 4:
                command_line = command_line + '-threads ' + repr(self.threadno) + ' '
            if not self.numanodes == 'Not set numnodes':
                command_line = command_line + '-numanodes "' + self.numanodes + ' '
                

            command_line = command_line + self.miffile

            return command_line
        else:
            print 'Test failed, can\'t write line'

    #This command resets all the properties of the oommf object
    def clearoommf(self):
        self.miffile = 'Not set mif file'
        self.threadno = 4
        self.tclroot = 'Not set tcl root'
        self.oommfroot = 'Not set oommf root'
        self.nice = 0
        self.exitdone = 1
        self.killtags = 'Kill tags not set'
        self.numanodes = 'Not set numnodes'
        self.restart = 0
        self.parameters = 'No set parameters'
        self.parameternames = []
        self.pause = 0
        self.parametersforhpc = 'No set parameters'
        self.shellfile = 'No shell file set'
        self.tk = 1

    def qsub_run_command(self,command_line):
        run_line = 'qsub -v command_to_run=\"%s\" %s' % (command_line, self.shellfile)
	#qsub_run = 'runmanyommffileonhpc.sh'
        #print run_line
        #This line sends the varable qsub_command to bash
        subprocess.check_call(run_line, shell = True)

    def run_commandwindows(self, command_line):
        print command_line
        subprocess.check_call(command_line, shell = True)


