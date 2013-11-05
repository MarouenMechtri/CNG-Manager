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

import httplib2
import pprint
import re

class OCCIdriverClient:

  def __init__(self, host, port, userAgent, category, attributes):
      self.host = host
      self.port = port
      self.userAgent = userAgent
      self.category = category
      self.attributes = attributes


  def Post(self):
      h = httplib2.Http(".cache")
      msg = 'POST /' + self.category + '/ HTTP/1.1' \
            '\r\nHost: http:// ' + self.host + ':' + self.port + \
            '\r\nUser-Agent: ' + self.userAgent + '/1.0' \
            '\r\nCATEGORY: '+ self.category + \
            ';\r\nscheme=\"http://scheme.compatibleone.fr/scheme/compatible#\";' \
            '\r\nclass=kind;\r\n rel=\"http://scheme.ogf.org/occi/resource#\";'
      for item in self.attributes:
          msg=msg + '\r\nX-OCCI-ATTRIBUTE: occi.'+ self.category +'.'+item+'='+self.attributes[item]
      msg=msg+'\r\n\r\n'

      resp, content = h.request('http://' + self.host + ':' + self.port + '/' + self.category + '/',
          msg,
          headers={'content-type': 'text/html', 'accept': 'text/json'},
          body='')

      if(resp.has_key('x-occi-location')):
          return resp['x-occi-location'].replace(' ', '')
      else:
          return ''


  def Get(self):
      h = httplib2.Http(".cache")
      msg = 'GET /' + self.category + '/ HTTP/1.1'\
            '\r\nHost: http:// ' + self.host + ':' + self.port +\
            '\r\nUser-Agent: ' + self.userAgent + '/1.0'\
            '\r\nCATEGORY: '+ self.category +\
            ';\r\nscheme=\"http://scheme.compatibleone.fr/scheme/compatible#\";'\
            '\r\nclass=kind;\r\n rel=\"http://scheme.ogf.org/occi/resource#\";'

      for item in self.attributes:
          msg=msg + '\r\nX-OCCI-ATTRIBUTE: occi.'+ self.category +'.'+item+'='+self.attributes[item]
      msg=msg+'\r\n\r\n'

      resp, content = h.request('http://' + self.host + ':' + self.port + '/' + self.category + '/',
          msg,
          headers={'content-type': 'text/html', 'accept': 'text/json'},
          body='')

      if(resp.has_key('x-occi-location')):
          return resp['x-occi-location'].split(',')
      else:
          return ''


  def Delete(self):
      h = httplib2.Http(".cache")
      msg = 'DELETE /' + self.category + '/ HTTP/1.1'\
            '\r\nHost: http:// ' + self.host + ':' + self.port +\
            '\r\nUser-Agent: ' + self.userAgent + '/1.0'\
            '\r\nCATEGORY: '+ self.category +\
            ';\r\nscheme=\"http://scheme.compatibleone.fr/scheme/compatible#\";'\
            '\r\nclass=kind;\r\n rel=\"http://scheme.ogf.org/occi/resource#\";'


      for item in self.attributes:
          msg=msg + '\r\nX-OCCI-ATTRIBUTE: occi.'+ self.category +'.'+item+'='+self.attributes[item]
      msg=msg+'\r\n\r\n'

      resp, content = h.request('http://' + self.host + ':' + self.port + '/' + self.category + '/',
          msg,
          headers={'content-type': 'text/html', 'accept': 'text/json'},
          body='')


  def Put(self,uuid):
      h = httplib2.Http(".cache")
      msg = 'PUT /' + self.category + '/' + uuid + ' HTTP/1.1'\
            '\r\nHost: http:// ' + self.host + ':' + self.port +\
            '\r\nUser-Agent: ' + self.userAgent + '/1.0'\
            '\r\nCATEGORY: '+ self.category +\
            ';\r\nscheme=\"http://scheme.compatibleone.fr/scheme/compatible#\";'\
            '\r\nclass=kind;\r\n rel=\"http://scheme.ogf.org/occi/resource#\";'

      for item in self.attributes:
          msg=msg + '\r\nX-OCCI-ATTRIBUTE: occi.'+ self.category +'.'+item+'='+self.attributes[item]
      msg=msg+'\r\n\r\n'

      resp, content = h.request('http://' + self.host + ':' + self.port + '/' + self.category + '/',
          msg,
          headers={'content-type': 'text/html', 'accept': 'text/json'},
          body='')


  def action(self, uuid, action):
      h = httplib2.Http(".cache")
      msg = 'POST /' + self.category + '/' + uuid + '?action=' + action + ' HTTP/1.1'\
            '\r\nHost: http:// ' + self.host + ':' + self.port +\
            '\r\nUser-Agent: ' + self.userAgent + '/1.0'\
            '\r\nCATEGORY: '+ self.category +\
            ';\r\nscheme=\"http://scheme.compatibleone.fr/scheme/compatible#\";'\
            '\r\nclass=kind;\r\n rel=\"http://scheme.ogf.org/occi/resource#\";' + '\r\n\r\n'
      resp, content = h.request('http://' + self.host + ':' + self.port + '/' + self.category + '/',
          msg,
          headers={'content-type': 'text/html', 'accept': 'text/json'},
          body='')
