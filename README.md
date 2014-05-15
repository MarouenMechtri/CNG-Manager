CNG-Manager - Cloud Networking Gateway Manager
==============================================

### Authors

Copyright (C) Marouen Mechtri <marouen.mechtri@it-sudparis.eu>

### Contributors

Marouen Mechtri <marouen.mechtri@it-sudparis.eu>

Djamal Zeghlache <djamal.zeghlache@it-sudparis.eu>

1. Introduction
---------------

The CNG Manager provides connectivity between resources acquired from distributed cloud providers
and hides heterogeneity in networking technologies. The CNG Manager controls and configures virtual gateways called CNGs.
The CNG Manager manages a list of [OCCI](http://occi-wg.org/) categories to configure connectivity. Since the CNG Manager is based on the OCCI
specification and service model, we have used [PyOCNI](https://github.com/jordan-developer/pyOCNI) as the OCCI server.

The CNG Manager has a northbound interface towards client requesting connectivity and a southbound interface
interacting with transport technologies through drivers.

* The northbound interface is composed of 3 elements responsible for the configuration of
gateways and links between these gateways. These elements are OCCI categories (cng, linkcng and intercng).


* The southbound interfaces towards the underlying networking technologies require technology specific drivers (such as
OpenVPN, GRE, IPsec, NAT, OpenFlow ... drivers). The CNG Manager relies on the designed drivers to remotely configure
the gateways (CNGs) deployed in the infrastructure layer.

If you want to use/test the CNG Manager framework, you have to download the [CNG image](https://github.com/MarouenMechtri/CNG-Manager#2-getting-the-cng-image-file) (qcow2 format) and to download CNG Manager source code. Use:
 
    git clone git@github.com:MarouenMechtri/CNG-Manager.git

2. Getting the CNG image file
-----------------------------

In fact, the CNG is a virtual appliance that provides a set of network technologies and functions.
The CNG also provides a RESTful interface to enable the configuration and the programmability of its features by the CNG Manager.

**Download CNG image file from:**

http://sourceforge.net/projects/cngmanager/files/cngimages/cngImage.qcow2/download

**Download a contextualized CNG image file prepared for OpenNebula from:**

http://sourceforge.net/projects/cngmanager/files/cngimages/cngImage-OpenNebula.qcow2/download

3. Installing CNG Manager
-------------------------

### Prerequisite Packages:

    sudo apt-get install python-setuptools
    sudo apt-get install python-all-dev

### Couchdb and pyOCNI installation:

    sudo apt-get install couchdb
    sudo python setup.py install


4. Starting CNG Manager
-----------------------

### Start pyOCNI server:

    sudo python start.py


### Start CNG-Manger server:

    sudo python start_CNG-M.py


5. Network configuration example
--------------------------------------

In the example below, we aim to interconnect VMs in site 1 with VMs in site 2.
Todo we have to deploy one CNG per site and after we configure them using CNG Manager framework.

As depicted in the figure below, the CNG Manager configures two
gateways CNG 1 and CNG 2 deployed respectively in site 1 and site 2.

The most important information needed for configuration is:

1. External IP address of CNG 1 _(1.1.1.1)_: **_publicaddrCNGsrc_**
2. Private IP address of CNG 1 _(192.168.1.1)_: **_privateaddrCNGsrc_**
3. Network address of VMs connected to CNG 1 _(192.168.1.0/24)_: **_privateNetToCNGsrc_**
4. External IP address of CNG 2 _(2.2.2.2)_: **_publicaddrCNGdst_**
5. Private IP address of CNG 2 _(10.10.10.1)_: **_privateaddrCNGdst_**
6. Network address of VMs connected to CNG 2 _(10.10.10.0/24)_: **_privateNetToCNGdst_**
7. The type of network between CNGs which can be "openvpn, ipsec and openflow": **_linkType_**

![Network Configuration Example](https://raw.github.com/MarouenMechtri/CNG-Manager/master/pyocni/img/config-example.jpg)


* Configuration file: intercng.json:

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


* Network configuration using cURL commands. The first cURL command instantiates an _"intercng"_ instance and the second command launches the configuration process:

        curl -X POST -d@intercng.json -H 'content-type: application/occi+json' -H 'accept: application/occi+json' -v http://127.0.0.1:8085/intercng/
        curl -X POST http://127.0.0.1:8085/intercng/8e007fe9-e535-4e1f-9794-b526fdb05d29?action=start

* Response of the first command:

        {
            "Location":[
                "http://127.0.0.1:8085/intercng/8e007fe9-e535-4e1f-9794-b526fdb05d29"
            ]
        }

* To bring connectivity between CNGs down:

        curl -X POST http://127.0.0.1:8085/intercng/8e007fe9-e535-4e1f-9794-b526fdb05d29?action=stop
        
### Acknowledgments

This appliance development was supported by EASI-CLOUDS and other collaborative projects. 
