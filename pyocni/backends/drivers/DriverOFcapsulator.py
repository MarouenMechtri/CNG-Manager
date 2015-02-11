# Copyright 2013 Institut Mines-Telecom - Telecom SudParis
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Created on Feb 25, 2013
@author: Marouen Mechtri
@contact: marouen.mechtri@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

import logging
from client import OCCIclient

logging.basicConfig(
    filename='logFile.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
)

class ofDriverCapsulator:
    """ Simple shell to run a command on the host """



    def configure_tunnel(self, gwinstance, gwaddress, OFport1, address, tunnelport, tunnelAddressDst, OFport2, tunnelTag):

        cmds=[]
        cmds.append(gwinstance.configure_Interface(OFport1, address))

        cmds.append(gwinstance.create_virtual_Interface(OFport2))
        cmds.append(gwinstance.configure_Tunnel_interface(tunnelport, tunnelAddressDst, OFport2, tunnelTag))

        gwinstance.execute_many_cmd_Cosacs(gwaddress, cmds)


    def connect_gw(self, gwinstance, gwaddress, datapath_ID, OFport1, OFport2, NOX, NOXport):
        cmds=[]
        cmds.append(gwinstance.configure_datapath(datapath_ID, OFport1, OFport2))
        cmds.append(gwinstance.start_openflow(NOX, NOXport))

        gwinstance.execute_many_cmd_Cosacs(gwaddress, cmds)



    def stop_gw(self, gwinstance, gwaddress):
        cmds=[]
        cmds.append(gwinstance.stop_process('ofdatapath'))
        cmds.append(gwinstance.stop_process('ofprotocol'))
        cmds.append(gwinstance.stop_process('capsulator'))

        gwinstance.execute_many_cmd_Cosacs(gwaddress, cmds)



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
    def configure_Tunnel_interface(self, tunnelport, tunnelAddressDst, OFport, tunnelTag):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd = 'cd /root/Capsulator; ./capsulator -t ' + tunnelport + ' -a -f ' + tunnelAddressDst + ' -vb ' + OFport + '\#' + tunnelTag + '&'
        return cmd


    #function to execute commands
    def configure_datapath(self, datapath_ID, OFport1, OFport2):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd = 'cd /root/openflow-1.0.0/; ./udatapath/ofdatapath --detach punix:/var/run/dp0 -d ' + datapath_ID + ' -i ' + OFport1 + ',' + OFport2
        return cmd

    #function to execute commands
    def start_openflow(self, NOX, NOX_port):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd = 'cd /root/openflow-1.0.0/; ./secchan/ofprotocol unix:/var/run/dp0 tcp:' + NOX + ':' + NOX_port + '&'
        return cmd

    #function to execute commands
    def stop_process(self, process):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd = '/usr/bin/killall ' + process
        return cmd


if __name__ == '__main__':



    # OpenFlow switch 1 settings
    OF1port1='eth1'
    OF1port2='tap0'
    datapath_ID1='004E46324304'

    # Capsulator tunnel 1 settings

    tunnelport1='eth0'                      # Physical tunnel interface
    tunnelAddressDst1='192.168.100.163'     # Tunnel destination IP address 


    # OpenFlow switch 2 settings
    OF2port1='eth2'
    OF2port2='tap0'
    datapath_ID2='004E46324305'

    # Capsulator tunnel 2 settings

    tunnelport2='eth1'                      # Physical tunnel interface
    tunnelAddressDst2='192.168.100.202'     # Tunnel destination IP address



    tunnelTag='1234'                       # Tunnel tag


    # OpenFlow controller settings

    NOX='192.168.122.20'
    NOXport='6633'


    gw1Address = '192.168.122.157'
    gw2Address = '192.168.122.185'

    gw1 = ofDriverCapsulator()
    gw2 = ofDriverCapsulator()

    ''' Configuration des gateways'''

    #gw1.configure_tunnel(gw1, gw1Address, OF1port1, '0.0.0.0', tunnelport1, tunnelAddressDst1, OF1port2, tunnelTag)
    #gw2.configure_tunnel(gw2, gw2Address, OF2port1, '0.0.0.0', tunnelport2, tunnelAddressDst2, OF2port2, tunnelTag)

    ''' Connecte les deux gateways'''
    #gw1.connect_gw(gw1, gw1Address, datapath_ID1, OF1port1, OF1port2, NOX, NOXport)
    #gw2.connect_gw(gw2, gw2Address, datapath_ID2, OF2port1, OF2port2, NOX, NOXport)


    ''' stop les deux gateways'''
    gw1.stop_gw(gw1, gw1Address)
    gw2.stop_gw(gw2, gw2Address)
