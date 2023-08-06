Python-CA  installation memo
============================

::: {.container}
KEK, High Energy Accelerator Research Organization Acceleator Lab Noboru
Yamamoto
:::

| 

1.  This program is retistered in PyPI.
    1.  you need to setup EPICSROOT environment varible before install
        this program using pip command. You may need other environment
        variables, such as WITH\_TK, TKINC, TKLIB, HOSTARCH.
    2.  You can create create EPICS\_config\_local.py files to setup
        these environment. Put this file in somewhere in your
        PYTHONPATH.
2.  You need Python 2.7 or later and EPICS 3.14.7 or later. (It may work
    with older version, but these are oldest versions I have built.) 
3.  Get a Python-CA extension module package as [a tarball 
    here](CaPython-1.10.tar.gz)\[updated on 2007/05/03\].
4.   Expand this tarball at  your working directory.
5.  Open setup.py in your favourite editor and change some parametes,
    such as EPICS architechture and installation path, appropriately.

        EPICSROOT=os.path.join("your epics root path")

        EPICSBASE=os.path.join(EPICSROOT,"base")

        EPICSEXT=os.path.join(EPICSROOT,"extensions")

        HOSTARCH="your epics host architecture"

6.  run the installation script, setup.py/  for build extension moules.

        python setup.py build

7.  if you encounter the compilation errors or any trouble , please send
    a message to  noboru.yamamoto\_at\_kek.jp.
8.  | You need to have write permission of the target directories for
      installation. Run:

        python setup.py install

9.  Test extension module.

::: {.container}
start python interpreter.
:::

     python

::: {.container}
Try to import ca module
:::

     import ca

::: {.container}
Check access to EPICS DB. (Assuming excas is running.)
:::

    ca.Get("fred")

Note to a GUI programmer:
-------------------------

| You should not call functions in GUI system(Tkinter or wxPython) in
  the Python-CA callback routines. It will crash your running program
  immediately.
