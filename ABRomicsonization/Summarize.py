#!/usr/bin/env python

import os
import sys
import json


class ReportSummary:
    """
    Merge some json files to one
    """

    def __init__(
        self, report_list: list, output_location=None, overwrite=False
    ):
        self._report_list = report_list
        self._output_location = output_location
        self._overwrite = overwrite
        self._default_output_name = "abromics_summary.json"
        self._default_location = (
            f"{self._output_location}/{self._default_output_name}"
        )

    def __check_output_path(self):
        """Check if the output information could be used to store json results
        Check if output path exits, could be overwrite.
        Raises:
            ValueError: The output file exist
            and the option --force to overwrite was not provided
            FileExistsError: The path canno't be created

        Returns:
            _io.TextIOWrapper: Console output or
            openned file to store results
        """
        if self._output_location:
            # appending if more than one report
            if not os.path.exists(self._output_location):
                out_fh = open(self._output_location, "w")
            elif os.path.isfile(self._output_location):
                if self._overwrite is True:
                    out_fh = open(self._output_location, "a")
                else:
                    raise ValueError(
                        f"{self._output_location} exist,\
                        choose --force to overwrite the file"
                    )
            elif os.path.isdir(self._output_location) and not os.path.exists(
                self._default_location
            ):
                out_fh = open(self._default_location, "w")
            else:
                raise FileExistsError(
                    f"No valid output path: {self._output_location}"
                )
        else:
            out_fh = sys.stdout
        return out_fh

    def __check_input_files(self, source):
        """Check if the input is available to be parsed
        Check if the file exist, if it's empty or if path not exist

        Args:
            source (str): string of the file path
        """
        if os.stat(source).st_size == 0:
            print(f"Warning: {source} is empty", file=sys.stderr)
            return 0
        try:
            self.stream = open(source, "r")
        except FileNotFoundError:  # path doesn't exist
            print(f"File {source} not found", file=sys.stderr)

    def __read_json_input(self, report):
        """Read the json input file

        Args:
            report (_io.TextIOWrapper): opened file stream

        Returns:
            list: json import to a list
        """
        validated_file = self.__check_input_files(report)
        if validated_file != 0:
            json_file = json.loads(self.stream.read())
            self.stream.close()
            return json_file

    def export_summary(self):
        """Export in json format results"""
        output_destination = self.__check_output_path()
        self.summary_json_list = [
            self.__read_json_input(report) for report in self._report_list
        ]
        json.dump(self.summary_json_list, output_destination)
