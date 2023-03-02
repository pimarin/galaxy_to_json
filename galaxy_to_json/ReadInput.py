import glob
import os.path
from pathlib import Path
import csv
import detect_delimiter
import magic
import glob
import pandas as pd
import argparse
import green
from argparse_color_formatter import ColorHelpFormatter
import coloredlogs, logging
from galaxy_to_json.ArgsInput import ArgsInput
from galaxy_to_json.CommandParseException import CommandParseException


class ReadRawData:

    def __init__(self,
                 sep="\t"):
        self.sep = sep
        self.dataframe = None
    def _check_file_exist(self):
        if len(self.args.input_files) == 0:
            raise CommandParseException("Must pass a file to process", self.args, print_help=True)

        for file in self.args.input_files:
            if not os.path.exists(file) or not os.access(file, os.R_OK):
                raise CommandParseException('File [' + file + '] does not exist', self.args)

        if self.args.output_dir:
            if Path.exists(self.args.output_dir):
                raise CommandParseException("Output directory [" + self.args.output_dir + "] already exists", self.args)

    def _read_files(self, input_file, sep="\t", header_row=0):
        with open(input_file, "r") as file:
            first_row = file.readline()
            if not sep == None:
                sep = self._check_delimiter(first_row)
        self.dataframe = pd.read_table(input_file, delimiter=sep, header=header_row)

    def _check_delimiter(self, file):
        separator = detect_delimiter.detect(file)
        return separator
