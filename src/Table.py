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
        self.options = {
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

    def create_xbrl_instance_table(self, path_or_str):
        """Create instance."""
        table = Instance(
            options=RuntimeOptions(**self.options),
            name='instance',
            path_or_str=path_or_str
        )
        return table
    
    def create_xbrl_schema_table(self, path_or_str):
        """Create schema."""
        table = Taxonomy(
            options=RuntimeOptions(**self.options),
            name='schema',
            path_or_str=path_or_str
        )
        return table




class Table:
    """..."""

    def __init__(self, options, name, path_or_str=None):
        #initialize arelle
        options.logFile = str( Path(options.logFile) / name)
        self.options = options

        #attrs
        self.xbrl_model = self.add_xbrl_model(path_or_str)
        #self.add_taxonomy
        #self.add_t_account()
        self.constraints = {}

    def __repr__(self):
        pass    

    def add_xbrl_model(self, path_or_str):
        if path_or_str:
            return self.load_xbrl(path_or_str)
        else:
            return path_or_str
        
    def validate_xbrl(self, model_xbrls):
        """Validate XBRL string as either instance or taxonomy.  All
        error-handling logic is contained, here.

        If your XBRL string references external schemas or linkbases,
        arelle will attempt to discover and load them based on the
        schemaLocation or link:linkbaseRef declarations within the
        string.  Ensure these referenced files are accessible to arelle
        (either locally or via a network).

        Args:
            xbrl_file_path (str): The path to the XBRL instance document.

        Returns:
            bool: True if the document is valid and no errors are found, False otherwise.
        
        """
        try:
            for model_xbrl in model_xbrls:
                xbrl_file_path = model_xbrl.fileSource.url
                if model_xbrl.errors:
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
            In Arelle, you do not directly instantiate the ModelDocument
            class.  Instead, it is managed internally by the ModelXbrl
            object, which represents a complete XBRL document set (DTS).
            You load an XBRL file using modelManager.load(), which returns
            a ModelXbrl insance, and then access the individual ModelDocument
            objects from there.

            When Arelle performs "discovery," it doesn't just load the single
            entry point file.  It also follows all the links and references
            within that file to bild a complete DTS.  This includes:
            * SchemaRef elements to load the XBRL schemas.
            * LinkbaseRef elements to load definition, presentation,
            calculation, and label linkbases.
            * Import statements in the schemas to find and load dependent schemas.
            The session.get_model() method then gives you access to the fully
            discovered and loaded DTS, represented by the ModelXbrl object.

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
        filelike_content = io.StringIO(content) #TODO:remove???
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
        
        Usage:
            metadata = table.get_metadta()
        """
        entry_doc = self.xbrl_model.modelDocument #the entry point ModelDocument
        all_docs = list(self.xbrl_model.urlDocs.values())
        metadata = {
            'entrypoint_doc': entry_doc.uri,
            'dts_doc_count': len(all_docs),
            'contexts': self.xbrl_model.contexts,
            'units': self.xbrl_model.units,
            'relationships': self.xbrl_model.relationshipSets
        }
        return metadata
        
    def to_file(self, filepath):
        """Export Instance and DTS package to filepath.
        
        Usage:
            table.to_file(filepath)
        """
        self.xbrl_model.saveInstance()
        self.xbrl_model.saveDTSpackage()
    
    def to_taxonomy_package_zip(self, source_dir, output_zip_path):
        """Create `taxonomy package` .zip file from a source directory.
        
        Args:
            source_dir (str): The path to the directory containing the taxonomy files.
            output_zip_path (str): The desired path for the output ZIP file.
        Usage:
            taxonomy_source_directory = 'path/to/your/taxonomy_files'
            output_zip_file = 'my_taxonomy_package.zip'
            create_taxonomy_package_zip(taxonomy_source_directory, output_zip_file)
        Note:
        must use the `zipfile` module
        """
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    #calculate the relative path within the zip file
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
        print(f'Taxonomy package created at {output_zip_path}')
        return True




class Instance(Table):
    """Complete XBRL Instance with all documents
    
    Needs:
        * use as general xbrl data store, such as H8
        * load using multiple formats: fof tbl, smdx, json, etc.
        * ...
        * easy selection for custom display (dimensions, periods)
        * display in variety of formats, fof tbl, financial (balance, income, etc.)
        * display making use of taxonomy for formatting
        * crud rules to display marking
    """

    def __init__(self, options, name, path_or_str=None):
        super().__init__(options, name, path_or_str)

    def get_dts_docs(self):
        """Get the xbrl model DTS documents.
        
        Usage:
            metadata = table.get_dts_docs()
        """
        all_docs = list(self.xbrl_model.urlDocs.values())
        for doc in all_docs:
            print(f"URI: {doc.uri}")
            print(f"Type: {doc.type}")  #example: 1 for SCHEMA, 2 for LINKBASE, 3 for INSTANCE
            print("-" * 20)
        return all_docs
    
    def get_facts(self):
        """Get xbrl instance facts.
        
        Usage:
            facts = table.get_facts()
            print( facts[0].qname.localName )
            print( facts[0].value )
            print( facts[0].contextID )
        """
        if self.xbrl_model:
            return list(self.xbrl_model.facts)


class Taxonomy(Table):
    """Taxonomy class
    
    Needs:
        * work with labels, definitions, examples
        * create taxonomy hierarchical structure
        * update with ontology structure
    """

    def __init__(self, options, name, path_or_str=None):
        super().__init__(options, name, path_or_str)

    def get_concept_labels(self):
        """..."""
        # A specific label role (e.g., standard, terse) and language can be specified.
        # The standard label role is the default.
        label_role = "http://www.xbrl.org/2003/role/label"
        label_lang = "en"
        if self.xbrl_model:
            # Iterate over all concepts in the DTS
            for concept in self.xbrl_model.qnameConcepts.values():
                # Get the label for the concept based on the specified role and language
                label = concept.label(preferredLabel=label_role, lang=label_lang, returnGen=False)

                # Print the concept name and its label, if found
                if label:
                    print(f"Concept: {concept.name}, Label: {label}")
                else:
                    print(f"Concept: {concept.name}, Label: No label found for role '{label_role}' and language '{label_lang}'")


class Taccount(Table):
    """T-account class

    TODO:godley table, or another?
    
    Needs:
        * crud rows
        * crud constraints to ensure compliance
        * display
        * link with other T-accounts for quadruple accounting
    """

    def __init__(self, options, name, path_or_str=None):
        super().__init__(options, name, path_or_str)

        