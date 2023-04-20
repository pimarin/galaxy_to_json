#!/usr/bin/env python
import json
import pandas as pd
from ABRomicsonization.Interfaces import AbromicsResultIterator

required_metadata = {
    "analysis_software_version": "kraken2 version",
    "reference_database_version": "kraken2 DB version",
    "seq_classification_file_path": (
        "file containing the classification of each reads"
    ),
    "classification_hid": (
        "historic ID for read classification file from Galaxy"
    ),
}


class Kraken2Iterator(AbromicsResultIterator):
    """Kraken2 tool parser
    Filter results from kraken2 taxonomy report
    Could also give path information for
    Read taxa assignation
    Args:
        AbromicsResultIterator (abc.ABCMeta): abstract class to the parser
    """

    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "kraken2"
        self.metadata = metadata
        self.colnames = [
            "fragment_coverage",
            "fragment_number",
            "assigned_fragment_number",
            "rank_code",
            "ncbi_taxonomic_id",
            "scientific_name",
        ]
        super().__init__(source, self.metadata)
        self.parse()

    def parse(self):
        """
        Extract taxonomy information
        Extract read assignation file path
        """
        # skip any manually specified fields for later
        reader = pd.read_table(self.stream, header=None, sep="\t")
        reader.columns = self.colnames
        reader = reader.replace("^[ \t]+", "", regex=True)
        reader = reader.replace(" ", "_", regex=True)
        reader = reader.to_json(orient="records")
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["content"] = json.loads(reader)
        if self.metadata["seq_classification_file_path"]:
            self.__check_input_files__(
                self.metadata["seq_classification_file_path"]
            )

            self.abromics_results["results"]["seq_classification"] = {
                "name": "classification",
                "file_path": self.abromics_results.pop(
                    "seq_classification_file_path"
                ),
                "hid": self.abromics_results.pop("classification_hid"),
                "content": {},
            }
