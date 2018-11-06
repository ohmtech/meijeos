##############################################################################
#
#     sysroot.py
#     Copyright (c) 2018 Raphael DINGE
#
#Tab=3########################################################################

import logging
import multiprocessing
import os
import shutil
import subprocess



PATH_THIS = os.path.abspath (os.path.dirname (__file__))
PATH_ARTIFACTS = os.path.join (os.path.dirname (PATH_THIS), 'artifacts')
PATH_SYSROOT = os.path.join (PATH_ARTIFACTS, 'sysroot')
PATH_GLIBC_OUTPUT = os.path.join (PATH_ARTIFACTS, 'glibc-output')
PATH_ALSA_OUTPUT = os.path.join (PATH_ARTIFACTS, 'alsa-output')
PATH_LINUX_OUTPUT = os.path.join (PATH_ARTIFACTS, 'linux-output')


#-----------------------------------------------------------------------------
# make

def make ():
   logging.info ('Making sysroot')
   clean ()
   copy ()
   link_usr()



#-----------------------------------------------------------------------------
# clean

def clean ():
   logging.info ('   Cleaning')

   if os.path.exists (PATH_SYSROOT):
      shutil.rmtree (PATH_SYSROOT)



#-----------------------------------------------------------------------------
# copy

def copy ():
   logging.info ('   Copying')

   os.makedirs (os.path.join (PATH_SYSROOT))

   logging.info ('      glibc')
   subprocess.check_call ('cp -r %s/* %s' % (PATH_GLIBC_OUTPUT, PATH_SYSROOT), shell=True)

   # Copy/Merge alsa
   # Note: this is not great but it's not easy to have the cp -R merging behavior in python
   logging.info ('      alsa')
   subprocess.check_call ('cp -R %s/* %s' % (PATH_ALSA_OUTPUT, PATH_SYSROOT), shell=True)

   # Copy linux headers
   logging.info ('      linux headers')
   subprocess.check_call ('cp -r %s/include %s' % (PATH_LINUX_OUTPUT, PATH_SYSROOT), shell=True)



#-----------------------------------------------------------------------------
# link_usr

def link_usr ():
   logging.info ('   Linking usr')
   os.makedirs (os.path.join (PATH_SYSROOT, 'usr'))

   for dir in ['include', 'lib', 'share']:
      os.symlink (
         os.path.join (PATH_SYSROOT, dir),
         os.path.join (PATH_SYSROOT, 'usr', dir)
      )
