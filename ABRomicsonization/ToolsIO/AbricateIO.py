#!/usr/bin/env python
import json
import pandas as pd
from ABRomicsonization.Interfaces import AbromicsResultIterator

required_metadata = {
    "analysis_software_version": "abricate version",
    "reference_database_version": "DB version",
    "abricate_hid": "historic ID for abricate file from galaxy",
}

"""Abricate tool parser
Extract all results from abricate report.tsv file
Args:
AbromicsResultIterator (abc.ABCMeta): abstract class to the parser
"""


class AbricateIterator(AbromicsResultIterator):
    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "abricate"
        self.metadata = metadata
        super().__init__(source, self.metadata)
        self.parse()

    def parse(self):
        """Extract information from abricate tabular file
        Extract header of file and related results
        """
        # skip any manually specified fields for later
        reader = pd.read_table(self.stream, header=0, sep="\t")
        self.reader = reader
        reader = self.reader
        reader.columns = reader.columns.str.replace("#", "")
        reader = reader.drop(["COVERAGE_MAP"], axis=1)
        reader = reader.to_json(orient="records")
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["content"] = json.loads(reader)
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["hid"] = self.abromics_results.pop("abricate_hid")
