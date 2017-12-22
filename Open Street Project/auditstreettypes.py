# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

expected = ["New Delhi", "Road", "Enclave", "Marg", "Lane", "Avenue"]
OSMFILE_sample = "D:/Udacity/Open Street Project/Centraldelhi.xml"
regex = re.compile(r'\b\S+\.?$', re.IGNORECASE)
regex2 = re.compile(r'name')
listn = []
street_types = defaultdict(set)

def audit_street(street_name): # Check condition if it matched with the regular expression or not and then creating dictionary for matched cases
    m = regex.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            return

def is_street_name(elem): # Check if it is a street name
    return (elem.attrib['k'] == "addr:street")


def audit_names(values, names):# check for the names where the attribute value is new delhi, but not in a proper manner.
    n = regex2.match(values)
    if n:
        listn.append(names)
        return



osm_file = open(OSMFILE_sample, "r")
for event, elem in ET.iterparse(osm_file, events=("start",)):
    if elem.tag == "node" or elem.tag == "way":
        for tag in elem.iter("tag"):
            if elem.attrib['id'] == "16173236":
                audit_names(tag.attrib['k'], tag.attrib['v'])# calling audit names function for node tag where id attribute value is 16173236.
            else:
                if is_street_name(tag):
                    audit_street(tag.attrib['v'])# calling audit street to print dictionary for street types
                                                     
            
                    
                        
print ",".join(listn)
print dict(street_types)

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




# Printing Updated Names

for street_type,ways in street_types.iteritems():
    if street_type in mapping1:
        print street_type  ,">", mapping1[street_type]

for name in listn:
    if name.encode('utf-8') in mapping2:
        print name ,">",mapping2[name.encode('utf-8')]



                        
            
