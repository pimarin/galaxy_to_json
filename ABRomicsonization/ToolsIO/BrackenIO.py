#!/usr/bin/env python
import json
import pandas as pd
from ABRomicsonization.Interfaces import AbromicsResultIterator

required_metadata = {
    "kraken2_hid": "Historic ID to kraken report file from Galaxy",
    "analysis_software_version": "bracken version",
    "reference_database_version": "bracken DB version",
    "read_len": "read length value",
    "level": "level to estimate abundance",
    "threshold": "number of reads required PRIOR to abundance estimation",
    "kraken_report_path": "New kraken report estimated from bracken",
    "kraken_report_hid": "Historic ID to kraken results file from Galaxy",
}


class BrackenIterator(AbromicsResultIterator):
    """Bracken tool parser
    Filter results from kraken2 report file
    Could also filter file for:
    bracken new kraken2 report

    Args:
        AbromicsResultIterator (abc.ABCMeta): abstract class to the parser
    """

    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "bracken"
        self.metadata = metadata
        self.kraken_colnames = [
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
        """Extract information from kraken2 report file
        Add information from new report estimated by bracken
        """
        # skip any manually specified fields for later
        reader = pd.read_table(self.stream, header=0, sep="\t")
        reader = reader.replace(" ", "_", regex=True)
        reader = reader.to_json(orient="records")
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["content"] = json.loads(reader)
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["hid"] = self.abromics_results.pop("kraken2_hid")

        if self.metadata["kraken_report_path"]:
            self.__check_input_files__(self.metadata["kraken_report_path"])
            self.abromics_results.pop("kraken_report_path")
            reader = pd.read_table(self.stream, header=None, sep="\t")
            reader.columns = self.kraken_colnames
            reader = reader.replace("^[ \t]+", "", regex=True)
            reader = reader.replace(" ", "_", regex=True)
            reader = reader.to_json(orient="records")
            self.abromics_results["results"]["kraken2_estimated"] = {
                "name": "kraken_report",
                "file_path": self.metadata["kraken_report_path"],
                "hid": self.abromics_results.pop("kraken_report_hid"),
                "content": json.loads(reader),
            }
