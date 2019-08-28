import lxml.etree as ET
import csv
import os

XML_NAMESPACE = '{http://www.w3.org/XML/1998/namespace}'
TEI_NAMESPACE = '{http://www.tei-c.org/ns/1.0}'

tree = ET.parse("../2541/2541/VUAMC2.xml")

paragraph_id = 0
for element in tree.iter(TEI_NAMESPACE + 'p'):
    element.attrib['n'] = str(paragraph_id)
    paragraph_id += 1

with open('../data/VUAMC3.xml', 'wb') as f:
    tree.write(f)
