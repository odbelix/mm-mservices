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
import datetime
import syslog
import socket
import threading
import sys

def clientOperation(conn,address):
    print "Connection from [%s]" % str(address)

def main():
    serversocket = socket.socket(
    socket.AF_INET, socket.SOCK_STREAM)
    #bind the socket to a public host,
    # and a well-known port
    serversocket.bind((socket.gethostname(), 1111))
    #become a server socket
    serversocket.listen(5)
    
    while 1:
       
        #accept connections from outside
        (clientsocket, address) = serversocket.accept()
        #now do something with the clientsocket
        #in this case, we'll pretend this is a threaded server
        #ct = clientOperation(clientsocket)
        client = threading.Thread(target=clientOperation, args=(clientsocket,address))
        client.start()
        
        try:
            print >>sys.stderr, 'connection from', address

            # Receive the data in small chunks and retransmit it
            while True:
                data = clientsocket.recv(16)
                print >>sys.stderr, 'received "%s"' % data
                if data:
                    print >>sys.stderr, 'sending data back to the client'
                    clientsocket.sendall(data)
                else:
                    print >>sys.stderr, 'no more data from', address
                    break
                
        finally:
        # Clean up the connection
            clientsocket.close()
        
    
if __name__ == "__main__":	
	main()
