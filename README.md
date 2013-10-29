CNG-Manager - Cloud Networking Gateway Manager
==============================================

1. Introduction
---------------

The CNG Manager is conceived to provide connectivity between resources acquired from distributed cloud providers
and to hide heterogeneity in networking technologies. CNG Manager controls and configures virtual gateway called CNG.



2. Getting the CNG image file
-----------------------------

The CNG is designed to provide a set of technologies and network functions 
in a virtual appliance and to provide a RESTful interface to enable the 
configuration and the programmability of its features.


Download CNG image file from: 

http://sourceforge.net/projects/cngmanager/files/cngimages/cngImage.qcow2/download

Download a contextualized CNG image file prepared for OpenNebula framework from:

http://sourceforge.net/projects/cngmanager/files/cngimages/cngImage-OpenNebula.qcow2/download

3. Installing CNG Manager
-------------------------

    sudo apt-get install couchdb
    sudo python setup.py install


4. Starting CNG Manager
-----------------------

Start PyOCNI server:

    sudo python start.py


Start CNG-Manger server:

    sudo python start_CNG-M.py


5. First network configuration example
--------------------------------------
