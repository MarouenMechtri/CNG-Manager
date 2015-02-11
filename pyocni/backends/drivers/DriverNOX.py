'''
Created on Feb 25, 2011
__author__       = 'Marouen Mechtri'
__contact__      = Marouen.Mechtri@it-sudparis.eu
__organization__ = Institut Telecom - Telecom SudParis

'''

import logging
from client import OCCIclient
import time

logging.basicConfig(
    filename='logFile.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
)

class gwProcci:
    """ Simple shell to run a command on the host """



    def configure_NOX(self, nox, NOXaddress, NOXport, NOXmodules):

        cmds=[]
        cmds.append(nox.configure_controller(NOXport, NOXmodules))

        nox.execute_many_cmd_Cosacs(NOXaddress, cmds)
        print "Starting NOX......OK"


    def stop_NOX(self, nox, NOXaddress):

        cmds=[]
        cmds.append(nox.stop_process('lt-nox_core'))

        nox.execute_many_cmd_Cosacs(NOXaddress, cmds)
        print "Stoping NOX......OK"

    def execute_many_cmd_Cosacs(self, address, cmds):
        for item in cmds:
            print item
            attributes = {
                'name': '',
                'syntax': item,
                'nature': 'system',
                'status': '',
                'identifier': ''
            }
            cl = OCCIclient(address, '8286', 'COSACS', 'script', attributes)
            cl.Post()

        cosacsStart = {
            'name': 'cosacs:start'
        }

        startcmd = OCCIclient(address, '8286', 'COSACS', 'script', cosacsStart)
        startcmd.Post()


    #function to execute commands
    def configure_Interface(self, interface, address):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd = '/sbin/ifconfig ' + interface + ' ' + address
        return cmd

    #function to execute commands
    def create_virtual_Interface(self, interface):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd = '/usr/sbin/tunctl -t  ' + interface + ';/sbin/ifconfig '+ interface + ' up'
        return cmd


    #function to execute commands
    def configure_controller(self, NOXport, NOXmodules):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd = 'cd /root/nox/build/src/; ./nox_core -i ptcp:' + NOXport + ' ' + NOXmodules + '&'
        return cmd

    #function to execute commands
    def stop_process(self, process):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd = '/usr/bin/killall ' + process
        return cmd


if __name__ == '__main__':



    # OpenFlow controller settings

    NOXport='6633'
    #NOXmodules='packetdump'

    NOXmodules='switch discovery'
    NOXaddress = '157.159.103.54'

    nox = gwProcci()

    ''' Configuration des gateways'''
    start_time = int(round(time.time() * 1000))

    #nox.configure_NOX(nox, NOXaddress, NOXport, NOXmodules)
    nox.stop_NOX(nox, NOXaddress)

    execution_time = int(round(time.time() * 1000)) - start_time
    file = open("executionTIMENOX", "w")
    file.write("execution time was " + str(execution_time) + " ms.\n")
    file.close()
