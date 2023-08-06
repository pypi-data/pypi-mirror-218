#!/opt/epics/base/bin/darwin-x86/softIoc -x softIOC
## Register all support components

#dbLoadDatabase("/opt/epics/base/dbd/softIoc.dbd")
#wfexample_registerRecordDeviceDriver(pdbbase)

dbLoadTemplate("excas.substitutions","")

#dbStateCreate daq

dbLoadRecords("./test.db","nelm=1024")

iocInit()

