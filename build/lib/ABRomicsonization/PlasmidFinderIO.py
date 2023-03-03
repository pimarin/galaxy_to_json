#!/usr/bin/env python

import csv
from ABRomicsonization.Interfaces import hAMRonizedResultIterator
from ABRomicsonization.constants import GENE_PRESENCE

required_metadata = ["analysis_software_version", "reference_database_version"]


class PlasmidFinderIterator(hAMRonizedResultIterator):
    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "PlasmidFinder"

        self.metadata = metadata

        self.field_mapping = {
            "Isolate ID": "input_file_name",
            "Plasmid": "plasmid_name",
            "%Identity": "sequence_identity",
            "%Overlap": "coverage_percentage",
            "HSP Length/Total Length": "coverage_ratio",
            "Contig": "input_sequence_id",
            "Start": "input_gene_start",
            "End": "input_gene_stop",
            "Accession": "reference_accession"
            }
        
        super().__init__(source, self.field_mapping, self.metadata)

    def parse(self, handle):
        """
        Read each and return it
        """
        # skip any manually specified fields for later
        reader = csv.DictReader(handle, delimiter="\t")
        for result in reader:
            yield self.hAMRonize(result, self.metadata)


