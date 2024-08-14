#!/usr/bin/env python

# Wrapper to submit a script to condor using a custom job script.
#
# __author__: Blaise Delaney
# __email__:blaise.delaney@cern.ch
# 
# with *many* thanks to John Smeaton for the template script

#===========================================================================
# run:"snakemake --cluster wrappers/condor_wrapper.py --jobs 10 target file"
#===========================================================================

from tempfile import NamedTemporaryFile
from snakemake.utils import read_job_properties
import subprocess
import sys
import os

# Get the jobscript, and the properties for this job
jobscript = sys.argv[1] #condor submission wrapper
job_props = read_job_properties(jobscript) #extrapolate job submission config for conda from wrapper
jobid = job_props["jobid"]

# Create a directory for condor logs, if this doesn't exist
logdir = os.path.abspath("CondorLogs")
if not os.path.exists(logdir):
    os.makedirs(logdir)


# Open a temporary file for the job submission script
with NamedTemporaryFile("w") as sub_file:

    # Condor environment
    #sub_file.write("Universe = vanilla \n")
    #sub_file.write("copy_to_spool = true \n")
    sub_file.write("getenv=False\n") # copy over conda env
    sub_file.write("should_transfer_files = YES \n")
    sub_file.write("when_to_transfer_output = ON_EXIT_OR_EVICT \n")
    #sub_file.write("environment = CONDOR_ID=$(Cluster).$(Process) \n")
    sub_file.write(f"LS_SUBCWD={logdir} \n")
    sub_file.write("Requirements = ( (OpSysAndVer =?= 'AlmaLinux9') && (Machine =!= LastRemoteHost) && (TARGET.has_avx2 =?= True) ) \n")

    # Rank hosts according to floating point speed
    sub_file.write("Rank = kflops \n")

    # Memory requirement
    sub_file.write("request_memory = 3000 \n")
    sub_file.write("RequestCpus = 4 \n")


    sub_file.write("JobFlavour      = 'longlunch'")
    sub_file.write("AccountingGroup = 'group_u_FCC.local_gen'")

    # Condor Output
    sub_file.write(f"output = {logdir}/out.{jobid} \n")
    sub_file.write(f"error  = {logdir}/err.{jobid} \n")
    sub_file.write(f"Log    = {logdir}/log.{jobid} \n")

    # Job script submission
    sub_file.write(f"Executable = {jobscript} \n")
    sub_file.write("Queue \n")

    # Now submit this condor script, and delete the temporary file
    sub_file.flush()
    subprocess.call( ["condor_submit", sub_file.name] )
