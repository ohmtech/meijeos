##############################################################################
#
#     glibc.py
#     Copyright (c) 2018 Raphael DINGE
#
#Tab=3########################################################################

import logging
import multiprocessing
import os
import shutil
import subprocess



SOURCE_BASE_URL = 'http://ftp.gnu.org/gnu/glibc'
GLIBC_VERSION = 'glibc-2.27'

PATH_THIS = os.path.abspath (os.path.dirname (__file__))
PATH_ARTIFACTS = os.path.join (os.path.dirname (PATH_THIS), 'artifacts')
PATH_GLIBC = os.path.join (PATH_ARTIFACTS, GLIBC_VERSION)
PATH_GLIBC_BUILD = os.path.join (PATH_ARTIFACTS, 'glibc-build')
PATH_GLIBC_OUTPUT = os.path.join (PATH_ARTIFACTS, 'glibc-output')
PATH_LINUX_OUTPUT = os.path.join (PATH_ARTIFACTS, 'linux-output')


#-----------------------------------------------------------------------------
# build

def build ():
   logging.info ('Building %s' % GLIBC_VERSION)
   fetch ()
   clean ()

   if not os.path.exists (PATH_GLIBC_BUILD):
      os.makedirs (PATH_GLIBC_BUILD)

   configure ()
   make ()

   if not os.path.exists (PATH_GLIBC_OUTPUT):
      os.makedirs (PATH_GLIBC_OUTPUT)

   install ()



#-----------------------------------------------------------------------------
# fetch

def fetch ():
   if not os.path.exists (PATH_ARTIFACTS):
      os.makedirs (PATH_ARTIFACTS)

   if not os.path.exists (PATH_GLIBC):
      logging.info ('   Downloading')

      dl_cmd = [
         'wget', '-q',
         '-O', os.path.join (PATH_ARTIFACTS, '%s.tar.bz2' % GLIBC_VERSION),
         '%s/%s.tar.bz2' % (SOURCE_BASE_URL, GLIBC_VERSION)
      ]

      subprocess.check_call (dl_cmd)

      logging.info ('   Extracting')

      tar_cmd = [
         'tar', '-xf', os.path.join (PATH_ARTIFACTS, '%s.tar.bz2' % GLIBC_VERSION)
      ]

      subprocess.check_call (tar_cmd, cwd = PATH_ARTIFACTS)


#-----------------------------------------------------------------------------
# clean

def clean ():
   logging.info ('   Cleaning')

   if os.path.exists (PATH_GLIBC_BUILD):
      shutil.rmtree (PATH_GLIBC_BUILD)

   if os.path.exists (PATH_GLIBC_OUTPUT):
      shutil.rmtree (PATH_GLIBC_OUTPUT)



#-----------------------------------------------------------------------------
# configure

def configure ():
   logging.info ('   Configuring')

   log_file = open (os.path.join (PATH_ARTIFACTS, '%s-configure-log.txt' % GLIBC_VERSION), 'w')

   cmd = [
      os.path.join (PATH_GLIBC, 'configure'),
      '--prefix=',
      '--with-headers=%s/include' % PATH_LINUX_OUTPUT,
      '--without-gd',
      '--without-selinux',
      '--disable-werror',
      'CFLAGS=-Os -s -fno-stack-protector -fomit-frame-pointer -U_FORTIFY_SOURCE'
   ]
   subprocess.check_call (cmd, cwd = PATH_GLIBC_BUILD, stdout = log_file, stderr = log_file)



#-----------------------------------------------------------------------------
# make

def make ():
   logging.info ('   Building')

   log_file = open (os.path.join (PATH_ARTIFACTS, '%s-make-log.txt' % GLIBC_VERSION), 'w')

   cmd = [
      'make',
      '-j', '%d' % multiprocessing.cpu_count ()
   ]
   subprocess.check_call (cmd, cwd = PATH_GLIBC_BUILD, stdout = log_file, stderr = log_file)



#-----------------------------------------------------------------------------
# install

def install ():
   logging.info ('   Installing')

   log_file = open (os.path.join (PATH_ARTIFACTS, '%s-make-install-log.txt' % GLIBC_VERSION), 'w')

   cmd = [
      'make', 'install',
      'DESTDIR=%s' % PATH_GLIBC_OUTPUT,
      '-j', '%d' % multiprocessing.cpu_count ()
   ]
   subprocess.check_call (cmd, cwd = PATH_GLIBC_BUILD, stdout = log_file, stderr = log_file)
