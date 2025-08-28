#!/usr/bin/env python3
"""
Test Table class

"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "AGPL-3.0"


from src.Table import TableFactory, Table

def test_table():
    logfile_dir = '/workspaces/Vba2Py_XBRL/tests/test_table/cache'
    tblfactory = TableFactory(logfile_dir)
    instance_path_or_str = '/workspaces/Vba2Py_XBRL/tests/test_table/data/HelloWorld.xml'
    table = tblfactory.create_xbrl_instance_table(instance_path_or_str)
    assert True == True