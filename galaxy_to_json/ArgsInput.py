import argparse
import glob
import os.path

import green
from argparse_color_formatter import ColorHelpFormatter
import coloredlogs, logging
from galaxy_to_json.CommandParseException import CommandParseException

class ArgsInput:

    def __init__(self):
        self.main_parser = None
        self.sub_parser = None

    def _setup_args(self):

        self.main_parser = argparse.ArgumentParser()
        self.main_parser.add_argument('-o',
                                '--output_dir',
                                action='store',
                                dest='output_dir',
                                type=str,
                                help="Specify directory output path (default is in local directory)",
                                default=None,
                                required=False)
        self.main_parser.add_argument('-t',
                                '--tool_name',
                                action='store',
                                choices=['staramr', 'abricate', 'shovill'],
                                dest='tool_name',
                                type=str,
                                help="Specify tool name which generate the input files",
                                default=None,
                                required=False)
        self.main_parser.add_argument('--tool_version',
                                action='store',
                                dest='tool_version',
                                type=str,
                                help="Tool version, could be add in the json file",
                                default=None,
                                required=False)
        self.main_parser.add_argument('--db_version',
                                action='store',
                                dest='db_version',
                                type=str,
                                help="Database name or version, could be add in the json file",
                                default=None,
                                required=False)
        self.main_parser.add_argument('--file_type',
                                action='store',
                                dest='file_type',
                                type=str,
                                help="Specify the file format (tabular, csv, json or blast default is tabular)",
                                default=None,
                                required=False)
        self.main_parser.add_argument('-i',
                                '--input_file',
                                action='store',
                                dest='file_type',
                                type=str,
                                help="input file",
                                default=None,
                                required=False)

        self.sub_parser = self.main_parser.add_subparsers(help='tool subcommands')
    def _staramr_optional_parser(self):
        staramr_subparser = self.sub_parser.add_parser('staramr', help='staramr options')
        staramr_subparser.add_argument('--result_file',
                                action='store',
                                dest='file_type',
                                type=str,
                                help="Result file (resfinder, mlst or plasmidfinder)",
                                default=None,
                                required=True)
        staramr_subparser.add_argument('--blast_file',
                                       action='store',
                                       dest='file_type',
                                       type=str,
                                       help="Blast hit file for resfinder or plasmidfinder analysis",
                                       default=None,
                                       required=False)

        try:
            return self.main_parser.parse_args()
        except SystemExit:
            raise CommandParseException('File parse Error', self.main_parser)