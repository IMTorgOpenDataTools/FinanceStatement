#!/usr/bin/env python3
"""

Table Class

"""

__author__ = "Jason Beach"
__version__ = "0.1.0"
__license__ = "AGPL-3.0"

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


class Table:
    """Table class
    
    Note:
        * XBRL (xbrl_model) and DTS refer to the same collection of docs
        * XBRL must be instantiated with either instance doc or taxonomy
        * session.models() contains the doc collection
    """

    supported_suffixes = ['.xsd', '.xbrl', '.xbrli']
    schema_suffix = supported_suffixes[:1]
    instance_suffix = supported_suffixes[1:]

    def __init__(self, options, name, filepath=None):
        #initialize
        self.options = RuntimeOptions(**options)
        self.name = name
        filepath = Path(filepath)
        if filepath.is_file() and filepath.suffix in Table.instance_suffix:
            #instance provided
            self.xbrl_model = self.load_xbrl(filepath)
        elif filepath.is_file() and filepath.suffix in Table.schema_suffix:
            #taxonomy provided
            self.xbrl_model = self.load_xbrl(filepath)
        else:
            #apply default taxonomy
            self.xbrl_model = self.create_default_schema()
        self.fact_rows = []
        self.constraints = {}

    def __repr__(self):
        pass    

    # SETTERS

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
    
    def load_xbrl(self, filepath=None):
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
        #prepare options
        self.options.entrypointFile = str(filepath)  #filelike_content
        self.options.validate = True
        #run
        with Session() as session:
            session.run(self.options)
            xbrl_models = session.get_models()    #.modelManager.modelXbrls
            xbrl_model = xbrl_models[0]
            self.validate_xbrl(xbrl_models)
        return xbrl_model
    
    def create_instance_from_taxonomy(self, instance_path):
        """After XBRL is loaded with taxonomy, create the instance doc.
        
        #TODO: perform testing on each step
        """
        #checks
        if not Path(instance_path).suffix in ['.xbrl', '.ixbrl']:
            raise Exception(f'must provide a path for the new instance doc')
        if Path(self.options.entrypointFile).suffix != '.xsd':
            raise Exception(f'options entrypointFile suffix must be .xsd')
        with Session() as session:
            #prepare schema
            session.run(self.options)
            xbrl_models = [
                mdl for mdl in session.get_models() 
                if mdl.uri==self.options.entrypointFile
                and mdl.modelDocument.type==2   #denotes schema doc
                ]
            if len(xbrl_models)==1:
                taxonomy_dts = xbrl_models[0]
            else:
                raise Exception(f'more than one primary xbrl_models')
            self.validate_xbrl([taxonomy_dts])
            #create instance
            #xbrl = taxonomy_dts.modelManager.modelXbrl #or taxonomy_dts.createInstance(url=instance_path)
            taxonomy_dts.createInstance(url=str(instance_path))
            assert session.get_models()[0].modelDocument.type == 4  #denotes instance doc
            #instance_model = taxonomy_dts.modelManager.create(
            #    newDocumentType=4, 
            #    url=instance_path, 
            #    schemaRefs=taxonomy_dts.modelDocument.uri  #taxonomy_dts.modelDocument.targetDocumentSchemaRefs or referencesDocument ???
            #    )
            priItem_qname = list(taxonomy_dts.qnameUtrUnits.keys())[232]  #or arelle.ModelValue.QName('http://fasb.org/us-gaap/2015-01-31', 'us-gaap:CashAndCashEquivalentsAtCarryingValue')
            context = taxonomy_dts.createContext(
                entityIdentScheme='http://www.sec.gov/cik', 
                entityIdentValue='0000000001',
                periodType='duration',
                periodStart=datetime.date(2024,1,1),
                periodEndInstant=datetime.date(2024,12,31),
                priItem=priItem_qname,  #primary item is either QName object of a taxonomy concept, or None if context is dimensional and its purpose is to define only the dimensions
                dims={},    #dimensional elements
                segOCCs=[], #segment information
                scenOCCs=[] #scenario information
            )
            unit = taxonomy_dts.createUnit(
                multiplyBy=[arelle.ModelValue.qname('iso4217:USD')],
                divideBy=[]
            )
            concept_name = [c for c,v in taxonomy_dts.qnameConcepts.items()][0]
            fact = taxonomy_dts.createFact(
                concept_name,
                attributes={"contextRef": context.id, "unitRef": unit.id, "decimals": "2"},
                text="10000.50",
            )
        self.xbrl_model = taxonomy_dts
        return True

    def create_default_schema(self, xbrl_model=None):
        """Get a default schema if Table not provided with either
        instance doc or taxonomy.
        
        TODO: get from data/ file
        
        """
        if not xbrl_model:
            schema_content = """<?xml version="1.0" encoding="UTF-8"?>
            <schema xmlns="http://www.w3.org/2001/XMLSchema"
                    xmlns:xbrli="http://www.xbrl.org/2003/instance"
                    xmlns:example="http://example.com/xbrl/taxonomy"
                    targetNamespace="http://example.com/xbrl/taxonomy"
                    elementFormDefault="qualified">
                <import namespace="http://www.xbrl.org/2003/instance"
                        schemaLocation=""http://www.xbrl.org/2003/xbrl-instance-2003-12-31.xsd"/>

                <element name="ExampleConcept" type="xbrli:monetaryItemType" substitutionGroup="xbrl:item"/>
            </schema>
            """
        else:
            #TODO:review creation steps and compare with above^^^ method: create_instance_from_taxonomy()
            #add ns definitions for the schema and instance
            xbrl_model.addNamespace()
            #add schema reference; typically remote in the real-world
            xbrl_model.schemaRefs.append(
                xbrl_model.createModelDocument(
                    file=os.path.abspath("example-schema.xsd"),
                    isEntry=False,
                    isSchema=True,
                    url=os.path.abspath("example-schema.xsd")
            ))
            #add context (entity and period) for the fact
            context_ref = xbrl_model.createContext(
                entityIdentScheme="http:/www.sec.gov/CIK",
                entityIdentValue="1234567890",
                periodType="duration",
                periodStart="2024-01-01",
                periodEndInstance="2024-12-31"
            ).id
            #add unit for the numeric fact
            unit_ref = xbrl_model.createUnit(
                uomQname="iso4217:USD"
            ).id
            #create and add fact from custom schema
            concept_qnam = xbrl_model("example:ExampleConcept")
            xbrl_model.createFact(
                concept_qnam,
                attributes={"contextRef": context_ref, "unitRef": unit_ref, "decimals": "2"},
                text="10000.50",
            )
            schema_content = '^^^WTF'
        return schema_content
    
    # GETTERS

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

    def get_dts_docs(self, verbose=False):
        """Get the xbrl model DTS documents.
        
        Usage:
            metadata = table.get_dts_docs()
        """
        all_docs = list(self.xbrl_model.urlDocs.values())
        if verbose:
            for doc in all_docs:
                print(f"URI: {doc.uri}")
                print(f"Type: {doc.type}")  #example: 1 for SCHEMA, 2 for LINKBASE, 3 for INSTANCE
                print("-" * 20)
        return all_docs
    
    def get_instance(self):
        """Get ModelXbrl's document and serialize it.
        """
        instance_doc = self.xbrl_model.modelDocument.xmlDocument
        if instance_doc:
            return etree.tostring(instance_doc, pretty_print=True, encoding='unicode')

    def get_schema(self, as_string=False, verbose=False):
        """Get XBRL schema with options for etree (as_string)
        and print list (verbose).
        """
        schema_documents = [
            doc for doc in self.xbrl_model.urlDocs.values()
            if doc.type == arelle.ModelDocument.Type.SCHEMA
        ]
        if schema_documents:
            if verbose:
                for schema_doc in schema_documents:
                    print(f"- {schema_doc.basename}")
                    print(f"- URI: {schema_doc.uri}")
                    print(f"- File path: {schema_doc.filepath}")
            if as_string:
                only_first_schema = schema_documents[0]
                schema_root = only_first_schema.xmlRootElement
                schema_documents = etree.tostring(schema_root, pretty_print=True, encoding='unicode')
        return schema_documents
    
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

    # EXPORT
      
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

        