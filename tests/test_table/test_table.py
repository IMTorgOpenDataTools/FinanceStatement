#!/usr/bin/env python3
"""
Test Table class

"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "AGPL-3.0"


from src.Table import TableFactory, Table

import tempfile
from pathlib import Path


def test_table_create_from_taxonomy():
    """Create DTS from taxonomy to create instance."""
    taxonomy_path = '/workspaces/Vba2Py_XBRL/tests/test_table/data/HelloWorld.xsd'
    working_dir = '/workspaces/Vba2Py_XBRL/tests/test_table/'
    tblfactory = TableFactory(working_dir)
    with tempfile.TemporaryDirectory() as temp_dir:
        tmp_instance_path = Path(temp_dir) / 'temp.xbrl'
        options = tblfactory.prepare_options(tmp_instance_path)
        table = Table(
            options=options,
            name='table_parent_class',
            filepath=taxonomy_path
        )
        check = table.create_instance_from_taxonomy(tmp_instance_path)
    assert check == True
    assert type( table.get_metadata() ) == dict
    assert type( table.get_dts_docs() ) == list
    assert type( table.get_facts() ) == list
    assert type( table.get_instance() ) == str
    assert type( table.get_schema(as_string=True) ) == str

def test_table_load_xbrl():
    logfile_dir = '/workspaces/Vba2Py_XBRL/tests/test_table/logs'
    tblfactory = TableFactory(logfile_dir)
    with tempfile.TemporaryDirectory() as temp_dir:
        tmp_instance_path = temp_dir / 'temp.xbrli'
        tacct = tblfactory.create_xbrl_instance_table(tmp_instance_path)
    assert True == True

def test_table_load_xsd():
    logfile_dir = '/workspaces/Vba2Py_XBRL/tests/test_table/logs'
    tblfactory = TableFactory(logfile_dir)
    with tempfile.TemporaryDirectory() as temp_dir:
        tmp_instance_path = temp_dir / 'temp.xbrli'
        tacct = tblfactory.create_xbrl_instance_table(tmp_instance_path)
    assert True == True



def test_instsance_class():
    logfile_dir = '/workspaces/Vba2Py_XBRL/tests/test_table/cache'
    tblfactory = TableFactory(logfile_dir)
    instance_path = '/workspaces/Vba2Py_XBRL/tests/test_table/data/HelloWorld.xml'
    table = tblfactory.create_xbrl_instance_table(instance_path)
    metadata = table.get_metadata()
    dts = table.get_dts_docs()
    facts = table.get_facts()
    assert True == True

def test_taxonomy_class():
    logfile_dir = '/workspaces/Vba2Py_XBRL/tests/test_table/cache'
    tblfactory = TableFactory(logfile_dir)
    schema_path = '/workspaces/Vba2Py_XBRL/tests/test_table/data/HelloWorld.xsd'
    schema = tblfactory.create_xbrl_schema_table(schema_path)
    types = schema.xbrl_model.qnameTypes
    concepts = schema.xbrl_model.qnameConcepts
    item1 = concepts.values()[0]
    item1.name, item1.namespaceURI
    assert True == True

def test_taccount():
    logfile_dir = '/workspaces/Vba2Py_XBRL/tests/test_table/logs'
    tblfactory = TableFactory(logfile_dir)
    with tempfile.TemporaryDirectory() as temp_dir:
        tmp_instance_path = temp_dir / 'temp.xbrli'
        tacct = tblfactory.create_xbrl_taccount_table(tmp_instance_path)
    assert True == True
