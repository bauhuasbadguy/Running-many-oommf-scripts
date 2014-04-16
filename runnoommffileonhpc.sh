#!/bin/bash
# This is an example submit script for the hello world program.
# OPTIONS FOR PBS PRO ==============================================================
#PBS -l walltime=24:00:00
# This specifies the job should run for no longer than 24 hours
#PBS -l select=1:ncpus=8:mem=2048mb
# This specifies the job needs 1 'chunk', with 1 CPU core, and 2048 MB of RAM (memory).
#PBS -j oe
# This joins up the error and output into one file rather that making two files
##PBS -o $working_folder/$PBS_JOBID-oommf_log
# This send your output to the file "hello_output" rather than the standard filename
# OPTIONS FOR PBS PRO ==============================================================
#PBS -P HPCA-000987-EFR
#PBS -M ppxsb3@nottingham.ac.uk
#PBS -m abe

# Here we just use Unix command to run our program
echo "Running on `hostname`"
# edit above line to the correct working directory for your job
echo "Working directory is $working_folder"

tclroot="/panfs/panasas01.panfs.cluster/ppxsb3/tcl/bin/tclsh8.5"
oommfroot="/panfs/panasas01.panfs.cluster/ppxsb3/oommf/oommf-1.2a5/oommf.tcl"
miffile="/panfs/panasas01.panfs.cluster/ppxsb3/oommfsimulationfiles/500nmsquare/unstrained/problems/square_500nm_10nm_pulse_sc1_0KJstrain_ampalter.mif"
out_file="/panfs/panasas01.panfs.cluster/ppxsb3/oommfsimulationfiles/500nmsquare/unstrained/amplitude10/square_pulse_MCA_ks_0KJ_amp10"
pulseamp=10
width=500
Ks=0


#echo $oommf
#echo "$oommf"
#echo "Parameters are: $parameters"
#echo "Mif file is: $mif_file"
#echo "Python script is: $py_script"
# Copying takes place after the job has begun to run, which means the files copied may not be the 
# most up to date...
#eval "cp $mif_file $working_folder/mif_file_JOBID_$PBS_JOBID.mif"
#eval "cp $py_script $working_folder/py_script_JOBID_$PBS_JOBID.py"
#eval "cp ${0} $working_folder/submission_script_JOBID_$PBS_JOBID.sh"

#command_to_run="$oommfroot \"$parameters JOB_ID $PBS_JOBID\" $mif_file"

echo "Command to run is $command_to_run "
eval $command_to_run
$tclroot $oommfroot boxsi -threads 8 -tk 0 -parameters  Ks 0 Amp $pulseamp width $width outdir $out_file $miffile 


sleep 20
echo "Finished job now"
