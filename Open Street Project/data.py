# -*- coding: utf-8 -*-
import csv
import codecs
import re
import xml.etree.cElementTree as ET
from unittest import TestCase

import cerberus
import schema

OSM_PATH = "D:/Udacity/Open Street Project/Centraldelhi.xml"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
regex1 = re.compile(r'\b\S+\.?$', re.IGNORECASE)
regex2 = re.compile(r'name')

SCHEMA = schema.schema

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

mapping1 = {"Ln":"Lane",
            "lane":"Lane"}

mapping2 = {"Nieu-Delhi":"New Delhi",
"ኒው ዴሊ":"New Delhi",
"Nueva Delhi":"New Delhi",
"Nīƿe Delhi":"New Delhi",
"دلهي الجديد":"New Delhi",
"نيودلهي":"New Delhi",
"دلهي جديد":"New Delhi",
"Naujasės Delės":"New Delhi",
"Нью-Дэлі":"New Delhi",
"Нью-Дэлі":"New Delhi",
"Ню Делхи":"New Delhi",
"নতুন দিল্লি":"New Delhi",
"ནེའུ་དིལ་ལི།":"New Delhi",
"নুৱা দিল্লী":"New Delhi",
"Nova Delhi":"New Delhi",
"Nueva Delhi":"New Delhi",
"نیودلھی":"New Delhi",
"Nyu Deli":"New Delhi",
"Nové Dillí":"New Delhi",
"Delhi Newydd":"New Delhi",
"Neu-Delhi":"New Delhi",
"Delhiyo Newe":"New Delhi",
"ނިއުދިއްލީ":"New Delhi",
"Νέο Δελχί":"New Delhi",
"Nov-Delhio":"New Delhi",
"Nueva Delhi":"New Delhi",
"Nueva Delhi":"New Delhi",
"دهلی نو":"New Delhi",
"Nij Delly":"New Delhi",
"Nua-Deilí":"New Delhi",
"Nova Deli - नई दिल्ली":"New Delhi",
"Delhi Noa":"New Delhi",
"ניו דלהי":"New Delhi",
"नई दिल्ली":"New Delhi",
"Niou Deli":"New Delhi",
"Újdelhi":"New Delhi",
"Նյու Դելի":"New Delhi",
"Nove Delhi":"New Delhi",
"Nova-Delhi":"New Delhi",
"Nýja Delí":"New Delhi",
"Nuova Delhi":"New Delhi",
"ニューデリー":"New Delhi",
"ნიუ-დელი":"New Delhi",
"Нью-Дели":"New Delhi",
"ಹೊಸ ದೆಹಲಿ":"New Delhi",
"뉴델리":"New Delhi",
"نٔو دلھی":"New Delhi",
"Delhiya Nû":"New Delhi",
"Dellium Novum":"New Delhi",
"Nei-Delhi":"New Delhi",
"Neuva Delhi":"New Delhi",
"Naujasis Delis":"New Delhi",
"Ņūdeli":"New Delhi",
"Њу Делхи":"New Delhi",
"ന്യൂ ഡെൽഹി":"New Delhi",
"Шинэ Дели":"New Delhi",
"नवी दिल्ली":"New Delhi",
"နယူးဒေလီမြို့":"New Delhi",
"نو دهلی":"New Delhi",
"Yancuīc Deli":"New Delhi",
"नयाँ दिल्ली":"New Delhi",
"Novi Deli":"New Delhi",
"Nòva Delhi":"New Delhi",
"Нью-Дели":"New Delhi",
"ਨਵੀਂ ਦਿੱਲੀ":"New Delhi",
"Nowe Delhi":"New Delhi",
"نئی دلی":"New Delhi",
"Nova Deli":"New Delhi",
"Musuq Dilhi":"New Delhi",
"Нью-Дели":"New Delhi",
"नवदेहली":"New Delhi",
"Саҥа Дели":"New Delhi",
"Nova Delhi":"New Delhi",
"නව දිල්ලිය":"New Delhi",
"Naí Dillí":"New Delhi",
"Њу Делхи":"New Delhi",
"புது தில்லி":"New Delhi",
"క్రొత్త ఢిల్లీ":"New Delhi",
"Ню-Дели":"New Delhi",
"นิวเดลี":"New Delhi",
"Bagong Delhi":"New Delhi",
"Yeni Delhi":"New Delhi",
"Yéngi Déhli":"New Delhi",
"Нью-Делі":"New Delhi",
"نئی دہلی":"New Delhi",
"Tân Delhi":"New Delhi",
"ניי דעלי":"New Delhi",
"新德里":"New Delhi",
"Sin Delhi":"New Delhi",
"新德里":"New Delhi",
}


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  

    if element.tag == 'node':
        for attrib in element.attrib:
            if attrib in NODE_FIELDS:
                node_attribs[attrib] = element.attrib[attrib]
        
        for child in element:
            node_tag = {}
            if LOWER_COLON.match(child.attrib['k']):
                node_tag['type'] = child.attrib['k'].split(':',1)[0]
                node_tag['key'] = child.attrib['k'].split(':',1)[1]
                node_tag['id'] = element.attrib['id']
                node_tag['value'] = child.attrib['v']
                if (child.attrib["k"] == 'addr:street'):# Data Cleaning
                    m = regex1.search(child.attrib['v'])
                    result = m.group()
                    if result in mapping1:
                        child.attrib['v'] = child.attrib['v'].replace(result,mapping1[result])
                        node_tag["value"] = child.attrib["v"]
                elif (regex2.match(child.attrib['k'])):
                    if element.attrib['id']=="16173236":
                        if child.attrib['v'].encode('utf-8') in mapping2:
                            node_tag['value']=mapping2[child.attrib['v'].encode('utf-8')]     
                      
                tags.append(node_tag)
            elif PROBLEMCHARS.match(child.attrib['k']):
                continue
            else:
                
                node_tag['type'] = 'regular'
                node_tag['key'] = child.attrib['k']
                node_tag['id'] = element.attrib['id']
                node_tag["value"] = child.attrib["v"]
                tags.append(node_tag)
        
        return {'node': node_attribs, 'node_tags': tags}
        
    elif element.tag == 'way':
        for attrib in element.attrib:
            if attrib in WAY_FIELDS:
                way_attribs[attrib] = element.attrib[attrib]
        
        position = 0
        for child in element:
            way_tag = {}
            way_node = {}
            
            if child.tag == 'tag':
                if LOWER_COLON.match(child.attrib['k']):
                    way_tag['type'] = child.attrib['k'].split(':',1)[0]
                    way_tag['key'] = child.attrib['k'].split(':',1)[1]
                    way_tag['id'] = element.attrib['id']
                    way_tag['value'] = child.attrib['v']
                    tags.append(way_tag)
                elif PROBLEMCHARS.match(child.attrib['k']):
                    continue
                else:
                    way_tag['type'] = 'regular'
                    way_tag['key'] = child.attrib['k']
                    way_tag['id'] = element.attrib['id']
                    way_tag['value'] = child.attrib['v']
                    tags.append(way_tag)
                    
            elif child.tag == 'nd':
                way_node['id'] = element.attrib['id']
                way_node['node_id'] = child.attrib['ref']
                way_node['position'] = position
                position += 1
                way_nodes.append(way_node)
            
        
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_strings = (
            "{0}: {1}".format(k, v if isinstance(v, str) else ", ".join(v))
            for k, v in errors.iteritems()
        )
        raise cerberus.ValidationError(
            message_string.format(field, "\n".join(error_strings))
        )


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    process_map(OSM_PATH, validate=True)
