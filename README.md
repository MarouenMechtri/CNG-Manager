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
paradigm, we have used [PyOCNI](https://github.com/jordan-developer/pyOCNI) as OCCI server.

The CNG Manager have a northbound interface towards connectivity request and a southbound interface
interacting with transport technologies through drivers.

* The northbound interface is composed of 3 elements responsible for the configuration of
gateways and the links between them. These elements are OCCI categories (cng, linkcng and intercng).


* The southbound interfaces towards the underlying networking technologies require technology specific drivers (such as
OpenVPN, GRE, IPsec, NAT, OpenFlow ...). The CNG Manager relies on the designed drivers to remotely configure
the gateways (CNGs) deployed in the infrastructure layer.



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
