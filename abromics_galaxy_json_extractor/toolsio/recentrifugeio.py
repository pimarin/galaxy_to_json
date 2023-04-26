#!/usr/bin/env python
import json
import pandas as pd
from abromics_galaxy_json_extractor.interfaces import (
    AbromicsResultIterator,
)

required_metadata = {
    "recentrifuge_hid": (
        "historic ID to recentrifuge data file provided by Galaxy"
    ),
    "analysis_software_version": "recentrifuge version",
    "taxa_db_version": "ncbi taxonomy DB version",
    "analysis_software_version": "recentrifuge version",
    "rcf_stat_file_path": "recentrifuge statistic file",
    "rcf_stat_hid": "historic ID provided by Galaxy",
    "rcf_html_path": "recentrifuge html report file",
    "rcf_html_hid": "recentrifuge html report file",
}


class RecentrifugeIterator(AbromicsResultIterator):
    """Recentrifuge tool parser
    parse result from tabular data
    Could also parse stat file
    Could keep path information to html report
    Args:
        AbromicsResultIterator (abc.ABCMeta): abstract class to the parser
    """

    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "recentrifuge"
        self.metadata = metadata
        self.rcf_stat_colnames = [
            "infos",
            "value",
        ]
        super().__init__(source, self.metadata)
        self.parse()

    def parse(self):
        """Parser for recentrifuge
        Could parse data and stat file
        Extract only html report path
        """
        # skip any manually specified fields for later
        reader = self._filter_dataframe_type(self.stream, header_position=1)
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["content"] = reader

        if self.metadata["rcf_stat_file_path"]:
            self._check_input_files(self.metadata["rcf_stat_file_path"])
            reader = self._filter_dataframe_type(
                self.stream,
                header_position=None,
                col_names=self.rcf_stat_colnames,
                skip=1,
            )
            self.abromics_results["results"]["recentrifuge_stat"] = {
                "name": "recentrifuge_statistics",
                "file_path": self.abromics_results.pop("rcf_stat_file_path"),
                "hid": self.abromics_results.pop("rcf_stat_hid"),
                "content": reader,
            }
        if self.metadata["rcf_html_path"]:
            self._check_input_files(self.metadata["rcf_html_path"])
            self.abromics_results["results"]["recentrifuge_report"] = {
                "name": "recentrifuge_report",
                "file_path": self.abromics_results.pop("rcf_html_path"),
                "hid": self.abromics_results.pop("rcf_html_hid"),
                "content": "",
            }

    def _filter_dataframe_type(
        self,
        handle,
        header_position=0,
        separator="\t",
        orient_type="records",
        col_names=None,
        skip=None,
    ):
        """Clean input recentrifuge files
        Remove bad character and keep only value informations

        Args:
            handle (_io.TextIOWrapper): opened file
            header_position (int, optional): header to use as column name.
            Defaults 0.
            separator (str, optional): Separator type. Defaults to "\t".
            orient_type (str, optional): Store dict format column and value.
            Defaults to "records".
            col_names (list, optional): List of name to replace colnames.
            Defaults to None.
            skip (int, optional): Row number to not use. Defaults to None.

        Returns:
            dict: filtered dictionnary
        """
        reader = pd.read_table(
            handle,
            header=header_position,
            sep=separator,
            skiprows=skip,
        )
        if col_names:
            reader.columns = col_names
        reader = reader.replace("^[ \t]+", "", regex=True)
        reader = reader.replace("[.]$", "", regex=True)
        reader = reader.replace(" ", "", regex=True)
        reader.columns = reader.columns.str.replace("%", "")
        reader = json.loads(reader.to_json(orient=orient_type))
        return reader
