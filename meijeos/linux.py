##############################################################################
#
#     linux.py
#     Copyright (c) 2018 Raphael DINGE
#
#Tab=3########################################################################

import logging
import multiprocessing
import os
import shutil
import subprocess



SOURCE_BASE_URL = 'http://kernel.org/pub/linux/kernel/v4.x'
LINUX_VERSION = 'linux-4.17.2'

PATH_THIS = os.path.abspath (os.path.dirname (__file__))
PATH_ARTIFACTS = os.path.join (os.path.dirname (PATH_THIS), 'artifacts')
PATH_LINUX = os.path.join (PATH_ARTIFACTS, LINUX_VERSION)
PATH_LINUX_OUTPUT = os.path.join (PATH_ARTIFACTS, 'linux-output')


#-----------------------------------------------------------------------------
# build

def build ():
   logging.info ('Building %s' % LINUX_VERSION)
   fetch ()
   clean ()
   configure ('linux.release.config')

   if os.path.exists (PATH_LINUX_OUTPUT):
      shutil.rmtree (PATH_LINUX_OUTPUT)

   if not os.path.exists (PATH_LINUX_OUTPUT):
      os.makedirs (PATH_LINUX_OUTPUT)

   make_kernel ()
   make_headers ()



#-----------------------------------------------------------------------------
# fetch

def fetch ():
   if not os.path.exists (PATH_ARTIFACTS):
      os.makedirs (PATH_ARTIFACTS)

   if not os.path.exists (PATH_LINUX):
      logging.info ('   Downloading')

      dl_cmd = [
         'wget', '-q',
         '-O', os.path.join (PATH_ARTIFACTS, '%s.tar.xz' % LINUX_VERSION),
         '%s/%s.tar.xz' % (SOURCE_BASE_URL, LINUX_VERSION)
      ]

      subprocess.check_call (dl_cmd)

      logging.info ('   Extracting')

      tar_cmd = [
         'tar', '-xf', os.path.join (PATH_ARTIFACTS, '%s.tar.xz' % LINUX_VERSION)
      ]

      subprocess.check_call (tar_cmd, cwd = PATH_ARTIFACTS)


#-----------------------------------------------------------------------------
# clean

def clean ():
   logging.info ('   Cleaning')

   log_file = open (os.path.join (PATH_ARTIFACTS, '%s-make-mrproper-log.txt' % LINUX_VERSION), 'w')

   cmd = [
      'make', 'mrproper',
      '-j', '%d' % multiprocessing.cpu_count ()
   ]
   subprocess.check_call (cmd, cwd = PATH_LINUX, stdout = log_file)



#-----------------------------------------------------------------------------
# configure

def configure (config):
   logging.info ('   Using configuration \033[92m%s\033[0m' % config)
   shutil.copyfile (
      os.path.join (PATH_THIS, 'assets', config),
      os.path.join (PATH_LINUX, '.config')
   )



#-----------------------------------------------------------------------------
# make_kernel

def make_kernel ():
   logging.info ('   Building Kernel')

   log_file = open (os.path.join (PATH_ARTIFACTS, '%s-make-bzimage-log.txt' % LINUX_VERSION), 'w')

   cmd = [
      'make',
      'CFLAGS=-Os -s -fno-stack-protector -fomit-frame-pointer -U_FORTIFY_SOURCE',
       'bzImage',
      '-j', '%d' % multiprocessing.cpu_count ()
   ]
   subprocess.check_call (cmd, cwd = PATH_LINUX, stdout = log_file)

   shutil.copyfile (
      os.path.join (PATH_LINUX, 'arch', 'x86', 'boot', 'bzImage'),
      os.path.join (PATH_LINUX_OUTPUT, 'kernel')
   )



#-----------------------------------------------------------------------------
# make_headers

def make_headers ():
   logging.info ('   Generating Headers')

   log_file = open (os.path.join (PATH_ARTIFACTS, '%s-make-headers-log.txt' % LINUX_VERSION), 'w')

   cmd = [
      'make',
      'INSTALL_HDR_PATH=%s' % PATH_LINUX_OUTPUT,
       'headers_install',
      '-j', '%d' % multiprocessing.cpu_count ()
   ]
   subprocess.check_call (cmd, cwd = PATH_LINUX, stdout = log_file)
