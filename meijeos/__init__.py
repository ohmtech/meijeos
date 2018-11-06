##############################################################################
#
#     __init__.py
#     Copyright (c) 2018 Raphael DINGE
#
#Tab=3########################################################################

import linux
import glibc
import alsa
import sysroot

def build_linux ():
   linux.build ()

def build_glibc ():
   glibc.build ()

def build_alsa ():
   alsa.build ()

def make_sysroot ():
   sysroot.make ()
