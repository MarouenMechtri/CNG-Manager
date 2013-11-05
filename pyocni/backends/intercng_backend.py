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

#import pyocni.backend.backend as backend
import uuid
from pyocni.backends.backend import backend_interface
import pyocni.pyocni_tools.config as config
from pyocni.backends.clientPyocni import OCCIinterfaceClient
# getting the Logger
logger = config.logger

""" Note: entity represent the intercng category.
        -Attributes of this category are:

		- name 
		- publicaddrCNGsrc 
		- privateaddrCNGsrc 
		- privateNetToCNGsrc 
		- ethernameCNGsrc     //not important for openvpn driver
		- providerCNGsrc 
		- publicaddrCNGdst 
		- privateaddrCNGdst 
		- privateNetToCNGdst 
		- ethernameCNGdst     //not important for openvpn driver 
		- providerCNGdst 
		- linkType            //3 types of link: openvpn,ipsec and openflow
                - reusable            //equal to 1 if user want to use its previous resources
		- linkcng             //will be initialised by create fonction (path of the linkcng category)
		- account 
		- state               //initialised to 0
"""

class backend(backend_interface):

    def create(self, entity):

        '''

        Create an entity (Resource or Link)

        '''

        if entity['attributes']['occi']['intercng']['reusable'] == '1':
            logger.debug('\n[intercng]-----Reuse existing cng for this user account and same IP address')

        elif entity['attributes']['occi']['intercng']['reusable'] == '0':
            logger.debug('\n[intercng]-----Do not reuse existing cng for this user account')

        attribute_cngSRC = {}
        attribute_cngSRC['name'] = entity['attributes']['occi']['intercng']['name']
        attribute_cngSRC['publicaddr'] = entity['attributes']['occi']['intercng']['publicaddrCNGsrc']
        attribute_cngSRC['privateaddr'] = entity['attributes']['occi']['intercng']['privateaddrCNGsrc']
        attribute_cngSRC['ethername'] = entity['attributes']['occi']['intercng']['ethernameCNGsrc']
        attribute_cngSRC['provider'] = entity['attributes']['occi']['intercng']['providerCNGsrc']
        attribute_cngSRC['intercng'] = 'http://' + config.OCNI_IP + ':' + config.OCNI_PORT + '/intercng/' + entity['id']
        attribute_cngSRC['connection'] = '0'
        attribute_cngSRC['account'] = entity['attributes']['occi']['intercng']['account']
        attribute_cngSRC['state'] = '0'

        clientpost = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'cng',  attribute_cngSRC)
        uuid_cngSRC = None
        uuid_cngSRC = str(uuid.uuid4())
        clientpost.POST(uuid_cngSRC)



        attribute_cngDST = {}
        attribute_cngDST['name'] = entity['attributes']['occi']['intercng']['name']
        attribute_cngDST['publicaddr'] = entity['attributes']['occi']['intercng']['publicaddrCNGdst']
        attribute_cngDST['privateaddr'] = entity['attributes']['occi']['intercng']['privateaddrCNGdst']
        attribute_cngDST['ethername'] = entity['attributes']['occi']['intercng']['ethernameCNGdst']
        attribute_cngDST['provider'] = entity['attributes']['occi']['intercng']['providerCNGdst']
        attribute_cngDST['intercng'] = 'http://' + config.OCNI_IP + ':' + config.OCNI_PORT + '/intercng/' + entity['id']
        attribute_cngDST['connection'] = '0'
        attribute_cngDST['account'] = entity['attributes']['occi']['intercng']['account']
        attribute_cngDST['state'] = '0'

        clientpost = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'cng',  attribute_cngDST)
        uuid_cngDST = None
        uuid_cngDST = str(uuid.uuid4())
        clientpost.POST(uuid_cngDST)


        attribute_linkcng = {}
        attribute_linkcng['name'] = entity['attributes']['occi']['intercng']['name']
        attribute_linkcng['cngSRC'] = 'http://' + config.OCNI_IP + ':' + config.OCNI_PORT + '/cng/' + uuid_cngSRC
        attribute_linkcng['cngDST'] = 'http://' + config.OCNI_IP + ':' + config.OCNI_PORT + '/cng/' + uuid_cngDST
        attribute_linkcng['publicaddrCNGsrc'] = entity['attributes']['occi']['intercng']['publicaddrCNGsrc']
        attribute_linkcng['publicaddrCNGdst'] = entity['attributes']['occi']['intercng']['publicaddrCNGdst']
        attribute_linkcng['privateNetToCNGsrc'] = entity['attributes']['occi']['intercng']['privateNetToCNGsrc']
        attribute_linkcng['privateNetToCNGdst'] = entity['attributes']['occi']['intercng']['privateNetToCNGdst']
        attribute_linkcng['linkType'] = entity['attributes']['occi']['intercng']['linkType']
        attribute_linkcng['intercng'] = 'http://' + config.OCNI_IP + ':' + config.OCNI_PORT + '/intercng/' + entity['id']
        attribute_linkcng['account'] = entity['attributes']['occi']['intercng']['account']
        attribute_linkcng['state'] = '0'

        clientpost = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'linkcng',  attribute_linkcng)
        uuid_linkcng = None
        uuid_linkcng = str(uuid.uuid4())
        clientpost.POST(uuid_linkcng)

        entity['attributes']['occi']['intercng']['linkcng'] = 'http://' + config.OCNI_IP + ':' + config.OCNI_PORT + '/linkcng/' + uuid_linkcng
        entity['attributes']['occi']['intercng']['state'] = '0'
        clientupdate = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'intercng', entity)
        clientupdate.PUT()


        logger.debug('\n[intercng]-----Receiving POST intercng')
        logger.debug('***The create operation of the intercng_backend***')

    def read(self, entity):

        '''

        Get the Entity's information

        '''
        logger.debug('\n[intercng]-----Receiving GET intercng')
        logger.debug('***The read operation of the intercng_backend***')

    def update(self, old_entity, new_entity):

        '''

        Update an Entity's information

        '''
        logger.debug('\n[intercng]-----Receiving PUT intercng')
        logger.debug('***The update operation of the intercng_backend***')

    def delete(self, entity):

        '''

        Delete an Entity

        '''
        clientaction = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'linkcng', {})
        clientaction.DELETE(clientaction.GetElement_pathuuid(entity['attributes']['occi']['intercng']['linkcng'])['uuid'])

        logger.debug('\n[intercng]-----Receiving DELETE intercng')
        logger.debug('***The delete operation of the intercng_backend***')



    def action(self, entity, action, attributes):

        '''

        Perform an action on an Entity

        '''

        if(action=="start"):

            logger.debug('\n[interCNG]-----Receiving action START intercng')

            clientaction = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'linkcng', {})
            clientaction.action("start", clientaction.GetElement_pathuuid(entity['attributes']['occi']['intercng']['linkcng'])['uuid'])

            entity['attributes']['occi']['intercng']['state']="1"
            clientupdate = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'intercng', entity)
            clientupdate.PUT()


        elif(action=="stop"):

            logger.debug('\n[interCNG]-----Receiving action STOP intercng')

            clientaction = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'linkcng', {})
            clientaction.action("stop", clientaction.GetElement_pathuuid(entity['attributes']['occi']['intercng']['linkcng'])['uuid'])

            entity['attributes']['occi']['intercng']['state']="0"
            clientupdate = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'intercng', entity)
            clientupdate.PUT()

        logger.debug('***The Entity\'s action operation of the intercng_backend***')
