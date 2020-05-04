# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# creationtop10Vgdb.py
# Created on: 26th January 2018 by benoit fricheteau
# edited on: 
#
# Parameter: none
# 
# ---------------------------------------------------------------------------
from owslib.util import ServiceException

import requests
import getpass
import os
import inspect
import time
import copy
from params import current_dir,get_param
from furl import furl
import urllib3 #import urlopen
from lxml import etree
from owslib.csw import CatalogueServiceWeb

http = urllib3.PoolManager()

class GNConnexion(object):

    def __init__(self, username=None, password=None):
    
        if username and password == None:
            # TODO: make parameters for username and password
            identifcateurs = {
                "username": get_param("geonetwork_user"),
                "password": get_param("geonetwork_password")
            }
        else:
            identifcateurs = {
                "username": username,
                "password": password
            }

        login="geonetwork/signin"
        self.radicalGN = get_param('geonetwork_url')
        urlGN = self.radicalGN + '/' + login
        self.session = requests.Session()

        self.session.get(self.radicalGN + "/geonetwork/srv/eng/catalog.signin")
        self.session.post(self.radicalGN + "/geonetwork/srv/eng/info?type=me")

        self.csrftoken = self.session.cookies['XSRF-TOKEN']
        identifcateurs['_csrf'] = self.csrftoken
        self.session.post(urlGN, data=identifcateurs)


    def uploadGNxml(self, xmlfile):
        jsessionid = self.session.cookies['JSESSIONID']
        params = {'file': ('test.xml', open(xmlfile, 'rb'), 'text/xml')}
        req = requests.Request('POST', self.radicalGN+"/geonetwork/srv/api/records", files=params,
                               data={'_csrf': self.csrftoken, 'metadataType': 'METADATA', 'uuidProcessing': 'NOTHING', 'transformWith': '', 'group': '20607', 'category': ''},
                               headers={'X-XSRF-TOKEN': self.csrftoken, 'Accept': 'application/json, text/javascript, */*; q=0.01'})
        prepped = self.session.prepare_request(req)
        prepped.headers['Cookie'] = prepped.headers['Cookie'] + ";JSESSIONID={};XSRF-TOKEN={}".format(jsessionid, self.csrftoken)

        r = self.session.send(prepped)
        print(r)


    def getrecordxml(self, id):
        """
        fetches the metadata where the fileIdentifier is equal to id
        """
        http = urllib3.PoolManager()
       # publishedrecord=urlopen(get_param('unpublished_record_url').format(id))
        r = http.request('GET', get_param('unpublished_record_url').format(id))
        publishedrecord = r.data
        tree=etree.parse(publishedrecord)
        root=tree.getroot()
        return root
        
        
        
        # r = self.session.get(get_param('unpublished_record_url').format(id))
        # return etree.fromstring(r.text.encode('utf-8'))
    
    def checkurl(self, url):
        print(url)
        try :
            r = http.request('GET', url)
            #ret = urlopen(url)
            if r.status == 200:
                exist=1
        except:
            exist=0
        return exist

    def deleteattachment(self, id, filename):
        url=self.radicalGN+"/geonetwork/srv/api/records/"+id+"/attachments/"+filename
        if self.checkurl(url)==1:
            jsessionid = self.session.cookies['JSESSIONID']
            req = requests.Request('DELETE', url, headers={'X-XSRF-TOKEN': self.csrftoken, 'Accept': 'application/json, text/javascript, */*; q=0.01'})
            prepped = self.session.prepare_request(req)
            prepped.headers['Cookie'] = prepped.headers['Cookie'] + ";JSESSIONID={};XSRF-TOKEN={}".format(jsessionid, self.csrftoken)
            r = self.session.send(prepped)
            print (r, r.text )
        else:
            print('no attachment')
            
    
    def addattachment(self, id, filename):
        file = current_dir+"\\"+filename
        params = {'file': (filename, open(file, 'rb'), 'text/xml')}
        jsessionid = self.session.cookies['JSESSIONID']
        req = requests.Request('POST', self.radicalGN+"/geonetwork/srv/api/records/"+id+"/attachments?visibility=public", files=params, headers={'X-XSRF-TOKEN': self.csrftoken, 'Accept': 'application/json, text/javascript, */*; q=0.01'})
        prepped = self.session.prepare_request(req)
        prepped.headers['Cookie'] = prepped.headers['Cookie'] + ";JSESSIONID={};XSRF-TOKEN={}".format(jsessionid, self.csrftoken)
        r = self.session.send(prepped)
        print (r, r.text)
    
    def updateattachmnet( self, id, filename):
        self.deleteattachment(id, filename)
        self.addattachment(id, filename)
        
    def unpublishrecord (self, id):
        jsessionid = self.session.cookies['JSESSIONID']
        params={"clear":"false","privileges":[{"group":"1","operations":{"view":"false","download":"false","dynamic":"false"}}]}
        req = requests.Request('PUT', self.radicalGN+"/geonetwork/srv/api/records/"+id+"/sharing", json=params, headers={'X-XSRF-TOKEN': self.csrftoken, 'Accept': 'application/json, text/plain, */*; q=0.01'})
        prepped = self.session.prepare_request(req)
        prepped.headers['Cookie'] = prepped.headers['Cookie'] + ";JSESSIONID={};XSRF-TOKEN={}".format(jsessionid, self.csrftoken)
        r = self.session.send(prepped)
        print (r, r.text)
    
    def publishrecord (self, id):
        jsessionid = self.session.cookies['JSESSIONID']
        params={"clear":"false","privileges":[{"group":"1","operations":{"view":"true","download":"true","dynamic":"true"}}]}
        req = requests.Request('PUT', self.radicalGN+"/geonetwork/srv/api/records/"+id+"/sharing", json=params, headers={'X-XSRF-TOKEN': self.csrftoken, 'Accept': 'application/json, text/plain, */*; q=0.01'})
        prepped = self.session.prepare_request(req)
        prepped.headers['Cookie'] = prepped.headers['Cookie'] + ";JSESSIONID={};XSRF-TOKEN={}".format(jsessionid, self.csrftoken)
        r = self.session.send(prepped)
        print (r, r.text)
        
class CSWConnexion(object):

    def __init__(self, csw_discovery_url,csw_publication_url, gn_username=None, gn_password=None):
        # TODO: make parameters for username and password      
        self.getrecordbyidparam='?request=GetRecordById&service=CSW&version=2.0.2&namespace=xmlns%28csw=http://www.opengis.net/cat/csw%29&resultType=results&outputSchema=http://www.isotc211.org/2005/gmd&outputFormat=application/xml&typeNames=csw:Record&elementSetName=full&constraintLanguage=CQL_TEXT&constraint_language_version=1.1.0'
        self.csw_discovery_url=csw_discovery_url
        self.csw_publication_url=csw_publication_url
        try:
            if gn_username is not None and gn_password is not None:
                self.csw_publication=CatalogueServiceWeb(self.csw_publication_url, username=gn_username, password=gn_password)
                self.csw_discovery=CatalogueServiceWeb(self.csw_discovery_url, username=gn_username, password=gn_password)
        except ServiceException:
            self.csw_publication=None
            self.csw_discovery=None
        try:
            self.csw_discovery=CatalogueServiceWeb(self.csw_discovery_url)
        except ServiceException:
            self.csw_discovery = None

    def get_record_list(self, keywords=[], typerecord=[]):			#par defaut les types et les keywords a selectionner sont vides --> toutes les fiches sont selectionnees
        from owslib.fes import PropertyIsEqualTo
        
        constraints=[]
        if len(typerecord) >0:
            for type in typerecord:
                print(type)
                constraints.append(PropertyIsEqualTo('dc:type', type))
        if len(keywords) >0:
            for keyword in keywords:
                constraints.append(PropertyIsEqualTo('dc:subject', keyword))
                constraints.append(PropertyIsEqualTo('keyword', keyword))
        self.csw_discovery.getrecords2(constraints=constraints, maxrecords=100000)
        print(self.csw_discovery.results)
        self.identifiers=[]
        for rec in self.csw_discovery.records:
            self.identifiers.append(self.csw_discovery.records[rec].identifier)

    def updaterecord(self, id, input_xml):
        if self.csw_publication is not None:
            if isinstance(input_xml, etree._Element):
                input_xml = etree.tostring(input_xml)
            self.csw_publication.transaction(ttype='update', typename='gmd:MD_Metadata', record=input_xml, identifier=id)
            print ("updated record "+id)
        else:
            print("Could not perform operation as password-protected CSW is unreachable.")
        
        
    def getrecordxml(self, id):
        """
        fetches the metadata where the fileIdentifier is equal to id
        """
        f=furl(self.csw_discovery_url + self.getrecordbyidparam)
        f.args['id']=id
        r = http.request('GET', f.url)
        publishedrecord = r.data
        #publishedrecord=urlopen(f.url)
        tree = etree.fromstring(publishedrecord)
        #tree=etree.parse(str(publishedrecord))
        root=tree[0]
        return root
