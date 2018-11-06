##############################################################################
#
#     busybox.py
#     Copyright (c) 2018 Raphael DINGE
#
#Tab=3########################################################################

import logging
import multiprocessing
import os
import shutil
import subprocess



SOURCE_BASE_URL = 'http://busybox.net/downloads'
BUSYBOX_VERSION = 'busybox-1.28.4'

PATH_THIS = os.path.abspath (os.path.dirname (__file__))
PATH_ARTIFACTS = os.path.join (os.path.dirname (PATH_THIS), 'artifacts')
PATH_BUSYBOX = os.path.join (PATH_ARTIFACTS, BUSYBOX_VERSION)
PATH_BUSYBOX_OUTPUT = os.path.join (PATH_ARTIFACTS, 'busybox-output')


#-----------------------------------------------------------------------------
# build

def build ():
   logging.info ('Building %s' % BUSYBOX_VERSION)
   fetch ()
   clean ()
   configure ('busybox.release.config')

   if os.path.exists (PATH_BUSYBOX_OUTPUT):
      shutil.rmtree (PATH_BUSYBOX_OUTPUT)

   if not os.path.exists (PATH_BUSYBOX_OUTPUT):
      os.makedirs (PATH_BUSYBOX_OUTPUT)

   make ()
   install ()



#-----------------------------------------------------------------------------
# fetch

def fetch ():
   if not os.path.exists (PATH_ARTIFACTS):
      os.makedirs (PATH_ARTIFACTS)

   if not os.path.exists (PATH_BUSYBOX):
      logging.info ('   Downloading')

      dl_cmd = [
         'wget', '-q',
         '-O', os.path.join (PATH_ARTIFACTS, '%s.tar.bz2' % BUSYBOX_VERSION),
         '%s/%s.tar.bz2' % (SOURCE_BASE_URL, BUSYBOX_VERSION)
      ]

      subprocess.check_call (dl_cmd)

      logging.info ('   Extracting')

      tar_cmd = [
         'tar', '-xf', os.path.join (PATH_ARTIFACTS, '%s.tar.bz2' % BUSYBOX_VERSION)
      ]

      subprocess.check_call (tar_cmd, cwd = PATH_ARTIFACTS)


#-----------------------------------------------------------------------------
# clean

def clean ():
   logging.info ('   Cleaning')

   log_file = open (os.path.join (PATH_ARTIFACTS, '%s-make-distclean-log.txt' % BUSYBOX_VERSION), 'w')

   cmd = [
      'make', 'distclean',
      '-j', '%d' % multiprocessing.cpu_count ()
   ]
   subprocess.check_call (cmd, cwd = PATH_BUSYBOX, stdout = log_file)



#-----------------------------------------------------------------------------
# configure

def configure (config):
   logging.info ('   Using configuration \033[92m%s\033[0m' % config)
   shutil.copyfile (
      os.path.join (PATH_THIS, 'assets', config),
      os.path.join (PATH_BUSYBOX, '.config')
   )



#-----------------------------------------------------------------------------
# make

def make ():
   logging.info ('   Building')

   log_file = open (os.path.join (PATH_ARTIFACTS, '%s-make-busybox-log.txt' % BUSYBOX_VERSION), 'w')

   cmd = [
      'make',
      'EXTRA_CFLAGS=-Os -s -fno-stack-protector -fomit-frame-pointer -U_FORTIFY_SOURCE',
       'busybox',
      '-j', '%d' % multiprocessing.cpu_count ()
   ]
   subprocess.check_call (cmd, cwd = PATH_BUSYBOX, stdout = log_file, stderr = log_file)



#-----------------------------------------------------------------------------
# install

def install ():
   logging.info ('   Installing')

   log_file = open (os.path.join (PATH_ARTIFACTS, '%s-make-install-log.txt' % BUSYBOX_VERSION), 'w')

   cmd = [
      'make',
      'CONFIG_PREFIX=%s' % PATH_BUSYBOX_OUTPUT,
       'install',
      '-j', '%d' % multiprocessing.cpu_count ()
   ]
   subprocess.check_call (cmd, cwd = PATH_BUSYBOX, stdout = log_file, stderr = log_file)
