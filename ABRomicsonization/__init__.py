#!/usr/bin/env python

__version__ = "0.1"

from ABRomicsonization import AbricateIO
from ABRomicsonization import PlasmidFinderIO
from ABRomicsonization import StarAmrIO

_FormatToIterator = {
    "abricate": AbricateIO.AbricateIterator,
    "plasmidfinder": PlasmidFinderIO.PlasmidFinderIterator,
    "staramr": StarAmrIO.StarAmrIterator
}

_ReportFileToUse = {
    "abricate": "OUTPUT.tsv",
    "plasmidfinder": "plasmidfinder.tsv",
    "staramr": "resfinder.tsv"
}


_RequiredToolMetadata = {
    "abricate": AbricateIO.required_metadata,
    "plasmidfinder": PlasmidFinderIO.required_metadata,
    "staramr": StarAmrIO.required_metadata
}


def parse(handle, metadata, tool):
    """Turn a sequence file into an iterator returning SeqRecords.
    Arguments:
     - handle   - handle to the file, or the filename as a string
     - tool - lower case string describing the file format.
     - required_arguments - dict containing the required arguments for tool
    Typical usage, opening a file to read in, and looping over the record(s):
    >>> import hAMRonization as hAMR
    >>> filename = "abricate_report.tsv"
    >>> metadata = {"analysis_software_version": "1.0.1",
    ...             "reference_database_version": "2019-Jul-28"}
    >>> for result in hAMR.parse(filename, required_arguments, "abricate"):
    ...    print(result)

    """
    if not isinstance(tool, str):
        raise TypeError("Need a string for the file format (lower case)")
    if not isinstance(metadata, dict):
        raise TypeError("Metadata must be provided as a dictionary")
    if not tool:
        raise ValueError("Tool required (lower case string)")
    if not tool.islower():
        raise ValueError(f"Tool string '{tool}' should be lower case")

    # check all required metadata has been provided
    try:
        tool_required_metadata = _RequiredToolMetadata[tool]
    except KeyError:
        raise ValueError(
            f"Unknown tool: {tool}\nMust be in " f"{_RequiredToolMetadata.keys()}"
        )
    missing_data = []
    for required in tool_required_metadata:
        if required not in metadata:
            missing_data.append(required)
    if missing_data:
        raise ValueError(
            f"{tool} requires {missing_data} supplied " "in metadata dictionary"
        )

    iterator_generator = _FormatToIterator.get(tool)
    if iterator_generator:
        return iterator_generator(handle, metadata)
    raise ValueError(f"Unknown tool: {tool}\nMust be in " f"{_FormatToIterator.keys()}")
