#!/usr/bin/env python
import json
import pandas as pd
from ABRomicsonization.Interfaces import AbromicsResultIterator

required_metadata = {
    "refseq_hid": "Historic ID to refseq result from Galaxy",
    "analysis_software_version": "refseqmasher version number",
}


class RefseqmasherIterator(AbromicsResultIterator):
    """Refseqmasher tool parser
    Filter results from refseq tabular file
    Args:
        AbromicsResultIterator (abc.ABCMeta): abstract class to the parser
    """

    def __init__(self, source, metadata):
        metadata["analysis_software_name"] = "refseqmasher"
        self.metadata = metadata
        super().__init__(source, metadata)

        self.parse()

    def parse(self):
        """Refseqmasher matches parser"""
        refseq_df = pd.read_table(self.source)
        refseq_json = refseq_df.to_json(
            orient="records",
        )
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["content"] = json.loads(refseq_json)
        self.abromics_results["results"][
            self.metadata["analysis_software_name"]
        ]["hid"] = self.abromics_results.pop("refseq_hid")
