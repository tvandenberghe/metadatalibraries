# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# creationtop10Vgdb.py
# Created on: 26th January 2018 by benoit fricheteau
# edited on: 
#
# Parameter: none
# 
# ---------------------------------------------------------------------------
#import sets

#from lxml.etree import XMLSyntaxError

#import requests
#import getpass
import os
#import inspect
#from furl import furl
#from urllib.request import urlopen
from lxml import etree
import geonetworkconnexion2
import params
import crawlthesaurus
import re
import secrets
from CSWRecord import CSWRecord
from secrets import gn_username, gn_password, csw_discovery, csw_publication


class modifyrecord(object):
    dico = ''

    def __init__(self, cswconnexion):
        self.cswconnexion = cswconnexion;

    @staticmethod
    def init_rdf():
        inspirethemes = os.path.join(params.current_dir, "Metadata", "thesauri", "inspiretheme.rdf")
        gemetconcept = os.path.join(params.current_dir, "Metadata", "thesauri", "gemetconcept.rdf")
        inspireconcept = os.path.join(params.current_dir, "Metadata", "thesauri", "inspireconcept.rdf")
        modifyrecord.dico = crawlthesaurus.thesaurusrdf(inspireconcept)

    def print_keywords(self, descriptiveKeywords):
        self.cswconnexion.get_record_list(descriptiveKeywords)
        i = 0
        for id in self.cswconnexion.identifiers:
            i = i + 1
            print(("dataset " + str(i) + ": " + id))
            xml = self.cswconnexion.getrecordxml(id)
            record = CSWRecord(xml, id)
            # keywords=record.selectsiblingtags('descriptiveKeywords',"maintag")
            descriptiveKeywords = record.selectsiblingtags('descriptiveKeywords')

            for descriptiveKeyword in descriptiveKeywords:
                keywords = set(descriptiveKeyword.xpath(
                    "gmd:MD_Keywords/gmd:keyword/gmx:Anchor/text() | gmd:MD_Keywords/gmd:keyword/gco:CharacterString/text()",
                    namespaces=CSWRecord.schemas))
                for text in keywords:
                    if text is not None:
                        print(("     keyword: " + text))
                        modifyrecord.dico.finduri(text)
                        if modifyrecord.dico.uri is not None:
                            pass
                        #   record.modifytag(descriptiveKeyword, "{"+CSWRecord.schemas["gmx"]+"}Anchor")
                        #   record.modifyattribute(descriptiveKeyword, "{"+CSWRecord.schemas["xlink"]+'}href',modifyrecord.dico.uri)
                        elif text == None:
                            print("no keyword", id)
                        # else:
                    #     print "unofficial keyword", tag, id
                    # print descriptiveKeyword.get("{" + CSWRecord.schemas["xlink"] + '}href')

        # self.cswconnexion.updaterecord(id, xml)

    # ---------------------
    def append_records_at(self, do_when_keyword, outer, before, xml_snippet, refuse_when_keyword=None):
        self.cswconnexion.get_record_list(do_when_keyword)
        for id in self.cswconnexion.identifiers:
            xml = self.cswconnexion.getrecordxml(id)
            csw_record = CSWRecord(xml, id)
            has_refused_keyword = False
            if refuse_when_keyword is not None:
                has_refused_keyword = len(csw_record.xml.xpath(
                    "//gmd:MD_Keywords/gmd:keyword/gmx:Anchor[text() = '" + refuse_when_keyword + "'] | //gmd:MD_Keywords/gmd:keyword/gco:CharacterString[text() = '" + refuse_when_keyword + "']",
                    namespaces=CSWRecord.schemas)) > 0

            if has_refused_keyword:
                print(("Keyword '" + refuse_when_keyword + "' present for dataset " + id + ". Not adding xml snippet."))
            else:
                self.append_csw_record_at(csw_record, outer=outer, before=before, xml_snippet=xml_snippet)

    def append_record_at(self, id, outer, before, xml_snippet):
        xml = self.cswconnexion.getrecordxml(id)
        csw_record = CSWRecord(xml, id)
        self.append_csw_record_at(csw_record, outer=outer, before=before, xml_snippet=xml_snippet)

    def append_csw_record_at(self, csw_record, outer, xml_snippet, before=None, after=None):
        if (before is None and after is None) or (before is not None and after is not None):
            raise ValueError("either before or after, not none, not both")
        element = before or after
        position = csw_record.get_position(outer, element)
        if after: position = position + 1
        csw_record.addtag(outer, xml_snippet, position)
        # print(csw_record.print_xml())
        self.cswconnexion.updaterecord(csw_record.id, csw_record.xml)

    # ---------------------
    def remove_records_keyword(self, do_when_keyword, keyword_textual_value):
        self.cswconnexion.get_record_list(do_when_keyword)
        for id in self.cswconnexion.identifiers:
            xml = self.cswconnexion.getrecordxml(id)
            csw_record = CSWRecord(xml, id)
            self.remove_csw_record_keyword(csw_record, keyword_textual_value)

    '''Remove the keyword that matches with keyword_textual_value from csw_record'''

    def remove_record_keyword(self, id, keyword_textual_value):
        xml = self.cswconnexion.getrecordxml(id)
        csw_record = CSWRecord(xml, id)
        self.remove_csw_record_keyword(csw_record, keyword_textual_value)

    def remove_csw_record_keyword(self, csw_record, keyword_textual_value):
        xpath = "//gmd:descriptiveKeywords[gmd:MD_Keywords/gmd:keyword/gmx:Anchor[text() = '" + keyword_textual_value + "']] | //gmd:descriptiveKeywords[gmd:MD_Keywords/gmd:keyword/gco:CharacterString[text() = '" + keyword_textual_value + "']]"
        self.remove_csw_record_xpath(csw_record, xpath)

    # ---------------------
    '''Remove the element that matches with xpath from csw_record. Optionally specify the index that should be deleted, counting from zero (else all matches are deleted). Method for all records in CSW matching a certain keyword.'''
    def remove_records_xpath(self, do_when_keyword, xpath, number=None):
        self.cswconnexion.get_record_list(do_when_keyword)
        for id in self.cswconnexion.identifiers:
            xml = self.cswconnexion.getrecordxml(id)
            csw_record = CSWRecord(xml, id)
            self.remove_csw_record_xpath(csw_record, xpath, number)

    '''Remove the element that matches with xpath from id. Optionally specify the index that should be deleted, counting from zero (else all matches are deleted). Method matching the fileIdentifier of one record'''
    def remove_record_xpath(self, id, xpath, number=None):
        xml = self.cswconnexion.getrecordxml(id)
        csw_record = CSWRecord(xml, id)
        self.remove_csw_record_xpath(csw_record, xpath, number)

    '''Remove the element that matches with xpath from csw_record. Optionally specify the index that should be deleted, counting from zero (else all matches are deleted). Method matching the CswRecord'''
    def remove_csw_record_xpath(self, csw_record, xpath, number=None):
        elements = csw_record.xml.xpath(xpath, namespaces=CSWRecord.schemas)
        if number is None:
            for element in elements:
                csw_record.remove_tag(element)
        elif elements:
            csw_record.remove_tag(elements[number])
        if elements:
            self.cswconnexion.updaterecord(csw_record.id, csw_record.xml)

    # ---------------------
    '''Replace the element that matches with xpath from csw_record. Optionally specify the index that should be deleted, counting from zero (else all matches are deleted). Method for all records in CSW matching a certain keyword.'''
    def replace_records_xpath(self, do_when_keyword, xpath, xml_snippet):
        self.cswconnexion.get_record_list(do_when_keyword)
        for id in self.cswconnexion.identifiers:
            xml = self.cswconnexion.getrecordxml(id)
            csw_record = CSWRecord(xml, id)
            self.replace_csw_record_xpath(csw_record, xpath, xml_snippet)


    '''Replace the element that matches with xpath from id. Optionally specify the index that should be deleted, counting from zero (else all matches are deleted). Method matching the fileIdentifier of one record'''
    def replace_record_xpath(self, id, xpath, xml_snippet):
        xml = self.cswconnexion.getrecordxml(id)
        csw_record = CSWRecord(xml, id)
        self.replace_csw_record_xpath(csw_record, xpath, xml_snippet)


    '''Replace the element that matches with xpath from csw_record. Optionally specify the index that should be deleted, counting from zero (else all matches are deleted). Method matching the CswRecord'''
    def replace_csw_record_xpath(self, csw_record, xpath, xml_snippet):
        elements = csw_record.xml.xpath(xpath, namespaces=CSWRecord.schemas)
        for element in elements:
           parent= element.getparent()
           index= parent.index(element)
           csw_record.remove_tag(element)
           csw_record.addtag(parent, xml_snippet, index)
        if elements:
            self.cswconnexion.updaterecord(csw_record.id, csw_record.xml)
    # ---------------------

    def replace_records_identifier_with_fileidentifier(self, do_when_keyword):
        self.cswconnexion.get_record_list(do_when_keyword)
        for id in self.cswconnexion.identifiers:
            xml = self.cswconnexion.getrecordxml(id)
            csw_record = CSWRecord(xml, id)
            self.replace_csw_record_identifier_with_fileidentifier(csw_record)


    def replace_record_identifier_with_fileidentifier(self, id):
        xml = self.cswconnexion.getrecordxml(id)
        csw_record = CSWRecord(xml, id)
        self.replace_csw_record_identifier_with_fileidentifier(csw_record)


    def replace_csw_record_identifier_with_fileidentifier(self, csw_record):
        file_identifier = csw_record.xml.xpath('//gmd:MD_Metadata/gmd:fileIdentifier/gco:CharacterString/text()',
                                               namespaces=CSWRecord.schemas)[0]
        nb_identifiers = len(csw_record.xml.xpath(
            '//gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier | //srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier',
            namespaces=CSWRecord.schemas))
        if nb_identifiers == 1:
            self.remove_csw_record_xpath(csw_record,
                                         "//gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier | //srv:SV_ServiceIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier",
                                         0)
            xml_snippet = '''<gmd:identifier>
                          <gmd:RS_Identifier>
                             <gmd:authority>
                                <gmd:CI_Citation>
                                   <gmd:title>
                                      <gco:CharacterString>Belgian Marine Data Centre</gco:CharacterString>
                                   </gmd:title>
                                   <gmd:date gco:nilReason="inapplicable"/>
                                </gmd:CI_Citation>
                             </gmd:authority>
                             <gmd:code>
                                <gco:CharacterString>''' + file_identifier + '''</gco:CharacterString>
                             </gmd:code>
                             <gmd:codeSpace>
                                <gco:CharacterString>http://metadata.naturalsciences.be</gco:CharacterString>
                             </gmd:codeSpace>
                          </gmd:RS_Identifier>
                       </gmd:identifier>'''
            self.append_csw_record_at(csw_record=csw_record, outer="CI_Citation", after="last_citation_date",
                                      xml_snippet=self.prep_input_string(xml_snippet))
            # print(csw_record.print_xml())
        else:
            print(("Warning! Record " + csw_record.id + " has more than one identifier! Identifier not replaced."))

        # ---------------------


    def replace_records_hard(self, do_when_keyword, fro=None, to=None, regex_fro=None, regex_to=None):
        self.cswconnexion.get_record_list(do_when_keyword)
        for id in self.cswconnexion.identifiers:
            xml = self.cswconnexion.getrecordxml(id)
            csw_record = CSWRecord(xml, id)
            self.replace_csw_record_hard(csw_record, fro, to, regex_fro, regex_to)


    def replace_record_hard(self, id, fro=None, to=None, regex_fro=None, regex_to=None):
        xml = self.cswconnexion.getrecordxml(id)
        csw_record = CSWRecord(xml, id)
        self.replace_csw_record_hard(csw_record, fro, to, regex_fro, regex_to)


    def replace_csw_record_hard(self, csw_record, fro=None, to=None, regex_fro=None, regex_to=None):
        xml = csw_record.xml
        xml = etree.tostring(xml)
        if regex_fro is None and regex_to is None:
            xml = xml.replace(fro, to)
        elif fro is None and to is None:
            xml = re.sub(regex_fro, regex_to, xml)
        self.cswconnexion.updaterecord(csw_record.id, xml)
        # ---------------------


    def modify_records_attribute(self, do_when_keyword, xpath, attribute, value):
        self.cswconnexion.get_record_list(do_when_keyword)
        for id in self.cswconnexion.identifiers:
            xml = self.cswconnexion.getrecordxml(id)
            csw_record = CSWRecord(xml, id)
            self.modify_csw_record_attribute(csw_record, xpath, attribute, value)


    def modify_record_attribute(self, id, xpath, attribute, value):
        xml = self.cswconnexion.getrecordxml(id)
        csw_record = CSWRecord(xml, id)
        self.modify_csw_record_attribute(csw_record, xpath, attribute, value)


    def modify_csw_record_attribute(self, csw_record, xpath, attribute, value):
        elements = csw_record.xml.xpath(xpath, namespaces=CSWRecord.schemas)
        for element in elements:
            csw_record.modifyattribute(element, attribute, value)
        if elements:
            a = 5
            # self.cswconnexion.updaterecord(csw_record.id, csw_record.xml)
        # ---------------------


    def replace_records_attr_value(self, do_when_keyword, fro, to):
        self.cswconnexion.get_record_list(do_when_keyword)
        for id in self.cswconnexion.identifiers:
            xml = self.cswconnexion.getrecordxml(id)
            csw_record = CSWRecord(xml, id)
            self.replace_csw_record_attr_value(csw_record)


    def replace_record_attr_value(self, id, fro, to):
        xml = self.cswconnexion.getrecordxml(id)
        csw_record = CSWRecord(xml, id)
        self.replace_csw_record_hard(csw_record, fro, to)


    def replace_csw_record_attr_value(self, csw_record, fro, to):
        xml = csw_record.xml
        xml = etree.tostring(xml).replace(fro, to)
        self.cswconnexion.updaterecord(csw_record.id, xml)

        # ---------------------


    def prep_input_file(self, filename):
        filename = os.path.join(params.current_dir, filename)
        file = open(filename, "r")
        file_content = file.read()
        return self.prep_input_string(file_content)


    def prep_input_string(self, xml_string):
        actual_namespaces = set(re.findall('</(.*?):.*?>', xml_string))
        if re.search('xlink:href', xml_string):
            actual_namespaces.add('xlink')
        if re.search('xsi:type', xml_string):
            actual_namespaces.add('xsi')
        xmlns = "".join("xmlns:" + k + "=\"" + v + "\" " if k in actual_namespaces else '' for k, v in
                        CSWRecord.schemas.items())
        file_content = re.sub(r'^<(.*)>', r'<\1 ' + xmlns + '>', xml_string)
        return file_content

        # ---------------------


    @staticmethod
    def main():
        # gn_username = raw_input("GeoNetwork username: ")
        # gn_password=getpass.getpass("GeoNetwork password: ")
        cswconnexion = geonetworkconnexion2.CSWConnexion(gn_username=secrets.gn_username,
                                                         gn_password=secrets.gn_password,
                                                         csw_discovery_url=secrets.csw_discovery,
                                                         csw_publication_url=secrets.csw_publication)

        mr = modifyrecord(cswconnexion)
        mr.init_rdf()
        # mr.print_keywords(descriptiveKeywords=["Reporting INSPIRE"])

        # mr.append_records_at(xml_snippet=mr.prep_input_file("input_national.xml"), outer="identification", before= "descriptiveKeywords", do_when_keyword=["Reporting INSPIRE"],refuse_when_keyword="National")
        # mr.append_records_at(xml_snippet=mr.prep_input_file("input_federal.xml"), outer="identification", before="descriptiveKeywords", do_when_keyword=["Reporting INSPIRE"], refuse_when_keyword="Federal government")
        # mr.remove_records_keyword(do_when_keyword=["National"], keyword_textual_value="National")
        # mr.append_records_at(xml_snippet=mr.prep_input_file("input_national.xml"), outer="identification",before="descriptiveKeywords", do_when_keyword=["Reporting INSPIRE"],refuse_when_keyword="National")

        # mr.remove_records_xpath(do_when_keyword=['Reporting INSPIRE'], xpath="//gmd:textGroup[gmd:LocalisedCharacterString[@locale='#EN']]")
        # mr.remove_records_xpath(do_when_keyword=['Reporting INSPIRE'], xpath="//gmd:locale")
        # mr.append_records_at(do_when_keyword=['Reporting INSPIRE'], xml_snippet=mr.prep_input_file("input_locale_nl.xml"), outer="MD_Metadata", before=["referenceSystemInfo","identificationInfo"])
        # mr.append_records_at(do_when_keyword=['Reporting INSPIRE'], xml_snippet=mr.prep_input_file("input_locale_fr.xml"), outer="MD_Metadata", before=["referenceSystemInfo","identificationInfo"])
        # mr.append_records_at(do_when_keyword=['Reporting INSPIRE'], xml_snippet=mr.prep_input_file("input_locale_de.xml"), outer="MD_Metadata", before=["referenceSystemInfo","identificationInfo"])
        # mr.remove_records_xpath(do_when_keyword=['Reporting INSPIRE'], xpath="//gmd:PT_FreeText[../gmx:Anchor]") #remove freetext within anchors
        #mr.replace_records_identifier_with_fileidentifier(do_when_keyword=['Reporting INSPIRE'])

        # mr.replace_records_hard(do_when_keyword=['Reporting INSPIRE'],fro='http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/ML_gmxCodelists.xml#', to='http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#')
        # mr.replace_records_hard(do_when_keyword=['Reporting INSPIRE'],fro='http://schemas.opengis.net/iso/19139/20070417/resources/Codelist/gmxCodelists.xml#',to='http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#')
        # mr.replace_records_hard(do_when_keyword=['Reporting INSPIRE'],fro='http://www.isotc211.org/2005/resources/Codelist/gmxCodelists.xml#',to='http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#')
        # mr.replace_records_hard(do_when_keyword=['Reporting INSPIRE'],fro='http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/Codelist/ML_gmxCodelists.xml#', to='http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#')
        # mr.replace_records_hard(do_when_keyword=['Reporting INSPIRE'],fro='http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources/codelist/ML_gmxCodelists.xml#',to='http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#')
        # mr.replace_records_hard(do_when_keyword=['Reporting INSPIRE'],fro='http://standards.iso.org/ittf/PubliclyAvailableStandards/ISO_19139_Schemas/resources /Codelist/ML_gmxCodelists.xml#',to='http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#')
        # mr.replace_records_hard(do_when_keyword=['Reporting INSPIRE'],fro='http://www.isotc211.org/2005/resources/codeList.xml#',to='http://standards.iso.org/iso/19139/resources/gmxCodelists.xml#')
        # mr.replace_records_hard(do_when_keyword=['Reporting INSPIRE'],fro='codeListValue="dataCentre"',to='codeListValue="theme"') #do a hard textual replace of the dataCentre codelistValue for keyword into theme
        # mr.replace_records_hard(do_when_keyword=['Reporting INSPIRE'],fro='xlink:href="http://metadata.naturalsciences.be/',to='xlink:href="http://geonetwork.bmdc.be/geonetwork/srv/eng/csw?service=CSW&amp;request=GetRecordById&amp;version=2.0.2&amp;outputSchema=http://www.isotc211.org/2005/gmd&amp;elementSetName=full&amp;id=')
        # mr.replace_records_hard(do_when_keyword=['Reporting INSPIRE'],regex_fro=r'(srv:operatesOn.*?)\.xml', regex_to=r'\1') #do a hard regex replace, in this case replace srv:operatesOn="file.xml" to srv:operatesOn="file
        # mr.modify_records_attribute(do_when_keyword=['Reporting INSPIRE'],xpath='//srv:serviceType/gco:LocalName',attribute='codeSpace',value='http://inspire.ec.europa.eu/metadata-codelist/SpatialDataServiceType')
        # mr.replace_records_hard(do_when_keyword=['Reporting INSPIRE'], fro='xsi:type="gml:TimePeriodType"',to='xsi:type="gml32:TimePeriodType"') #do a textual replace of all the occurrences of a into b
        #mr.remove_records_xpath(do_when_keyword=['Reporting INSPIRE'], xpath="//gmd:RS_Identifier/gmd:codeSpace") #remove the gmd:RS_Identifier/gmd:codeSpace elements in all the datasets having the "inspire reporting" keyword
        #mr.replace_records_xpath(do_when_keyword=['humanGeographicViewer', 'infoFeatureAccessService'],xml_snippet=mr.prep_input_file("service_conformance.xml"),xpath="//gmd:report/*/gmd:result", ) # correct conformance for services
        #mr.remove_records_keyword(do_when_keyword=["humanGeographicViewer"], keyword_textual_value="infoFeatureAccessService") # a record can't be WMS and WFS at the same time
        #mr.remove_records_keyword(do_when_keyword=["infoFeatureAccessService"],keyword_textual_value="humanGeographicViewer")  # a record can't be WMS and WFS at the same time
        ## mr.replace_records_hard(do_when_keyword=['Reporting INSPIRE'], fro='<gmd:PT_FreeText />', to='') #do a hard textual replace and not a node replace
        ## mr.modify_records_attribute(do_when_keyword=['Reporting INSPIRE'],xpath="//*[@xsi:type='gmd:PT_FreeText_PropertyType']",attribute='xsi:type',value='') #set all values of the xsi:type attribute to empty, effectively deleting it
        #mr.remove_records_xpath(do_when_keyword=['Reporting INSPIRE','Federal government'], xpath="//srv:coupledResource") #srv:coupledResource is not needed
        #mr.append_record_at(id="29f40b0d-2a3e-49a8-870a-e9b4acd4d1e3", xml_snippet=mr.prep_input_file("input_marine_essentials.xml"), outer="identification", before="descriptiveKeywords")
        #mr.append_record_at(id="83bdcd87-e4ea-4a76-ab98-ff9f45e529f5", xml_snippet=mr.prep_input_file("input_marine_essentials.xml"), outer="identification", before="descriptiveKeywords")
        #mr.append_record_at(id="7b53a7db-eedb-4220-923a-94304c854e75", xml_snippet=mr.prep_input_file("input_marine_essentials.xml"), outer="identification", before="descriptiveKeywords")
        #mr.append_record_at(id="69a40ea3-868e-4f56-a6b2-b313e625ee22", xml_snippet=mr.prep_input_file("input_marine_essentials.xml"), outer="identification", before="descriptiveKeywords")
        #mr.append_record_at(id="7eca7c5e-f1da-4abb-aad3-acc5038bf5ba", xml_snippet=mr.prep_input_file("input_marine_essentials.xml"), outer="identification", before="descriptiveKeywords")
        #mr.append_record_at(id="d409cd5d-3a54-4722-b255-2b4d4374d8ae", xml_snippet=mr.prep_input_file("input_marine_essentials.xml"), outer="identification", before="descriptiveKeywords")
        #mr.append_record_at(id="ee056fd6-995e-40a7-8ebf-b145ea0a30e0", xml_snippet=mr.prep_input_file("input_marine_essentials.xml"), outer="identification", before="descriptiveKeywords")
        #mr.append_record_at(id="8b317fed-fd7e-4374-a378-4831ff458c09", xml_snippet=mr.prep_input_file("input_marine_essentials.xml"), outer="identification", before="descriptiveKeywords")

        print('Finished updating GeoNetwork records')
if __name__ == '__main__':
    modifyrecord.main()
