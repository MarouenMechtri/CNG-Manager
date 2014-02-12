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

import pycurl
import StringIO
import pyocni.pyocni_tools.config as config

actions = """{
	"actions": [
	   {
		"term": "start",
		"scheme": "http://schemas.ogf.org/occi/infrastructure/intercng/action#",
		"title": "Start intercng instance"
	   },
	   {
		"term": "stop",
		"scheme": "http://schemas.ogf.org/occi/infrastructure/intercng/action#",
		"title": "Stop intercng instance"
	   }
	]
}"""


category = """{
	"kinds": [
	   {
		"term": "intercng",
		"scheme": "http://schemas.ogf.org/occi/infrastructure#",
		"title": "intercng Resource",
		"related": [
			"http://schemas.ogf.org/occi/core#resource"
		],
		"attributes": {
			"occi": {
				"intercng": {
					"name": {
						"mutable": true,
						"required": false,
						"type": "string"
					},
					"publicaddrCNGsrc": {
						"mutable": true,
						"required": true,
						"pattern": "(\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3})",
						"type": "string"
					},
					"privateaddrCNGsrc": {
						"mutable": true,
						"required": true,
						"pattern": "(\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3})",
						"type": "string"
					},
					"privateNetToCNGsrc": {
						"mutable": true,
						"required": true,
						"pattern": "(\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}/\\\\d{1,2})",
						"type": "string"
					},
					"ethernameCNGsrc": {
						"mutable": true,
						"required": false,
						"type": "string"
					},
					"providerCNGsrc": {
						"mutable": true,
						"required": false,
						"type": "string"
					},
					"publicaddrCNGdst": {
						"mutable": true,
						"required": true,
						"pattern": "(\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3})",
						"type": "string"
					},
					"privateaddrCNGdst": {
						"mutable": true,
						"required": true,
						"pattern": "(\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3})",
						"type": "string"
					},
					"privateNetToCNGdst": {
						"mutable": true,
						"required": true,
						"pattern": "(\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}/\\\\d{1,2})",
						"type": "string"
					},
					"ethernameCNGdst": {
						"mutable": true,
						"required": false,
						"type": "string"
					},
					"providerCNGdst": {
						"mutable": true,
						"required": false,
						"type": "string"
					},
					"linkType": {
						"mutable": true,
						"required": false,
						"pattern": "openvpn|ipsec|openflow",
						"type": "string",
						"default": "openvpn"
					},
					"reusable": {
						"mutable": true,
						"required": false,
						"pattern": "0|1",
						"type": "string",
						"default": "0"
					},
                                        "linkcng": {
                                                "mutable": true,
                                                "required": false,
                                                "type": "string"
                                        },
                                        "account": {
                                                "mutable": true,
                                                "required": false,
                                                "type": "string"
                                        },
                                        "state": {
						"mutable": true,
						"required": false,
						"pattern": "0|1",
						"type": "string",
						"default": "0"
                                        }
				}
			}
		},
		"actions": [
			"http://schemas.ogf.org/occi/infrastructure/intercng/action#start",
			"http://schemas.ogf.org/occi/infrastructure/intercng/action#stop"
		],
		"location": "/intercng/"
	   }
	]
}"""


updateProv = """{
 "providers": [
         {
         "Provider": {
             "local": [
                 "intercng"
             ]
         },
         "OCCI_ID": "http://schemas.ogf.org/occi/infrastructure#intercng"
     }
 ]
}"""


def post_action():

  storage = StringIO.StringIO()
  c = pycurl.Curl()
  c.setopt(c.URL, 'http://' + config.OCNI_IP + ':' + config.OCNI_PORT + '/-/')
  c.setopt(c.HTTPHEADER, ['Accept:text/plain', 'Content-Type: application/occi+json'])
  c.setopt(c.VERBOSE, True)
  c.setopt(pycurl.POSTFIELDS, actions)
  c.setopt(c.CUSTOMREQUEST, 'POST')
  c.setopt(c.WRITEFUNCTION, storage.write)
  c.perform()
  content = storage.getvalue()
  print " ========== Body content ==========\n " + content + " \n ==========\n"


def post_cat():

  storage = StringIO.StringIO()
  c = pycurl.Curl()
  c.setopt(c.URL, 'http://' + config.OCNI_IP + ':' + config.OCNI_PORT + '/-/')
  c.setopt(c.HTTPHEADER, ['Accept:text/plain', 'Content-Type: application/occi+json'])
  c.setopt(c.VERBOSE, True)
  c.setopt(pycurl.POSTFIELDS, category)
  c.setopt(c.CUSTOMREQUEST, 'POST')
  c.setopt(c.WRITEFUNCTION, storage.write)
  c.perform()
  content = storage.getvalue()
  print " ========== Body content ==========\n " + content + " \n ==========\n"


def update_provider():

  storage = StringIO.StringIO()
  c = pycurl.Curl()
  c.setopt(c.URL, 'http://' + config.OCNI_IP + ':' + config.OCNI_PORT + '/-/')
  c.setopt(c.HTTPHEADER, ['Accept:text/plain', 'Content-Type: application/occi+json'])
  c.setopt(c.VERBOSE, True)
  c.setopt(pycurl.POSTFIELDS, updateProv)
  c.setopt(c.CUSTOMREQUEST, 'PUT')
  c.setopt(c.WRITEFUNCTION, storage.write)
  c.perform()
  content = storage.getvalue()
  print " ========== Body content ==========\n " + content + " \n ==========\n"



if __name__ == '__main__':
  post_action()
  post_cat()
  update_provider()
