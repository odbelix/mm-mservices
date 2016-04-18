#!/usr/bin/env python
########################################################################
# <mservices, Monitor for Services>
# Copyright (C) 2015  Manuel Moscoso Dominguez manuel.moscoso.d@gmail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
########################################################################
# Manuel Moscoso Dominguez <manuel.moscoso.d@gmail.com>
########################################################################
import time
import datetime
import syslog
import socket

def startBackUpMachie(machine):
    


def checkPortService(host,port):
    try:
        print host
        print port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((host,port))
        sock.close()
        if result == 0:
             syslog.syslog(syslog.LOG_INFO,"Service port[%d] is Open in the Host[%s]" % (port,host))
             return True
        else:
            syslog.syslog(syslog.LOG_ERR,"Error: Service port[%d] is not Open in the Host[%s]:error(%s) " % (port,host,str(result)))
            return False
    except socket.error as e:
        syslog.syslog(syslog.LOG_ERR,"Error: " + str(e))
        return False


def main():
    servicio = True	
    timePre = 0 
    
    hosts = {}
    hosts["DNS"] = {}
    hosts["DNS"]["address"] = "192.168.20.2"
    hosts["DNS"]["serviceport"] = "53"
    hosts["DNS"]["backup"] = "startvm vm-dns-2"
    hosts["DNS"]["state"] = "off"
    
    
    hosts["WEBSITE"] = {}
    hosts["WEBSITE"]["address"] = "192.168.20.2"
    hosts["WEBSITE"]["serviceport"] = "80"
    hosts["WEBSITE"]["backup"] = "startvm vm-web-2"
    hosts["WEBSITE"]["state"] = "off"
    
    
    secondCount = 0
    secondPeriod = 10
    
    
    while servicio == True:
        timeNow = datetime.datetime.now()
        seconds = timeNow.second
        if seconds % secondPeriod == 0:
            syslog.syslog(syslog.LOG_INFO,"------------ INIT mservice - Checking --------------")
            print timeNow
            for host in hosts:
                print host
                if checkPortService(hosts[host]["address"],int(hosts[host]["serviceport"])) is False:
                    hosts[host]["state"] = "on"
                    syslog.syslog(syslog.LOG_INFO,"Starting Backup HOST for service: %s / %s / %s. " % (host,hosts[host]["address"],hosts[host]["serviceport"]))
                    #### Instruction for turn on the VM
                    
                else:
                    syslog.syslog(syslog.LOG_INFO,"Service is OK: %s / %s / %s. " % (host,hosts[host]["address"],hosts[host]["serviceport"]))
            
            syslog.syslog(syslog.LOG_INFO,"------------ FINISH mservice -------------- ")
            secondCount = 0
        else:
            secondCount = secondCount + 1
        
        time.sleep(1)
        
    
if __name__ == "__main__":	
	main()
