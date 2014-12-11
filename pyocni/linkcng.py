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
		"scheme": "http://schemas.ogf.org/occi/infrastructure/linkcng/action#",
		"title": "Start linkcng instance"
	   },
	   {
		"term": "stop",
		"scheme": "http://schemas.ogf.org/occi/infrastructure/linkcng/action#",
		"title": "Stop linkcng instance"
	   }
	]
}"""


category = """{
	"kinds": [
	   {
		"term": "linkcng",
		"scheme": "http://schemas.ogf.org/occi/infrastructure#",
		"title": "linkcng Resource",
		"related": [
			"http://schemas.ogf.org/occi/core#resource"
		],
		"attributes": {
			"occi": {
				"linkcng": {
					"name": {
						"mutable": true,
						"required": false,
						"type": "string"
					},
					"cngSRC": {
						"mutable": true,
						"required": false,
						"type": "string"
					},
                                        "cngDST": {
                                                "mutable": true,
                                                "required": false,
                                                "type": "string"
                                        },
                                        "privateNetToCNGsrc": {
                                                "mutable": true,
                                                "required": true,
                                                "pattern": "(\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3})",
                                                "type": "string"
                                        },
                                        "privateNetToCNGdst": {
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
					"privateNetToCNGdst": {
						"mutable": true,
						"required": true,
						"pattern": "(\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}/\\\\d{1,2})",
						"type": "string"
					},
					"linkType": {
						"mutable": true,
						"required": false,
						"pattern": "openvpn|ipsec|openflow",
						"type": "string",
						"default": "openvpn"
					},
                                        "tunneladdrSrc": {
                                                "mutable": true,
                                                "required": true,
                                                "pattern": "(\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3})",
                                                "type": "string"
                                        },
                                        "tunneladdrDst": {
                                                "mutable": true,
                                                "required": true,
                                                "pattern": "(\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3}\\\\.\\\\d{1,3})",
                                                "type": "string"
                                        },
                                        "tunnelportSrc": {
                                                "mutable": true,
                                                "required": false,
                                                "type": "string"
                                        },
                                        "tunnelportDst": {
                                                "mutable": true,
                                                "required": false,
                                                "type": "string"
                                        },
                                        "tunneladdrprefix": {
                                                "mutable": true,
                                                "required": false,
                                                "type": "string"
                                        },
                                        "tunnelinterface": {
                                                "mutable": true,
                                                "required": false,
                                                "type": "string"
                                        },
                                        "tunnelauthenticationkey": {
                                                "mutable": true,
                                                "required": false,
                                                "type": "string"
                                        },
                                        "intercng": {
                                                "mutable": true,
                                                "required": true,
                                                "type": "string"
                                        },
                                        "account": {
                                                "mutable": true,
                                                "required": true,
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
			"http://schemas.ogf.org/occi/infrastructure/linkcng/action#start",
			"http://schemas.ogf.org/occi/infrastructure/linkcng/action#stop"
		],
		"location": "/linkcng/"
	   }
	]
}"""


updateProv = """{
 "providers": [
         {
         "Provider": {
             "local": [
                 "linkcng"
             ]
         },
         "OCCI_ID": "http://schemas.ogf.org/occi/infrastructure#linkcng"
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
