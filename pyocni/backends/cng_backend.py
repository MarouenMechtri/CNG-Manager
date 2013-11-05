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

""" Note: entity represent the cng category.
        -Attributes of this category are:

                - name 
                - publicaddr 
                - privateaddr 
                - ethername        //interface name having the public IP address  
                - provider 
                - intercng         //Path of the intercng category 
                - connection       //store the number of connections on this cng
                - account 
                - state 
"""


#import pyocni.backend.backend as backend
from pyocni.backends.backend import backend_interface
import pyocni.pyocni_tools.config as config
from pyocni.backends.clientPyocni import OCCIinterfaceClient
# getting the Logger
logger = config.logger

class backend(backend_interface):

    def create(self, entity):

        '''

        Create an entity (Resource or Link)

        '''
        logger.debug('\n-----[cng]-----Receiving POST cng')
        logger.debug('***The create operation of the cng_backend***')

    def read(self, entity):

        '''

        Get the Entity's information

        '''
        logger.debug('\n-----[cng]-----Receiving GET cng')
        logger.debug('***The read operation of the cng_backend***')

    def update(self, old_entity, new_entity):

        '''

        Update an Entity's information

        '''
        logger.debug('\n-----[cng]-----Receiving PUT cng')
        logger.debug('***The update operation of the cng_backend***')

    def delete(self, entity):

        '''

        Delete an Entity

        '''
        logger.debug('\n-----[cng]-----Receiving DELETE cng')
        logger.debug('***The delete operation of the cng_backend***')

    def action(self, entity, action, attributes):
        '''

        Perform an action on an Entity

        '''
        if(action=="start"):
            logger.debug('\n-----[cng]-----Receiving action START cng')
            if(entity['attributes']['occi']['cng']['state']=="0"):
                entity['attributes']['occi']['cng']['state']="1"
                entity['attributes']['occi']['cng']['connection']="1"
                logger.debug('\n-----[cng:start]-----Initialising connection in the cng')
                clientupdate = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'cng', entity)
                clientupdate.PUT()

            else:
                nbconnection = str(int(entity['attributes']['occi']['cng']['connection'])+1)
                entity['attributes']['occi']['cng']['connection']=nbconnection
                logger.debug('\n-----[cng:start]-----Increasing connection in the cng')
                clientupdate = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'cng', entity)
                clientupdate.PUT()

        elif(action=="stop"):
            logger.debug('\n-----[cng]-----Receiving action STOP cng')
            if(entity['attributes']['occi']['cng']['connection']=="1"):
                entity['attributes']['occi']['cng']['state']="0"
                entity['attributes']['occi']['cng']['connection']="0"
                logger.debug('\n-----[cng:stop]-----Last connection in the cng')
                clientupdate = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'cng', entity)
                clientupdate.PUT()

            elif(entity['attributes']['occi']['cng']['connection']=="0"):
                logger.debug('\n-----[cng:stop]-----No connection in the cng')
            else:
                nbconnection = str(int(entity['attributes']['occi']['cng']['connection'])-1)
                entity['attributes']['occi']['cng']['connection']=nbconnection
                logger.debug('\n-----[cng:stop]-----Decreasing the number of connections in the cng')
                clientupdate = OCCIinterfaceClient(config.OCNI_IP, config.OCNI_PORT, 'cng', entity)
                clientupdate.PUT()


        logger.debug('***The Entity\'s action operation of the cng_backend***')
