#!/usr/bin/env python

import json
from ABRomicsonization.Interfaces import AbromicsResultIterator

required_metadata = {
    "analysis_software_version": "fastp version number",
    "fastp_hid": "historic ID for fastp file from galaxy",
}


class FastpIterator(AbromicsResultIterator):
    """Fastp tool parser
    Filter results from fastp json file
    Args:
        AbromicsResultIterator (abc.ABCMeta): abstract class to the parser
    """

    def __init__(self, source, metadata):

        metadata["analysis_software_name"] = "fastp"
        super().__init__(source, metadata)

        self.parse()

    def parse(self):
        """Read json output file from fastp trimming"""
        fastp_json_object = json.loads(self.stream.read())
        self.abromics_results["analysis_software_version"] = fastp_json_object[
            "summary"
        ].pop("fastp_version")
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["content"] = fastp_json_object.pop("summary")
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["hid"] = self.abromics_results.pop("fastp_hid")
