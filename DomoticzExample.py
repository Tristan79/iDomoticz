# -*- coding: utf8 -*-

import sys

from Domoticz import *


#------------------------------------------------------
# DOMOTICZ INTERFACE EXAMPLE
#
# Python interface to domoticz
#
# https://github.com/Tristan79/???
#
# 2016 Copyright © 2016 Tristan (@monkeycat.nl)
#
# CRAP WRAP v0.01
#------------------------------------------------------


# EXAMPLE

domoticz = Domoticz("localhost:8080")



    print "Hardware IDX: " + str(domoticz.hardware_idx)
    
    # BUG IN DOMOTICZ v3.5 NEVER PUT TWO OF THE SAME SENSOR TYPE AT THE BEGINNING
    
    temp_name = "Temperature Sensor TEST"
    temp_type = domoticz.SensorTemperature
    
    temp_idx = domoticz.use_virtual_sensor(temp_name,temp_type)
    if temp_idx == "None":
        print "Failed to get [" + temp_name + "]"
        sys.exit()


    hum_name = "Humidity Sensor"
    hum_type = domoticz.SensorHumidity

    hum_idx = domoticz.use_virtual_sensor(hum_name,hum_type)
    if hum_idx == "None":
        print "Failed to get [" + hum_name + "]"
        sys.exit()


    test1_name = "Temperature Sensor Test 1"
    test1_type = domoticz.SensorTemperature

    test1_idx = domoticz.use_virtual_sensor(test1_name,test1_type)
    if test1_idx == "None":
        print "Failed to get [" + test_name + "]"
        sys.exit()


    test2_name = "Temperature Sensor Test 2"
    test2_type = domoticz.SensorTemperature

    test2_idx = domoticz.use_virtual_sensor(test2_name,test2_type)
    if test2_idx == "None":
        print "Failed to get [" + test2_name + "]"
        sys.exit()


else:
    print "Failed to get hardware"
    sys.exit()

# IF YOU HERE YOU HAVE IDX AND NAMES OF YOUR VIRTUAL SENSORS.... (whether they where already in domoticz or not)


print domoticz.print_type(temp_type) + " ["+ temp_name + "] IDX " + str(temp_idx)
print domoticz.print_type(hum_type) + "["+ hum_name + "] IDX " + str(hum_idx)
print domoticz.print_type(test1_type) + "["+ test1_name + "] IDX " + str(test1_idx)
print domoticz.print_type(test2_type) + "["+ test2_name + "] IDX " + str(test2_idx)


