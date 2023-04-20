#!/usr/bin/env python
import pandas as pd
from ABRomicsonization.Interfaces import AbromicsResultIterator

required_metadata = {
    "analysis_software_version": "bandage version number",
    "bandage_hid": "historic ID for bandage file from galaxy",
}


class BandageIterator(AbromicsResultIterator):
    """Bandage tool parser
    Extract result from Bandage info results
    Args:
        AbromicsResultIterator (abc.ABCMeta): abstract class to the parser
    """

    def __init__(self, source, metadata):

        metadata["analysis_software_name"] = "bandage"
        super().__init__(source, metadata)

        self.parse()

    def parse(self):
        """Extract information from bandage info"""
        bandage_infos = pd.read_table(self.source, header=None, sep=":")
        bandage_infos[0] = bandage_infos[0].replace(" ", "_", regex=True)
        bandage_infos[1] = bandage_infos[1].replace(" ", "", regex=True)
        bandage_infos = dict(zip(bandage_infos[0], bandage_infos[1]))
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["content"] = bandage_infos
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["hid"] = self.abromics_results.pop("bandage_hid")
