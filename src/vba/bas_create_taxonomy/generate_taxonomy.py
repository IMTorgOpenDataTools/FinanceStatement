#!/usr/bin/env python3
"""
Entrypoint for creating instance document file

Note: In the Python code, you'll need to replace the placeholder values (like 
"C6_value.txt", "C4_value", "C5_value", and the sample elements) with the 
actual values from your Excel sheet. You might also need to adjust the file 
path and element data structure based on your specific requirements.

"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "AGPL-3.0"



import os
from datetime import datetime

def create_using_string(args):
    output_file = args['output_file']
    namespace_prefix = args['namespace_prefix']
    namespace_identifier = args['namespace_identifier']
    # Create and write to the file
    with open(output_file, 'w', encoding='utf-8') as file:
        # Write XML header and comments
        file.write('<?xml version="1.0" encoding="utf-8"?>\n')
        file.write('<!-- HelloWorld Example -->\n')
        file.write(f'<!-- Date/time created: {datetime.now()} -->\n\n')

        # Write schema opening tag
        file.write('<schema  xmlns="http://www.w3.org/2001/XMLSchema"\n')
        file.write('         xmlns:xbrli="http://www.xbrl.org/2003/instance"\n')
        file.write('         xmlns:link="http://www.xbrl.org/2003/linkbase"\n')
        file.write('         xmlns:xlink="http://www.w3.org/1999/xlink"\n')
        file.write(f'         xmlns:{namespace_prefix}="{namespace_identifier}"\n')  # Replace "C4_value" and "C5_value" with actual values from cells C4 and C5
        file.write(f'         targetNamespace="{namespace_identifier}"\n')  # Replace "C5_value" with actual value from cell C5
        file.write('         elementFormDefault="qualified"\n')
        file.write('         attributeFormDefault="unqualified">\n\n')

        # Write import section
        file.write('   <import\n')
        file.write('      namespace="http://www.xbrl.org/2003/instance"\n')
        file.write('      schemaLocation="http://www.xbrl.org/2003/xbrl-instance-2003-12-31.xsd" />\n\n')

        # Write elements (replace with actual data from your Excel sheet)
        elements = [
            {"name": "Element1", "type": "Type1", "period_type": "Period1", "substitution_group": "Group1"},
            {"name": "Element2", "type": "Type2", "period_type": "Period2", "substitution_group": "Group2"},
            # Add more elements as needed
        ]

        for element in elements:
            file.write('   <element\n')
            file.write(f'       name="{element["name"]}"\n')
            file.write(f'       type="{element["type"]}"\n')
            file.write(f'       substitutionGroup="{element["substitution_group"]}"\n')
            file.write(f'       xbrli:periodType="{element["period_type"]}" />\n\n')

        # Write closing tag
        file.write('</schema>')



from lxml import etree

def create_using_lxml(args):
    """..."""
    output_file = args['output_file']
    namespace_prefix = args['namespace_prefix']
    namespace_identifier = args['namespace_identifier']
    nsmap = {
        'xmlns': 'http://www.w3.org/2001/XMLSchema',
        'xbrli': 'http://www.xbrl.org/2003/instance'
        }
    remove_xlmns_placeholder = 'xmlns'
    etree.register_namespace(remove_xlmns_placeholder, nsmap['xmlns'])
    etree.register_namespace('xbrli', nsmap['xbrli'])
    elementsInfo = [
        {"name": "Element1", "type": etree.QName(nsmap['xbrli'],"Type1"), "substitutionGroup": etree.QName(nsmap['xbrli'],"Group1"), etree.QName(nsmap['xbrli'],"periodType"): "Period1"},
        {"name": "Element2", "type": etree.QName(nsmap['xbrli'],"Type2"), "substitutionGroup": etree.QName(nsmap['xbrli'],"Group2"), etree.QName(nsmap['xbrli'],"periodType"): "Period2"},
        # Add more elements as needed
        ]
    #schema
    root = etree.Element("root")
    # Create an element with a namespace
    #schema = etree.Element('{%s}schema' % (nsmap["xmlns"]), nsmap={None: nsmap["xmlns"]})
    schema  = etree.SubElement(root, 'schema')   #, '{%s}schema' % (nsmap["xmlns"]))
    qname = etree.QName(nsmap["xmlns"], 'xbrli')
    schema.attrib[qname] = "http://www.xbrl.org/2003/instance"
    qname = etree.QName(nsmap["xmlns"], 'xbrli')
    schema.attrib[qname] = "http://www.xbrl.org/2003/instance"
    qname = etree.QName(nsmap["xmlns"], 'link')
    schema.attrib[qname] = "http://www.xbrl.org/2003/linkbase"
    qname = etree.QName(nsmap["xmlns"], 'xlink')
    schema.attrib[qname] = "http://www.w3.org/1999/xlink"
    qname = etree.QName(nsmap["xmlns"], output_file )
    schema.attrib[qname] = f"http://xbrl.squarespace.com/{output_file}"
    schema.attrib['targetNamespace'] = f"http://xbrl.squarespace.com/{output_file}"
    schema.attrib['elementFormDefault'] = "qualified"
    schema.attrib['attributeFormDefault'] = "unqualified"

    #import
    elImport = etree.SubElement(schema, "import")
    elImport.attrib['namespace'] = 'http://www.xbrl.org/2003/instance'
    elImport.attrib['schemaLocation'] = 'http://www.xbrl.org/2003/xbrl-instance-2003-12-31.xsd'

    #child.text = "This is a child element"
    for info in elementsInfo:
        el = etree.SubElement(schema, "element")
        for k,v in info.items():
            el.attrib[k] = v

    tree = etree.ElementTree(schema)
    tree_str = etree.tostring(tree).decode()
    tree_str = tree_str.replace(f':{remove_xlmns_placeholder}=', '=')
    tree = etree.fromstring(tree_str)
    tree = etree.ElementTree(tree)
    tree.write(output_file, pretty_print=True, xml_declaration=True, encoding="utf-8")




def generate_taxonomy(file_path, method='string'):
    #get the output file path
    output_file = os.path.join(os.getcwd(), file_path)  # Replace "C6_value.txt" with the actual value from cell C6
    args = {
        'output_file' : output_file,
        'namespace_prefix' : 'HelloWorld',
        'namespace_identifier': 'http://xbrl.squarespace.com/HelloWorld'
    }
    #create taxonomy
    match method:
        case 'string': 
            create_using_string(args)
        case 'lxml': 
            create_using_lxml(args)
        case _: 
            pass
    return True

# Call the function to generate the taxonomy
#generate_taxonomy()
