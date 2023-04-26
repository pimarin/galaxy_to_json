#!/usr/bin/env python

import sys
import os
import json
import argparse
import abromics_galaxy_json_extractor
from abc import ABC, abstractmethod
from abromics_galaxy_json_extractor import (
    summarize,
)


class AbromicsResultIterator(ABC):
    """
    Base class for the parsers for each tool

    This should return an appropriate iterator for results
    from whatever
    tool report is being parsed
    """

    def __init__(self, source, metadata):
        """
        Create an abromicsResultIterator for which ever tool report is
        being parsed

        Based on:
        github.com/biopython/biopython/blob/master/Bio/SeqIO/Interfaces.py#L23

        Arguments:
            - source: input file stream or path to input
            - tool: name of tool report that is being parsed
        """
        self.source = source
        self.metadata = metadata
        self._check_input_files(self.source)
        self._abromics_structure()

    def _check_input_files(self, source):
        """
        Check if the input is available to be parsed

        Check if the file exist, if it's empty or if path not exist

        Args:
            source (str): string of the file path
        """
        if os.stat(source).st_size == 0:  # file is empty
            print(
                f"Warning: {source} is empty",
                file=sys.stderr,
            )

        try:
            self.stream = open(source, "r")
        except FileNotFoundError:  # path doesn't exist
            print(
                f"File {source} not found",
                file=sys.stderr,
            )
            exit(1)

    def _abromics_structure(self):
        """
        Template structure for the final json file

        This template built with the tool name, then with
        a results dictionnary which contain some other dict
        to each parsed file
        Always keep tool name and path of parsed file
        """
        self.abromics_results = {}
        filename = os.path.splitext(os.path.basename(self.source))[0]
        for metadata_info in self.metadata:
            if self.metadata[metadata_info]:
                self.abromics_results[metadata_info] = self.metadata[
                    metadata_info
                ]
            else:
                self.abromics_results[metadata_info] = ""
        self.abromics_results["results"] = {
            self.metadata["analysis_software_name"]: {
                "name": filename,
                "file_path": self.source,
                "hid": "",
                "content": {},
            }
        }

    @abstractmethod
    def parse(self, handle):
        """
        Start parsing the file and return an abromics iterator
        """

    def write(
        self,
        report_list,
        total_report_count=1,
        output_location=None,
    ):
        """
        Class to write to output the abromics report (to either stdout or
        a filehandle) in json format

        Get number of reports and which report this one is
        """

        if output_location:
            # appending if more than one report
            if os.path.exists(output_location) and total_report_count > 1:
                out_fh = open(output_location, "a")
            else:
                out_fh = open(output_location, "w")
        else:
            out_fh = sys.stdout

        # remove empty value from dicts
        report_list = [
            self._filter_json_output(report) for report in report_list
        ]
        json.dump(report_list, out_fh)

        if out_fh is not sys.stdout:
            out_fh.close()

    def _filter_json_output(self, report):
        """
        Remove empty items from the parser output

        Args:
            report (dict): a dictionnary with all parsed informations

        Returns:
            dict: filtered dictionnary
        """
        return {key: value for key, value in report.items() if value}


def generate_tool_subparser(subparser, analysis_tool):
    """
    Build the argument parser for a specific tool

    (used to generate a tool-specific cli-parser and a generic tool parser)
    """
    report_file = abromics_galaxy_json_extractor._ReportFileToUse[
        analysis_tool
        ]
    description = (
        "Applies abromics specification to output(s) from "
        f"{analysis_tool} ({report_file})"
    )
    usage = f"abromics.py {analysis_tool} <options>"
    help = f"abromics {analysis_tool}'s output report i.e., {report_file}"

    tool_parser = subparser.add_parser(
        analysis_tool,
        description=description,
        usage=usage,
        help=help,
    )

    tool_parser.add_argument(
        "report",
        nargs="+",
        help="Path to report(s)",
    )
    tool_parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output location",
    )

    # any missing mandatory fields need supplied as CLI argument
    required_mandatory_metadata = (
        abromics_galaxy_json_extractor._RequiredToolMetadata[analysis_tool]
    )

    for field in required_mandatory_metadata:
        tool_parser.add_argument(
            f"--{field}",
            required=False,
            help=f"{required_mandatory_metadata[field]} for {analysis_tool}",
        )

    return subparser


def generate_summarize_subparser(subparser):
    """Add summary argument to the subparser

    Args:
        subparser (argparse._SubParsersAction):
        Subparser with provied tools arguments

    Returns:
        argparse._SubParsersAction: Complete parser
    """

    # add summarize subparser
    # not very pretty to have this tied into the analysis tools list
    # but there still doesn't seem a good way to group subparsers in
    # the argparse library
    description = "Concatenate and summarize AMR detection reports"
    usage = "abromics summarize <options> <list of reports>"
    summarize_help = (
        "Provide a list of paths to the reports you wish to summarize"
    )

    summarize_subparser = subparser.add_parser(
        "summarize",
        description=description,
        usage=usage,
        help=summarize_help,
    )

    summarize_subparser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output file path for summary",
    )

    summarize_subparser.add_argument(
        "-f",
        "--force",
        type=str,
        default=False,
        help="Overwrite to the output file mandatory",
    )
    summarize_subparser.add_argument(
        "abromics_reports",
        nargs="+",
        help="list of abromics reports",
    )
    return summarize_subparser


def generic_cli_interface():
    """
    Generate a generic tool report parser that passes to the tool specific
    parser
    """
    parser = argparse.ArgumentParser(
        description=(
            "Convert ABRomics workflow results "
            "tool output(s) to "
            "abromics specification"
            "format"
        ),
        prog="abromics",
        usage="abromics <tool> <options>",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {abromics_galaxy_json_extractor.__version__}",
    )

    # add tool specific parsers
    subparser = parser.add_subparsers(
        title="Tools with abromics reports",
        help="",
        dest="analysis_tool",
    )

    for (
        analysis_tool
    ) in abromics_galaxy_json_extractor._RequiredToolMetadata.keys():
        subparser = generate_tool_subparser(subparser, analysis_tool)

    generate_summarize_subparser(subparser)

    args = parser.parse_args()

    if args.analysis_tool and args.analysis_tool != "summarize":
        required_mandatory_metadata = (
            abromics_galaxy_json_extractor._RequiredToolMetadata[
                args.analysis_tool
            ]
        )
        metadata = {f: getattr(args, f) for f in required_mandatory_metadata}
        # parse reports and write as appropriate (only first report with head
        # in tsv mode)
        # check number of reports and append correctly if >1
        total_report_count = len(args.report)
        report_list = []
        for report in args.report:
            parsed_report = abromics_galaxy_json_extractor.parse(
                report,
                metadata,
                args.analysis_tool,
            )
            report_list.append(parsed_report.abromics_results)

        parsed_report.write(
            report_list=report_list,
            total_report_count=total_report_count,
            output_location=args.output,
        )

    elif args.analysis_tool == "summarize":
        export = summarize.ReportSummary(
            report_list=args.abromics_reports,
            output_location=args.output,
        )
        export.export_summary()
    else:
        parser.print_help()
