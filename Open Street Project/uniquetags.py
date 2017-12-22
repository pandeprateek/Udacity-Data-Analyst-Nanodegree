"""
Parse the OSM file and count the numbers of unique tag
"""

import xml.etree.cElementTree as ET
import pprint

tags = {}
OSMFILE = "D:/Udacity/Open Street Project/Centraldelhi.xml"
context = ET.iterparse(OSMFILE, events=("start", "end"))
context = iter(context)
event, root = context.next()
for event, elem in context:
    if elem.tag in tags:
        tags[elem.tag] += 1
    else:
        tags[elem.tag] = 1
    root.clear()


print tags




    



    
    

