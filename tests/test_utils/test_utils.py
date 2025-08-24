#!/usr/bin/env python3
"""
Test utils

"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "AGPL-3.0"


from src.utils import (
    parse_xbrl_instance
)


def test_parse_xbrl_instance():
    check = parse_xbrl_instance()
    assert check == True