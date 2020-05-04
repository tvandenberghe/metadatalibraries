# CSW-T library
## Credits
Originally written by Benoit Fricheteau of the NGI for Python 2 and adapted for use at RBINS for python 3.
## Installation
Install PyCharm (or just use the command line and cd to where you kep your projects)

    cd PycharmProjects
    git clone https://github.com/tvandenberghe/metadatalibraries.git
 
It is best to use a virtual environment to satisfy the dependencies correctly.
To do so:

Create a virtual environment in 
    
    cd metadatalibraries
    python3 -m venv ./env
    source env/bin/activate
    
Within the current python virtual environment
    
    python3 -m pip install -r requirements.txt
    exit
    
Make the following change in the file metadatalibraries/env/lib/python3.6/site-packages/owslib/csw.py:
 
Add the following in line 351:
 
    self._setconstraint(node1, None, propertyname, keywords, bbox, cql, identifier)

Make a copy of the file secrets.example.py, and name it secrets.py. Change the login credentials of your test and production environments accordingly. Under no circumstances upload system passwords to github. Meaning, do not ever change secrets.example.py or change anything inside .gitignore.

This ensures that request is adequately constrained to the metadata record with the specific id. This bug appeared to be absent when using python 2.7 (weird). Never mind, 3.6 is best.

## Usage
### Updating records
You can change one specific record or update a set of records by providing a keyword.
Add a line in the main method of modifyrecord.py. Comment the line when you have succesfully run it in a production environment. Do not remove previous lines as this keeps a trace of all previous modifications. After modifications, please 
 
    git add .
    git commit -m 'commit message'
    git push origin master
    
I will give you the necessary credentials to push new code to my git.
 
### Update possibilities

### Production vs development environments
When using the software for the first time, DO NOT use it in a production environment. Always test the outcome of the result in a test geonetwork, 
ie. inspect the actual metadata xml. With docker on https://hub.docker.com/_/geonetwork it is a oneliner to create a new geonetwork instance. Make sure your test geonetwork instance:

 * has harvested all records in the production environment
 * has the setting 'Allow editing on harvested records' enabled. Do not enable this in the procuction server! In production, you obviously only modify records that are manually created. 
 * depening on the install, make sure the port is set correctly in the CSW settings else the CSWT doesn't work. (only needed if you override the 80 or 8080 default) 

### Varia
I am currently not really making use of the excel functionality that Benoit used to store the xpath to commonly used elements. I just use the xpath in the method argumeent.
