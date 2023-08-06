# EPICS CA library interface module (KEK, Japan)

## Overview

This is a distribution of Python extension module for EPICS/CA libarary.
It allow you to access EPICS runtime database or CA server through CA
library. Now it support multi-threaded EPICS CA library in Release 3.14
or later of EPICS.

Please read doc/InstallationMemo.html for installation proceduce.

Thank you,

2007/5/7

Noboru Yamamoto EPICS group, Accelerator Lab. KEK, JAPAN

\* contributors: Takashi Obina PF-AR/KEK Tatsuro Nakamura KEKB/KEK Wang
Xiaoqiang PSI

\* Special Thanks: to All users who gave us comments.

### installation

A setup script of this module need to know the location of your EPICS
installation. Please EPICSROOT environment variable as the path where
your EPICS base is.

1.  download source package from PyPI site.

2.  exapnd the file at appropriate directory

3.  goto this directory and run

    env EPICS_ROOT=/your/epics/root python3 setup.py build clean install

### memo:2019.4.19

This module is updated so that it is now compatible with both Python2.x
(x\>6) and Python3.y. (I just tested with Python2.7 and Python3.7).

This module also include calib module which is developed with Cython. It
is still under development. Once this module is completed, ca314.cpp
will be obsoleted and will be replaced by python module based on calib.

### memo:2020.11.17

\_ca_kek.py and \_ca314.cpp are tweaked to support \"SyncGroup\"
function.

\_ca_kek.py is also clean-upped with 2to3 and pylint.

### memo:2020.11.19

A crash on centOS was caused by incorrect data conversion format in
PyArg_ParseTuple in \_ca314.cpp. A size of data specified by the fromat
should be matched with the size of the correspondig argument. Functions,
sg_test/sg_reset/sg_state, were affected by this incorrect format
characters.

Most of python scripts in sample/ directory now works on both python2
and python3. I don\'t have PyQt, wxPython in the current test platform,
so scripts using PyQt or wxPython are not tested( but converted with
2to3 anyway). You may need to install future module (not \_\_future\_\_
module) into your python2 enviroment, to test sicripts using tkinter
module.
