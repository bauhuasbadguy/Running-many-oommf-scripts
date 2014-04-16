#runningmultipleoommffilesonhpc

import subprocess
import os
import sys
sys.path.append('/panfs/panasas01.panfs.cluster/ppxsb3/oommfsimulationfiles/500nmsquare/unstrained/problems')
#sys.path.append('F:/runningoommfonHPC')
import oommfonhpc as omf
x = omf.oommfsettings()
ks = 0
x.setparams('Ks', ks)
for amp in range(10,250,10):
    x.setshell('F:/runningoommfonHPC/sample.sh')
    x.setparams('Ks', ks)
    x.setparams('Amp', amp)
    targetdirectory = '/panfs/panasas01.panfs.cluster/ppxsb3/oommfsimulationfiles/500nmsquare/unstrained'
    targetdirectory = targetdirectory + '/amplitude' + repr(amp) + '/square_pulse_MCA_Ks_' + repr(ks)
    targetdirectory = targetdirectory + 'KJ_amp_' +repr(amp)
    x.setparams('outdir', targetdirectory)
    x.setshell('F:/runningoommfonHPC/sample.sh')
    x.settclpath('C:/Tcl/bin/tclsh85.exe')
    x.setoommfpath('C:/oommf/oommf.tcl')
    x.setmifpath('F:/oommf programs/FeGa_FluxClosed_circle_sc_-10e3.mif')
    q = x.check(1)
    command_line = x.write_settings(q)
    x.run_command(command_line)
    x.clearoommf()
    
