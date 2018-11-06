#!/usr/bin/env python
#
#     build.py
#     Copyright (c) 2018 Raphael DINGE
#
#Tab=3########################################################################


##### IMPORT #################################################################

import argparse
import fileinput
import logging
import multiprocessing
import os
import platform
import subprocess
import sys

import meijeos



##############################################################################

if sys.version_info < (2, 7):
   print >>sys.stderr, 'This script requires python 2.7 or greater.'
   sys.exit (1)

PATH_THIS = os.path.abspath (os.path.dirname (__file__))



"""
==============================================================================
Name : parse_args
==============================================================================
"""

def parse_args ():
   arg_parser = argparse.ArgumentParser ()

   arg_parser.add_argument(
      '-c', '--configuration',
      default = 'Release',
      choices = ['Debug', 'Release'],
      help = 'The build configuration to use. Defaults to Release'
   )

   arg_parser.add_argument (
      '-q', '--quiet',
      dest = 'logging_level', default = logging.INFO,
      action = 'store_const', const = logging.ERROR,
      help = 'Provides less output.'
   )

   arg_parser.add_argument (
      '-v', '--verbose',
      dest = 'logging_level', default = logging.INFO,
      action = 'store_const', const = logging.DEBUG,
      help = 'Provides more output.'
   )

   return arg_parser.parse_args (sys.argv[1:])



"""
==============================================================================
Name : build_linux
==============================================================================
"""

def build_linux (args):
   meijeos.build_linux ()
   meijeos.build_glibc ()
   meijeos.build_alsa ()
   meijeos.make_sysroot ()



"""
==============================================================================
Name : build
==============================================================================
"""

def build (args):
   if platform.system () != 'Linux':
      logging.error ("Fatal error: Only Linux can be used to build meijeos")
      sys.exit(1)

   build_linux (args)



##############################################################################

if __name__ == '__main__':
   logging.basicConfig(format='%(message)s', level=logging.INFO, stream=sys.stdout)

   try:
      sys.exit (build (parse_args ()))
   except subprocess.CalledProcessError as error:
      print >>sys.stderr, 'Build command exited with %d' % error.returncode
      sys.exit(1)
