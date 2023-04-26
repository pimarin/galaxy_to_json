#!/usr/bin/env python
import json
import pandas as pd
from abromics_galaxy_json_extractor.interfaces import (
    AbromicsResultIterator,
)

required_metadata = {
    "integronfinder_hid": "historic ID for integronfinder file from galaxy",
    "analysis_software_version": "integronfinder version",
    "summary_file_path": "integronfinder summary file path",
    "summary_hid": "historic ID for summary file from galaxy",
}


class IntegronFinderIterator(AbromicsResultIterator):
    """IntegronFinder2 tool parser
    Filter results from integrons file
    Could also filter file for:
    summary file
    Args:
        AbromicsResultIterator (abc.ABCMeta): abstract class to the parser
    """

    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "integronfinder2"
        self.metadata = metadata
        super().__init__(source, self.metadata)
        self.parse()

    def parse(self):
        """Build a dictionnary from integronfinder results
        Integrons and summary file could be analyzed
        """
        integron_df = pd.read_table(self.stream, header=1)
        integron_json = integron_df.to_json(orient="records")
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["content"] = json.loads(integron_json)
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["hid"] = self.abromics_results.pop("integronfinder_hid")

        if self.metadata["summary_file_path"]:
            self._check_input_files(self.abromics_results["summary_file_path"])
            summary_df = pd.read_table(self.stream, header=1)
            summary_json = summary_df.to_json(orient="records")
            self.abromics_results["results"]["summary"] = {
                "name": "summary",
                "file_path": self.abromics_results.pop("summary_file_path"),
                "hid": self.abromics_results.pop("summary_hid"),
                "content": json.loads(summary_json),
            }
