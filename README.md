CNG-Manager - Cloud Networking Gateway Manager
==============================================

### Authors

Copyright (C) Marouen Mechtri <marouen.mechtri@it-sudparis.eu>

### Contributors

Marouen Mechtri <marouen.mechtri@it-sudparis.eu>

Djamal Zeghlache <djamal.zeghlache@it-sudparis.eu>

1. Introduction
---------------

The CNG Manager is conceived to provide connectivity between resources acquired from distributed cloud providers
and to hide heterogeneity in networking technologies. CNG Manager controls and configures virtual gateway called CNG.
The CNG Manager manages a list of [OCCI](http://occi-wg.org/) categories to configure connectivity. Since the CNG Manager is based on OCCI 
paradigm, we have used [pyOCNI](https://github.com/jordan-developer/pyOCNI) as OCCI server.

The CNG Manager have a northbound interface towards connectivity request and a southbound interface
interacting with transport technologies through drivers.

* The northbound interface is composed of 3 elements responsible for the configuration of
gateways and the links between them. These elements are OCCI categories (cng, linkcng and intercng).


* The southbound interfaces towards the underlying networking technologies require technology specific drivers (such as
OpenVPN, GRE, IPsec, NAT, OpenFlow ...). The CNG Manager relies on the designed drivers to remotely configure
the gateways (CNGs) deployed in the infrastructure layer.

If you want to use/test the CNG Manager framework, you have to download the CNG image (qcow2 format) and to download CNG Manager source code.
 
    $git clone git@github.com:MarouenMechtri/CNG-Manager.git

2. Getting the CNG image file
-----------------------------

The CNG is designed to provide a set of technologies and network functions in a virtual appliance and to provide a RESTful interface to enable the configuration and the programmability of its features.

Before start using CNG Manager we download the CNG image file.

**Download CNG image file from:**

http://sourceforge.net/projects/cngmanager/files/cngimages/cngImage.qcow2/download

**Download a contextualized CNG image file prepared for OpenNebula framework from:**

http://sourceforge.net/projects/cngmanager/files/cngimages/cngImage-OpenNebula.qcow2/download

3. Installing CNG Manager
-------------------------

### Pre-requisite Packages:

    sudo apt-get install python-setuptools
    sudo apt-get install python-all-dev

### Couchdb and pyOCNI installation:

    sudo apt-get install couchdb
    sudo python setup.py install


4. Starting CNG Manager
-----------------------

### Start PyOCNI server:

    sudo python start.py


### Start CNG-Manger server:

    sudo python start_CNG-M.py


5. First network configuration example
--------------------------------------

![Network Configuration Example](https://raw.github.com/MarouenMechtri/CNG-Manager/master/pyocni/img/config-example.jpg)





* Post intercng:

        curl -X POST -d@intercng.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://127.0.0.1:8085/intercng/

* Response:

        {
            "Location":[
                "http://127.0.0.1:8085/intercng/8e007fe9-e535-4e1f-9794-b526fdb05d29"
            ]
        }

* intercng.json:

        {
            "resources":[
                {
                    "kind":"http://schemas.ogf.org/occi/infrastructure#intercng",
                    "attributes":{
                        "occi":{
                            "intercng":{
                                "name":"First Network Configuration Example",
                                "publicaddrCNGsrc":"1.1.1.1",
                                "privateaddrCNGsrc":"192.168.1.1",
                                "privateNetToCNGsrc":"192.168.1.0/24",
                                "ethernameCNGsrc":"eth0",
                                "providerCNGsrc":"site1",
                                "publicaddrCNGdst":"2.2.2.2",
                                "privateaddrCNGdst":"10.10.10.1",
                                "privateNetToCNGdst":"10.10.10.0/24",
                                "ethernameCNGdst":"eth0",
                                "providerCNGdst":"site2",
                                "linkType":"openvpn",
                                "reusable":"1",
                                "account":"userTest"
                            }
                        }
                    }
                }
            ]
        }

