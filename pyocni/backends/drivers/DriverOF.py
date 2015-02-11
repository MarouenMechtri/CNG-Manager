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
import time

logging.basicConfig(
    filename='logFile.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
)

class gwProcci:
    """ Simple shell to run a command on the host """



    #function to execute commands
    def stop_process(self, process):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd = '/usr/bin/killall ' + process
        return cmd


    #function to execute commands
    def delete_vpn(self):
        """run <command>
        Execute this command on all hosts in the list"""
        return self.configure('delete vpn')


    #function to execute commands
    def delete_protocols(self):
        """run <command>
        Execute this command on all hosts in the list"""
        return self.configure('delete protocols')

    #function to execute commands
    def delete_tunnel(self):
        """run <command>
        Execute this command on all hosts in the list"""
        return self.configure('delete interfaces tunnel')


    #function to execute commands
    def configure(self, cmd):
        cmd_conf = '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper '
        cmdConfig=    cmd_conf + 'begin &&' + cmd_conf + cmd + '&&' + cmd_conf + 'commit &&' + cmd_conf + 'end &&' + cmd_conf + 'save'
        return cmdConfig

    #function to execute commands
    def load(self):
        return self.configure('load')


    #function to execute commands
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


    '''
    OpenFlow Configuration
    '''


    #function to execute commands
    def configure_datapath(self, datapath_ID, listOFport):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd = 'cd /root/openflow-1.0.0/; ./udatapath/ofdatapath --detach punix:/var/run/dp0 -d ' + datapath_ID + ' -i '
        for i in range(len(listOFport)-1):
            cmd = cmd + listOFport[i] + ','
        cmd = cmd + listOFport[len(listOFport)-1]
        return cmd

    #function to execute commands
    def start_openflow(self, NOX, NOX_port):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd = 'cd /root/openflow-1.0.0/; ./secchan/ofprotocol unix:/var/run/dp0 tcp:' + NOX + ':' + NOX_port + '&'
        return cmd



    '''
    IPSEC Configuration
    '''


    #function to execute commands
    def configure_IKE_proposal(self, ikeName, proposalNum, encryption, hash):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd_conf = '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper '
        return self.configure(
            'set vpn ipsec ike-group ' + ikeName + ' proposal ' + proposalNum + ' encryption ' + encryption +
            '&&' + cmd_conf + 'set vpn ipsec ike-group ' + ikeName + ' proposal ' + proposalNum + ' hash ' + hash)

    #function to execute commands
    def configure_Protocol_lifetime(self, protocol, Name, lifetime):
        """run <command>
        Execute this command on all hosts in the list"""
        return self.configure('set vpn ipsec ' + protocol + '-group ' + Name + ' lifetime ' + lifetime)


    #function to execute commands
    def configure_ESP_proposal(self, espName, proposalNum, encryption, hash):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd_conf = '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper '
        return self.configure(
            'set vpn ipsec esp-group ' + espName + ' proposal ' + proposalNum + ' encryption ' + encryption +
            '&&' + cmd_conf + 'set vpn ipsec esp-group ' + espName + ' proposal ' + proposalNum + ' hash ' + hash)

    #function to execute commands
    def configure_ESP_lifetime(self, espName, lifetime):
        """run <command>
        Execute this command on all hosts in the list"""
        return self.configure('set vpn ipsec esp-group ' + espName + ' lifetime ' + lifetime)


    #function to execute commands
    def configure_IPSEC_interface(self, interface):
        """run <command>
        Execute this command on all hosts in the list"""
        return self.configure('set vpn ipsec ipsec-interfaces interface ' + interface)



    '''
    site-to-site Configuration (Ipsec between two site)
    '''



    #function to execute commands
    def configure_IPSEC_SiteToSite_withfile(self, remoteAddress, authenticationKey, esp, ike, localAddress, tunnelNum, protocol):
        return '/home/vyatta/addipsec '+remoteAddress+' '+authenticationKey+' '+esp+' '+ike+' '+localAddress+' '+tunnelNum+' '+protocol


    '''
    GRE Configuration
    '''


    #function to execute commands
    def configure_GRE(self, tunnelName, tunnelAddress, description, mode, localAddress, remoteAddress):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd_conf = '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper '
        return self.configure(
            'set interfaces tunnel ' + tunnelName + ' address ' + tunnelAddress +
            '&&' + cmd_conf + 'set interfaces tunnel ' + tunnelName + ' description "' + description + '"' +
            '&&' + cmd_conf + 'set interfaces tunnel ' + tunnelName + ' encapsulation ' + mode +
            '&&' + cmd_conf + 'set interfaces tunnel ' + tunnelName + ' multicast enable ' +
            '&&' + cmd_conf + 'set interfaces tunnel ' + tunnelName + ' local-ip ' + localAddress +
            '&&' + cmd_conf + 'set interfaces tunnel ' + tunnelName + ' remote-ip ' + remoteAddress)









    def configure_protocol_IPSEC(self, gwinstance, address, ethername, IKEname, ESPname):

        cmds=[]
        cmds.append(gwinstance.configure_IPSEC_interface(ethername))
        print "Configuration of IPSEC interface......OK"
        cmds.append(gwinstance.configure_IKE_proposal(IKEname, '1', 'aes256','sha1'))
        cmds.append(gwinstance.configure_IKE_proposal(IKEname, '2', 'aes128','sha1'))
        print "Configuration of IKE protocol......OK"
        cmds.append(gwinstance.configure_Protocol_lifetime('ike', IKEname, '3600'))
        print "Configuration of IKE lifetime......OK"

        cmds.append(gwinstance.configure_ESP_proposal(ESPname, '1', 'aes256','sha1'))
        cmds.append(gwinstance.configure_ESP_proposal(ESPname, '2', '3des','md5'))
        print "Configuration of ESP protocol......OK"
        cmds.append(gwinstance.configure_Protocol_lifetime('esp', ESPname, '1800'))
        print "Configuration of ESP lifetime......OK"
        gwinstance.execute_many_cmd_Cosacs(address, cmds)




    def connect_gw(self, gwinstance, greInterface, greAdress, prefix, tunnelnum, tunnelProtocol, localAddress, remoteAddress, authenticationKey, IKE, ESP):
        cmds=[]
        cmds.append(gwinstance.configure_GRE(greInterface, greAdress+'/'+prefix, 'GRE description', tunnelProtocol, localAddress, remoteAddress))
        print "Configuration of GRE protocol......OK"
        cmds.append(gwinstance.configure_IPSEC_SiteToSite_withfile(remoteAddress, authenticationKey, ESP, IKE, localAddress, tunnelnum , tunnelProtocol))
        cmds.append(gwinstance.load())
        print "Configuration of IPSEC Site To Site tunnel......OK"

        gwinstance.execute_many_cmd_Cosacs(localAddress, cmds)


    def connect_openflow(self, gwinstance, gwAddress, datapath_ID, listOFport, NOX, NOXport):
        cmds=[]
        cmds.append(gwinstance.configure_datapath(datapath_ID, listOFport))
        print "Configuration of openflow datapath......OK"
        cmds.append(gwinstance.start_openflow(NOX, NOXport))
        print "Starting Openflow......OK"


        gwinstance.execute_many_cmd_Cosacs(gwAddress, cmds)




    def stop_gw(self, gwinstance, gwaddress):

        cmds=[]

        cmds.append(gwinstance.stop_process('ofdatapath'))
        print "Stoping openflow datapath......OK"
        cmds.append(gwinstance.stop_process('ofprotocol'))
        print "Stoping openflow......OK"

        cmds.append(gwinstance.delete_vpn())
        print "Stoping IPSEC tunnel......OK"
        cmds.append(gwinstance.delete_protocols())
        print "Stoping protocols......OK"
        cmds.append(gwinstance.delete_tunnel())
        print "Stoping GRE tunnel......OK"

        gwinstance.execute_many_cmd_Cosacs(gwaddress, cmds)




if __name__ == '__main__':

    gw1 = gwProcci()
    gw2 = gwProcci()
    #gw3 = gwProcci()
    #gw4 = gwProcci()
    #gw5 = gwProcci()
    #gw6 = gwProcci()
    #gw7 = gwProcci()
    #gw8 = gwProcci()
    #gw9 = gwProcci()
    #gw10 = gwProcci()

    gw1Address = '157.159.249.234'
    gw2Address = '157.159.249.235'
    gw3Address = '157.159.249.232'
    gw4Address = '157.159.249.233'
    gw5Address = '157.159.249.238'
    gw6Address = '157.159.249.239'
    gw7Address = '157.159.249.232'
    gw8Address = '157.159.249.233'
    gw9Address = '157.159.249.235'
    gw10Address = '157.159.249.237'


    greAddresslink1gw1 = '10.3.1.1'
    greAddresslink1gw2 = '10.3.1.2'
    greAddresslink2gw1 = '10.3.2.1'
    greAddresslink2gw2 = '10.3.2.2'
    greAddresslink3gw1 = '10.3.3.1'
    greAddresslink3gw2 = '10.3.3.2'
    greAddresslink4gw1 = '10.3.4.1'
    greAddresslink4gw2 = '10.3.4.2'
    greAddresslink5gw1 = '10.3.5.1'
    greAddresslink5gw2 = '10.3.5.2'
    greAddresslink6gw1 = '10.3.6.1'
    greAddresslink6gw2 = '10.3.6.2'
    greAddresslink7gw1 = '10.3.7.1'
    greAddresslink7gw2 = '10.3.7.2'
    greAddresslink8gw1 = '10.3.8.1'
    greAddresslink8gw2 = '10.3.8.2'
    greAddresslink9gw1 = '10.3.9.1'
    greAddresslink9gw2 = '10.3.9.2'
    greAddresslink10gw1 = '10.3.10.1'
    greAddresslink10gw2 = '10.3.10.2'
    greAddresslink11gw1 = '10.3.11.1'
    greAddresslink11gw2 = '10.3.11.2'
    greAddresslink12gw1 = '10.3.12.1'
    greAddresslink12gw2 = '10.3.12.2'
    greAddresslink13gw1 = '10.3.13.1'
    greAddresslink13gw2 = '10.3.13.2'
    greAddresslink14gw1 = '10.3.14.1'
    greAddresslink14gw2 = '10.3.14.2'
    greAddresslink15gw1 = '10.3.15.1'
    greAddresslink15gw2 = '10.3.15.2'
    greAddresslink16gw1 = '10.3.16.1'
    greAddresslink16gw2 = '10.3.16.2'
    greAddresslink17gw1 = '10.3.17.1'
    greAddresslink17gw2 = '10.3.17.2'
    greAddresslink18gw1 = '10.3.18.1'
    greAddresslink18gw2 = '10.3.18.2'
    greAddresslink19gw1 = '10.3.19.1'
    greAddresslink19gw2 = '10.3.19.2'
    greAddresslink20gw1 = '10.3.20.1'
    greAddresslink20gw2 = '10.3.20.2'

    tunnelinterfacegw1='eth0'
    tunnelinterfacegw2='eth0'
    tunnelinterfacegw3='eth0'
    tunnelinterfacegw4='eth0'
    tunnelinterfacegw5='eth0'
    tunnelinterfacegw6='eth0'
    tunnelinterfacegw7='eth0'
    tunnelinterfacegw8='eth0'
    tunnelinterfacegw9='eth0'
    tunnelinterfacegw10='eth0'

    OFinterfacegw1='eth1'
    OFinterfacegw2='eth1'
    OFinterfacegw3='eth1'
    OFinterfacegw4='eth1'
    OFinterfacegw5='eth1'
    OFinterfacegw6='eth1'
    OFinterfacegw7='eth1'
    OFinterfacegw8='eth1'
    OFinterfacegw9='eth1'
    OFinterfacegw10='eth1'


    greInterfacelink1='tun0'
    greInterfacelink2='tun1'
    greInterfacelink3='tun2'
    greInterfacelink4='tun3'
    greInterfacelink5='tun4'
    greInterfacelink6='tun5'
    greInterfacelink7='tun6'
    greInterfacelink8='tun7'
    greInterfacelink9='tun8'
    greInterfacelink10='tun9'
    greInterfacelink11='tun10'
    greInterfacelink12='tun11'
    greInterfacelink13='tun12'
    greInterfacelink14='tun13'
    greInterfacelink15='tun14'
    greInterfacelink16='tun15'
    greInterfacelink17='tun16'
    greInterfacelink18='tun17'
    greInterfacelink19='tun18'
    greInterfacelink20='tun19'

    prefix = '30'
    tunnelProtocol = 'gre'


    tunnelnumlink1='1'
    tunnelnumlink2='2'
    tunnelnumlink3='3'
    tunnelnumlink4='4'
    tunnelnumlink5='5'
    tunnelnumlink6='6'
    tunnelnumlink7='7'
    tunnelnumlink8='8'
    tunnelnumlink9='9'
    tunnelnumlink10='10'
    tunnelnumlink11='11'
    tunnelnumlink12='12'
    tunnelnumlink13='13'
    tunnelnumlink14='14'
    tunnelnumlink15='15'
    tunnelnumlink16='16'
    tunnelnumlink17='17'
    tunnelnumlink18='18'
    tunnelnumlink19='19'
    tunnelnumlink20='20'


    authenticationKeylink1 = 'test_key_1'
    authenticationKeylink2 = 'test_key_2'
    authenticationKeylink3 = 'test_key_3'
    authenticationKeylink4 = 'test_key_4'
    authenticationKeylink5 = 'test_key_5'
    authenticationKeylink6 = 'test_key_6'
    authenticationKeylink7 = 'test_key_7'
    authenticationKeylink8 = 'test_key_8'
    authenticationKeylink9 = 'test_key_9'
    authenticationKeylink10 = 'test_key_10'
    authenticationKeylink11 = 'test_key_11'
    authenticationKeylink12 = 'test_key_12'
    authenticationKeylink13 = 'test_key_13'
    authenticationKeylink14 = 'test_key_14'
    authenticationKeylink15 = 'test_key_15'
    authenticationKeylink16 = 'test_key_16'
    authenticationKeylink17 = 'test_key_17'
    authenticationKeylink18 = 'test_key_18'
    authenticationKeylink19 = 'test_key_19'
    authenticationKeylink20 = 'test_key_20'


    IKEgw1 = 'IKEgw1'
    ESPgw1 = 'ESPgw1'
    IKEgw2 = 'IKEgw2'
    ESPgw2 = 'ESPgw2'
    IKEgw3 = 'IKEgw3'
    ESPgw3 = 'ESPgw3'
    IKEgw4 = 'IKEgw4'
    ESPgw4 = 'ESPgw4'
    IKEgw5 = 'IKEgw5'
    ESPgw5 = 'ESPgw5'
    IKEgw6 = 'IKEgw6'
    ESPgw6 = 'ESPgw6'
    IKEgw7 = 'IKEgw7'
    ESPgw7 = 'ESPgw7'
    IKEgw8 = 'IKEgw8'
    ESPgw8 = 'ESPgw8'
    IKEgw9 = 'IKEgw9'
    ESPgw9 = 'ESPgw9'
    IKEgw10 = 'IKEgw10'
    ESPgw10 = 'ESPgw10'


    datapath_ID1='004E46324301'
    datapath_ID2='004E46324302'
    datapath_ID3='004E46324303'
    datapath_ID4='004E46324304'
    datapath_ID5='004E46324305'
    datapath_ID6='004E46324306'
    datapath_ID7='004E46324307'
    datapath_ID8='004E46324308'
    datapath_ID9='004E46324309'
    datapath_ID10='004E4632430A'


    ''' configuration pour une topologie de taille 2 noeuds et 1 lien'''
    #'''
    # OpenFlow switch 1 settings
    listOF1port=[OFinterfacegw1, greInterfacelink1]

    # OpenFlow switch 2 settings
    listOF2port=[OFinterfacegw2, greInterfacelink1]
    #'''

    ''' configuration pour une topologie de taille 4 noeuds et 4 liens'''
    '''
    # OpenFlow switch 1 settings
    listOF1port=[OFinterfacegw1, greInterfacelink1, greInterfacelink2, greInterfacelink3]

    # OpenFlow switch 2 settings
    listOF2port=[OFinterfacegw2, greInterfacelink1]

    # OpenFlow switch 3 settings
    listOF3port=[OFinterfacegw3, greInterfacelink2, greInterfacelink4]

    # OpenFlow switch 4 settings
    listOF4port=[OFinterfacegw4, greInterfacelink3, greInterfacelink4]
    '''



    ''' configuration pour une topologie de taille 6 noeuds et 6 liens'''
    '''
    # OpenFlow switch 1 settings
    listOF1port=[OFinterfacegw1, greInterfacelink1, greInterfacelink2, greInterfacelink3]

    # OpenFlow switch 2 settings
    listOF2port=[OFinterfacegw2, greInterfacelink1, greInterfacelink4]

    # OpenFlow switch 3 settings
    listOF3port=[OFinterfacegw3, greInterfacelink5]

    # OpenFlow switch 4 settings
    listOF4port=[OFinterfacegw4, greInterfacelink6, greInterfacelink5]

    # OpenFlow switch 5 settings
    listOF5port=[OFinterfacegw5, greInterfacelink2, greInterfacelink6]

    # OpenFlow switch 6 settings
    listOF6port=[OFinterfacegw6, greInterfacelink3, greInterfacelink4]
    '''



    ''' configuration pour une topologie de taille 8 noeuds et 12 liens'''
    '''
    # OpenFlow switch 1 settings
    listOF1port=[OFinterfacegw1, greInterfacelink1, greInterfacelink2, greInterfacelink3]

    # OpenFlow switch 2 settings
    listOF2port=[OFinterfacegw2, greInterfacelink1, greInterfacelink4, greInterfacelink5]

    # OpenFlow switch 3 settings
    listOF3port=[OFinterfacegw3, greInterfacelink6, greInterfacelink7, greInterfacelink8]

    # OpenFlow switch 4 settings
    listOF4port=[OFinterfacegw4, greInterfacelink4, greInterfacelink6, greInterfacelink9, greInterfacelink10, greInterfacelink11]

    # OpenFlow switch 5 settings
    listOF5port=[OFinterfacegw5, greInterfacelink9]

    # OpenFlow switch 6 settings
    listOF6port=[OFinterfacegw6, greInterfacelink2, greInterfacelink7, greInterfacelink10, greInterfacelink12]

    # OpenFlow switch 7 settings
    listOF7port=[OFinterfacegw7, greInterfacelink3]

    # OpenFlow switch 8 settings
    listOF8port=[OFinterfacegw8, greInterfacelink5, greInterfacelink8, greInterfacelink11, greInterfacelink12]
    '''




    ''' configuration pour une topologie de taille 10 noeuds et 16 liens'''
    '''
    # OpenFlow switch 1 settings
    listOF1port=[OFinterfacegw1, greInterfacelink1, greInterfacelink2, greInterfacelink3, greInterfacelink4]

    # OpenFlow switch 2 settings
    listOF2port=[OFinterfacegw2, greInterfacelink1, greInterfacelink5, greInterfacelink6, greInterfacelink7, greInterfacelink8, greInterfacelink9]

    # OpenFlow switch 3 settings
    listOF3port=[OFinterfacegw3, greInterfacelink2, greInterfacelink5, greInterfacelink10, greInterfacelink11]

    # OpenFlow switch 4 settings
    listOF4port=[OFinterfacegw4, greInterfacelink10]

    # OpenFlow switch 5 settings
    listOF5port=[OFinterfacegw5, greInterfacelink6, greInterfacelink12]

    # OpenFlow switch 6 settings
    listOF6port=[OFinterfacegw6, greInterfacelink3, greInterfacelink9, greInterfacelink14]

    # OpenFlow switch 7 settings
    listOF7port=[OFinterfacegw7, greInterfacelink7, greInterfacelink15, greInterfacelink16]

    # OpenFlow switch 8 settings
    listOF8port=[OFinterfacegw8, greInterfacelink8, greInterfacelink13, greInterfacelink15]

    # OpenFlow switch 9 settings
    listOF9port=[OFinterfacegw9, greInterfacelink9, greInterfacelink11, greInterfacelink16]

    # OpenFlow switch 10 settings
    listOF10port=[OFinterfacegw10, greInterfacelink4, greInterfacelink12, greInterfacelink14]
    '''

    # OpenFlow controller settings

    NOX='157.159.249.166'
    NOXport='6633'



    ''' Configuration des gateways'''
    start_time = int(round(time.time() * 1000))




    '''
    gw1.configure_protocol_IPSEC(gw1, gw1Address, tunnelinterfacegw1, IKEgw1, ESPgw1)
    gw2.configure_protocol_IPSEC(gw2, gw2Address, tunnelinterfacegw2, IKEgw2, ESPgw2)
    #gw3.configure_protocol_IPSEC(gw3, gw3Address, tunnelinterfacegw3, IKEgw3, ESPgw3)
    #gw4.configure_protocol_IPSEC(gw4, gw4Address, tunnelinterfacegw4, IKEgw4, ESPgw4)
    #gw5.configure_protocol_IPSEC(gw5, gw5Address, tunnelinterfacegw5, IKEgw5, ESPgw5)
    #gw6.configure_protocol_IPSEC(gw6, gw6Address, tunnelinterfacegw6, IKEgw6, ESPgw6)
    #gw7.configure_protocol_IPSEC(gw7, gw7Address, tunnelinterfacegw7, IKEgw7, ESPgw7)
    #gw8.configure_protocol_IPSEC(gw8, gw8Address, tunnelinterfacegw8, IKEgw8, ESPgw8)
    #gw9.configure_protocol_IPSEC(gw9, gw9Address, tunnelinterfacegw9, IKEgw9, ESPgw9)
    #gw10.configure_protocol_IPSEC(gw10, gw10Address, tunnelinterfacegw10, IKEgw10, ESPgw10)
    '''

    ''' Connecte les gateways'''
    ''' configuration 2 noeuds 1 links'''
    #gw1.connect_gw(gw1, greInterfacelink1, greAddresslink1gw1, prefix, tunnelnumlink1, tunnelProtocol, gw1Address, gw2Address, authenticationKeylink1, IKEgw1, ESPgw1)
    #gw2.connect_gw(gw2, greInterfacelink1, greAddresslink1gw2, prefix, tunnelnumlink1, tunnelProtocol, gw2Address, gw1Address, authenticationKeylink1, IKEgw2, ESPgw2)



    ''' configuration 4 noeuds 4 links'''
    '''
    gw1.connect_gw(gw1, greInterfacelink1, greAddresslink1gw1, prefix, tunnelnumlink1, tunnelProtocol, gw1Address, gw2Address, authenticationKeylink1, IKEgw1, ESPgw1)
    gw2.connect_gw(gw2, greInterfacelink1, greAddresslink1gw2, prefix, tunnelnumlink1, tunnelProtocol, gw2Address, gw1Address, authenticationKeylink1, IKEgw2, ESPgw2)

    gw1.connect_gw(gw1, greInterfacelink2, greAddresslink2gw1, prefix, tunnelnumlink2, tunnelProtocol, gw1Address, gw3Address, authenticationKeylink2, IKEgw1, ESPgw1)
    gw3.connect_gw(gw3, greInterfacelink2, greAddresslink2gw2, prefix, tunnelnumlink2, tunnelProtocol, gw3Address, gw1Address, authenticationKeylink2, IKEgw3, ESPgw3)

    gw1.connect_gw(gw1, greInterfacelink3, greAddresslink3gw1, prefix, tunnelnumlink3, tunnelProtocol, gw1Address, gw4Address, authenticationKeylink3, IKEgw1, ESPgw1)
    gw4.connect_gw(gw4, greInterfacelink3, greAddresslink3gw2, prefix, tunnelnumlink3, tunnelProtocol, gw4Address, gw1Address, authenticationKeylink3, IKEgw4, ESPgw4)

    gw3.connect_gw(gw3, greInterfacelink4, greAddresslink4gw1, prefix, tunnelnumlink4, tunnelProtocol, gw3Address, gw4Address, authenticationKeylink4, IKEgw3, ESPgw3)
    gw4.connect_gw(gw4, greInterfacelink4, greAddresslink4gw2, prefix, tunnelnumlink4, tunnelProtocol, gw4Address, gw3Address, authenticationKeylink4, IKEgw4, ESPgw4)
    '''


    ''' configuration 6 noeuds 6 links'''
    '''
    gw1.connect_gw(gw1, greInterfacelink1, greAddresslink1gw1, prefix, tunnelnumlink1, tunnelProtocol, gw1Address, gw2Address, authenticationKeylink1, IKEgw1, ESPgw1)
    gw2.connect_gw(gw2, greInterfacelink1, greAddresslink1gw2, prefix, tunnelnumlink1, tunnelProtocol, gw2Address, gw1Address, authenticationKeylink1, IKEgw2, ESPgw2)

    gw1.connect_gw(gw1, greInterfacelink2, greAddresslink2gw1, prefix, tunnelnumlink2, tunnelProtocol, gw1Address, gw5Address, authenticationKeylink2, IKEgw1, ESPgw1)
    gw5.connect_gw(gw5, greInterfacelink2, greAddresslink2gw2, prefix, tunnelnumlink2, tunnelProtocol, gw5Address, gw1Address, authenticationKeylink2, IKEgw5, ESPgw5)

    gw1.connect_gw(gw1, greInterfacelink3, greAddresslink3gw1, prefix, tunnelnumlink3, tunnelProtocol, gw1Address, gw6Address, authenticationKeylink3, IKEgw1, ESPgw1)
    gw6.connect_gw(gw6, greInterfacelink3, greAddresslink3gw2, prefix, tunnelnumlink3, tunnelProtocol, gw6Address, gw1Address, authenticationKeylink3, IKEgw6, ESPgw6)

    gw2.connect_gw(gw2, greInterfacelink4, greAddresslink4gw1, prefix, tunnelnumlink4, tunnelProtocol, gw2Address, gw6Address, authenticationKeylink4, IKEgw2, ESPgw2)
    gw6.connect_gw(gw6, greInterfacelink4, greAddresslink4gw2, prefix, tunnelnumlink4, tunnelProtocol, gw6Address, gw2Address, authenticationKeylink4, IKEgw6, ESPgw6)

    gw3.connect_gw(gw3, greInterfacelink5, greAddresslink5gw1, prefix, tunnelnumlink5, tunnelProtocol, gw3Address, gw4Address, authenticationKeylink5, IKEgw3, ESPgw3)
    gw4.connect_gw(gw4, greInterfacelink5, greAddresslink5gw2, prefix, tunnelnumlink5, tunnelProtocol, gw4Address, gw3Address, authenticationKeylink5, IKEgw4, ESPgw4)

    gw4.connect_gw(gw4, greInterfacelink6, greAddresslink6gw1, prefix, tunnelnumlink6, tunnelProtocol, gw4Address, gw5Address, authenticationKeylink6, IKEgw4, ESPgw4)
    gw5.connect_gw(gw5, greInterfacelink6, greAddresslink6gw2, prefix, tunnelnumlink6, tunnelProtocol, gw5Address, gw4Address, authenticationKeylink6, IKEgw5, ESPgw5)
    '''



    ''' configuration 8 noeuds 12 links'''
    '''
    gw1.connect_gw(gw1, greInterfacelink1, greAddresslink1gw1, prefix, tunnelnumlink1, tunnelProtocol, gw1Address, gw2Address, authenticationKeylink1, IKEgw1, ESPgw1)
    gw2.connect_gw(gw2, greInterfacelink1, greAddresslink1gw2, prefix, tunnelnumlink1, tunnelProtocol, gw2Address, gw1Address, authenticationKeylink1, IKEgw2, ESPgw2)

    gw1.connect_gw(gw1, greInterfacelink2, greAddresslink2gw1, prefix, tunnelnumlink2, tunnelProtocol, gw1Address, gw6Address, authenticationKeylink2, IKEgw1, ESPgw1)
    gw6.connect_gw(gw6, greInterfacelink2, greAddresslink2gw2, prefix, tunnelnumlink2, tunnelProtocol, gw6Address, gw1Address, authenticationKeylink2, IKEgw6, ESPgw6)

    gw1.connect_gw(gw1, greInterfacelink3, greAddresslink3gw1, prefix, tunnelnumlink3, tunnelProtocol, gw1Address, gw7Address, authenticationKeylink3, IKEgw1, ESPgw1)
    gw7.connect_gw(gw7, greInterfacelink3, greAddresslink3gw2, prefix, tunnelnumlink3, tunnelProtocol, gw7Address, gw1Address, authenticationKeylink3, IKEgw7, ESPgw7)

    gw2.connect_gw(gw2, greInterfacelink4, greAddresslink4gw1, prefix, tunnelnumlink4, tunnelProtocol, gw2Address, gw4Address, authenticationKeylink4, IKEgw2, ESPgw2)
    gw4.connect_gw(gw4, greInterfacelink4, greAddresslink4gw2, prefix, tunnelnumlink4, tunnelProtocol, gw4Address, gw2Address, authenticationKeylink4, IKEgw4, ESPgw4)

    gw2.connect_gw(gw2, greInterfacelink5, greAddresslink5gw1, prefix, tunnelnumlink5, tunnelProtocol, gw2Address, gw8Address, authenticationKeylink5, IKEgw2, ESPgw2)
    gw8.connect_gw(gw8, greInterfacelink5, greAddresslink5gw2, prefix, tunnelnumlink5, tunnelProtocol, gw8Address, gw2Address, authenticationKeylink5, IKEgw8, ESPgw8)

    gw4.connect_gw(gw4, greInterfacelink6, greAddresslink6gw1, prefix, tunnelnumlink6, tunnelProtocol, gw4Address, gw3Address, authenticationKeylink6, IKEgw4, ESPgw4)
    gw3.connect_gw(gw3, greInterfacelink6, greAddresslink6gw2, prefix, tunnelnumlink6, tunnelProtocol, gw3Address, gw4Address, authenticationKeylink6, IKEgw3, ESPgw3)

    gw3.connect_gw(gw3, greInterfacelink7, greAddresslink7gw1, prefix, tunnelnumlink7, tunnelProtocol, gw3Address, gw6Address, authenticationKeylink7, IKEgw3, ESPgw3)
    gw6.connect_gw(gw6, greInterfacelink7, greAddresslink7gw2, prefix, tunnelnumlink7, tunnelProtocol, gw6Address, gw3Address, authenticationKeylink7, IKEgw6, ESPgw6)

    gw3.connect_gw(gw3, greInterfacelink8, greAddresslink8gw1, prefix, tunnelnumlink8, tunnelProtocol, gw3Address, gw8Address, authenticationKeylink8, IKEgw3, ESPgw3)
    gw8.connect_gw(gw8, greInterfacelink8, greAddresslink8gw2, prefix, tunnelnumlink8, tunnelProtocol, gw8Address, gw3Address, authenticationKeylink8, IKEgw8, ESPgw8)

    gw4.connect_gw(gw4, greInterfacelink9, greAddresslink9gw1, prefix, tunnelnumlink9, tunnelProtocol, gw4Address, gw5Address, authenticationKeylink9, IKEgw4, ESPgw4)
    gw5.connect_gw(gw5, greInterfacelink9, greAddresslink9gw2, prefix, tunnelnumlink9, tunnelProtocol, gw5Address, gw4Address, authenticationKeylink9, IKEgw5, ESPgw5)

    gw4.connect_gw(gw4, greInterfacelink10, greAddresslink10gw1, prefix, tunnelnumlink10, tunnelProtocol, gw4Address, gw6Address, authenticationKeylink10, IKEgw4, ESPgw4)
    gw6.connect_gw(gw6, greInterfacelink10, greAddresslink10gw2, prefix, tunnelnumlink10, tunnelProtocol, gw6Address, gw4Address, authenticationKeylink10, IKEgw6, ESPgw6)

    gw8.connect_gw(gw8, greInterfacelink11, greAddresslink11gw1, prefix, tunnelnumlink11, tunnelProtocol, gw8Address, gw4Address, authenticationKeylink11, IKEgw8, ESPgw8)
    gw4.connect_gw(gw4, greInterfacelink11, greAddresslink11gw2, prefix, tunnelnumlink11, tunnelProtocol, gw4Address, gw8Address, authenticationKeylink11, IKEgw4, ESPgw4)

    gw6.connect_gw(gw6, greInterfacelink12, greAddresslink12gw1, prefix, tunnelnumlink12, tunnelProtocol, gw6Address, gw8Address, authenticationKeylink12, IKEgw6, ESPgw6)
    gw8.connect_gw(gw8, greInterfacelink12, greAddresslink12gw2, prefix, tunnelnumlink12, tunnelProtocol, gw8Address, gw6Address, authenticationKeylink12, IKEgw8, ESPgw8)
    '''


    ''' configuration 10 noeuds 16 links'''
    '''
    gw1.connect_gw(gw1, greInterfacelink1, greAddresslink1gw1, prefix, tunnelnumlink1, tunnelProtocol, gw1Address, gw2Address, authenticationKeylink1, IKEgw1, ESPgw1)
    gw2.connect_gw(gw2, greInterfacelink1, greAddresslink1gw2, prefix, tunnelnumlink1, tunnelProtocol, gw2Address, gw1Address, authenticationKeylink1, IKEgw2, ESPgw2)

    gw1.connect_gw(gw1, greInterfacelink2, greAddresslink2gw1, prefix, tunnelnumlink2, tunnelProtocol, gw1Address, gw3Address, authenticationKeylink2, IKEgw1, ESPgw1)
    gw3.connect_gw(gw3, greInterfacelink2, greAddresslink2gw2, prefix, tunnelnumlink2, tunnelProtocol, gw3Address, gw1Address, authenticationKeylink2, IKEgw3, ESPgw3)

    gw1.connect_gw(gw1, greInterfacelink3, greAddresslink3gw1, prefix, tunnelnumlink3, tunnelProtocol, gw1Address, gw6Address, authenticationKeylink3, IKEgw1, ESPgw1)
    gw6.connect_gw(gw6, greInterfacelink3, greAddresslink3gw2, prefix, tunnelnumlink3, tunnelProtocol, gw6Address, gw1Address, authenticationKeylink3, IKEgw6, ESPgw6)

    gw1.connect_gw(gw1, greInterfacelink4, greAddresslink4gw1, prefix, tunnelnumlink4, tunnelProtocol, gw1Address, gw10Address, authenticationKeylink4, IKEgw1, ESPgw1)
    gw10.connect_gw(gw10, greInterfacelink4, greAddresslink4gw2, prefix, tunnelnumlink4, tunnelProtocol, gw10Address, gw1Address, authenticationKeylink4, IKEgw10, ESPgw10)

    gw2.connect_gw(gw2, greInterfacelink5, greAddresslink5gw1, prefix, tunnelnumlink5, tunnelProtocol, gw2Address, gw3Address, authenticationKeylink5, IKEgw2, ESPgw2)
    gw3.connect_gw(gw3, greInterfacelink5, greAddresslink5gw2, prefix, tunnelnumlink5, tunnelProtocol, gw3Address, gw2Address, authenticationKeylink5, IKEgw3, ESPgw3)

    gw2.connect_gw(gw2, greInterfacelink6, greAddresslink6gw1, prefix, tunnelnumlink6, tunnelProtocol, gw2Address, gw5Address, authenticationKeylink6, IKEgw2, ESPgw2)
    gw5.connect_gw(gw5, greInterfacelink6, greAddresslink6gw2, prefix, tunnelnumlink6, tunnelProtocol, gw5Address, gw2Address, authenticationKeylink6, IKEgw5, ESPgw5)

    gw2.connect_gw(gw2, greInterfacelink7, greAddresslink7gw1, prefix, tunnelnumlink7, tunnelProtocol, gw2Address, gw7Address, authenticationKeylink7, IKEgw2, ESPgw2)
    gw7.connect_gw(gw7, greInterfacelink7, greAddresslink7gw2, prefix, tunnelnumlink7, tunnelProtocol, gw7Address, gw2Address, authenticationKeylink7, IKEgw7, ESPgw7)

    gw2.connect_gw(gw2, greInterfacelink8, greAddresslink8gw1, prefix, tunnelnumlink8, tunnelProtocol, gw2Address, gw8Address, authenticationKeylink8, IKEgw2, ESPgw2)
    gw8.connect_gw(gw8, greInterfacelink8, greAddresslink8gw2, prefix, tunnelnumlink8, tunnelProtocol, gw8Address, gw2Address, authenticationKeylink8, IKEgw8, ESPgw8)

    gw2.connect_gw(gw2, greInterfacelink9, greAddresslink9gw1, prefix, tunnelnumlink9, tunnelProtocol, gw2Address, gw9Address, authenticationKeylink9, IKEgw2, ESPgw2)
    gw9.connect_gw(gw9, greInterfacelink9, greAddresslink9gw2, prefix, tunnelnumlink9, tunnelProtocol, gw9Address, gw2Address, authenticationKeylink9, IKEgw9, ESPgw9)

    gw3.connect_gw(gw3, greInterfacelink10, greAddresslink10gw1, prefix, tunnelnumlink10, tunnelProtocol, gw3Address, gw4Address, authenticationKeylink10, IKEgw3, ESPgw3)
    gw4.connect_gw(gw4, greInterfacelink10, greAddresslink10gw2, prefix, tunnelnumlink10, tunnelProtocol, gw4Address, gw3Address, authenticationKeylink10, IKEgw4, ESPgw4)

    gw3.connect_gw(gw3, greInterfacelink11, greAddresslink11gw1, prefix, tunnelnumlink11, tunnelProtocol, gw3Address, gw9Address, authenticationKeylink11, IKEgw3, ESPgw3)
    gw9.connect_gw(gw9, greInterfacelink11, greAddresslink11gw2, prefix, tunnelnumlink11, tunnelProtocol, gw9Address, gw3Address, authenticationKeylink11, IKEgw9, ESPgw9)

    gw5.connect_gw(gw5, greInterfacelink12, greAddresslink12gw1, prefix, tunnelnumlink12, tunnelProtocol, gw5Address, gw10Address, authenticationKeylink12, IKEgw5, ESPgw5)
    gw10.connect_gw(gw10, greInterfacelink12, greAddresslink12gw2, prefix, tunnelnumlink12, tunnelProtocol, gw10Address, gw5Address, authenticationKeylink12, IKEgw10, ESPgw10)

    gw6.connect_gw(gw6, greInterfacelink13, greAddresslink13gw1, prefix, tunnelnumlink13, tunnelProtocol, gw6Address, gw8Address, authenticationKeylink13, IKEgw6, ESPgw6)
    gw8.connect_gw(gw8, greInterfacelink13, greAddresslink13gw2, prefix, tunnelnumlink13, tunnelProtocol, gw8Address, gw6Address, authenticationKeylink13, IKEgw8, ESPgw8)

    gw6.connect_gw(gw6, greInterfacelink14, greAddresslink14gw1, prefix, tunnelnumlink14, tunnelProtocol, gw6Address, gw10Address, authenticationKeylink14, IKEgw6, ESPgw6)
    gw10.connect_gw(gw10, greInterfacelink14, greAddresslink14gw2, prefix, tunnelnumlink14, tunnelProtocol, gw10Address, gw6Address, authenticationKeylink14, IKEgw10, ESPgw10)

    gw7.connect_gw(gw7, greInterfacelink15, greAddresslink15gw1, prefix, tunnelnumlink15, tunnelProtocol, gw7Address, gw8Address, authenticationKeylink15, IKEgw7, ESPgw7)
    gw8.connect_gw(gw8, greInterfacelink15, greAddresslink15gw2, prefix, tunnelnumlink15, tunnelProtocol, gw8Address, gw7Address, authenticationKeylink15, IKEgw8, ESPgw8)

    gw7.connect_gw(gw7, greInterfacelink16, greAddresslink16gw1, prefix, tunnelnumlink16, tunnelProtocol, gw7Address, gw9Address, authenticationKeylink16, IKEgw7, ESPgw7)
    gw9.connect_gw(gw9, greInterfacelink16, greAddresslink16gw2, prefix, tunnelnumlink16, tunnelProtocol, gw9Address, gw7Address, authenticationKeylink16, IKEgw9, ESPgw9)
    '''


    ''' configure openflow'''
    '''
    gw1.connect_openflow(gw1, gw1Address, datapath_ID1, listOF1port, NOX, NOXport)
    gw2.connect_openflow(gw2, gw2Address, datapath_ID2, listOF2port, NOX, NOXport)
    #gw3.connect_openflow(gw3, gw3Address, datapath_ID3, listOF3port, NOX, NOXport)
    #gw4.connect_openflow(gw4, gw4Address, datapath_ID4, listOF4port, NOX, NOXport)
    #gw5.connect_openflow(gw5, gw5Address, datapath_ID5, listOF5port, NOX, NOXport)
    #gw6.connect_openflow(gw6, gw6Address, datapath_ID6, listOF6port, NOX, NOXport)
    #gw7.connect_openflow(gw7, gw7Address, datapath_ID7, listOF7port, NOX, NOXport)
    #gw8.connect_openflow(gw8, gw8Address, datapath_ID8, listOF8port, NOX, NOXport)
    #gw9.connect_openflow(gw9, gw9Address, datapath_ID9, listOF9port, NOX, NOXport)
    #gw10.connect_openflow(gw10, gw10Address, datapath_ID10, listOF10port, NOX, NOXport)
    '''

    ''' stop les deux gateways'''
    #'''
    gw1.stop_gw(gw1, gw1Address)
    gw2.stop_gw(gw2, gw2Address)
    #gw3.stop_gw(gw3, gw3Address)
    #gw4.stop_gw(gw4, gw4Address)
    #gw5.stop_gw(gw5, gw5Address)
    #gw6.stop_gw(gw6, gw6Address)
    #gw7.stop_gw(gw7, gw7Address)
    #gw8.stop_gw(gw8, gw8Address)
    #gw9.stop_gw(gw9, gw9Address)
    #gw10.stop_gw(gw10, gw10Address)
    #'''


    execution_time = int(round(time.time() * 1000)) - start_time
    file = open("executionTIMEOF", "w")
    file.write("execution time was " + str(execution_time) + " ms.\n")
    file.close()
