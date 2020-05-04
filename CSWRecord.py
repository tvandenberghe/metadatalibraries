import params
import time
import copy
from lxml import etree as ET
class CSWRecord(object):

    schemas = {
        "gmd": "http://" + "www.isotc211.org/2005/gmd",
        "gco": "http://" + "www.isotc211.org/2005/gco",
        "gmx": "http://" + "www.isotc211.org/2005/gmx",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
      #  "xmlns": "http://www.opengis.net/wms",
        "xlink": "http://www.w3.org/1999/xlink",
        'atom': "http://www.w3.org/2005/Atom",
        'wfs': "http://www.opengis.net/wfs/2.0",
        'srv': 'http://www.isotc211.org/2005/srv',
        'rdf': "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "skos": "http://www.w3.org/2004/02/skos/core#"
    }

    def __init__(self, xml,id):
        self.xml=xml
        self.id=id

    def get_position(self,outer, inner):
        outer_el=self.xml.xpath(params.get_metadata_elmt(outer), namespaces=CSWRecord.schemas)[0]
        inner_element = None
        if isinstance(inner,list):
            for inner_token in inner:
                for element in self.xml.xpath(params.get_metadata_elmt(inner_token), namespaces=CSWRecord.schemas):
                    if element is not None and inner_element is None:
                        inner_element = element
        else:
            inner_element = self.xml.xpath(params.get_metadata_elmt(inner), namespaces=CSWRecord.schemas)[0]
        position = outer_el.index(inner_element)
        return position

    def selectsiblingtags(self, xpath, extrapath=None):             #extrapath=maintag pour la balise principale, PT_FreeText pour une balise d'une langue locale et demeure vide pour les balises sans texte (code liste, date,...)
        path= params.get_metadata_elmt(xpath)
        if extrapath is not None:
            path= params.get_metadata_elmt(xpath) + params.get_metadata_elmt(extrapath)

        return self.xml.xpath(path, namespaces=CSWRecord.schemas)

    def updatemetadatadate(self):
        yy=str(time.strftime("%Y"))
        mm=str(time.strftime("%m"))
        dd=str(time.strftime("%d"))
        hour=str(time.strftime("%H"))
        min=str(time.strftime("%M"))
        sec=str(time.strftime("%S"))
        metadatadate=self.xml.xpath(params.get_metadata_elmt("metadatadate"), namespaces=CSWRecord.schemas)[0]
        metadatadate.text=str(yy)+'-'+str(mm)+'-'+str(dd)+'T'+str(hour)+':'+str(min)+':'+str(sec)


    def updaterevisiondate (self):
        yy=str(time.strftime("%Y"))
        mm=str(time.strftime("%m"))
        dd=str(time.strftime("%d"))
        hour=str(time.strftime("%H"))
        min=str(time.strftime("%M"))
        sec=str(time.strftime("%S"))
        date=str(yy)+'-'+str(mm)+'-'+str(dd)
        try:
            revision=self.xml.xpath(params.get_metadata_elmt('revisiondate'), namespaces=CSWRecord.schemas)
            revision=revision[0].xpath("./gmd:CI_Date/gmd:date/gco:Date",namespaces=CSWRecord.schemas)
            revision[0].text=date

        except:
            creation=self.xml.xpath(params.get_metadata_elmt('creationdate'), namespaces=CSWRecord.schemas)
            revision=copy.deepcopy(creation[0])
            revision.xpath('./gmd:CI_Date/gmd:dateType/gmd:CI_DateTypeCode', namespaces=CSWRecord.schemas)[0].set('codeListValue','revision')
            CI_Citation=self.xml.xpath(params.get_metadata_elmt('CI_Citation'), namespaces=CSWRecord.schemas)[0]
            i=CI_Citation.index(creation[0])
            CI_Citation.insert(i,revision)
            revision=CI_Citation.xpath("./gmd:date/gmd:CI_Date/gmd:date/gco:Date", namespaces=CSWRecord.schemas)
            revision[0].text=date

        self.updatemetadatadate()

    def print_xml(self):
        return ET.tostring(self.xml, pretty_print=True)

    def remove_tag(self, tag):  # 1 balise peut repondre au XPATH
        tag.getparent().remove(tag)
        self.updatemetadatadate()

    def modifytag(self, oldtag, newtag):                                     #1 balise peut repondre au XPATH
        oldtag.tag=newtag
        self.updatemetadatadate()

    def modifyattribute(self, oldtag, attribute, value):
        oldtag.set(attribute,value)
        self.updatemetadatadate()

    def modifycontent(self,oldtag, value):
        oldtag.text=value
        self.updatemetadatadate()

    def addtag(self,mothertag, input_xml, position=0):
        if isinstance(mothertag,str):
            mothertag = self.xml.xpath(params.get_metadata_elmt(mothertag), namespaces=CSWRecord.schemas)[0]
        if isinstance(mothertag,ET._Element):
            mothertag=mothertag
        if isinstance(input_xml,str):
            input_xml =  ET.fromstring(input_xml)
           # input_xml = input_xml.getroot()
        if isinstance(input_xml,ET._Element):
            mothertag.insert(position, input_xml)
            self.updatemetadatadate()
