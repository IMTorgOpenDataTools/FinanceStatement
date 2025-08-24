#!/usr/bin/env python3
"""
Test template (default) workflow

"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "AGPL-3.0"


from src.bas_create_taxonomy import generate_taxonomy as gt
from src.bas_create_instance_doc import None
from src.utils import are_xml_files_identical_lxml


def test_generate_taxonomy_string():
    file_path = 'tests/test_hello_world/HelloWorld.xsd'
    test_path = 'tests/test_hello_world/data/HelloWorld_no_attrs.xsd'
    check = gt.generate_taxonomy(file_path, 'string')
    check = are_xml_files_identical_lxml(file_path, test_path)
    assert check == True

def test_generate_taxonomy_lxml():
    file_path = 'tests/test_hello_world/HelloWorld.xsd'
    test_path = 'tests/test_hello_world/data/HelloWorld_no_attrs.xsd'
    check = gt.generate_taxonomy(file_path, 'lxml')
    check = are_xml_files_identical_lxml(file_path, test_path)
    assert check == True

def test_validate_data():
    assert True == True

def test_generate_instance_lxml():
    assert True == True