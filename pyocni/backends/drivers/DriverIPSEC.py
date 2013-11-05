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
Created on Feb 25, 2013

@author: Marouen Mechtri
@contact: marouen.mechtri@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

import pyocni.pyocni_tools.config as config
from pyocni.backends.drivers.client import OCCIdriverClient
# getting the Logger
logger = config.logger

class ipsecDriver:
    """ Simple shell to run a command on the host """

    def configure(self, cmd):
        cmd_conf = '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper '
        cmdConfig=    cmd_conf + 'begin &&' + cmd_conf + cmd + '&&' + cmd_conf + 'commit &&' + cmd_conf + 'end &&' + cmd_conf + 'save'
        return cmdConfig

    def load(self):
        return self.configure('load')





    '''
    Configure default gateway user VM
    '''

    def config_gwVM(self, addressVM, gwAddress, ethername):
        return '/home/vyatta/executeRemote_cmd '+addressVM+' '+gwAddress+' '+ethername
        




    '''
    DHCP Configuration
    '''

    def configure_DHCP(self, namePool, subnet, start, stop, gatewayAddress, dnsAddress):
        cmd_conf = '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper '
        return self.configure(
            'set service dhcp-server shared-network-name ' + namePool + ' subnet ' + subnet + ' start ' + start + ' stop ' + stop +
            '&&' + cmd_conf + 'set service dhcp-server shared-network-name ' + namePool + ' subnet ' + subnet + ' default-router ' + gatewayAddress +
            '&&' + cmd_conf + 'set service dhcp-server shared-network-name ' + namePool + ' subnet ' + subnet + ' dns-server ' + dnsAddress)

    def configure_DHCP_addrPool(self, namePool, subnet, start, stop):
        return self.configure(
            'set service dhcp-server shared-network-name ' + namePool + ' subnet ' + subnet + ' start ' + start + ' stop ' + stop)

    def configure_DHCP_defaultGW(self, namePool, subnet, gatewayAddress):
        return self.configure(
            'set service dhcp-server shared-network-name ' + namePool + ' subnet ' + subnet + ' default-router ' + gatewayAddress)

    def configure_DHCP_dnsServer(self, namePool, subnet, dnsAddress):
        return self.configure(
            'set service dhcp-server shared-network-name ' + namePool + ' subnet ' + subnet + ' dns-server ' + dnsAddress)





    '''
    NAT Configuration
    '''

    def configure_NAT(self, ruleNumb, address, outInterface, type):
        cmd_conf = '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper '
        return self.configure(
            'set service nat rule ' + ruleNumb + ' source address ' + address + '&&' + cmd_conf +
            'set service nat rule ' + ruleNumb + ' outbound-interface ' + outInterface + '&&' + cmd_conf +
            'set service nat rule ' + ruleNumb + ' type ' + type)

    def configure_Interface(self, interface, address):
        return self.configure('set interfaces ethernet ' + interface + ' address ' + address)

    def configure_DNSServer(self, dnsAddress):
        return self.configure('set system name-server ' + dnsAddress)

    def configure_DefaultGW(self, gatewayAddress):
        return self.configure('set system gateway-address ' + gatewayAddress)

    def configure_NameServer(self, nameServer):
        return self.configure('set system host-name ' + nameServer)





    '''
    GRE Configuration
    '''

    def configure_GRE(self, tunnelName, tunnelAddress, description, mode, localAddress, remoteAddress):
        cmd_conf = '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper '
        return self.configure(
            'set interfaces tunnel ' + tunnelName + ' address ' + tunnelAddress +
            '&&' + cmd_conf + 'set interfaces tunnel ' + tunnelName + ' description "' + description + '"' +
            '&&' + cmd_conf + 'set interfaces tunnel ' + tunnelName + ' encapsulation ' + mode +
            '&&' + cmd_conf + 'set interfaces tunnel ' + tunnelName + ' multicast enable ' +
            '&&' + cmd_conf + 'set interfaces tunnel ' + tunnelName + ' local-ip ' + localAddress +
            '&&' + cmd_conf + 'set interfaces tunnel ' + tunnelName + ' remote-ip ' + remoteAddress)

    def configure_Tunnel_interface(self, tunnelName, tunnelAddress):
        return self.configure('set interfaces tunnel ' + tunnelName + ' address ' + tunnelAddress)

    def configure_Tunnel_description(self, tunnelName, description):
        return self.configure('set interfaces tunnel ' + tunnelName + ' description "' + description + '"')

    def configure_Tunnel_encapsulationMode(self, tunnelName, mode):
        return self.configure('set interfaces tunnel ' + tunnelName + ' encapsulation ' + mode)

    def configure_Tunnel_multicast(self, tunnelName):
        return self.configure('set interfaces tunnel ' + tunnelName + ' multicast enable')

    def configure_Tunnel_localIP(self, tunnelName, localAddress):
        return self.configure('set interfaces tunnel ' + tunnelName + ' local-ip ' + localAddress)

    def configure_Tunnel_remoteIP(self, tunnelName, remoteAddress):
        return self.configure('set interfaces tunnel ' + tunnelName + ' remote-ip ' + remoteAddress)

    def configure_staticRoute(self, dstNetwork, nextHop):
        return self.configure('set protocols static route ' + dstNetwork + ' next-hop ' + nextHop)





    '''
    IPSEC Configuration
    '''

    def configure_IKE_proposal(self, ikeName, proposalNum, encryption, hash):
        cmd_conf = '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper '
        return self.configure(
            'set vpn ipsec ike-group ' + ikeName + ' proposal ' + proposalNum + ' encryption ' + encryption +
            '&&' + cmd_conf + 'set vpn ipsec ike-group ' + ikeName + ' proposal ' + proposalNum + ' hash ' + hash)

    def configure_Protocol_lifetime(self, protocol, Name, lifetime):
        return self.configure('set vpn ipsec ' + protocol + '-group ' + Name + ' lifetime ' + lifetime)

    def configure_ESP_proposal(self, espName, proposalNum, encryption, hash):
        cmd_conf = '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper '
        return self.configure(
            'set vpn ipsec esp-group ' + espName + ' proposal ' + proposalNum + ' encryption ' + encryption +
            '&&' + cmd_conf + 'set vpn ipsec esp-group ' + espName + ' proposal ' + proposalNum + ' hash ' + hash)

    def configure_ESP_lifetime(self, espName, lifetime):
        return self.configure('set vpn ipsec esp-group ' + espName + ' lifetime ' + lifetime)

    def configure_IPSEC_interface(self, interface):
        return self.configure('set vpn ipsec ipsec-interfaces interface ' + interface)





    '''
    site-to-site Configuration (Ipsec between two site)
    '''

    def configure_IPSEC_SiteToSite(self, remoteAddress, authenticationKey, esp, ike, localAddress, tunnelNum, protocol):
        cmd_conf = '/opt/vyatta/sbin/vyatta-cfg-cmd-wrapper '
        return  self.configure(
            'set vpn ipsec site-to-site peer ' + remoteAddress + ' authentication mode pre-shared-secret ' +
            '&&' + cmd_conf + 'edit vpn ipsec site-to-site peer ' + remoteAddress +
            '&&' + cmd_conf + 'set authentication pre-shared-secret ' + authenticationKey +
            '&&' + cmd_conf + 'set default-esp-group ' + esp +
            '&&' + cmd_conf + 'set ike-group ' + ike +
            '&&' + cmd_conf + 'set local-ip ' + localAddress +
            '&&' + cmd_conf + 'set tunnel ' + tunnelNum + ' protocol ' + protocol +
            '&&' + cmd_conf + 'top ')

    def configure_IPSEC_SiteToSite_withfile(self, remoteAddress, authenticationKey, esp, ike, localAddress, tunnelNum, protocol):
        return '/home/vyatta/addipsec '+remoteAddress+' '+authenticationKey+' '+esp+' '+ike+' '+localAddress+' '+tunnelNum+' '+protocol

    def delete_vpn(self, address):
        return self.configure('delete vpn ipsec site-to-site peer ' + address)

    def delete_protocols(self, network):
        return self.configure('delete protocols static route ' + network)

    def delete_tunnel(self, tunnelname):
        return self.configure('delete interfaces tunnel ' + tunnelname)


    def configure_protocol_IPSEC(self, gwinstance, address, ethername, IKEname, ESPname):

        cmds=[]
        cmds.append(gwinstance.configure_IPSEC_interface(ethername))
        logger.debug('\n[IPSEC Driver]-----Configure IPSEC interface for the CNG: ' + address + '...............OK')


        cmds.append(gwinstance.configure_IKE_proposal(IKEname, '1', 'aes256','sha1'))
        cmds.append(gwinstance.configure_IKE_proposal(IKEname, '2', 'aes128','sha1'))
        cmds.append(gwinstance.configure_Protocol_lifetime('ike', IKEname, '3600'))
        logger.debug('\n[IPSEC Driver]-----Configure IKE for the CNG: ' + address + '...............OK')

        cmds.append(gwinstance.configure_ESP_proposal(ESPname, '1', 'aes256','sha1'))
        cmds.append(gwinstance.configure_ESP_proposal(ESPname, '2', '3des','md5'))
        cmds.append(gwinstance.configure_Protocol_lifetime('esp', ESPname, '1800'))
        logger.debug('\n[IPSEC Driver]-----Configure ESP for the CNG: ' + address + '...............OK')
        gwinstance.execute_many_cmd_Cosacs(address, cmds)


    def connect_gw(self, gwinstance, greInterface, greAdress, prefix, tunnelnum, tunnelProtocol, localAddress, remoteAddress, authenticationKey, IKE, ESP, grenexthop, dstNetwork):
        cmds=[]
        cmds.append(gwinstance.configure_GRE(greInterface, greAdress+'/'+prefix, 'GRE description', tunnelProtocol, localAddress, remoteAddress))
        logger.debug('\n[IPSEC Driver]-----Configure GRE tunnel between ' + localAddress + ' and ' + remoteAddress + '...............OK')
        cmds.append(gwinstance.configure_IPSEC_SiteToSite_withfile(remoteAddress, authenticationKey, ESP, IKE, localAddress, tunnelnum , tunnelProtocol))
        cmds.append(gwinstance.load())
        logger.debug('\n[IPSEC Driver]-----Configure IPSEC between ' + localAddress + ' and ' + remoteAddress + '...............OK')

        cmds.append(gwinstance.configure_staticRoute(dstNetwork, grenexthop))
        logger.debug('\n[IPSEC Driver]-----Configure routing table...............OK')

        gwinstance.execute_many_cmd_Cosacs(localAddress, cmds)


    def config_VMattachedGW(self, gwinstance, address, AddressgwtoVM, vmsAttachedgw):
        cmds=[]
        for item in vmsAttachedgw:
            cmds.append(gwinstance.config_gwVM(item, AddressgwtoVM, 'eth0'))

        gwinstance.execute_many_cmd_Cosacs(address, cmds)


    def stop_gw(self, gwinstance, gwaddress, addressDst, networkDst, tunnelname):
        cmds=[]

        cmds.append(gwinstance.delete_vpn(addressDst))
        logger.debug('\n[IPSEC Driver]-----Stoping IPSEC tunnel on CNG: ' + gwaddress + '...............OK')

        cmds.append(gwinstance.delete_protocols(networkDst))
        logger.debug('\n[IPSEC Driver]-----Stoping protocols on CNG: ' + gwaddress + '...............OK')

        cmds.append(gwinstance.delete_tunnel(tunnelname))
        logger.debug('\n[IPSEC Driver]-----Stoping GRE tunnel on CNG: ' + gwaddress + '...............OK')

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
