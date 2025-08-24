import json
from lxml import etree
import xml.etree.ElementTree as ET


def are_xml_files_identical_lxml(file1_path, file2_path):
    """Determine if two xml files are identical."""
    try:
        parser = etree.XMLParser(remove_comments=True)
        tree1 = etree.parse(file1_path, parser)
        tree2 = etree.parse(file2_path, parser)

        # Canonicalize the XML trees for a robust comparison
        # This handles differences in whitespace, attribute order, etc.
        xml_string1 = etree.tostring(tree1, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')
        xml_string2 = etree.tostring(tree2, pretty_print=True, encoding='utf-8', xml_declaration=True).decode('utf-8')

        return xml_string1 == xml_string2
    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML: {e}")
        return False
    except FileNotFoundError:
        print("One or both files not found.")
        return False
    

def json_to_xml(json_obj, line_padding=""):
    """Convert .json to .xml
    
    ::usage
    json_data = '{"name": "John", "age": 30, "city": "New York"}'
    json_obj = json.loads(json_data)
    xml_data = json_to_xml(json_obj)
    print(f"<root>\n{xml_data}\n</root>")
    """
    result_list = []
    for key, value in json_obj.items():
        if isinstance(value, dict):
            result_list.append(f"{line_padding}<{key}>")
            result_list.append(json_to_xml(value, line_padding + "  "))
            result_list.append(f"{line_padding}</{key}>")
        elif isinstance(value, list):
            for item in value:
                result_list.append(f"{line_padding}<{key}>")
                result_list.append(json_to_xml(item, line_padding + "  "))
                result_list.append(f"{line_padding}</{key}>")
        else:
            result_list.append(f"{line_padding}<{key}>{value}</{key}>")
    return "\n".join(result_list)




def parse_xbrl_instance():
    """..."""
    from lxml import etree

    # Example XBRL instance document content (simplified for illustration)
    xbrl_content = """
    <xbrli:xbrl
        xmlns:xbrli="http://www.xbrl.org/2003/instance"
        xmlns:xbrldi="http://xbrl.org/2006/xbrldi"
        xmlns:us-gaap="http://fasb.org/us-gaap/2024-01-31"
        xmlns:iso4217="http://www.xbrl.org/2003/iso4217"
        xmlns:link="http://www.xbrl.org/2003/linkbase"
        xmlns:xlink="http://www.w3.org/1999/xlink">

        <xbrli:context id="c_2024Q1">
            <xbrli:entity>
                <xbrli:identifier scheme="http://www.sec.gov/cik">0000123456</xbrli:identifier>
            </xbrli:entity>
            <xbrli:period>
                <xbrli:startDate>2024-01-01</xbrli:startDate>
                <xbrli:endDate>2024-03-31</xbrli:endDate>
            </xbrli:period>
        </xbrli:context>

        <us-gaap:Revenues contextRef="c_2024Q1" unitRef="USD">
            100000000
        </us-gaap:Revenues>

        <xbrli:unit id="USD">
            <xbrli:measure>iso4217:USD</xbrli:measure>
        </xbrli:unit>

    </xbrli:xbrl>
    """

    # Parse the XBRL content from a string
    root = etree.fromstring(xbrl_content)

    # Define namespaces for easier element access
    nsmap = {
        "xbrli": "http://www.xbrl.org/2003/instance",
        "us-gaap": "http://fasb.org/us-gaap/2024-01-31"
    }

    # Find and print the value of the 'Revenues' element
    revenues_element = root.find(".//us-gaap:Revenues", namespaces=nsmap)
    if revenues_element is not None:
        print(f"Revenues: {revenues_element.text}")
        print(f"Context Reference: {revenues_element.get('contextRef')}")
        print(f"Unit Reference: {revenues_element.get('unitRef')}")

    # Find and print the entity identifier from the context
    entity_identifier_element = root.find(".//xbrli:identifier", namespaces=nsmap)
    if entity_identifier_element is not None:
        print(f"Entity Identifier: {entity_identifier_element.text}")
        print(f"Scheme: {entity_identifier_element.get('scheme')}")

    # Find and print the period dates
    start_date_element = root.find(".//xbrli:startDate", namespaces=nsmap)
    end_date_element = root.find(".//xbrli:endDate", namespaces=nsmap)
    if start_date_element is not None and end_date_element is not None:
        print(f"Period Start Date: {start_date_element.text}")
        print(f"Period End Date: {end_date_element.text}")

    return True