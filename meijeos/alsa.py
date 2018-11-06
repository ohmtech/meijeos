##############################################################################
#
#     alsa.py
#     Copyright (c) 2018 Raphael DINGE
#
#Tab=3########################################################################

import logging
import multiprocessing
import os
import shutil
import subprocess



SOURCE_BASE_URL = 'http://www.mirrorservice.org/sites/ftp.alsa-project.org/pub/lib'
ALSA_VERSION = 'alsa-lib-1.1.6'

PATH_THIS = os.path.abspath (os.path.dirname (__file__))
PATH_ARTIFACTS = os.path.join (os.path.dirname (PATH_THIS), 'artifacts')
PATH_ALSA = os.path.join (PATH_ARTIFACTS, ALSA_VERSION)
PATH_ALSA_BUILD = os.path.join (PATH_ARTIFACTS, 'alsa-build')
PATH_ALSA_OUTPUT = os.path.join (PATH_ARTIFACTS, 'alsa-output')
PATH_LINUX_OUTPUT = os.path.join (PATH_ARTIFACTS, 'linux-output')


#-----------------------------------------------------------------------------
# build

def build ():
   logging.info ('Building %s' % ALSA_VERSION)
   fetch ()
   clean ()

   if not os.path.exists (PATH_ALSA_BUILD):
      os.makedirs (PATH_ALSA_BUILD)

   configure ()
   make ()

   if not os.path.exists (PATH_ALSA_OUTPUT):
      os.makedirs (PATH_ALSA_OUTPUT)

   install ()



#-----------------------------------------------------------------------------
# fetch

def fetch ():
   if not os.path.exists (PATH_ARTIFACTS):
      os.makedirs (PATH_ARTIFACTS)

   if not os.path.exists (PATH_ALSA):
      logging.info ('   Downloading')

      dl_cmd = [
         'wget', '-q',
         '-O', os.path.join (PATH_ARTIFACTS, '%s.tar.bz2' % ALSA_VERSION),
         '%s/%s.tar.bz2' % (SOURCE_BASE_URL, ALSA_VERSION)
      ]

      subprocess.check_call (dl_cmd)

      logging.info ('   Extracting')

      tar_cmd = [
         'tar', '-xf', os.path.join (PATH_ARTIFACTS, '%s.tar.bz2' % ALSA_VERSION)
      ]

      subprocess.check_call (tar_cmd, cwd = PATH_ARTIFACTS)


#-----------------------------------------------------------------------------
# clean

def clean ():
   logging.info ('   Cleaning')

   if os.path.exists (PATH_ALSA_BUILD):
      shutil.rmtree (PATH_ALSA_BUILD)

   if os.path.exists (PATH_ALSA_OUTPUT):
      shutil.rmtree (PATH_ALSA_OUTPUT)



#-----------------------------------------------------------------------------
# configure

def configure ():
   logging.info ('   Configuring')

   log_file = open (os.path.join (PATH_ARTIFACTS, '%s-configure-log.txt' % ALSA_VERSION), 'w')

   cmd = [
      os.path.join (PATH_ALSA, 'configure'),
      '--prefix=',
      '--enable-shared=yes',
      '--enable-static=no',
      '--with-headers=%s/include' % PATH_LINUX_OUTPUT,
      'CFLAGS=-Os -s -fno-stack-protector -fomit-frame-pointer -U_FORTIFY_SOURCE'
   ]
   subprocess.check_call (cmd, cwd = PATH_ALSA_BUILD, stdout = log_file, stderr = log_file)



#-----------------------------------------------------------------------------
# make

def make ():
   logging.info ('   Building')

   log_file = open (os.path.join (PATH_ARTIFACTS, '%s-make-log.txt' % ALSA_VERSION), 'w')

   cmd = [
      'make',
      '-j', '%d' % multiprocessing.cpu_count ()
   ]
   subprocess.check_call (cmd, cwd = PATH_ALSA_BUILD, stdout = log_file, stderr = log_file)



#-----------------------------------------------------------------------------
# install

def install ():
   logging.info ('   Installing')

   log_file = open (os.path.join (PATH_ARTIFACTS, '%s-make-install-log.txt' % ALSA_VERSION), 'w')

   cmd = [
      'make', 'install',
      'DESTDIR=%s' % PATH_ALSA_OUTPUT,
      '-j', '%d' % multiprocessing.cpu_count ()
   ]
   subprocess.check_call (cmd, cwd = PATH_ALSA_BUILD, stdout = log_file, stderr = log_file)
