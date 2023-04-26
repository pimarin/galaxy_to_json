#!/usr/bin/env python

import pandas as pd
from abromics_galaxy_json_extractor.interfaces import (
    AbromicsResultIterator,
)

required_metadata = {
    "quast_hid": "Historic ID to quast file from Galaxy",
    "analysis_software_version": "Quast version number",
}


class QuastIterator(AbromicsResultIterator):
    """Quast tool parser
    Extract information from quast tabular results
    Args:
        AbromicsResultIterator (abc.ABCMeta): abstract class to the parser
    """

    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "quast"
        self.metadata = metadata
        super().__init__(source, self.metadata)
        self.parse()

    def parse(self):
        """Parse Quast tabular file"""
        reader = pd.read_table(
            self.source,
            delimiter="\t",
            header=None,
            index_col=False,
        )
        reader[0] = reader[0].replace({r"#": ""}, regex=True)
        reader[0] = reader[0].replace({r"^\s": ""}, regex=True)
        reader[0] = reader[0].replace({r"\s": "_"}, regex=True)
        ziped_values = zip(reader[0], reader[1])
        ziped_values = dict(ziped_values)
        self.abromics_results["results"][
            self.abromics_results["analysis_software_name"]
        ]["content"] = ziped_values
        self.abromics_results["results"][
            self.abromics_results["analysis_software_name"]
        ]["hid"] = self.abromics_results.pop("quast_hid")
