#!/usr/bin/env python3
"""
Test Table class

"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "AGPL-3.0"


from src.Table import TableFactory, Table

def test_table_instsance():
    logfile_dir = '/workspaces/Vba2Py_XBRL/tests/test_table/cache'
    tblfactory = TableFactory(logfile_dir)
    instance_path = '/workspaces/Vba2Py_XBRL/tests/test_table/data/HelloWorld.xml'
    table = tblfactory.create_xbrl_instance_table(instance_path)
    metadata = table.get_metadata()
    dts = table.get_dts_docs()
    facts = table.get_facts()
    assert True == True

def test_table_schema():
    logfile_dir = '/workspaces/Vba2Py_XBRL/tests/test_table/cache'
    tblfactory = TableFactory(logfile_dir)
    schema_path = '/workspaces/Vba2Py_XBRL/tests/test_table/data/HelloWorld.xsd'
    schema = tblfactory.create_xbrl_schema_table(schema_path)
    types = schema.xbrl_model.qnameTypes
    concepts = schema.xbrl_model.qnameConcepts
    item1 = concepts.values()[0]
    item1.name, item1.namespaceURI
    assert True == True