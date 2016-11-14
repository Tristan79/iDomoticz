# -*- coding: utf8 -*-

import json
import urllib

#------------------------------------------------------
# DOMOTICZ INTERFACE
#
# Python interface to Domoticz
#
# https://github.com/Tristan79/???
#
# 2016 Copyright © 2016 Tristan (@monkeycat.nl)
#
# CRAP WRAP v0.02
#------------------------------------------------------



#------------------------------------------------------
# DOMOTICZ INTERFACE CLASS
#------------------------------------------------------


class Domoticz:

    SensorText        = 5
    SensorSwitch      = 6
    SensorTemperature = 80
    SensorHumidity    = 81
    SensorCustom      = 1004

    SwitchTypeNormal  = 0
    SwitchTypeMotion  = 8
    SwitchtypeDimmer  = 7
    SwitchTypeContact = 2
    
    CustomImageNormal = 0
    CustomimageWater  = 11
    CustomImageAlarm  = 13
    CustomimageTree   = 14
    CustomImageHeat   = 15


    def __init__(self,server,secure = False):
        self.server = server
        self.secure = secure


    def base(self):
        s = ""
        if self.secure:
            s = "s"
        return "http" + s + "://" + self.server + "/json.htm?"


    def exists_hardware(self,name):
        url = self.base() + "type=hardware"
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        if "result" in data:
            for i in range(0,len(data["result"])):
                if name == data["result"][i]["Name"]:
                    return data["result"][i]["idx"]
        return "None"


    def use_virtual_hardware(self,name):
        self.hardware_idx = self.exists_hardware(name)
        if "None" == self.hardware_idx:
            nameurl = name.replace(" ", "%20")
            url = self.base() + "type=command&param=addhardware&htype=15&port=1&name=" + nameurl + "&enabled=true"
            response = urllib.urlopen(url)
            self.hardware_idx = self.exists_hardware(name)
            if "None" == self.hardware_idx:
                return False
        return True
    

    def exists_sensor(self,name):
        url = self.base() + "type=devices&filter=all&used=true&order=Name"
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        if "result" in data:
            for i in range(0,len(data["result"])):
                if name == data["result"][i]["Name"] and int(self.hardware_idx) == data["result"][i]["HardwareID"]:
                    return data["result"][i]["idx"]
        
        return "None"


    def use_virtual_sensor(self,name,type,options=""):
        nameurl = name.replace(" ", "%20")
        idx = self.exists_sensor(name)
        if "None" != idx:
            return idx
        if "None" == idx:
            url = self.base() + "type=createvirtualsensor&idx="+ self.hardware_idx + "&sensorname=" + nameurl +  "&sensortype=" + str(type)
            if options != "":
                url = url + "&sensoroptions=" + options
            response = urllib.urlopen(url)
            return self.exists_sensor(name)
        else:
            return "None"


    def use_virtual_custom(self,name,ax=""):
        return self.use_virtual_sensor(name,self.SensorCustom,"1;"+ax)


    def use_virtual_custom_water(self,name,ax=""):
        idx = self.use_virtual_sensor(name,self.SensorCustom,"1;"+ax)
        self.set_switch_type(idx,name,self.SwitchTypeNormal,self.CustomimageWater)
        return idx


    def set_switch_type(self,idx,name,switchType,switchImage):
        url = self.base() + "type=setused&idx=" + idx + "&switchtype=" + str(switchType) + "&name=" + str(name) + "&description=&strparam1=&strparam2=&protected=false&customimage=" +str(switchImage) + "&used=true&addjvalue=0&options="
        response = urllib.urlopen(url)
        data = json.loads(response.read())


    def set_custom_type(self,idx,name,switchImage):
        url = self.base() + "type=setused&idx=" + idx + "&switchtype=0&name=" + str(name) + "&description=&customimage=" +str(switchImage) + "&used=true"
        response = urllib.urlopen(url)
        data = json.loads(response.read())


    def use_virtual_temperature(self,name):
        return self.use_virtual_sensor(name,self.SensorTemperature)


    def use_virtual_text(self,name):
        return self.use_virtual_sensor(name,self.SensorText)


    def use_virtual_humidy(self,name):
        return self.use_virtual_sensor(name,self.SensorHumidity)


    def use_virtual_motion(self,name):
        idx = self.use_virtual_sensor(name,self.SensorSwitch)
        self.set_switch_type(idx,name,self.SwitchTypeMotion,self.CustomImageNormal)
        return idx


    def use_virtual_heat_dimmer(self,name):
        idx = self.use_virtual_sensor(name,self.SensorSwitch)
        self.set_switch_type(idx,name,self.SwitchtypeDimmer,self.CustomImageHeat)
        return idx


    def print_type(self,type):
        if type == self.SensorTemperature:  return "Temperature"
        elif type == self.SensorHumidity:   return "Humidity"
        elif type == self.SensorCustom:     return "Custom"
        elif type == self.SensorSwitch:     return "Switch"
        else:                               return "Unknown"



    # no check if right sensor....

    # should chop of ax... just do not use ax for the moment...
    def get_custom(self,idx):
        url = self.base() + "type=devices&rid=" + idx
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        return data["result"][0]["Data"]


    # should chop of ax... just do not use ax for the moment...
    def set_custom(self,idx,custom,check=True):
        url = self.base() + "type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue="+str(custom)
        if check:
            if float(self.get_custom(idx)) != float(custom):
                response = urllib.urlopen(url)
                return True
            else:
                return False
        else:
            response = urllib.urlopen(url)
            return True


    def get_temperature(self,idx):
        url = self.base() + "type=devices&rid=" + idx
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        return data["result"][0]["Temp"]
    

    def set_temperature(self,idx,temperature,check=True):
        url = self.base() + "type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue="+str(temperature)
        if check:
            if float(self.get_temperature(idx)) != float(temperature):
                response = urllib.urlopen(url)
                return True
            else:
                return False
        else:
            response = urllib.urlopen(url)
            return True


    def get_text(self,idx):
        url = self.base() + "type=devices&rid=" + idx
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        return data["result"][0]["Data"]
    

    def set_text(self,idx,text):
        if str(self.get_text(idx)) != str(text):
            url = self.base() + "type=command&param=udevice&idx=" + idx + "&nvalue=0&svalue="+text
            response = urllib.urlopen(url)
            return True
        return False

    def get_motion(self,idx):
        url = self.base() + "type=devices&rid=" + idx
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        return data["result"][0]["Status"]
    

    def set_motion(self,idx,switch):
        if switch:
            status = "On"
        else:
            status = "Off"
        if self.get_motion(idx) != status:
            url = self.base() + "type=command&param=switchlight&idx=" + idx + "&switchcmd="+str(status)
            response = urllib.urlopen(url)
            return True
        return False

