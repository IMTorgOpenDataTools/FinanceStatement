#!/usr/bin/env python3
"""

TableFactory Class

"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "AGPL-3.0"


from .Table import (
    Instance,
    Taxonomy,
    Taccount
    )

import arelle
from arelle.api.Session import Session
from arelle.logging.handlers.StructuredMessageLogHandler import StructuredMessageLogHandler
from arelle.RuntimeOptions import RuntimeOptions
from arelle.ModelXbrl import ModelXbrl

import xml.etree.ElementTree as ET
from lxml import etree

from pathlib import Path
import io
import os
import zipfile
import copy
import datetime


class TableFactory():
    """..."""

    def __init__(self, working_dir):
        working_dir = Path(working_dir)
        self.local_cache_path = working_dir / 'cache'
        self.logfile_dir = working_dir / 'logs'
        self.options = {
            'entrypointFile': None,
            'disclosureSystemName': None, #ex: 'esef',
            'keepOpen': True, #prevent an open xbrl_model from being automatically closed after a session completes
            'validate': True, #validate format on discovery

            'internetConnectivity': 'online', #'offline'
            'xdgConfigHome': self.local_cache_path, #dir maintains discovered dts docs
            'internetLogDownloads': True, #options: log downloads to confirm cacheing
            'packages': None, #tells arelle where to find taxonomy packages (complex, multi-file xbrl taxonomies that are distributed as .zip files)
            
            'logFile': None,
            'logFormat': "[%(messageCode)s] %(message)s - %(file)s",
            
            'plugins': None, #ex: 'validate/ESEF', 'inlineXbrlDocumentSet (processing iXBRL)
        }

    def prepare_options(self, filepath):
        filepath = Path(filepath)
        options = copy.deepcopy(self.options)
        options['entrypointFile'] = filepath
        options['logFile'] = str(self.logfile_dir / filepath.stem)
        options = {k:str(v) for k,v in options.items()}
        return options

    def create_xbrl_instance_table(self, filepath):
        """Create instance."""
        options = self.prepare_options(filepath)
        table = Instance(
            options=options,
            name='instance',
            path_or_str=filepath
        )
        return table
    '''
    def create_xbrl_schema_table(self, path_or_str):
        """Create schema."""
        table = Taxonomy(
            options=self.options,
            name='schema',
            path_or_str=path_or_str
        )
        return table
    
    def create_xbrl_taccount_table(self):
        """Create schema."""
        table = Taccount(
            options=self.options,
            name='tacct'
        )
        return table
    '''