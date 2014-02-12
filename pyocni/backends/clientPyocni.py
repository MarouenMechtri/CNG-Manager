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

import pycurl
import StringIO
import urllib
from multiprocessing import Process, Value
import simplejson as json
import ast

class OCCIinterfaceClient:

  def __init__(self, host, port, category, entity):
      self.host = host
      self.port = port
      self.category = category
      self.entity = entity

  def postall_process(self):
      resource = {}
      resource['resources']=[self.entity]
      c = pycurl.Curl()
      c.setopt(c.URL, 'http://' + self.host + ':' + self.port + '/' + self.category + '/')
      c.setopt(c.HTTPHEADER, ['Accept:text/plain', 'Content-Type: application/occi+json'])
      c.setopt(pycurl.POSTFIELDS, json.dumps(resource))
      c.setopt(c.CUSTOMREQUEST, 'POST')
      c.perform()


  def update_process(self):
      resource = {}
      resource['resources']=[self.entity]
      c = pycurl.Curl()
      c.setopt(c.URL, 'http://' + self.host + ':' + self.port + '/' + self.category + '/' + self.entity['id'])
      c.setopt(c.HTTPHEADER, ['Accept:text/plain', 'Content-Type: application/occi+json'])
      c.setopt(pycurl.POSTFIELDS, json.dumps(resource))
      c.setopt(c.CUSTOMREQUEST, 'PUT')
      c.perform()


  def action_process(self, action, uuid):

      actionresource = ['actions']
      actionresource[0]={}
      actionresource[0]['term']=action
      actionresource[0]['scheme']='http://schemas.ogf.org/occi/infrastructure/' + self.category + 'action#'
      actions = {}
      actions['actions'] = actionresource

      c = pycurl.Curl()
      c.setopt(c.URL, 'http://' + self.host + ':' + self.port + '/' + self.category + '/' + uuid + '?action=' + action)
      c.setopt(c.HTTPHEADER, ['Accept:text/plain', 'Content-Type: application/occi+json'])
      c.setopt(c.CUSTOMREQUEST, 'POST')
      c.setopt(pycurl.POSTFIELDS, json.dumps(actions))
      c.perform()


  def get_process(self, uuid):

      storage = StringIO.StringIO()
      c = pycurl.Curl()
      c.setopt(c.URL, 'http://' + self.host + ':' + self.port + '/' + self.category + '/' + uuid)
      c.setopt(c.HTTPHEADER, ['Accept:application/occi+json', 'Content-Type: application/occi+json'])
      c.setopt(c.CUSTOMREQUEST, 'GET')
      c.setopt(c.WRITEFUNCTION, storage.write)
      c.perform()
      content = storage.getvalue()
      resources = ast.literal_eval(content)
      return resources['resources'][0]['attributes']['occi'][self.category]



  def post_process(self, uuid):

      attribute = {}
      attribute [self.category] = self.entity

      occi = {}
      occi['occi'] = attribute

      categ = {}
      categ['id'] = uuid
      categ['attributes'] = occi
      categ['kind'] = 'http://schemas.ogf.org/occi/infrastructure#' + self.category

      resource = {}
      resource['resources']=[categ]

      c = pycurl.Curl()
      c.setopt(c.URL, 'http://' + self.host + ':' + self.port + '/' + self.category + '/')
      c.setopt(c.HTTPHEADER, ['Accept:text/plain', 'Content-Type: application/occi+json'])
      c.setopt(pycurl.POSTFIELDS, json.dumps(resource))
      c.setopt(c.CUSTOMREQUEST, 'POST')
      c.perform()


  def delete_process(self, uuid):

      c = pycurl.Curl()
      c.setopt(c.URL, 'http://' + self.host + ':' + self.port + '/' + self.category + '/' + uuid)
      c.setopt(c.HTTPHEADER, ['Accept:text/plain', 'Content-Type: application/occi+json'])
      c.setopt(c.CUSTOMREQUEST, 'DELETE')
      c.perform()


  def GetElement_pathuuid(self, pathuuid):
      parametres = {}
      templist = pathuuid.split()
      pathuuid = ''.join(templist)
      temppath = pathuuid[7:]
      parametres['host']=temppath[:temppath.find(':')]
      temppath = temppath[temppath.find(':')+1:]
      if (temppath.find('/') != -1):
          parametres['port']=temppath[:temppath.find('/')]
          temppath = temppath[temppath.find('/')+1:]
          parametres['category']=temppath[:temppath.find('/')]
          parametres['uuid']=temppath[temppath.find('/')+1:]
      else:
          parametres['port']=temppath
      return parametres


  def GET(self, uuid):
      p1 = Process(target = self.get_process, args = (uuid,))
      p1.start()


  def POSTall(self):
      p1 = Process(target = self.postall_process)
      p1.start()


  def POST(self, uuid):
      p1 = Process(target = self.post_process, args = (uuid,))
      p1.start()


  def DELETE(self, uuid):
      p1 = Process(target = self.delete_process, args = (uuid,))
      p1.start()


  def PUT(self):
      p1 = Process(target = self.update_process)
      p1.start()


  def action(self, action, uuid):
      p1 = Process(target = self.action_process, args = (action, uuid))
      p1.start()

if __name__ == '__main__':
   deletes = OCCIinterfaceClient('127.0.0.1', '8085', 'intercng', {})
   deletes.DELETE('mmmaraa-dd9a-dd504f-8861-aeadsds') 
