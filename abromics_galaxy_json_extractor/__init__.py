#!/usr/bin/env python

# tool version
__version__ = "0.1"

from abromics_galaxy_json_extractor.toolsio import (
    abricateio,
    plasmidfinderio,
    staramrio,
    shovillio,
    fastpio,
    quastio,
    refseqmasherio,
    bandageio,
    baktaio,
    integronfinder2io,
    isescanio,
    kraken2io,
    brackenio,
    recentrifugeio,
    tabulario)

_FormatToIterator = {
    "abricate": abricateio.AbricateIterator,
    "plasmidfinder": plasmidfinderio.PlasmidFinderIterator,
    "staramr": staramrio.StarAmrIterator,
    "shovill": shovillio.ShovillIterator,
    "fastp": fastpio.FastpIterator,
    "quast": quastio.QuastIterator,
    "refseqmasher": refseqmasherio.RefseqmasherIterator,
    "bandage": bandageio.BandageIterator,
    "bakta": baktaio.BaktaIterator,
    "integronfinder2": integronfinder2io.IntegronFinderIterator,
    "isescan": isescanio.IseScanIterator,
    "kraken2": kraken2io.Kraken2Iterator,
    "bracken": brackenio.BrackenIterator,
    "recentrifuge": recentrifugeio.RecentrifugeIterator,
    "tabular_file": tabulario.GenericTabularIterator,
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
    "abricate": abricateio.required_metadata,
    "plasmidfinder": plasmidfinderio.required_metadata,
    "shovill": shovillio.required_metadata,
    "staramr": staramrio.required_metadata,
    "fastp": fastpio.required_metadata,
    "quast": quastio.required_metadata,
    "refseqmasher": refseqmasherio.required_metadata,
    "bandage": bandageio.required_metadata,
    "bakta": baktaio.required_metadata,
    "integronfinder2": integronfinder2io.required_metadata,
    "isescan": isescanio.required_metadata,
    "kraken2": kraken2io.required_metadata,
    "bracken": brackenio.required_metadata,
    "recentrifuge": recentrifugeio.required_metadata,
    "tabular_file": tabulario.required_metadata,
    "tooltest": abricateio.required_metadata,
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
