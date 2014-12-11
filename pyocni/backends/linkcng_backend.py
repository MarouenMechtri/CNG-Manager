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
Created on Jul 15, 2013

@author: Marouen Mechtri
@contact: marouen.mechtri@it-sudparis.eu
@organization: Institut Mines-Telecom - Telecom SudParis
@license: Apache License, Version 2.0
"""

""" Note: entity represent the linkcng category.
        -Attributes of this category are:

                - name 
                - cngSRC                     //Path of the cng source category
                - cngDST                     //Path of the cng destination category 
                - publicaddrCNGsrc
                - publicaddrCNGdst
                - privateNetToCNGsrc 
                - privateNetToCNGdst 
                - linkType                   //3 types of link: openvpn,ipsec and openflow
                - tunneladdrSrc              //will be initialised by the create fonction based on linkType
                - tunneladdrDst              //will be initialised by the create fonction based on linkType
                - tunnelportSrc              //will be initialised by the create fonction based on linkType
                - tunnelportDst              //will be initialised by the create fonction based on linkType
                - tunneladdrprefix           //will be initialised by the create fonction based on linkType
                - tunnelinterface            //will be initialised by the create fonction based on linkType
                - tunnelauthenticationkey    //will be initialised by the create fonction based on linkType
                - intercng                   //Path of the intercng category 
                - account 
                - state 
"""

#import pyocni.backend.backend as backend
from pyocni.backends.backend import backend_interface
import pyocni.pyocni_tools.config as config
from pyocni.backends.clientPyocni import OCCIinterfaceClient
# import drivers (openvpn, ipsec, openflow)
from pyocni.backends.drivers.DriverOVPN import *
from pyocni.backends.drivers.DriverIPSEC import *
# getting the Logger
logger = config.logger

import pyocni.pyocni_tools.config as config

class backend(backend_interface):

    def create(self, entity):

        '''

        Create an entity (Resource or Link)

        '''
        if entity['attributes']['occi']['linkcng']['linkType'] == "openvpn":

            database = config.get_PyOCNI_db()
            nb_tunnelAdd = database.info()['doc_count'] - 10
            firstdecimal = nb_tunnelAdd%255
            seconddecimal = nb_tunnelAdd/255
            if firstdecimal == 0:
                firstdecimal=1
            elif firstdecimal >= 254:
                firstdecimal=1
                seconddecimal+=1
            entity['attributes']['occi']['linkcng']['tunneladdrSrc']="192.168." + str(seconddecimal) + "." + str(firstdecimal)
            entity['attributes']['occi']['linkcng']['tunneladdrDst']="192.168." + str(seconddecimal) + "." + str(firstdecimal+1)
            entity['attributes']['occi']['linkcng']['tunnelportSrc']=str(9612+(nb_tunnelAdd/2))
            entity['attributes']['occi']['linkcng']['tunnelportDst']=str(9612+(nb_tunnelAdd/2))
            entity['attributes']['occi']['linkcng']['tunnelinterface']="vtun" + str(nb_tunnelAdd)

            logger.debug('\n[linkCNG:start]-----Setting OpenVPN tunnel parameters')
        elif entity['attributes']['occi']['linkcng']['linkType'] == "ipsec":

            entity['attributes']['occi']['linkcng']['tunneladdrSrc']="10.10.1.1"
            entity['attributes']['occi']['linkcng']['tunneladdrDst']="10.10.1.2"
            entity['attributes']['occi']['linkcng']['tunneladdrprefix']="30"
            entity['attributes']['occi']['linkcng']['tunnelinterface']="tun0"
            entity['attributes']['occi']['linkcng']['tunnelauthenticationkey']="testkey"


            logger.debug('\n[linkCNG:start]-----Setting IPSEC tunnel parameters')
        elif entity['attributes']['occi']['linkcng']['linkType'] == "openflow":
            logger.debug('\n[linkCNG:start]-----Setting OpenFlow tunnel parameters')


        clientupdate = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'linkcng', entity)
        clientupdate.PUT()

        logger.debug('\n[linkCNG]-----Receiving POST linkcng')
        logger.debug('***The create operation of the linkcng_backend***')

    def read(self, entity):

        '''

        Get the Entity's information

        '''
        logger.debug('\n[linkCNG]-----Receiving GET linkcng')
        logger.debug('***The read operation of the linkcng_backend***')

    def update(self, old_entity, new_entity):

        '''

        Update an Entity's information

        '''
        logger.debug('\n[linkCNG]-----Receiving PUT linkcng')
        logger.debug('***The update operation of the linkcng_backend***')

    def delete(self, entity):

        '''

        Delete an Entity

        '''

        if(entity['attributes']['occi']['linkcng']['state'] == "0"):
            logger.debug('\n[linkCNG:stop]-----link is not configured')
        else:

            clientaction = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'cng', {})
            clientaction.action("stop", clientaction.GetElement_pathuuid(entity['attributes']['occi']['linkcng']['cngSRC'])['uuid'])


            clientaction = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'cng', {})
            clientaction.action("stop", clientaction.GetElement_pathuuid(entity['attributes']['occi']['linkcng']['cngDST'])['uuid'])

            if entity['attributes']['occi']['linkcng']['linkType'] == "openvpn":

                cngsrcDriver = ovpnDriver()
                cngdstDriver = ovpnDriver()

                publicaddrCNGsrc = entity['attributes']['occi']['linkcng']['publicaddrCNGsrc']
                publicaddrCNGdst = entity['attributes']['occi']['linkcng']['publicaddrCNGdst']
                privateNetToCNGsrc = entity['attributes']['occi']['linkcng']['privateNetToCNGsrc']
                privateNetToCNGdst = entity['attributes']['occi']['linkcng']['privateNetToCNGdst']
                tunnelinterface = entity['attributes']['occi']['linkcng']['tunnelinterface']

                cngsrcDriver.stop_site_to_site_OVPN(cngsrcDriver, publicaddrCNGsrc, tunnelinterface, privateNetToCNGdst)
                cngdstDriver.stop_site_to_site_OVPN(cngdstDriver, publicaddrCNGdst, tunnelinterface, privateNetToCNGsrc)

                logger.debug('\n[linkCNG:stop]-----End Release of OpenVPN link')

            elif entity['attributes']['occi']['linkcng']['linkType'] == "ipsec":

                cngsrcDriver = ipsecDriver()
                cngdstDriver = ipsecDriver()

                publicaddrCNGsrc = entity['attributes']['occi']['linkcng']['publicaddrCNGsrc']
                publicaddrCNGdst = entity['attributes']['occi']['linkcng']['publicaddrCNGdst']
                privateNetToCNGsrc = entity['attributes']['occi']['linkcng']['privateNetToCNGsrc']
                privateNetToCNGdst = entity['attributes']['occi']['linkcng']['privateNetToCNGdst']
                tunnelinterface = entity['attributes']['occi']['linkcng']['tunnelinterface']

                cngsrcDriver.stop_gw(cngsrcDriver, publicaddrCNGsrc, publicaddrCNGdst, privateNetToCNGdst, tunnelinterface)
                cngdstDriver.stop_gw(cngdstDriver, publicaddrCNGdst, publicaddrCNGsrc, privateNetToCNGsrc, tunnelinterface)

                logger.debug('\n[linkCNG:start]-----End Release of IPSEC link')

            elif entity['attributes']['occi']['linkcng']['linkType'] == "openflow":
                logger.debug('\n[linkCNG:stop]-----End Release of OpenFlow link')


        logger.debug('\n[linkCNG]-----Receiving DELETE linkcng')
        logger.debug('***The delete operation of the linkcng_backend***')

    def action(self, entity, action, attributes):

        '''

        Perform an action on an Entity

        '''

        if(action=="start"):
            logger.debug('\n[linkCNG]-----Receiving action START linkcng')
            if(entity['attributes']['occi']['linkcng']['state'] == "1"):
                logger.debug('\n[linkCNG:start]-----link is configured')
            else:
                logger.debug('\n[linkCNG:start]-----link is not configured')


                clientaction = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'cng', {})
                clientaction.action("start", clientaction.GetElement_pathuuid(entity['attributes']['occi']['linkcng']['cngSRC'])['uuid'])


                clientaction = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'cng', {})
                clientaction.action("start", clientaction.GetElement_pathuuid(entity['attributes']['occi']['linkcng']['cngDST'])['uuid'])


                if entity['attributes']['occi']['linkcng']['linkType'] == "openvpn":

                    cngsrcDriver = ovpnDriver()
                    cngdstDriver = ovpnDriver()

                    publicaddrCNGsrc = entity['attributes']['occi']['linkcng']['publicaddrCNGsrc']
                    publicaddrCNGdst = entity['attributes']['occi']['linkcng']['publicaddrCNGdst']
                    tunnelinterface = entity['attributes']['occi']['linkcng']['tunnelinterface']
                    privateNetToCNGsrc = entity['attributes']['occi']['linkcng']['privateNetToCNGsrc']
                    privateNetToCNGdst = entity['attributes']['occi']['linkcng']['privateNetToCNGdst']
                    tunneladdrSrc = entity['attributes']['occi']['linkcng']['tunneladdrSrc']
                    tunneladdrDst = entity['attributes']['occi']['linkcng']['tunneladdrDst']
                    tunnelportSrc = entity['attributes']['occi']['linkcng']['tunnelportSrc']
                    tunnelportDst = entity['attributes']['occi']['linkcng']['tunnelportDst']

                    cngsrcDriver.configure_site_to_site_openvpn(cngsrcDriver, publicaddrCNGsrc, tunnelinterface, tunneladdrSrc, tunneladdrDst, publicaddrCNGdst, privateNetToCNGdst, tunnelportSrc, tunnelportDst)
                    cngdstDriver.configure_site_to_site_openvpn(cngdstDriver, publicaddrCNGdst, tunnelinterface, tunneladdrDst, tunneladdrSrc, publicaddrCNGsrc, privateNetToCNGsrc, tunnelportDst, tunnelportSrc)
                    
                    logger.debug('\n[linkCNG:start]-----End configuration of OpenVPN link')
                elif entity['attributes']['occi']['linkcng']['linkType'] == "ipsec":

                    cngsrcDriver = ipsecDriver()
                    cngdstDriver = ipsecDriver()

                    publicaddrCNGsrc = entity['attributes']['occi']['linkcng']['publicaddrCNGsrc']
                    publicaddrCNGdst = entity['attributes']['occi']['linkcng']['publicaddrCNGdst']
                    privateNetToCNGsrc = entity['attributes']['occi']['linkcng']['privateNetToCNGsrc']
                    privateNetToCNGdst = entity['attributes']['occi']['linkcng']['privateNetToCNGdst']
                    tunneladdrSrc = entity['attributes']['occi']['linkcng']['tunneladdrSrc']
                    tunneladdrDst = entity['attributes']['occi']['linkcng']['tunneladdrDst']
                    tunnelinterface = entity['attributes']['occi']['linkcng']['tunnelinterface']
                    tunneladdrprefix = entity['attributes']['occi']['linkcng']['tunneladdrprefix']
                    tunnelauthenticationkey = entity['attributes']['occi']['linkcng']['tunnelauthenticationkey']

                    clientinformation = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'linkcng', {})
                    uuid_src = clientinformation.GetElement_pathuuid(entity['attributes']['occi']['linkcng']['cngSRC'])['uuid']
                    uuid_dst = clientinformation.GetElement_pathuuid(entity['attributes']['occi']['linkcng']['cngDST'])['uuid']

                    cngsrcDriver.configure_protocol_IPSEC(cngsrcDriver, publicaddrCNGsrc, "eth0", 'IKE'+uuid_src, 'ESP'+uuid_src)
                    cngdstDriver.configure_protocol_IPSEC(cngdstDriver, publicaddrCNGdst, "eth0", 'IKE'+uuid_dst, 'ESP'+uuid_dst)


                    cngsrcDriver.connect_gw(cngsrcDriver, tunnelinterface, tunneladdrSrc, tunneladdrprefix, '1', 'gre', publicaddrCNGsrc, publicaddrCNGdst, tunnelauthenticationkey, 'IKE'+uuid_src, 'ESP'+uuid_src, tunneladdrDst, privateNetToCNGdst)
                    cngdstDriver.connect_gw(cngdstDriver, tunnelinterface, tunneladdrDst, tunneladdrprefix, '1', 'gre', publicaddrCNGdst, publicaddrCNGsrc, tunnelauthenticationkey, 'IKE'+uuid_dst, 'ESP'+uuid_dst, tunneladdrSrc, privateNetToCNGsrc)

                    logger.debug('\n[linkCNG:start]-----End configuration of IPSEC link')
                elif entity['attributes']['occi']['linkcng']['linkType'] == "openflow":
                    logger.debug('\n[linkCNG:start]-----End configuration of OpenFlow link')


                entity['attributes']['occi']['linkcng']['state']="1"
                clientupdate = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'linkcng', entity)
                clientupdate.PUT()


        elif(action=="stop"):
            logger.debug('\n[linkCNG]-----Receiving action STOP linkcng')

            if(entity['attributes']['occi']['linkcng']['state'] == "0"):
                logger.debug('\n[linkCNG:stop]-----link is not configured')
            else:

                clientaction = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'cng', {})
                clientaction.action("stop", clientaction.GetElement_pathuuid(entity['attributes']['occi']['linkcng']['cngSRC'])['uuid'])


                clientaction = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'cng', {})
                clientaction.action("stop", clientaction.GetElement_pathuuid(entity['attributes']['occi']['linkcng']['cngDST'])['uuid'])

                if entity['attributes']['occi']['linkcng']['linkType'] == "openvpn":

                    cngsrcDriver = ovpnDriver()
                    cngdstDriver = ovpnDriver()

                    publicaddrCNGsrc = entity['attributes']['occi']['linkcng']['publicaddrCNGsrc']
                    publicaddrCNGdst = entity['attributes']['occi']['linkcng']['publicaddrCNGdst']
                    privateNetToCNGsrc = entity['attributes']['occi']['linkcng']['privateNetToCNGsrc']
                    privateNetToCNGdst = entity['attributes']['occi']['linkcng']['privateNetToCNGdst']
                    tunnelinterface = entity['attributes']['occi']['linkcng']['tunnelinterface']

                    cngsrcDriver.stop_site_to_site_OVPN(cngsrcDriver, publicaddrCNGsrc, tunnelinterface, privateNetToCNGdst)
                    cngdstDriver.stop_site_to_site_OVPN(cngdstDriver, publicaddrCNGdst, tunnelinterface, privateNetToCNGsrc)

                    logger.debug('\n[linkCNG:stop]-----End Release of OpenVPN link')

                elif entity['attributes']['occi']['linkcng']['linkType'] == "ipsec":

                    cngsrcDriver = ipsecDriver()
                    cngdstDriver = ipsecDriver()

                    publicaddrCNGsrc = entity['attributes']['occi']['linkcng']['publicaddrCNGsrc']
                    publicaddrCNGdst = entity['attributes']['occi']['linkcng']['publicaddrCNGdst']
                    privateNetToCNGsrc = entity['attributes']['occi']['linkcng']['privateNetToCNGsrc']
                    privateNetToCNGdst = entity['attributes']['occi']['linkcng']['privateNetToCNGdst']
                    tunnelinterface = entity['attributes']['occi']['linkcng']['tunnelinterface']

                    cngsrcDriver.stop_gw(cngsrcDriver, publicaddrCNGsrc, publicaddrCNGdst, privateNetToCNGdst, tunnelinterface)
                    cngdstDriver.stop_gw(cngdstDriver, publicaddrCNGdst, publicaddrCNGsrc, privateNetToCNGsrc, tunnelinterface)


                    logger.debug('\n[linkCNG:start]-----End Release of IPSEC link')
                elif entity['attributes']['occi']['linkcng']['linkType'] == "openflow":
                    logger.debug('\n[linkCNG:stop]-----End Release of OpenFlow link')


                entity['attributes']['occi']['linkcng']['state']="0"
                clientupdate = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'linkcng', entity)
                clientupdate.PUT()



        logger.debug('***The Entity\'s action operation of the linkcng_backend***')
