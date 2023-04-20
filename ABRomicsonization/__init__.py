#!/usr/bin/env python

# tool version
__version__ = "0.1"

from ABRomicsonization.ToolsIO import AbricateIO
from ABRomicsonization.ToolsIO import PlasmidFinderIO
from ABRomicsonization.ToolsIO import StarAmrIO
from ABRomicsonization.ToolsIO import ShovillIO
from ABRomicsonization.ToolsIO import FastpIO
from ABRomicsonization.ToolsIO import QuastIO
from ABRomicsonization.ToolsIO import RefSeqMasherIO
from ABRomicsonization.ToolsIO import BandageIO
from ABRomicsonization.ToolsIO import BaktaIO
from ABRomicsonization.ToolsIO import IntegronFinderIO
from ABRomicsonization.ToolsIO import IseScanIO
from ABRomicsonization.ToolsIO import Kraken2IO
from ABRomicsonization.ToolsIO import BrackenIO
from ABRomicsonization.ToolsIO import RecentrifugeIO
from ABRomicsonization.ToolsIO import TabularIO

_FormatToIterator = {
    "abricate": AbricateIO.AbricateIterator,
    "plasmidfinder": PlasmidFinderIO.PlasmidFinderIterator,
    "staramr": StarAmrIO.StarAmrIterator,
    "shovill": ShovillIO.ShovillIterator,
    "fastp": FastpIO.FastpIterator,
    "quast": QuastIO.QuastIterator,
    "refseqmasher": RefSeqMasherIO.RefseqmasherIterator,
    "bandage": BandageIO.BandageIterator,
    "bakta": BaktaIO.BaktaIterator,
    "integronfinder2": IntegronFinderIO.IntegronFinderIterator,
    "isescan": IseScanIO.IseScanIterator,
    "kraken2": Kraken2IO.Kraken2Iterator,
    "bracken": BrackenIO.BrackenIterator,
    "recentrifuge": RecentrifugeIO.RecentrifugeIterator,
    "tabular_file": TabularIO.GenericTabularIterator,
}

_ReportFileToUse = {
    "abricate": "OUTPUT.tsv",
    "plasmidfinder": "plasmidfinder.tsv",
    "staramr": "resfinder.tsv",
    "shovill": "contig.fasta",
    "fastp": "report.json",
    "quast": "report.tsv",
    "refseqmasher": "OUTPUT.tsv",
    "bandage": "OUTPUT.txt",
    "bakta": "OUTPUT.json",
    "integronfinder2": "OUTPUT.integrons, OUTPUT.summary",
    "isescan": "OUTPUT.tsv",
    "kraken2": "report.tsv",
    "bracken": "report.tsv",
    "recentrifuge": "data.tsv",
    "tabular_file": "report.tsv",
    "tooltest": "unitest",
}

_RequiredToolMetadata = {
    "abricate": AbricateIO.required_metadata,
    "plasmidfinder": PlasmidFinderIO.required_metadata,
    "shovill": ShovillIO.required_metadata,
    "staramr": StarAmrIO.required_metadata,
    "fastp": FastpIO.required_metadata,
    "quast": QuastIO.required_metadata,
    "refseqmasher": RefSeqMasherIO.required_metadata,
    "bandage": BandageIO.required_metadata,
    "bakta": BaktaIO.required_metadata,
    "integronfinder2": IntegronFinderIO.required_metadata,
    "isescan": IseScanIO.required_metadata,
    "kraken2": Kraken2IO.required_metadata,
    "bracken": BrackenIO.required_metadata,
    "recentrifuge": RecentrifugeIO.required_metadata,
    "tabular_file": TabularIO.required_metadata,
    "tooltest": AbricateIO.required_metadata,
}


def parse(handle, metadata, tool):
    """Turn a sequence file into a python json file format

    Raises:
        TypeError: string control of the tool name
        TypeError: metadata are a dict type
        ValueError: tool name was provided
        ValueError: tool name is a lower case string
        ValueError: Tool name was not an available key to check metadata
        ValueError: Tool name is not an avaiable value to extract parser

    Returns:
        _type_: ToolIterator
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
            f"toto Unknown tool: {tool}\nMust be in"
            f" {_RequiredToolMetadata.keys()}"
        )

    metadata = {
        key: metadata[key] if metadata[key] is not None else ""
        for key, metadata[key] in metadata.items()
    }

    missing_values = {
        key: tool_required_metadata[key]
        for key in set(tool_required_metadata) ^ set(metadata)
    }
    if missing_values:
        print(f"No informations provided to {list(missing_values)}")

    for key in missing_values.keys():
        metadata[key] = ""

    iterator_generator = _FormatToIterator.get(tool)
    if iterator_generator:
        return iterator_generator(handle, metadata)
    else:
        raise ValueError(
            f"Unknown tool: {tool}\nMust be in {_FormatToIterator.keys()}"
        )
