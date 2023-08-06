#!/opt/epics/R7/base/bin/darwin-x86/softIocPVA -x softIOC
#!/usr/bin/env softIoc
#!/opt/epics/R7/base/bin/darwin-x86/softIoc -x softIOC
## Register all support components

#softIoc_registerRecordDeviceDriver(pdbbase)
dbLoadTemplate("./excas.substitutions","")
# device support will create State variable automatically.
#dbStateCreate daq 
dbLoadRecords("./test.db")

#iocInit # for EPICS 3.x

