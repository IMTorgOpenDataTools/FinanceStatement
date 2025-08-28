#!/usr/bin/env python3
"""

Table Class

"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "AGPL-3.0"


from arelle.api.Session import Session
from arelle.logging.handlers.StructuredMessageLogHandler import StructuredMessageLogHandler
from arelle.RuntimeOptions import RuntimeOptions

import xml.etree.ElementTree as ET

from pathlib import Path
import io
import os
import zipfile


class TableFactory():
    """..."""

    def __init__(self, logfile_dir):
        local_cache_path = os.path.abspath('/workspaces/Vba2Py_XBRL/tests/test_table/cache')
        options = {
            'entrypointFile': None,
            #'disclosureSystemName': 'esef',
            'keepOpen': True, #prevent an open xbrl_model from being automatically closed after a session completes

            'internetConnectivity': 'online',
            'xdgConfigHome': local_cache_path,
            'internetLogDownloads': True, #options: log downloads to confirm cacheing

            'logFile': Path(logfile_dir),
            'logFormat': "[%(messageCode)s] %(message)s - %(file)s",
            #'packages': None, #tells arelle where to find taxonomy packages (complex, multi-file xbrl taxonomies that are distributed as .zip files)
            #'plugins': 'validate/ESEF',
            'validate': True,
        }
        self.options = RuntimeOptions(**options)

    def create_xbrl_instance_table(self, instance_path_or_str):
        """Create instance."""
        table = Table(
            options=self.options,
            name='instance',
            instance=instance_path_or_str
        )




class Table:
    """..."""

    def __init__(self, options, name, instance=None, taxonomy=None):
        #initialize arelle
        options.logFile = str( options.logFile / name)
        self.options = options

        #attrs
        self.instance = None
        self.taxonomy = None
        self.xbrl_model = self.add_xbrl_model(instance)
        #self.instance
        #self.add_taxonomy
        #self.add_t_account()
        self.constraints = {}

    def __repr__(self):
        pass    

    def add_xbrl_model(self, instance):
        if instance:
            return self.load_xbrl(instance)
        else:
            return instance
        
    def validate_xbrl(self, model_xbrls):
        """Validate XBRL ..."""
        try:
            for model_xbrl in model_xbrls:
                if model_xbrl.errors:
                    xbrl_file_path = model_xbrl.fileSource.url
                    print(f"Validation error found in {xbrl_file_path}:")
                    for error in model_xbrl.errors:
                        print(f"  - {error}")
                    return False
                else:
                    print(f"Validation successful for '{xbrl_file_path}.  No errors found.")
                    return True
        except Exception as e:
            print(f"an unexpected error occurred during validation: {e}")
            return False
    
    def load_xbrl(self, path_or_str=None):
        """Load xbrl from a file path or directly from string.
        
        Note:
            In Arelle, ...
        """
        #prepare input
        path = Path(path_or_str)
        if path.is_file():
            with open(path, 'r') as f:
                content = f.read()
        else:
            content = path_or_str
        self.instance = content
        #prepare options
        filelike_content = io.StringIO(content)
        if not filelike_content:
            raise Exception(f'there was an error in loading xbrl: {path_or_str}')
        self.options.entrypointFile = path_or_str  #filelike_content
        self.options.validate = True
        #run
        with Session() as session:
            session.run(self.options)
            xbrl_models = session.get_models()    #.modelManager.modelXbrls
            xbrl_model = xbrl_models[0]
            self.validate_xbrl(xbrl_models)
        return xbrl_model
    
    def get_metadata(self):
        """Get the xbrl model metadata.
        
        """
        pass


        