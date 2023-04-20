#!/usr/bin/env python
import json
import pandas as pd
from ABRomicsonization.Interfaces import AbromicsResultIterator

required_metadata = {
    "file_hid": "Historic ID provided by Galaxy for tabular file"
}


class GenericTabularIterator(AbromicsResultIterator):
    """Generic tool parser for tabular files
    Parse tabular file using generic options
    Args:
        AbromicsResultIterator (abc.ABCMeta): abstract class to the parser
    """

    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "tabular_file"
        self.metadata = metadata
        super().__init__(source, self.metadata)
        self.parse()

    def parse(self):
        """Parse tabular dataframe with header"""
        # skip any manually specified fields for later
        reader = self._filter_dataframe_type(self.stream)
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["content"] = reader
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["hid"] = self.abromics_results.pop("file_hid")

    def _filter_dataframe_type(
        self, handle, header_position=0, separator="\t", orient_type="records"
    ):
        reader = pd.read_table(handle, header=header_position, sep=separator)
        reader = reader.replace("^[ \t]+", "", regex=True)
        reader = reader.replace("[.]$", "", regex=True)
        reader = reader.replace(" ", "", regex=True)
        reader = json.loads(reader.to_json(orient=orient_type))
        return reader
