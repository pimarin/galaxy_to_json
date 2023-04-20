#!/usr/bin/env python
import json
import pandas as pd
from ABRomicsonization.Interfaces import AbromicsResultIterator

required_metadata = {
    "resfinder_hid": "Historic ID provided by Galaxy for resfinder file",
    "analysis_software_version": "tool version",
    "mlst_file_path": "mlst output file from staramr",
    "mlst_hid": "Historic ID provided by Galaxy for mlst file",
    "plasmidfinder_file_path": "plasmid output file from staramr",
    "plasmid_hid": "Historic ID provided by Galaxy for plasmid file",
    "pointfinder_file_path": "pointfinder output file from staramr",
    "pointfinder_hid": "Historic ID provided by Galaxy for pointfinder file",
    "setting_file_path": "setting file from staramr analysis",
    "setting_hid": "Historic ID provided by Galaxy for settings file",
}


class StarAmrIterator(AbromicsResultIterator):
    """STARamr tool parser
    Filter results from resfinder file
    Could also parse results for:
    mlst scheme file
    plasmid file
    pointfinder file
    settings file
    Args:
        AbromicsResultIterator (abc.ABCMeta): abstract class to the parser
    """

    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "staramr"
        self.metadata = metadata
        super().__init__(source, self.metadata)
        self.parse()

    def parse(self):
        """STARamr resfinder parser
        Parse resfinder result and could also
        parse other file:
        mlst, pointfinder, plasmidfinder and settings
        """
        # skip any manually specified fields for later
        reader = self._filter_dataframe_type(self.stream)
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["content"] = reader
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["hid"] = self.abromics_results.pop("resfinder_hid")

        if self.metadata["mlst_file_path"]:
            self.__check_input_files__(self.metadata["mlst_file_path"])
            reader = self._filter_dataframe_type(self.stream)
            tool_name = "mlst"
            self.abromics_results["results"][tool_name] = {
                "name": tool_name,
                "file_path": self.abromics_results.pop(
                    f"{tool_name}_file_path"
                ),
                "hid": self.abromics_results.pop(f"{tool_name}_hid"),
                "content": reader,
            }

        if self.metadata["plasmidfinder_file_path"]:
            input_files = self.metadata["plasmidfinder_file_path"]
            self.__check_input_files__(input_files)
            reader = self._filter_dataframe_type(self.stream)
            tool_name = "plasmidfinder"
            self.abromics_results["results"][tool_name] = {
                "name": tool_name,
                "file_path": self.abromics_results.pop(
                    f"{tool_name}_file_path"
                ),
                "hid": self.abromics_results.pop("plasmid_hid"),
                "content": reader,
            }

        if self.metadata["pointfinder_file_path"]:
            input_files = self.metadata["pointfinder_file_path"]
            self.__check_input_files__(input_files)
            reader = self._filter_dataframe_type(self.stream)
            tool_name = "pointfinder"
            self.abromics_results["results"][tool_name] = {
                "name": tool_name,
                "file_path": self.abromics_results.pop(
                    f"{tool_name}_file_path"
                ),
                "hid": self.abromics_results.pop(f"{tool_name}_hid"),
                "content": reader,
            }
        if self.metadata["setting_file_path"]:
            self.__check_input_files__(self.metadata["setting_file_path"])
            reader = self._filter_dataframe_type(
                self.stream, header_position=None, separator="="
            )
            self.abromics_results["results"]["settings"] = {
                "name": "settings",
                "file_path": self.abromics_results.pop("setting_file_path"),
                "hid": self.abromics_results.pop("setting_hid"),
                "content": reader,
            }

    def _filter_dataframe_type(
        self, handle, header_position=0, separator="\t", orient_type="records"
    ):
        """Filter input dataframe
        Remove bad character and add coverage ratio value

        Args:
            handle (_type_): _description_
            header_position (int, optional): _description_. Defaults to 0.
            separator (str, optional): _description_. Defaults to "\t".
            orient_type (str, optional): _description_. Defaults to "records".

        Returns:
            dict: filtered data
        """
        reader = pd.read_table(handle, header=header_position, sep=separator)
        reader = reader.replace("^[ \t]+", "", regex=True)
        reader = reader.replace("[.]$", "", regex=True)
        reader = reader.replace(" ", "", regex=True)
        if "HSP Length/Total Length" in reader.columns:
            coverage_ratio = reader["HSP Length/Total Length"].str.split(
                pat="/", expand=True
            )
            coverage_ratio = pd.to_numeric(coverage_ratio[1]) / pd.to_numeric(
                coverage_ratio[0]
            )
            reader["coverage_ratio"] = coverage_ratio
        try:
            reader.columns = reader.columns.str.replace("%", "")
            reader = json.loads(reader.to_json(orient=orient_type))
            return reader
        except AttributeError:
            reader = dict(zip(reader[0], reader[1]))
            return reader
