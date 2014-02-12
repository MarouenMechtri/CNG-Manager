#  Copyright 2013 Institut Mines-Telecom - Telecom SudParis
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Created on Jun 4, 2013

@author: Marouen Mechtri
@contact: marouen.mechtri@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

import pyocni.pyocni_tools.config as config
from pyocni.backends.drivers.client import OCCIdriverClient
# getting the Logger
logger = config.logger

class ovpnDriver:
    """ Simple shell to run a command on the host """

    def configure(self, cmd):
        cmd_conf = '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper '
        cmdConfig=    cmd_conf + 'begin &&' + cmd_conf + cmd + '&&' + cmd_conf + 'commit &&' + cmd_conf + 'end &&' + cmd_conf + 'save'
        return cmdConfig



    def load(self):
        return self.configure('load')


    def delete_openVPN(self, interfaceName):
        """run <command>
        Execute this command on all hosts in the list"""
        return self.configure('delete interfaces openvpn ' + interfaceName)


    def delete_staticRoute_interface(self, dstNetwork):
        """run <command>
        Execute this command on all hosts in the list"""
        return self.configure('delete protocols static interface-route ' + dstNetwork)



    '''
    site-to-site Configuration (openVPN between two site)
    '''


    def configure_openVPN_Site_to_Site(self, interfaceName, localAddress, remoteAddress, remoteHost):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd_conf = '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper '
        return  self.configure(
            'set interfaces openvpn ' + interfaceName +
            '&&' + cmd_conf + 'set interfaces openvpn ' + interfaceName + ' local-address ' + localAddress +
            '&&' + cmd_conf + 'set interfaces openvpn ' + interfaceName + ' mode site-to-site' +
            '&&' + cmd_conf + 'set interfaces openvpn ' + interfaceName + ' remote-address ' + remoteAddress +
            '&&' + cmd_conf + 'set interfaces openvpn ' + interfaceName + ' remote-host ' + remoteHost +
            '&&' + cmd_conf + 'set interfaces openvpn ' + interfaceName + ' shared-secret-key-file /config/auth/secret ')



    def configure_staticRoute_interface(self, dstNetwork, interfaceName):
        return self.configure('set protocols static interface-route ' + dstNetwork + ' next-hop-interface ' + interfaceName)



    def configure_site_to_site_openvpn(self, gwinstance, address, interfaceName, localAddress, remoteAddress, remoteHost, dstNetwork):

        cmds=[]
        logger.debug('\n[OpenVPN Driver]-----Establishing Tunnel between ' + address + ' and ' + remoteHost +  '...............OK')

        cmds.append(gwinstance.configure_openVPN_Site_to_Site(interfaceName, localAddress, remoteAddress, remoteHost))
        logger.debug('\n[OpenVPN Driver]-----Configuring gateway (' + address + ') to reach network ' + dstNetwork + '..............OK')

        cmds.append(gwinstance.configure_staticRoute_interface(dstNetwork, interfaceName))

        gwinstance.execute_many_cmd_Cosacs(address, cmds)



    def stop_site_to_site_OVPN(self, gwinstance, gwaddress, interfaceName, dstNetwork):
        cmds=[]
        cmds.append(gwinstance.delete_openVPN(interfaceName))
        logger.debug('\n[OpenVPN Driver]-----Stoping openVPN tunnel......OK')
        cmds.append(gwinstance.delete_staticRoute_interface(dstNetwork))
        logger.debug('\n[OpenVPN Driver]-----Stoping protocols......OK')

        gwinstance.execute_many_cmd_Cosacs(gwaddress, cmds)



    '''
    remote-site Configuration (openVPN between two site)
    '''



    def configure_Server_openVPN_remoteSite(self, serverSubnet, interfaceName):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd_conf = '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper '
        return  self.configure(
            'set interfaces openvpn ' + interfaceName +
            '&&' + cmd_conf + 'set interfaces openvpn vtun0 mode server' +
            '&&' + cmd_conf + 'set interfaces openvpn vtun0 server subnet ' + serverSubnet +
            '&&' + cmd_conf + 'set interfaces openvpn vtun0 tls ca-cert-file /config/auth/ca.crt' +
            '&&' + cmd_conf + 'set interfaces openvpn vtun0 tls cert-file /config/auth/server.crt' +
            '&&' + cmd_conf + 'set interfaces openvpn vtun0 tls dh-file /config/auth/dh.pem' +
            '&&' + cmd_conf + 'set interfaces openvpn vtun0 tls key-file /config/auth/server.key ')


    def configure_Client_openVPN_remoteSite(self, serverAddress, interfaceName):
        """run <command>
        Execute this command on all hosts in the list"""
        cmd_conf = '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper '
        return  self.configure(
            'set interfaces openvpn ' + interfaceName +
            '&&' + cmd_conf + 'set interfaces openvpn vtun0 mode client' +
            '&&' + cmd_conf + 'set interfaces openvpn vtun0 remote-host ' + serverAddress +
            '&&' + cmd_conf + 'set interfaces openvpn vtun0 tls ca-cert-file /config/auth/ca.crt' +
            '&&' + cmd_conf + 'set interfaces openvpn vtun0 tls cert-file /config/auth/client.crt' +
            '&&' + cmd_conf + 'set interfaces openvpn vtun0 tls key-file /config/auth/client.key')



    def configure_server_openvpn(self, gwinstance, address, serverSubnet, interfaceName):

        cmds=[]
        cmds.append(gwinstance.configure_Server_openVPN_remoteSite(serverSubnet, interfaceName))

        gwinstance.execute_many_cmd_Cosacs(address, cmds)



    def configure_client_openvpn(self, gwinstance, address, serverAddress, interfaceName):

        cmds=[]
        cmds.append(gwinstance.configure_Client_openVPN_remoteSite(serverAddress, interfaceName))

        gwinstance.execute_many_cmd_Cosacs(address, cmds)


    def stop_gw(self, gwinstance, gwaddress, interfaceName):
        cmds=[]
        cmds.append(gwinstance.delete_openVPN(interfaceName))
        logger.debug('\n[OpenVPN Driver]-----Stoping openVPN tunnel......OK')

        gwinstance.execute_many_cmd_Cosacs(gwaddress, cmds)





    def execute_many_cmd_Cosacs(self, address, cmds):
        for item in cmds:
            attributes = {
                'name': '',
                'syntax': item,
                'nature': 'system',
                'status': '',
                'identifier': ''
            }
            cl = OCCIdriverClient(address, '8286', 'COSACS', 'script', attributes)
            cl.Post()

        cosacsStart = {
            'name': 'cosacs:start'
        }

        startcmd = OCCIdriverClient(address, '8286', 'COSACS', 'script', cosacsStart)
        startcmd.Post()
