import xml.etree.cElementTree as ET
import pprint
import re

from collections import defaultdict

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

OSMFILE = "D:/Udacity/Open Street Project/Centraldelhi.xml"

keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
context = ET.iterparse(OSMFILE, events=("start", "end"))
context = iter(context)
event, root = context.next()
for event, elem in context:
    if elem.tag == "tag":
        for tag in elem.iter('tag'):
            k = tag.get('k')
            if lower.search(elem.attrib['k']):
                keys['lower'] = keys['lower'] + 1
            elif lower_colon.search(elem.attrib['k']):
                keys['lower_colon'] = keys['lower_colon'] + 1
            elif problemchars.search(elem.attrib['k']):
                keys['problemchars'] = keys['problemchars'] + 1
            else:
                keys['other'] = keys['other'] + 1
        
print keys
