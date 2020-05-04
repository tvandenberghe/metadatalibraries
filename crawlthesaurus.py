from lxml import etree
import os
import sys
import inspect
import pandas
import time
import copy
import uuid
import shutil
import getpass
import requests
import urllib3
import geonetworkconnexion2
import params
from CSWRecord import CSWRecord

class thesaurusrdf(object):

    def __init__(self, input):
        self.input = input
        self.parsed = etree.parse(input)
        self.thesaurus = self.parsed.getroot()

    def findconcept(self, uri):
        self.uri = uri
        self.concept = \
        self.thesaurus.xpath('//rdf:RDF/skos:Concept[@rdf:about=' + "'" + self.uri + "']", namespaces=CSWRecord.schemas)[0]

    def findpreflabel(self, langue):
        self.preflabel = self.concept.xpath('./skos:prefLabel[@xml:lang="' + langue + '"]', namespaces=CSWRecord.schemas)[0]

    def finduri(self, preflabel):  # to add uri where there are none of them
        results = self.thesaurus.xpath('/rdf:RDF/skos:Concept[skos:prefLabel="' + preflabel + '"]', namespaces=CSWRecord.schemas)
        if len(results) > 0:
            self.concept = results[0]
            self.uri = self.concept.get("{" + CSWRecord.schemas["rdf"] + "}" + 'about')
        else:
            self.concept = None
            self.uri = None
